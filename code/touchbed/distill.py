"""Distillation of G* into a belief-free, finger-relative student (docs/07_hypotheses_v3.md §2.1, §1.6; amendment v3.0
C7, v3.1 D1).

Loss per labelled decision (feasible-scored set F = teacher mask):
    L = CE(p, q) + lambda * CE(p, onehot(a_teacher)),   p = softmax over F of the student logits,
    q = softmax over F of beta_T * s / sigma_s,  sigma_s = SD of s over F  (q uniform over argmax s if sigma_s < 1e-6).
Gradient wrt the logits on F: (1 + lambda) p - q - lambda onehot  (0 outside F).

Floored normalised regret (§1.6): r = (s_max - s(a)) / max(s_max - s_med, rho s_max), rho = 0.05, s_med = median of s
over F; decisions with s_max = 0 are excluded (counted); tie decision iff s_max - s_med < rho s_max.
"""
from __future__ import annotations

import math
from dataclasses import asdict, dataclass

import numpy as np

from .nn import Adam
from .relframe import RelDeepSets, rel_ctx, rel_features
from .travel import A

RHO = 0.05

HP_GRID = (  # amendment v3.0 C7: (lr, beta_T, lambda, batch)
    (1e-3, 4.0, 0.5, 256),
    (3e-4, 4.0, 0.5, 256),
    (1e-3, 16.0, 0.5, 256),
    (1e-3, 4.0, 0.0, 512),
)


# ─── targets, loss, regret ───────────────────────────────────────────────────────────────────────────────────────────
def soft_target(s, mask, beta_T):
    """q over the last axis; s, mask (..., A)."""
    s = np.asarray(s, dtype=float)
    n = mask.sum(-1, keepdims=True)
    mu = np.where(mask, s, 0.0).sum(-1, keepdims=True) / np.maximum(n, 1)
    sd = np.sqrt(np.where(mask, (s - mu) ** 2, 0.0).sum(-1, keepdims=True) / np.maximum(n, 1))
    smax = np.where(mask, s, -np.inf).max(-1, keepdims=True)
    tied = sd < 1e-6
    z = np.where(mask, beta_T * (s - smax) / np.where(tied, 1.0, sd), -np.inf)
    q = np.exp(z)
    q = q / q.sum(-1, keepdims=True)
    uni = mask & (s >= smax)
    uni = uni / np.maximum(uni.sum(-1, keepdims=True), 1)
    return np.where(tied, uni, q)


def masked_softmax(logits, mask):
    z = np.where(mask, logits, -np.inf)
    z = z - z.max(-1, keepdims=True)
    p = np.exp(z)
    return p / p.sum(-1, keepdims=True)


def loss_and_grad(logits, s, mask, a_teacher, valid, beta_T, lam):
    """logits, s, mask: (B, T, A); a_teacher, valid: (B, T). Mean loss over valid decisions and d loss / d logits."""
    m = mask & valid[..., None]
    m_safe = np.where(valid[..., None], m, True)        # invalid rows: any well-defined softmax, zero weight below
    p = masked_softmax(logits, m_safe)
    q = soft_target(s, m_safe, beta_T)
    oh = np.zeros_like(p)
    np.put_along_axis(oh, np.clip(a_teacher, 0, A - 1)[..., None], 1.0, axis=-1)
    logp = np.log(np.where(m_safe, p, 1.0))
    li = -(q * logp).sum(-1) - lam * (oh * logp).sum(-1)
    n = max(int(valid.sum()), 1)
    loss = float((li * valid).sum() / n)
    g = ((1.0 + lam) * p - q - lam * oh) * m_safe * valid[..., None] / n
    return loss, g


def regret(s, mask, a):
    """Floored normalised regret of action(s) a; returns (r, excluded, tie) arrays."""
    s = np.asarray(s, dtype=float)
    smax = np.where(mask, s, -np.inf).max(-1)
    smed = np.array([np.median(si[mi]) for si, mi in zip(s.reshape(-1, s.shape[-1]), mask.reshape(-1, s.shape[-1]))]
                    ).reshape(smax.shape)
    sa = np.take_along_axis(s, np.asarray(a)[..., None], axis=-1)[..., 0]
    excluded = smax <= 0
    den = np.maximum(smax - smed, RHO * smax)
    r = np.where(excluded, np.nan, (smax - sa) / np.where(excluded, 1.0, den))
    tie = (~excluded) & (smax - smed < RHO * smax)
    return r, excluded, tie


