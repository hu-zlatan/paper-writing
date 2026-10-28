"""v2 policy training (docs/07_hypotheses_v2.md §2.1): travel action model, masked categorical head over the shared
256-action set, ball-sPCE rewards (L contrastive prior samples, J in-ball samples in the numerator), PPO.

method:
  spce_total        gamma = 1, returns-to-go of r_t                                  (ours)
  spce_myopic_rate  gamma = 0, reward r_t / c(a_t)                                   (ablation A1 / H2 comparator)
  full_state        spce_total with the v1 full-state numerator p(h|s0)              (ablation A2)
  no_nc_input       spce_total with no-contact touches removed from the DeepSets sum (ablation A3)
"""
from __future__ import annotations

import json
import math
import time
from dataclasses import asdict, dataclass, field

import numpy as np
from scipy.special import logsumexp

from .ball import sample_in_ball
from .evaluate import stream
from .geometry import Library, cast
from .likelihood import ObsModel, loglik_from_pred, sample_obs
from .nn import FEAT_DIM, MLP, Adam, obs_features
from .pf import Prior
from .shapes import get_set
from .travel import A, PHI, PSI, cost
from .relframe import RelDeepSets, rel_ctx, rel_features

CTX_DIM = 3  # cos phi_t, sin phi_t, tau_rem / tau


class CategoricalDeepSets:
    """psi: FEAT -> H -> H (summed over executed touches, exclusive prefix); rho: [E, ctx] -> H -> H -> out."""

    def __init__(self, rng, out_dim, hidden=128, out_scale=0.01):
        self.psi = MLP([FEAT_DIM, hidden, hidden], rng)
        self.rho = MLP([hidden + CTX_DIM, hidden, hidden, out_dim], rng, out_scale=out_scale)

    def params(self):
        return self.psi.params() + self.rho.params()

    def forward(self, F, ctx):
        P, pc = self.psi.forward(F)
        E = np.cumsum(P, axis=1) - P
        out, rc = self.rho.forward(np.concatenate([E, ctx], axis=-1))
        return out, (pc, rc)

    def backward(self, cache, gout):
        pc, rc = cache
        g_rho, gX = self.rho.backward(rc, gout)
        gE = gX[..., :-CTX_DIM]
        gP = np.flip(np.cumsum(np.flip(gE, axis=1), axis=1), axis=1) - gE
        g_psi, _ = self.psi.backward(pc, gP)
        return g_psi + g_rho


def masked_log_softmax(logits, mask):
    z = np.where(mask, logits, -np.inf)
    return z - logsumexp(z, axis=-1, keepdims=True)


@dataclass
class TrainConfigV2:
    setname: str = "S"
    method: str = "spce_total"
    kappa: float = 6.0
    tau: float = 10.0
    L: int = 4095
    J: int = 16
    batch: int = 128
    lr: float = 3e-4
    critic_lr: float = 1e-3
    ent_coef: float = 1e-3
    clip: float = 0.2
    epochs: int = 4
    hidden: int = 128
    max_episodes: int = 100_000
    val_every: int = 10_240
    val_episodes: int = 500
    plateau_window: int = 5
    plateau_tol: float = 0.02   # nats
    seed: int = 0
    budget_minutes: float = 330.0
    extra: dict = field(default_factory=dict)


