"""Policy learning on the exact notch control (gate G3 (iii) and H2b-P2; docs/07_hypotheses_v2.md §3, §4).
Same PPO update as touchbed/train_v2.py (clip 0.2, 4 epochs, tanh MLPs of width 128, masked-free categorical head over
the 72 notch actions, gamma = 1 returns-to-go, normalised advantages, entropy bonus). The reward is the exact sPCE of
the notch problem: with K = 2 identities and x marginalised exactly on the 401-point grid, the sPCE equals the realised
identity information log P(k* | h_t) - log P(k*); per-step increments are the rewards.
  method 'spce_total': returns-to-go over the T = 2 probes; 'spce_myopic': gamma = 0 (immediate increment only).
Evaluation is exact: V_pi = EIG(a1) + E_{y1}[EIG(pi(a1, y1) | b1)] by the quadrature of touchbed/notch.py, with the
argmax policy (and the sampled policy's probability of a horizontal first probe)."""
import json
import math
import time

import numpy as np

from . import notch as N
from .nn import MLP, Adam

FEAT = 6


def feats(step, a1, nc, z):
    """step-1 input: [1, 0, 0, 0, 0, 0]; step-2 input: [0, 1, is_H(a1), u1/70, nc1, z1/50 (0 if NC)]."""
    B = len(a1)
    F = np.zeros((B, FEAT))
    if step == 0:
        F[:, 0] = 1.0
        return F
    isH = a1 == N.H_ACT
    F[:, 1] = 1.0
    F[:, 2] = isH
    F[:, 3] = np.where(isH, 0.0, N.U_GRID[np.minimum(a1, len(N.U_GRID) - 1)] / 70.0)
    F[:, 4] = nc
    F[:, 5] = np.where(nc, 0.0, z / 50.0)
    return F


def log_softmax(z):
    m = z.max(-1, keepdims=True)
    return z - m - np.log(np.exp(z - m).sum(-1, keepdims=True))