# ─── data ────────────────────────────────────────────────────────────────────────────────────────────────────────────
def episode_arrays(history, labels, T):
    """Pack one labelled episode: RAW (T, 6), PHIT, TAUR (T), valid (T), S (T, A) float32, MASK (T, A), AT (T)."""
    RAW = np.zeros((T, 6)); PHIT = np.zeros(T); TAUR = np.zeros(T); valid = np.zeros(T, dtype=bool)
    S = np.zeros((T, A), dtype=np.float32); MASK = np.zeros((T, A), dtype=bool); AT = np.zeros(T, dtype=np.int16)
    BF = np.zeros((T, BELIEF_DIM), dtype=np.float32)
    for t, lab in enumerate(labels[:T]):
        PHIT[t], TAUR[t], valid[t] = lab["phi_t"], lab["tau_rem"], True
        S[t], MASK[t], AT[t] = lab["s"], lab["mask"], lab["a_teacher"]
        if "belief" in lab:
            BF[t] = lab["belief"]
    for i, (phi, psi, o) in enumerate(history[:T]):
        RAW[i] = [phi, psi, float(o[0]), float(o[1]), float(o[2]), float(o[3])]
    return dict(RAW=RAW, PHIT=PHIT, TAUR=TAUR, valid=valid, S=S, MASK=MASK, AT=AT, BF=BF)


def stack(eps):
    return {k: np.stack([e[k] for e in eps]) for k in eps[0]}


def save_shard(path, eps, meta):
    import os
    os.makedirs(os.path.dirname(os.path.abspath(path)), exist_ok=True)
    d = stack(eps)
    np.savez_compressed(path, meta=np.array(__import__("json").dumps(meta)), **d)


def load_shards(paths):
    parts = [dict(np.load(p, allow_pickle=False)) for p in paths]
    out = {k: np.concatenate([p[k] for p in parts]) for k in parts[0] if k != "meta"}
    return out


# ─── model ───────────────────────────────────────────────────────────────────────────────────────────────────────────
@dataclass
class DistillConfig:
    lr: float = 1e-3
    beta_T: float = 4.0
    lam: float = 0.5
    batch: int = 256            # decisions-equivalent: episodes per step = max(1, batch // T)
    hidden: int = 128
    tau: float = 10.0
    max_epochs: int = 50
    stop_tol: float = 0.005
    stop_patience: int = 3
    seed: int = 501
    budget_minutes: float = 330.0


class Student:
    """Finger-relative DeepSets head (relframe.RelDeepSets), belief-free; argmax over feasible actions."""
    name = "student"
    needs_belief = False

    def __init__(self, rng, hidden=128, tau=10.0):
        self.net = RelDeepSets(rng, A, hidden)
        self.tau = tau

    def logits(self, RAW, PHIT, TAUR, valid):
        Fr, M = rel_features(RAW, PHIT, valid)
        ctx, sh = rel_ctx(PHIT, TAUR, self.tau)
        return self.net.forward(Fr, M, ctx, sh)

    def act(self, hview, ts):
        """Decision t uses touches 0..t-1 (the full relative history is re-encoded, as timed in Lat′)."""
        t = len(hview.hist)
        RAW = np.zeros((1, t + 1, 6)); PHIT = np.full((1, t + 1), ts.phi); TAUR = np.full((1, t + 1), ts.tau_rem)
        for i, (phi, psi, o) in enumerate(hview.hist):
            RAW[0, i] = [phi, psi, float(o[0]), float(o[1]), float(o[2]), float(o[3])]
        valid = np.zeros((1, t + 1), dtype=bool); valid[0, :t] = True
        out, _ = self.logits(RAW, PHIT, TAUR, valid)
        z = np.where(ts.feasible(), out[0, t], -np.inf)
        return int(np.argmax(z))

    def get_state(self):
        return [p.copy() for p in self.net.params()]

    def set_state(self, ps):
        for p, v in zip(self.net.params(), ps):
            p[...] = v


def decision_logits(student, D, idx):
    """Logits (B, T, A) for the decisions of episodes idx (decision t sees touches < t: valid mask shifted)."""
    PHIT, TAUR = D["PHIT"][idx], D["TAUR"][idx]
    if isinstance(student, BeliefStudent):
        return student.logits_from(D["BF"][idx], PHIT, TAUR)
    return student.logits(D["RAW"][idx], PHIT, TAUR, D["valid"][idx])


def mean_regret(student, D, idx=None, chunk=256):
    idx = np.arange(len(D["valid"])) if idx is None else np.asarray(idx)
    rs, n_ex, n_tie, n = [], 0, 0, 0
    for c in range(0, len(idx), chunk):
        j = idx[c:c + chunk]
        out, _ = decision_logits(student, D, j)
        V, S, M = D["valid"][j], D["S"][j].astype(float), D["MASK"][j]
        a = np.argmax(np.where(M, out, -np.inf), axis=-1)
        r, ex, tie = regret(np.where(V[..., None], S, 1.0), np.where(V[..., None], M, True), a)
        rs.append(r[V & ~ex]); n_ex += int((ex & V).sum()); n_tie += int((tie & V).sum()); n += int(V.sum())
    r = np.concatenate(rs) if rs else np.array([])
    return {"R_bar": float(np.mean(r)) if len(r) else float("nan"), "n_decisions": n, "n_excluded": n_ex,
            "tie_fraction": n_tie / max(n - n_ex, 1)}


