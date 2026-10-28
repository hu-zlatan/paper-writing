"""Finger-relative policy parametrisation (exploratory v2 dev variant; enabled by TrainConfigV2.extra["frame"] = "rel").

Motivation (docs/07c_amendment_v2_0.md, status note run 4): the absolute-action head scores the 256 actions in the
world frame from a context (cos phi_t, sin phi_t, tau_rem/tau), and the trained pilot policies ignored the random start
angle phi0. Here every decision is made in the frame of the current finger angle phi_t:
- the touch history is re-expressed relative to phi_t (probe angles phi_i - phi_t; contact point and normal rotated by
  -phi_t) and re-encoded by the DeepSets psi at every decision (T <= 6, so the T x T re-encoding is cheap);
- the head outputs logits over *relative* actions j = (dphi index, psi index); the absolute action is
  a = ((j_phi + s) mod N_PHI) * N_PSI + j_psi with s = round(phi_t / dphi) mod N_PHI;
- the context is (cos delta, sin delta, tau_rem/tau, cos phi_t, sin phi_t), delta = phi_t - s * dphi (sub-grid offset
  of the continuous start angle; zero after the first probe). The absolute (cos, sin) phi_t terms are kept because the
  prior on (x, y) is a square, so the task is only 4-fold rotation-symmetric.
The relative <-> absolute map is a per-row permutation, so its backward pass is the inverse permutation.
"""
from __future__ import annotations

import math

import numpy as np

from .nn import FEAT_DIM, MLP, obs_features
from .travel import N_PHI, N_PSI

REL_CTX_DIM = 5
DPHI = 2 * math.pi / N_PHI


def shift_and_delta(phi_t):
    phi_t = np.asarray(phi_t, dtype=float)
    s = np.rint(phi_t / DPHI).astype(int) % N_PHI
    d = (phi_t - s * DPHI + np.pi) % (2 * np.pi) - np.pi
    return s, d


def abs_index_of_rel(s):
    """(..., A) array: absolute action index for every relative index j, given shift s (...)."""
    j = np.arange(N_PHI * N_PSI)
    return (((j // N_PSI)[None, :] + np.asarray(s).reshape(-1, 1)) % N_PHI * N_PSI + (j % N_PSI)[None, :]).reshape(
        np.shape(s) + (N_PHI * N_PSI,))


def rel_index_of_abs(s):
    """(..., A) array: relative index for every absolute action a, given shift s (...)."""
    a = np.arange(N_PHI * N_PSI)
    return (((a // N_PSI)[None, :] - np.asarray(s).reshape(-1, 1)) % N_PHI * N_PSI + (a % N_PSI)[None, :]).reshape(
        np.shape(s) + (N_PHI * N_PSI,))


def rel_features(raw, phit, valid, drop_nc=False):
    """raw (B, T, 6) = (phi, psi, c, px, py, n) of executed touches; phit (B, T) finger angle at each decision;
    valid (B, T) whether touch i exists. Returns Frel (B, T, T, FEAT) and mask M (B, T, T) with M[b, t, i] = i < t and
    valid[b, i]."""
    B, T, _ = raw.shape
    ph = phit[:, :, None]                                   # decision t
    phi, psi, c, px, py, n = (raw[:, None, :, k] for k in range(6))   # touch i
    cr, sr = np.cos(-ph), np.sin(-ph)
    rpx, rpy = cr * px - sr * py, sr * px + cr * py
    F = obs_features(phi - ph, psi, c, rpx, rpy, n - ph, drop_nc=drop_nc)
    M = (np.arange(T)[None, :, None] > np.arange(T)[None, None, :]) & valid[:, None, :]
    return F, M


class RelDeepSets:
    def __init__(self, rng, out_dim, hidden=128, out_scale=0.01):
        self.out_dim = out_dim
        self.psi = MLP([FEAT_DIM, hidden, hidden], rng)
        self.rho = MLP([hidden + REL_CTX_DIM, hidden, hidden, out_dim], rng, out_scale=out_scale)

    def params(self):
        return self.psi.params() + self.rho.params()

    def forward(self, Frel, M, ctx, s):
        P, pc = self.psi.forward(Frel)
        Mf = M[..., None].astype(float)
        E = (P * Mf).sum(axis=2)
        out, rc = self.rho.forward(np.concatenate([E, ctx], axis=-1))
        if self.out_dim > 1:
            out = np.take_along_axis(out, rel_index_of_abs(s), axis=-1)   # absolute order
        return out, (pc, rc, Mf, s)

    def backward(self, cache, gout):
        pc, rc, Mf, s = cache
        if self.out_dim > 1:
            gout = np.take_along_axis(gout, abs_index_of_rel(s), axis=-1)  # back to relative order
        g_rho, gX = self.rho.backward(rc, gout)
        gE = gX[..., :-REL_CTX_DIM]
        g_psi, _ = self.psi.backward(pc, gE[:, :, None, :] * Mf)
        return g_psi + g_rho


def rel_ctx(phit, tau_rem, tau):
    s, d = shift_and_delta(phit)
    return np.stack([np.cos(d), np.sin(d), tau_rem / tau, np.cos(phit), np.sin(phit)], axis=-1), s