class TrainerV2:
    def __init__(self, cfg: TrainConfigV2, om: ObsModel | None = None):
        self.cfg = cfg
        self.om = om or ObsModel()
        self.lib = Library(get_set(cfg.setname))
        self.prior = Prior(self.lib.K)
        self.rng = stream("train_v2", cfg.setname, cfg.method, cfg.kappa, cfg.tau, cfg.seed, cfg.L,
                          json.dumps(cfg.extra, sort_keys=True))
        self.rel = cfg.extra.get("frame", "abs") == "rel"
        Net = RelDeepSets if self.rel else CategoricalDeepSets
        self.pi = Net(self.rng, A, cfg.hidden)
        self.vf = Net(self.rng, 1, cfg.hidden)
        self.opt_pi = Adam(self.pi.params(), lr=cfg.lr)
        self.opt_vf = Adam(self.vf.params(), lr=cfg.critic_lr)
        self.episodes = 0
        self.history = []
        self.Tmax = int(math.floor(cfg.tau + 1e-9))

    def _states(self, rng, B):
        cfg = self.cfg
        k0, x0, y0, t0 = self.prior.sample(rng, B)
        J = 1 if cfg.method == "full_state" else cfg.J
        if J == 1:
            kb, xb, yb, tb = k0[:, None], x0[:, None], y0[:, None], t0[:, None]
        else:
            ib = [sample_in_ball(self.lib, self.prior, rng, (k0[b], x0[b], y0[b], t0[b]), J) for b in range(B)]
            kb, xb, yb, tb = (np.stack([v[i] for v in ib]) for i in range(4))
        kc, xc, yc, tc = (v.reshape(B, cfg.L) for v in self.prior.sample(rng, B * cfg.L))
        cat = lambda a, b: np.concatenate([a, b], axis=1)
        return (k0, x0, y0, t0), J, (cat(kb, kc), cat(xb, xc), cat(yb, yc), cat(tb, tc))

    def rollout(self, rng, B=None, greedy=False):
        cfg, om, lib = self.cfg, self.om, self.lib
        B = B or cfg.batch
        T = self.Tmax
        (k0, x0, y0, t0), J, (kS, xS, yS, tS) = self._states(rng, B)
        phi_t = rng.uniform(0, 2 * math.pi, B)
        tau_rem = np.full(B, cfg.tau)
        F = np.zeros((B, T, FEAT_DIM)); CTX = np.zeros((B, T, CTX_DIM))
        MASK = np.zeros((B, T, A), dtype=bool); ACT = np.zeros((B, T), dtype=int)
        R = np.zeros((B, T)); COST = np.ones((B, T)); alive = np.zeros((B, T), dtype=bool)
        RAW = np.zeros((B, T, 6)); PHIT = np.zeros((B, T)); TAUR = np.zeros((B, T))
        cum = np.zeros((B, J + cfg.L))
        g_prev = np.zeros(B)
        drop = cfg.method == "no_nc_input"
        for t in range(T):
            live = tau_rem >= 1.0 - 1e-12
            alive[:, t] = live
            CTX[:, t] = np.stack([np.cos(phi_t), np.sin(phi_t), tau_rem / cfg.tau], axis=1)
            PHIT[:, t], TAUR[:, t] = phi_t, tau_rem
            c_all = 1.0 + cfg.kappa * np.abs((PHI[None, :] - phi_t[:, None] + np.pi) % (2 * np.pi) - np.pi) / np.pi
            feas = c_all <= tau_rem[:, None] + 1e-12
            feas[~live] = True  # dead rows: any value, masked out of the loss
            MASK[:, t] = feas
            logits, _ = self.pi.forward(*self._inputs(F, CTX, RAW, PHIT, TAUR, alive, t + 1))
            lp = masked_log_softmax(logits[:, t], feas)
            if greedy:
                a = np.argmax(lp, axis=1)
            else:
                g = rng.gumbel(size=lp.shape)
                a = np.argmax(np.where(feas, lp + g, -np.inf), axis=1)
            ACT[:, t] = a
            phi, psi = PHI[a], PSI[a]
            c = c_all[np.arange(B), a]
            COST[:, t] = c
            o = sample_obs(om, lib, rng, k0, x0, y0, t0, phi, psi)
            hit, qx, qy, qn = cast(lib, kS, xS, yS, tS, phi[:, None], psi[:, None])
            ll = loglik_from_pred(om, o[0][:, None], o[1][:, None], o[2][:, None], o[3][:, None], hit, qx, qy, qn)
            cum += ll * live[:, None]
            lnum = logsumexp(cum[:, :J], axis=1) - math.log(J)
            lden = np.logaddexp(lnum, logsumexp(cum[:, J:], axis=1)) - math.log(cfg.L + 1)
            g = lnum - lden
            R[:, t] = np.where(live, g - g_prev, 0.0)
            g_prev = np.where(live, g, g_prev)
            F[:, t] = np.where(live[:, None], obs_features(phi, psi, *o, drop_nc=drop), 0.0)
            RAW[:, t] = np.stack([phi, psi, *(np.asarray(v, dtype=float) for v in o)], axis=1)
            tau_rem = np.where(live, tau_rem - c, tau_rem)
            phi_t = np.where(live, phi, phi_t)
        return dict(F=F, CTX=CTX, MASK=MASK, ACT=ACT, R=R, COST=COST, alive=alive, g_T=g_prev,
                    n_probes=alive.sum(1), RAW=RAW, PHIT=PHIT, TAUR=TAUR)

    def _inputs(self, F, CTX, RAW, PHIT, TAUR, alive, upto):
        """Network inputs for decisions 0..upto-1 (absolute: (F, CTX); finger-relative: (Frel, M, ctx, shift))."""
        if not self.rel:
            return F[:, :upto], CTX[:, :upto]
        Fr, M = rel_features(RAW[:, :upto], PHIT[:, :upto], alive[:, :upto],
                             drop_nc=self.cfg.method == "no_nc_input")
        ctx, sh = rel_ctx(PHIT[:, :upto], TAUR[:, :upto], self.cfg.tau)
        return Fr, M, ctx, sh

    def update(self, ro):
        cfg = self.cfg
        F, CTX, MASK, ACT, R, alive = ro["F"], ro["CTX"], ro["MASK"], ro["ACT"], ro["R"], ro["alive"]
        if cfg.method == "spce_myopic_rate":
            ret = R / ro["COST"]
        else:
            ret = np.flip(np.cumsum(np.flip(R, axis=1), axis=1), axis=1)
        m = alive
        nm = m.sum()
        T = F.shape[1]
        X = self._inputs(F, CTX, ro["RAW"], ro["PHIT"], ro["TAUR"], alive, T)
        V, _ = self.vf.forward(*X)
        adv = ret - V[..., 0]
        adv = (adv - adv[m].mean()) / (adv[m].std() + 1e-8)
        logits, _ = self.pi.forward(*X)
        lp_old = np.take_along_axis(masked_log_softmax(logits, MASK), ACT[..., None], axis=-1)[..., 0]
        onehot = np.zeros(MASK.shape); np.put_along_axis(onehot, ACT[..., None], 1.0, axis=-1)
        for _ in range(cfg.epochs):
            logits, cache = self.pi.forward(*X)
            lsm = masked_log_softmax(logits, MASK)
            p = np.where(MASK, np.exp(lsm), 0.0)
            lp = np.take_along_axis(lsm, ACT[..., None], axis=-1)[..., 0]
            ratio = np.exp(lp - lp_old)
            unc = ratio * adv
            clp = np.clip(ratio, 1 - cfg.clip, 1 + cfg.clip) * adv
            use = (unc <= clp) & m
            dL_dlp = np.where(use, -adv * ratio, 0.0) / nm
            g_logits = dL_dlp[..., None] * (onehot - p)
            # entropy bonus: loss -= ent_coef * H, dH/dz_i = -p_i (log p_i + H)
            plogp = np.where(MASK, p * np.where(MASK, lsm, 0.0), 0.0)
            H = -plogp.sum(-1, keepdims=True)
            dH = -p * (np.where(MASK, lsm, 0.0) + H)
            g_logits -= cfg.ent_coef * dH * m[..., None] / nm
            self.opt_pi.step(self.pi.backward(cache, g_logits))
        for _ in range(cfg.epochs):
            V, vc = self.vf.forward(*X)
            gV = np.where(m, V[..., 0] - ret, 0.0)[..., None] / nm
            self.opt_vf.step(self.vf.backward(vc, gV))
        return {"v_loss": float(np.mean(((V[..., 0] - ret) ** 2)[m])), "entropy": float(H[..., 0][m].mean())}

    def validate(self, greedy: bool = True):
        """Plateau metric: mean ball-sPCE g_T of the greedy (argmax) policy on fixed validation episodes (no PF).
        greedy=False gives the sampled-policy value (diagnostic)."""
        rng = stream("val_v2", self.cfg.setname, self.cfg.kappa, self.cfg.tau)
        tot, n = 0.0, 0
        while n < self.cfg.val_episodes:
            b = min(128, self.cfg.val_episodes - n)
            ro = self.rollout(rng, B=b, greedy=greedy)
            tot += float(ro["g_T"].sum()); n += b
        return tot / n

    def train(self, log_path=None, verbose=True):
        cfg = self.cfg
        t0 = time.time()
        vals, status = [], "max_episodes"
        cap = math.log(cfg.L + 1)
        while self.episodes < cfg.max_episodes:
            ro = self.rollout(self.rng)
            st = self.update(ro)
            self.episodes += cfg.batch
            rec = {"episodes": self.episodes, "g_T_mean": float(ro["g_T"].mean()),
                   "sat_frac": float(np.mean(ro["g_T"] > cap - 0.5)), "probes_mean": float(ro["n_probes"].mean()),
                   "elapsed_s": time.time() - t0, **st}
            if self.episodes % cfg.val_every < cfg.batch:
                v = self.validate()
                vals.append(v)
                rec["val_ball_spce"] = v
                rec["val_ball_spce_sampled"] = self.validate(greedy=False)
                if verbose:
                    print(json.dumps(rec), flush=True)
                w = cfg.plateau_window
                if len(vals) >= 2 * w and np.mean(vals[-w:]) - np.mean(vals[-2 * w:-w]) < cfg.plateau_tol:
                    status = "plateau"
                    self.history.append(rec)
                    break
            self.history.append(rec)
            if time.time() - t0 > 0.8 * cfg.budget_minutes * 60:
                status = "EARLY_STOP_AT_80_PCT_BUDGET"
                print(status, flush=True)
                break
        self.status = status
        if log_path:
            json.dump({"config": asdict(cfg), "status": status, "history": self.history}, open(log_path, "w"))
        return status

    def act(self, pf, ts):
        """Deterministic (argmax) action for evaluation: history from the PF, context from the travel state."""
        t = len(pf.hist)
        F = np.zeros((1, t + 1, FEAT_DIM))
        for i, (phi, psi, o) in enumerate(pf.hist):
            F[0, i] = obs_features(phi, psi, o[0], o[1], o[2], o[3], drop_nc=self.cfg.method == "no_nc_input")
        ctx = np.zeros((1, t + 1, CTX_DIM))
        ctx[0, t] = [math.cos(ts.phi), math.sin(ts.phi), ts.tau_rem / ts.tau]
        if self.rel:
            RAW = np.zeros((1, t + 1, 6)); PHIT = np.full((1, t + 1), ts.phi); TAUR = np.full((1, t + 1), ts.tau_rem)
            for i, (phi, psi, o) in enumerate(pf.hist):
                RAW[0, i] = [phi, psi, float(o[0]), float(o[1]), float(o[2]), float(o[3])]
            alive = np.zeros((1, t + 1), dtype=bool); alive[0, :t] = True
            logits, _ = self.pi.forward(*self._inputs(F, ctx, RAW, PHIT, TAUR, alive, t + 1))
        else:
            logits, _ = self.pi.forward(F, ctx)
        lsm = masked_log_softmax(logits[0, t], ts.feasible())
        return int(np.argmax(lsm))