def train_round(student, opt, D, train_idx, val_D, val_idx, cfg: DistillConfig, rng, log, t0=None):
    """Epochs over the aggregated data until validation R̄ improves by < stop_tol over stop_patience evaluations
    (cap max_epochs). Returns the stop status. Last checkpoint is kept (no success-based selection)."""
    import time
    t0 = t0 or time.time()
    T = D["valid"].shape[1]
    ep_per_step = max(1, cfg.batch // T)
    best, since = math.inf, 0
    for epoch in range(cfg.max_epochs):
        perm = rng.permutation(train_idx)
        losses = []
        for c in range(0, len(perm), ep_per_step):
            j = perm[c:c + ep_per_step]
            out, cache = decision_logits(student, D, j)
            loss, g = loss_and_grad(out, D["S"][j].astype(float), D["MASK"][j], D["AT"][j].astype(int), D["valid"][j],
                                    cfg.beta_T, cfg.lam)
            opt.step(student.net.backward(cache, g))
            losses.append(loss)
        vr = mean_regret(student, val_D, val_idx)
        log.append({"epoch": epoch, "train_loss": float(np.mean(losses)), **{f"val_{k}": v for k, v in vr.items()},
                    "wall_s": time.time() - t0})
        if vr["R_bar"] < best - cfg.stop_tol:
            best, since = vr["R_bar"], 0
        else:
            since += 1
        if since >= cfg.stop_patience:
            return "converged"
        if time.time() - t0 > 0.8 * cfg.budget_minutes * 60:
            return "EARLY_STOP_AT_80_PCT_BUDGET"
    return "max_epochs"


def config_dict(cfg):
    return asdict(cfg)


# ─── belief-input student (H2 control, D3-B; 07_hypotheses_v3 §2.2, amendment v3.0 C9) ─────────────────────────────────
BELIEF_DIM = 48


def belief_features(pf) -> np.ndarray:
    """Per identity k (K = 8): (w_k, weighted mean x, y, weighted SD x, y, resultant length of |G_k|·theta), flattened
    (48,). Positions in mm / 100. Identities with no weight get zeros."""
    w = pf.weights()
    K = pf.prior.K
    out = np.zeros((K, 6))
    for k in range(K):
        sel = pf.k == k
        wk = float(w[sel].sum())
        if wk <= 0:
            continue
        ww = w[sel] / wk
        mx, my = float(ww @ pf.x[sel]), float(ww @ pf.y[sel])
        sx = math.sqrt(max(float(ww @ (pf.x[sel] - mx) ** 2), 0.0))
        sy = math.sqrt(max(float(ww @ (pf.y[sel] - my) ** 2), 0.0))
        g = len(pf.lib.sym[k])
        R = abs(complex(ww @ np.cos(g * pf.th[sel]), ww @ np.sin(g * pf.th[sel])))
        out[k] = [wk, mx / 100.0, my / 100.0, sx / 100.0, sy / 100.0, R]
    return out.reshape(-1)


class BeliefStudent:
    """Same output head and recipe as Student, input = belief_features(PF) + the relative context (no DeepSets)."""
    name = "belief_student"
    needs_belief = True

    def __init__(self, rng, hidden=128, tau=10.0):
        from .nn import MLP
        from .relframe import REL_CTX_DIM
        self.rho = MLP([BELIEF_DIM + REL_CTX_DIM, hidden, hidden, A], rng, out_scale=0.01)
        self.tau = tau

    class _Net:  # adapter so training code can call .net.params() / .net.backward()
        def __init__(self, outer):
            self.o = outer

        def params(self):
            return self.o.rho.params()

        def backward(self, cache, gout):
            from .relframe import abs_index_of_rel
            rc, s = cache
            gout = np.take_along_axis(gout, abs_index_of_rel(s), axis=-1)
            g, _ = self.o.rho.backward(rc, gout)
            return g

    @property
    def net(self):
        return BeliefStudent._Net(self)

    def logits_from(self, BF, PHIT, TAUR):
        from .relframe import rel_index_of_abs
        ctx, sh = rel_ctx(PHIT, TAUR, self.tau)
        out, rc = self.rho.forward(np.concatenate([BF, ctx], axis=-1))
        return np.take_along_axis(out, rel_index_of_abs(sh), axis=-1), (rc, sh)

    def act(self, pf, ts):
        out, _ = self.logits_from(belief_features(pf)[None, None, :], np.full((1, 1), ts.phi),
                                  np.full((1, 1), ts.tau_rem))
        return int(np.argmax(np.where(ts.feasible(), out[0, 0], -np.inf)))

    def get_state(self):
        return [p.copy() for p in self.rho.params()]

    def set_state(self, ps):
        for p, v in zip(self.rho.params(), ps):
            p[...] = v
