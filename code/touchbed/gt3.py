"""Ball-sPCE g_T of recorded v3 episodes on fixed per-episode contrastive draws (08 plan v3, metric ball_sPCE_g_T; H2).

g_T = log((1/J) sum_j p(h_T | s_j^B)) - log((1/(L+1)) [ (1/J) sum_j p(h_T | s_j^B) + sum_l p(h_T | s_l) ]),
s_j^B ~ uniform in B(s0) (J = 16), s_l ~ prior (L = 4,095) -- the reward of touchbed/train_v2.py::TrainerV2.rollout.
The draws come from stream('gT3_contrast', *ep_key) with the method-free episode key, so every method is scored on the
same draws (common random numbers). The history h_T is rebuilt exactly from the recorded actions
(gridpost.rebuild_history: observations are stream('obs', *ep_key) in order), so g_T is a post-hoc read-out of any
eval3 output and needs no new rollouts."""
from __future__ import annotations

import math

import numpy as np
from scipy.special import logsumexp

from .ball import sample_in_ball
from .evaluate import stream
from .geometry import cast
from .likelihood import loglik_from_pred

J_DEFAULT, L_DEFAULT = 16, 4095


def contrast_draws(lib, prior, s0, ep_key, J: int = J_DEFAULT, L: int = L_DEFAULT):
    """(k, x, y, th) arrays of length J + L: J in-ball states first, then L prior states."""
    rng = stream("gT3_contrast", *ep_key)
    kb, xb, yb, tb = sample_in_ball(lib, prior, rng, s0, J)
    kc, xc, yc, tc = prior.sample(rng, L)
    return (np.concatenate([kb, kc]), np.concatenate([xb, xc]), np.concatenate([yb, yc]), np.concatenate([tb, tc]))


def g_T(lib, om, hist, draws, J: int = J_DEFAULT):
    """Ball-sPCE of a touch history [(phi, psi, (c, px, py, n)), ...] against fixed contrastive draws."""
    kS, xS, yS, tS = draws
    L = len(kS) - J
    cum = np.zeros(len(kS))
    for phi, psi, o in hist:
        hit, qx, qy, qn = cast(lib, kS, xS, yS, tS, float(phi), float(psi))
        cum += loglik_from_pred(om, o[0], o[1], o[2], o[3], hit, qx, qy, qn)
    lnum = logsumexp(cum[:J]) - math.log(J)
    lden = np.logaddexp(lnum, logsumexp(cum[J:])) - math.log(L + 1)
    return float(lnum - lden)
