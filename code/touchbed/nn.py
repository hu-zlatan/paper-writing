"""Small numpy neural networks with hand-written backpropagation and Adam (PyTorch is not installable in this
environment; see PROGRESS.md stage 10). Gradients are verified against finite differences in tests/test_nn.py.

DeepSets touch-history encoder (docs/07_hypotheses.md §2):  e(h_{t-1}) = sum_{tau < t} psi(f_tau),
policy head:  rho([e, remaining_budget/10, t/10]) -> Gaussian mean over unconstrained (phi~, psi~) + state-independent
log-std; critic head: same structure, scalar output. All prefix sums for a whole batch of trajectories are computed with
an exclusive cumulative sum, so one forward pass evaluates every (episode, step) decision.
"""
from __future__ import annotations

import math

import numpy as np

from .geometry import PSI_MAX, RHO

FEAT_DIM = 9  # [1, cos phi, sin phi, psi/psi_max, c, c*px/RHO, c*py/RHO, c*cos n, c*sin n]


def obs_features(phi, psi, c, px, py, n, drop_nc: bool = False):
    """Per-touch feature vector(s); arrays broadcast. If drop_nc, no-contact touches get an all-zero feature
    (removed from the DeepSets sum: the No-NC-input ablation)."""
    phi, psi, c, px, py, n = np.broadcast_arrays(*map(np.asarray, (phi, psi, c, px, py, n)))
    c = c.astype(float)
    f = np.stack([np.ones_like(phi, dtype=float), np.cos(phi), np.sin(phi), psi / PSI_MAX, c, c * px / RHO,
                  c * py / RHO, c * np.cos(n), c * np.sin(n)], axis=-1)
    if drop_nc:
        f = f * c[..., None]
    return f


class MLP:
    """Fully connected net with tanh hidden activations and linear output."""

    def __init__(self, sizes, rng: np.random.Generator, out_scale: float = 1.0):
        self.W, self.b = [], []
        for i, (a, b) in enumerate(zip(sizes[:-1], sizes[1:])):
            s = math.sqrt(1.0 / a) * (out_scale if i == len(sizes) - 2 else 1.0)
            self.W.append(rng.standard_normal((a, b)) * s)
            self.b.append(np.zeros(b))

    def params(self):
        return self.W + self.b

    def forward(self, x):
        cache = [x]
        h = x
        for i, (W, b) in enumerate(zip(self.W, self.b)):
            z = h @ W + b
            h = np.tanh(z) if i < len(self.W) - 1 else z
            cache.append(h)
        return h, cache

    def backward(self, cache, gout):
        """Returns (grads aligned with params(), grad wrt input)."""
        gW, gb = [None] * len(self.W), [None] * len(self.b)
        g = gout
        for i in reversed(range(len(self.W))):
            h_in = cache[i]
            if i < len(self.W) - 1:
                g = g * (1.0 - cache[i + 1] ** 2)  # tanh'
            gW[i] = h_in.reshape(-1, h_in.shape[-1]).T @ g.reshape(-1, g.shape[-1])
            gb[i] = g.reshape(-1, g.shape[-1]).sum(axis=0)
            g = g @ self.W[i].T
        return gW + gb, g


class DeepSetsNet:
    """psi: FEAT_DIM -> H -> H ; rho: H + 2 -> H -> H -> out."""

    def __init__(self, rng, out_dim: int, hidden: int = 128, out_scale: float = 0.01, encoder: str = "deepsets",
                 t_max: int = 10):
        self.encoder = encoder
        self.t_max = t_max
        self.psi = MLP([FEAT_DIM, hidden, hidden], rng)
        if encoder == "deepsets":
            rho_in = hidden + 2
        elif encoder == "concat":  # padded concatenation of the last t_max touch features (ablation A3)
            rho_in = FEAT_DIM * t_max + 2
        else:
            raise ValueError(encoder)
        self.rho = MLP([rho_in, hidden, hidden, out_dim], rng, out_scale=out_scale)

    def params(self):
        ps = self.rho.params()
        return (self.psi.params() + ps) if self.encoder == "deepsets" else ps

    def _inputs(self, F, budget_left, step):
        """F: (B, T, FEAT) features of executed touches; decision at step t uses touches tau < t."""
        B, T, _ = F.shape
        ctx = np.stack([budget_left / 10.0, step / 10.0], axis=-1)  # (B, T, 2)
        if self.encoder == "deepsets":
            P, pc = self.psi.forward(F)                                   # (B, T, H)
            E = np.cumsum(P, axis=1) - P                                  # exclusive prefix sum
            return np.concatenate([E, ctx], axis=-1), pc
        Z = np.zeros((B, T, FEAT_DIM * self.t_max))
        for t in range(T):
            for j in range(min(t, self.t_max)):
                Z[:, t, j * FEAT_DIM:(j + 1) * FEAT_DIM] = F[:, j]
        return np.concatenate([Z, ctx], axis=-1), None

    def forward(self, F, budget_left, step):
        X, pc = self._inputs(F, budget_left, step)
        out, rc = self.rho.forward(X)
        return out, (pc, rc)

    def backward(self, cache, gout):
        pc, rc = cache
        g_rho, gX = self.rho.backward(rc, gout)
        if self.encoder != "deepsets":
            return g_rho
        gE = gX[..., :-2]
        # E_t = sum_{tau < t} P_tau  =>  dL/dP_tau = sum_{t > tau} dL/dE_t (reverse exclusive cumsum)
        gP = np.flip(np.cumsum(np.flip(gE, axis=1), axis=1), axis=1) - gE
        g_psi, _ = self.psi.backward(pc, gP)
        return g_psi + g_rho


class Adam:
    def __init__(self, params, lr: float = 3e-4, b1: float = 0.9, b2: float = 0.999, eps: float = 1e-8,
                 max_grad_norm: float = 1.0):
        self.params, self.lr, self.b1, self.b2, self.eps, self.mgn = params, lr, b1, b2, eps, max_grad_norm
        self.m = [np.zeros_like(p) for p in params]
        self.v = [np.zeros_like(p) for p in params]
        self.t = 0

    def step(self, grads):
        """Gradient DEscent step (callers pass gradients of the loss to minimize). Global-norm clipping."""
        gn = math.sqrt(sum(float(np.sum(g * g)) for g in grads))
        scale = min(1.0, self.mgn / (gn + 1e-12)) if self.mgn else 1.0
        self.t += 1
        for p, g, m, v in zip(self.params, grads, self.m, self.v):
            g = g * scale
            m *= self.b1
            m += (1 - self.b1) * g
            v *= self.b2
            v += (1 - self.b2) * g * g
            mh = m / (1 - self.b1 ** self.t)
            vh = v / (1 - self.b2 ** self.t)
            p -= self.lr * mh / (np.sqrt(vh) + self.eps)
        return gn


def gaussian_logp(u, mu, log_std):
    z = (u - mu) / np.exp(log_std)
    return np.sum(-0.5 * z * z - log_std - 0.5 * math.log(2 * math.pi), axis=-1)


def squash(u):
    """Unconstrained (phi~, psi~) -> probe action (phi in [-pi, pi), psi in (-psi_max, psi_max))."""
    phi = (u[..., 0] + np.pi) % (2 * np.pi) - np.pi
    psi = PSI_MAX * np.tanh(u[..., 1])
    return phi, psi
