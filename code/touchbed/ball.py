"""Ball (success-region) information utilities (docs/07_hypotheses_v2.md §1.3-1.4)."""
from __future__ import annotations

import math

import numpy as np
from scipy.special import logsumexp

from .geometry import cast
from .likelihood import loglik_from_pred, wrap

R_XY = 5.0
R_TH = math.radians(5.0)


def in_ball(lib, k, x, y, th, k0, x0, y0, t0):
    g = lib.sym[k0]
    return ((np.asarray(k) == k0) & (np.hypot(np.asarray(x) - x0, np.asarray(y) - y0) < R_XY)
            & (np.min(np.abs(wrap(np.asarray(th)[..., None] - t0 - g)), axis=-1) < R_TH))


def neighbours(lib, k, x, y, th):
    """(N, N) boolean: particle n in the ball of particle i."""
    same = k[:, None] == k[None, :]
    near = np.hypot(x[:, None] - x[None, :], y[:, None] - y[None, :]) < R_XY
    nb = same & near
    out = np.zeros_like(nb)
    for kk in np.unique(k):
        sel = np.flatnonzero(k == kk)
        g = lib.sym[kk]
        d = np.min(np.abs(wrap(th[sel][:, None, None] - th[sel][None, :, None] - g[None, None, :])), axis=-1)
        out[np.ix_(sel, sel)] = nb[np.ix_(sel, sel)] & (d < R_TH)
    return out


def ball_eig(pf, phi, psi, M: int, rng, particles=None, nb=None, chunk: int = 16):
    """One-step expected increment of log P(B(s0) | h) on a particle belief, for candidates (phi[c], psi[c]):
    EIG_B(a) = 1/M sum_m [ log sum_{n in B(j_m)} w_n p(y_m|s_n,a) - log sum_{n in B(j_m)} w_n - log sum_n w_n p(y_m|s_n,a) ]."""
    k, x, y, th, w = particles if particles is not None else (pf.k, pf.x, pf.y, pf.th, pf.weights())
    if nb is None:
        nb = neighbours(pf.lib, k, x, y, th)
    om, lib = pf.om, pf.lib
    lw = np.log(np.maximum(w, 1e-300))
    out = []
    for c0 in range(0, len(phi), chunk):
        ph, ps = phi[c0:c0 + chunk], psi[c0:c0 + chunk]
        C = len(ph)
        hit, qx, qy, qn = cast(lib, k[:, None], x[:, None], y[:, None], th[:, None], ph[None, :], ps[None, :])
        j = rng.choice(len(w), size=(M, C), p=w)
        cols = np.arange(C)[None, :]
        shp = (M, C)
        ub = rng.random(shp) < om.eps
        uc = rng.random(shp) < 0.5
        cc = np.where(ub, uc, hit[j, cols])
        r = 100.0 * np.sqrt(rng.random(shp))
        aa = rng.uniform(-np.pi, np.pi, shp)
        px = np.where(ub, r * np.cos(aa), qx[j, cols] + om.sigma_p * rng.standard_normal(shp))
        py = np.where(ub, r * np.sin(aa), qy[j, cols] + om.sigma_p * rng.standard_normal(shp))
        pn = np.where(ub, rng.uniform(-np.pi, np.pi, shp), wrap(qn[j, cols] + om.sigma_n * rng.standard_normal(shp)))
        ll = loglik_from_pred(om, cc[:, None, :], px[:, None, :], py[:, None, :], pn[:, None, :],
                              hit[None], qx[None], qy[None], qn[None])                 # (M, N, C)
        joint = ll + lw[None, :, None]
        mask = nb[j]                                                                   # (M, C, N)
        mask = np.transpose(mask, (0, 2, 1))                                           # (M, N, C)
        l_ball = logsumexp(np.where(mask, joint, -np.inf), axis=1)
        l_wb = logsumexp(np.where(mask, lw[None, :, None], -np.inf), axis=1)
        l_all = logsumexp(joint, axis=1)
        out.append(np.mean(l_ball - l_wb - l_all, axis=0))
    return np.concatenate(out)


def sample_in_ball(lib, prior, rng, s0, J: int):
    """J states uniform in B(s0) intersected with the prior support (rejection for the box clip)."""
    k0, x0, y0, t0 = s0
    g = lib.sym[k0]
    xs, ys = [], []
    while len(xs) < J:
        r = R_XY * np.sqrt(rng.random(4 * J))
        a = rng.uniform(-np.pi, np.pi, 4 * J)
        x, y = x0 + r * np.cos(a), y0 + r * np.sin(a)
        ok = prior.inside(x, y)
        xs += list(x[ok]); ys += list(y[ok])
    th = wrap(t0 + g[rng.integers(0, len(g), J)] + rng.uniform(-R_TH, R_TH, J))
    return np.full(J, k0), np.array(xs[:J]), np.array(ys[:J]), th
