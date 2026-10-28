"""Touch-selection baselines: random, coverage (max-min distance, as in zheng2026bayesian) and greedy PF-EIG
(one-step expected information gain by nested Monte Carlo on the particle belief; docs/07_hypotheses.md §2)."""
from __future__ import annotations

import math

import numpy as np
from scipy.special import logsumexp
from scipy.stats import qmc

from .geometry import PSI_MAX, cast
from .likelihood import loglik_from_pred, wrap


def sobol_candidates(rng: np.random.Generator, C: int):
    m = int(math.ceil(math.log2(max(C, 2))))
    u = qmc.Sobol(d=2, scramble=True, seed=rng).random(1 << m)[:C]
    return (u[:, 0] * 2 - 1) * math.pi, (u[:, 1] * 2 - 1) * PSI_MAX


class RandomPolicy:
    name = "random"

    def __init__(self, rng):
        self.rng = rng

    def act(self, pf):
        return float(self.rng.uniform(-math.pi, math.pi)), float(self.rng.uniform(-PSI_MAX, PSI_MAX))


class CoveragePolicy:
    """Pick the candidate whose predicted contact on the current MAP state is farthest from all previous contacts."""
    name = "coverage"

    def __init__(self, rng, C: int = 64):
        self.rng, self.C = rng, C

    def act(self, pf):
        phi, psi = sobol_candidates(self.rng, self.C)
        mass = pf.identity_mass()
        kh = int(np.argmax(mass))
        sel = np.flatnonzero(pf.k == kh)
        i = sel[np.argmax(pf.loglik_hist[sel])] if len(sel) else 0
        hit, qx, qy, _ = cast(pf.lib, kh, pf.x[i], pf.y[i], pf.th[i], phi, psi)
        contacts = np.array([[o[1], o[2]] for _, _, o in pf.hist if o[0]]).reshape(-1, 2)
        if not hit.any():
            j = int(self.rng.integers(self.C))
        elif len(contacts) == 0:
            j = int(np.flatnonzero(hit)[0])
        else:
            d = np.min(np.hypot(qx[:, None] - contacts[None, :, 0], qy[:, None] - contacts[None, :, 1]), axis=1)
            d = np.where(hit, d, -np.inf)
            j = int(np.argmax(d))
        return float(phi[j]), float(psi[j])


def eig_candidates(pf, phi, psi, M: int, rng: np.random.Generator, particles=None):
    """Nested-MC one-step EIG for each candidate (phi[c], psi[c]) on the PF belief (or a given particle subset).
    EIG(a) = 1/M sum_m [ log p(y_m | s_jm, a) - log sum_n w_n p(y_m | s_n, a) ],  j_m ~ w, y_m ~ p(. | s_jm, a)."""
    if particles is None:
        k, x, y, th, w = pf.k, pf.x, pf.y, pf.th, pf.weights()
    else:
        k, x, y, th, w = particles
    om = pf.om
    C = len(phi)
    hit, qx, qy, qn = cast(pf.lib, k[:, None], x[:, None], y[:, None], th[:, None], phi[None, :], psi[None, :])  # (N, C)
    j = rng.choice(len(w), size=(M, C), p=w)
    cols = np.arange(C)[None, :]
    h_j, x_j, y_j, n_j = hit[j, cols], qx[j, cols], qy[j, cols], qn[j, cols]                         # (M, C)
    # sample y_m from p_eps(. | s_jm, a): geometric branch with prob 1 - eps, uniform branch otherwise
    shp = (M, C)
    ub = rng.random(shp) < om.eps
    uc = rng.random(shp) < 0.5
    c = np.where(ub, uc, h_j)
    r = 100.0 * np.sqrt(rng.random(shp))
    a = rng.uniform(-np.pi, np.pi, shp)
    px = np.where(ub, r * np.cos(a), x_j + om.sigma_p * rng.standard_normal(shp))
    py = np.where(ub, r * np.sin(a), y_j + om.sigma_p * rng.standard_normal(shp))
    pn = np.where(ub, rng.uniform(-np.pi, np.pi, shp), wrap(n_j + om.sigma_n * rng.standard_normal(shp)))
    # log-likelihood of each sampled outcome under every particle: (M, N, C)
    ll = loglik_from_pred(om, c[:, None, :], px[:, None, :], py[:, None, :], pn[:, None, :],
                          hit[None], qx[None], qy[None], qn[None])
    ll_true = np.take_along_axis(ll, j[:, None, :], axis=1)[:, 0, :]                                   # (M, C)
    ll_marg = logsumexp(ll + np.log(w)[None, :, None], axis=1)                                          # (M, C)
    return np.mean(ll_true - ll_marg, axis=0)


class GreedyEIGPolicy:
    """Greedy PF-EIG: the PF itself (N particles) is the belief; C Sobol candidates re-drawn each step; M outcomes."""
    name = "greedy_eig"

    def __init__(self, rng, C: int = 64, M: int = 64, chunk: int = 16):
        self.rng, self.C, self.M, self.chunk = rng, C, M, chunk

    def act(self, pf):
        phi, psi = sobol_candidates(self.rng, self.C)
        eig = np.concatenate([eig_candidates(pf, phi[i:i + self.chunk], psi[i:i + self.chunk], self.M, self.rng)
                              for i in range(0, self.C, self.chunk)])
        j = int(np.argmax(eig))
        self.last_eig = float(eig[j])
        return float(phi[j]), float(psi[j])