class NotchTrainer:
    def __init__(self, method="spce_total", seed=0, lr=3e-4, critic_lr=1e-3, ent_coef=1e-3, batch=128, clip=0.2,
                 epochs=4, hidden=128):
        self.method, self.batch, self.clip, self.epochs, self.ent = method, batch, clip, epochs, ent_coef
        self.rng = np.random.default_rng(seed)
        self.pi = MLP([FEAT, hidden, hidden, N.N_ACT], self.rng, out_scale=0.01)
        self.vf = MLP([FEAT, hidden, hidden, 1], self.rng)
        self.opt_pi = Adam(self.pi.params(), lr=lr)
        self.opt_vf = Adam(self.vf.params(), lr=critic_lr)
        self.P = N.NotchProblem()
        self.episodes = 0
        self.lw0 = np.log(N.prior_belief())

    def _info(self, LW, s):
        """realised identity information for each row: log P(k_s | h) - log 1/2."""
        W = np.exp(LW - LW.max(1, keepdims=True))
        same = N.STATE_K[None, :] == N.STATE_K[s][:, None]
        return np.log((W * same).sum(1) / W.sum(1)) + math.log(2.0)

    def rollout(self, B, greedy=False):
        rng = self.rng
        s = rng.integers(0, N.NS, B)
        LW = np.tile(self.lw0, (B, 1))
        F = np.zeros((B, 2, FEAT)); ACT = np.zeros((B, 2), int); R = np.zeros((B, 2))
        a1 = np.zeros(B, int); nc1 = np.zeros(B, bool); z1 = np.zeros(B)
        g_prev = np.zeros(B)
        for t in range(2):
            F[:, t] = feats(t, a1, nc1, z1)
            logits, _ = self.pi.forward(F[:, t])
            lp = log_softmax(logits)
            a = np.argmax(lp, 1) if greedy else np.argmax(lp + rng.gumbel(size=lp.shape), 1)
            ACT[:, t] = a
            nc = np.zeros(B, bool); z = np.zeros(B)
            for aa in np.unique(a):
                sel = np.flatnonzero(a == aa)
                nc[sel], z[sel] = self.P.sample_obs_batch(int(aa), s[sel], rng)
                LW[sel] += self.P.loglik_batch(int(aa), nc[sel], z[sel])
            g = self._info(LW, s)
            R[:, t] = g - g_prev
            g_prev = g
            if t == 0:
                a1, nc1, z1 = a, nc, z
        return dict(F=F, ACT=ACT, R=R, g_T=g_prev)

    def update(self, ro):
        F, ACT, R = ro["F"], ro["ACT"], ro["R"]
        ret = R.copy() if self.method == "spce_myopic" else np.flip(np.cumsum(np.flip(R, 1), 1), 1)
        V, _ = self.vf.forward(F)
        adv = ret - V[..., 0]
        adv = (adv - adv.mean()) / (adv.std() + 1e-8)
        lp_old = np.take_along_axis(log_softmax(self.pi.forward(F)[0]), ACT[..., None], -1)[..., 0]
        onehot = np.zeros(F.shape[:2] + (N.N_ACT,)); np.put_along_axis(onehot, ACT[..., None], 1.0, -1)
        n = ACT.size
        for _ in range(self.epochs):
            logits, cache = self.pi.forward(F)
            lsm = log_softmax(logits)
            p = np.exp(lsm)
            lp = np.take_along_axis(lsm, ACT[..., None], -1)[..., 0]
            ratio = np.exp(lp - lp_old)
            use = (ratio * adv) <= (np.clip(ratio, 1 - self.clip, 1 + self.clip) * adv)
            g_logits = (np.where(use, -adv * ratio, 0.0) / n)[..., None] * (onehot - p)
            H = -(p * lsm).sum(-1, keepdims=True)
            g_logits -= self.ent * (-p * (lsm + H)) / n
            self.opt_pi.step(self.pi.backward(cache, g_logits)[0])
        for _ in range(self.epochs):
            V, vc = self.vf.forward(F)
            self.opt_vf.step(self.vf.backward(vc, (V[..., 0] - ret)[..., None] / n)[0])
        return float(H.mean())

    def policy_step2(self, a1, nc, z):
        logits, _ = self.pi.forward(feats(1, np.full(len(z), a1), nc, z))
        return np.argmax(logits, 1)

    def exact_value(self, T=None):
        """Exact two-step identity information of the argmax policy from the prior, and the sampled policy's
        probability of a horizontal first probe."""
        T = T or N._Tables()
        w = N.prior_belief()
        l1 = log_softmax(self.pi.forward(feats(0, np.zeros(1, int), np.zeros(1, bool), np.zeros(1)))[0])[0]
        a1 = int(np.argmax(l1))
        eig1 = N.eig_batch(w[None], T)[0][a1]
        Pst, pr = N.posteriors(w, a1, T)
        nz = len(T.z[a1])
        nc = np.r_[np.zeros(nz, bool), True, False]
        z = np.r_[T.z[a1], 0.0, -90.0]
        a2 = self.policy_step2(a1, nc, z)
        E = N.eig_batch(Pst, T)
        v = eig1 + float((pr * E[np.arange(len(a2)), a2]).sum())
        return {"a1": a1, "a1_is_horizontal": a1 == N.H_ACT, "p_horizontal_first": float(np.exp(l1[N.H_ACT])),
                "v_pi": v}

    def train(self, max_episodes=100_000, eval_every=10_240, log_path=None):
        T = N._Tables()
        t0 = time.time()
        hist = []
        while self.episodes < max_episodes:
            ro = self.rollout(self.batch)
            H = self.update(ro)
            self.episodes += self.batch
            if self.episodes % eval_every < self.batch:
                rec = {"episodes": self.episodes, "g_T_mean": float(ro["g_T"].mean()), "entropy": H,
                       "elapsed_s": time.time() - t0, **self.exact_value(T)}
                hist.append(rec)
                print(json.dumps(rec), flush=True)
        final = self.exact_value(T)
        if log_path:
            json.dump({"method": self.method, "episodes": self.episodes, "history": hist, "final": final,
                       "wall_s": time.time() - t0}, open(log_path, "w"), indent=1, default=float)
        return final
