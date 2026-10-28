"""Policy training on per-step sPCE increments with PPO (docs/07_hypotheses.md §3, docs/08_experiment_plan.yaml).

Methods (cfg.method):
  spce_total   — ours: advantage uses full returns-to-go G_t = sum_{tau>=t} r_tau (gamma = 1)  [non-myopic]
  spce_myopic  — control: advantage uses only the immediate increment r_t (gamma = 0)           [ablation A1]
  no_nc_obj    — spce_total with the normalized conditional likelihood q (misses carry no ratio) [ablation A2a]
  no_nc_input  — spce_total with no-contact touches removed from the DeepSets sum               [ablation A2b]
  rl_success   — sparse terminal reward 1[success] from a training PF (N = 1000)                 [baseline H1c]
r_t = g_t - g_{t-1},  g_t = log p(h_t|s_0) - log( 1/(L+1) sum_{l=0}^{L} p(h_t|s_l) ),  s_1..s_L ~ prior (fresh per episode).
"""
from __future__ import annotations

import json
import math
import time
from dataclasses import asdict, dataclass, field

import numpy as np
from scipy.special import logsumexp

from .geometry import Library, cast
from .likelihood import ObsModel, loglik_from_pred, sample_obs
from .nn import Adam, DeepSetsNet, gaussian_logp, obs_features, squash
from .pf import ParticleFilter, Prior, success
from .evaluate import make_states, stream


@dataclass
class TrainConfig:
    setname: str = "S"
    method: str = "spce_total"
    L: int = 255
    batch: int = 256
    T_choices: tuple = (3, 5, 8, 10)
    lr: float = 3e-4
    critic_lr: float = 1e-3
    ent_coef: float = 1e-3
    clip: float = 0.2
    epochs: int = 4
    hidden: int = 128
    encoder: str = "deepsets"
    budget_input: bool = True
    init_log_std: float = -0.5
    max_episodes: int = 400_000
    val_every: int = 20_000
    val_episodes: int = 200
    val_T: int = 5
    val_n_pf: int = 1000
    plateau_window: int = 5
    plateau_tol: float = 0.005     # 0.5 pp
    seed: int = 0
    budget_minutes: float = 300.0  # time_guard budget; stops at 80 %
    extra: dict = field(default_factory=dict)


def q_loglik_no_nc(om: ObsModel, c, px, py, n, hit, qx, qy, qn):
    """Normalized conditional likelihood q of ablation A2a: NC outcomes give log q = 0 for every state; a contact gives
    log p_eps(y | contact, s, a) if the ray hits s, otherwise the uniform contact density."""
    log_u_c = math.log(1.0 / (math.pi * 100.0 ** 2 * 2 * math.pi))
    full = loglik_from_pred(om, True, px, py, n, hit, qx, qy, qn)            # log p_eps(y, contact | s)
    p_contact_hit = math.log((1 - om.eps) + om.eps * 0.5)
    log_contact = np.where(hit, full - p_contact_hit, log_u_c)
    return np.where(np.asarray(c, dtype=bool), log_contact, 0.0)


class Trainer:
    def __init__(self, cfg: TrainConfig, om: ObsModel | None = None):
        self.cfg = cfg
        self.om = om or ObsModel()
        from .shapes import get_set
        self.lib = Library(get_set(cfg.setname))
        self.prior = Prior(self.lib.K)
        self.rng = stream("train", cfg.setname, cfg.method, cfg.seed, cfg.L, json.dumps(cfg.extra, sort_keys=True))
        self.pi = DeepSetsNet(self.rng, 2, cfg.hidden, out_scale=0.01, encoder=cfg.encoder)
        self.vf = DeepSetsNet(self.rng, 1, cfg.hidden, out_scale=0.01, encoder=cfg.encoder)
        self.log_std = np.full(2, cfg.init_log_std)
        self.opt_pi = Adam(self.pi.params() + [self.log_std], lr=cfg.lr)
        self.opt_vf = Adam(self.vf.params(), lr=cfg.critic_lr)
        self.episodes = 0
        self.history = []

    # ------------------------------------------------------------------------------------------------------------
    def _ctx(self, T_ep, Tmax):
        t = np.arange(Tmax)[None, :].astype(float)
        bl = (T_ep[:, None] - t)
        if not self.cfg.budget_input:
            bl = np.zeros_like(bl)
        return bl, np.broadcast_to(t, bl.shape).copy()

    def rollout(self, rng):
        cfg, om, lib = self.cfg, self.om, self.lib
        B, L = cfg.batch, cfg.L
        T_ep = rng.choice(np.asarray(cfg.T_choices), B)
        Tmax = int(T_ep.max())
        mask = np.arange(Tmax)[None, :] < T_ep[:, None]
        k0, x0, y0, t0 = self.prior.sample(rng, B)
        kc, xc, yc, tc = self.prior.sample(rng, B * L)
        kS = np.concatenate([k0[:, None], kc.reshape(B, L)], axis=1)
        xS = np.concatenate([x0[:, None], xc.reshape(B, L)], axis=1)
        yS = np.concatenate([y0[:, None], yc.reshape(B, L)], axis=1)
        tS = np.concatenate([t0[:, None], tc.reshape(B, L)], axis=1)
        F = np.zeros((B, Tmax, 9))
        U = np.zeros((B, Tmax, 2))
        R = np.zeros((B, Tmax))
        G = np.zeros((B, Tmax))
        obs_all = []
        bl, st = self._ctx(T_ep, Tmax)
        cum = np.zeros((B, L + 1))
        g_prev = np.zeros(B)
        drop = cfg.method == "no_nc_input"
        std = np.exp(self.log_std)
        for t in range(Tmax):
            out, _ = self.pi.forward(F[:, :t + 1], bl[:, :t + 1], st[:, :t + 1])
            u = out[:, t] + std * rng.standard_normal((B, 2))
            U[:, t] = u
            phi, psi = squash(u)
            c, px, py, n = sample_obs(om, lib, rng, k0, x0, y0, t0, phi, psi)
            obs_all.append((phi, psi, c, px, py, n))
            hit, qx, qy, qn = cast(lib, kS, xS, yS, tS, phi[:, None], psi[:, None])
            args = (c[:, None], px[:, None], py[:, None], n[:, None], hit, qx, qy, qn)
            ll = q_loglik_no_nc(om, *args) if cfg.method == "no_nc_obj" else loglik_from_pred(om, *args)
            cum += ll * mask[:, t, None]
            g = cum[:, 0] - (logsumexp(cum, axis=1) - math.log(L + 1))
            R[:, t] = (g - g_prev) * mask[:, t]
            G[:, t] = g
            g_prev = g
            F[:, t] = obs_features(phi, psi, c, px, py, n, drop_nc=drop)
        g_T = G[np.arange(B), T_ep - 1]
        if cfg.method == "rl_success":
            R = np.zeros((B, Tmax))
            R[np.arange(B), T_ep - 1] = self._success_reward(rng, (k0, x0, y0, t0), obs_all, T_ep)
        return dict(F=F, U=U, R=R, mask=mask, T_ep=T_ep, bl=bl, st=st, g_T=g_T, Tmax=Tmax)

    def _success_reward(self, rng, s0s, obs_all, T_ep):
        out = np.zeros(len(T_ep))
        for b in range(len(T_ep)):
            pf = ParticleFilter(self.lib, self.om, self.prior, 1000, rng)
            for t in range(T_ep[b]):
                phi, psi, c, px, py, n = (v[b] for v in obs_all[t])
                pf.update(phi, psi, (c, px, py, n))
            s0 = tuple(v[b] for v in s0s)
            out[b] = float(success(self.lib, pf.estimate(refine_iters=10), s0)["success"])
        return out

    # ------------------------------------------------------------------------------------------------------------
    def update(self, ro):
        cfg = self.cfg
        F, U, R, mask, bl, st = ro["F"], ro["U"], ro["R"], ro["mask"], ro["bl"], ro["st"]
        if cfg.method == "spce_myopic":
            ret = R.copy()                                            # gamma = 0: only the immediate increment
        else:
            ret = np.flip(np.cumsum(np.flip(R * mask, axis=1), axis=1), axis=1)  # gamma = 1 returns-to-go
        V, vcache = self.vf.forward(F, bl, st)
        V = V[..., 0]
        adv = (ret - V)
        m = mask
        nm = m.sum()
        a_mean = adv[m].mean()
        a_std = adv[m].std() + 1e-8
        adv = (adv - a_mean) / a_std
        out, _ = self.pi.forward(F, bl, st)
        logp_old = gaussian_logp(U, out, self.log_std)
        stats = {}
        for _ in range(cfg.epochs):
            out, cache = self.pi.forward(F, bl, st)
            std = np.exp(self.log_std)
            logp = gaussian_logp(U, out, self.log_std)
            ratio = np.exp(logp - logp_old)
            unclipped = ratio * adv
            clipped = np.clip(ratio, 1 - cfg.clip, 1 + cfg.clip) * adv
            use_unclipped = unclipped <= clipped
            # loss = -mean(min(unclipped, clipped)) - ent_coef * entropy
            dL_dlogp = np.where(use_unclipped & m, -adv * ratio, 0.0) / nm
            z = (U - out) / std
            g_mu = dL_dlogp[..., None] * z / std
            g_logstd = np.sum(dL_dlogp[..., None] * (z * z - 1.0), axis=(0, 1)) - cfg.ent_coef * np.ones(2)
            grads = self.pi.backward(cache, g_mu)
            self.opt_pi.step(grads + [g_logstd])
            self.log_std[:] = np.clip(self.log_std, -4.0, 1.0)
            stats["clipfrac"] = float(np.mean((~use_unclipped)[m]))
        for _ in range(cfg.epochs):
            V, vcache = self.vf.forward(F, bl, st)
            gV = np.where(m, V[..., 0] - ret, 0.0)[..., None] / nm
            self.opt_vf.step(self.vf.backward(vcache, gV))
        stats["v_loss"] = float(np.mean(((V[..., 0] - ret) ** 2)[m]))
        return stats

    # ------------------------------------------------------------------------------------------------------------
    def act_deterministic(self, hist, T: int):
        """Policy mean action for a single history [(phi, psi, (c, px, py, n)), ...] with total budget T."""
        t = len(hist)
        F = np.zeros((1, t + 1, 9))
        for i, (phi, psi, o) in enumerate(hist):
            F[0, i] = obs_features(phi, psi, o[0], o[1], o[2], o[3], drop_nc=self.cfg.method == "no_nc_input")
        bl, st = self._ctx(np.array([T]), t + 1)
        out, _ = self.pi.forward(F, bl, st)
        phi, psi = squash(out[0, t])
        return float(phi), float(psi)

    def validate(self):
        """Neutral plateau metric: success at T = val_T on fixed validation states with a small PF (N = val_n_pf)."""
        cfg = self.cfg
        lib, prior, states = make_states(cfg.setname, "val", cfg.val_episodes)
        succ, igs = [], []
        for i, s0 in enumerate(states):
            pf = ParticleFilter(lib, self.om, prior, cfg.val_n_pf, stream("val_pf", cfg.setname, i))
            orng = stream("val_obs", cfg.setname, i)
            for t in range(cfg.val_T):
                phi, psi = self.act_deterministic(pf.hist, cfg.val_T)
                obs = tuple(v[0] for v in sample_obs(self.om, lib, orng, np.array([s0[0]]), s0[1], s0[2], s0[3], phi, psi))
                pf.update(phi, psi, obs)
            succ.append(success(lib, pf.estimate(refine_iters=10), s0)["success"])
            igs.append(pf.realized_ig_evidence(s0))
        return float(np.mean(succ)), float(np.mean(igs))

    def train(self, log_path=None, verbose=True):
        cfg = self.cfg
        t_start = time.time()
        vals = []
        status = "max_episodes"
        while self.episodes < cfg.max_episodes:
            ro = self.rollout(self.rng)
            st = self.update(ro)
            self.episodes += cfg.batch
            rec = {"episodes": self.episodes, "spce_T_mean": float(ro["g_T"].mean()),
                   "sat_frac": float(np.mean(ro["g_T"][ro["T_ep"] == max(cfg.T_choices)] > math.log(cfg.L + 1) - 0.5)),
                   "log_std": self.log_std.tolist(), "elapsed_s": time.time() - t_start, **st}
            if self.episodes % cfg.val_every < cfg.batch:
                vs, vig = self.validate()
                vals.append(vs)
                rec.update({"val_success": vs, "val_ig": vig})
                if verbose:
                    print(json.dumps(rec), flush=True)
                if len(vals) >= 2 * cfg.plateau_window:
                    w = cfg.plateau_window
                    if np.mean(vals[-w:]) - np.mean(vals[-2 * w:-w]) < cfg.plateau_tol:
                        status = "plateau"
                        self.history.append(rec)
                        break
            self.history.append(rec)
            if time.time() - t_start > 0.8 * cfg.budget_minutes * 60:
                status = "EARLY_STOP_AT_80_PCT_BUDGET"
                print(status, flush=True)
                break
        self.status = status
        if log_path:
            with open(log_path, "w") as f:
                json.dump({"config": asdict(self.cfg), "status": status, "history": self.history}, f)
        return status

    def state_dict(self):
        return {"pi": [p.copy() for p in self.pi.params()], "log_std": self.log_std.copy(),
                "vf": [p.copy() for p in self.vf.params()]}
