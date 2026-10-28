"""epsilon-softened probe observation model (docs/07_hypotheses.md §1.1) — the single code path used by training,
greedy PF-EIG and the evaluation particle filter.

Observation y = (c, px, py, n): c = 1 contact with point (px, py) [mm] and normal angle n [rad]; c = 0 no contact (NC).
p_eps(y | s, a) = (1 - eps) p_geom(y | s, a) + eps u(y), where u puts mass 1/2 on NC and density 1/2 / (A * 2 pi) on the
contact branch (A = area of the workspace disc of radius RHO).
p_geom: NC with probability 1 if the ray misses s; otherwise contact point ~ N(true point, sigma_p^2 I) and normal angle
~ wrapped N(true normal, sigma_n^2) (sigma_n << pi so the wrapped density is evaluated on the wrapped difference).
"""
from __future__ import annotations

import math
from dataclasses import dataclass

import numpy as np

from .geometry import RHO, cast


@dataclass(frozen=True)
class ObsModel:
    sigma_p: float = 1.0                      # mm
    sigma_n: float = math.radians(5.0)        # rad
    eps: float = 1e-3

    @property
    def log_u_contact(self) -> float:
        return math.log(self.eps * 0.5 / (math.pi * RHO ** 2 * 2 * math.pi))

    @property
    def log_nc_hit(self) -> float:            # log p(NC | ray hits s)
        return math.log(self.eps * 0.5)

    @property
    def log_nc_miss(self) -> float:           # log p(NC | ray misses s)
        return math.log((1 - self.eps) + self.eps * 0.5)


def wrap(a):
    return (np.asarray(a) + np.pi) % (2 * np.pi) - np.pi


def loglik_from_pred(om: ObsModel, c, px, py, n, hit, qx, qy, qn):
    """log p_eps(y | s, a) given the predicted geometry (hit, qx, qy, qn) of state s under action a.
    Observation fields (c, px, py, n) broadcast against the prediction arrays."""
    c = np.asarray(c, dtype=bool)
    d2 = (px - qx) ** 2 + (py - qy) ** 2
    dn = wrap(n - qn)
    log_geom = (math.log(1 - om.eps) - math.log(2 * math.pi * om.sigma_p ** 2) - 0.5 * d2 / om.sigma_p ** 2
                - math.log(math.sqrt(2 * math.pi) * om.sigma_n) - 0.5 * dn ** 2 / om.sigma_n ** 2)
    log_contact = np.where(hit, np.logaddexp(log_geom, om.log_u_contact), om.log_u_contact)
    log_nc = np.where(hit, om.log_nc_hit, om.log_nc_miss)
    return np.where(c, log_contact, log_nc)


def loglik(om: ObsModel, lib, y, k, x, y_, th, phi, psi):
    """log p_eps(y | s, a) for states (k, x, y_, th) (arrays) and a single action/observation (or broadcastable)."""
    hit, qx, qy, qn = cast(lib, k, x, y_, th, phi, psi)
    c, px, py, n = y
    return loglik_from_pred(om, c, px, py, n, hit, qx, qy, qn)


def sample_obs(om: ObsModel, lib, rng: np.random.Generator, k, x, y_, th, phi, psi):
    """Draw y ~ p_eps(. | s, a) for a batch of (state, action) pairs. Returns (c, px, py, n) arrays."""
    hit, qx, qy, qn = cast(lib, k, x, y_, th, phi, psi)
    shape = hit.shape
    u_branch = rng.random(shape) < om.eps
    u_contact = rng.random(shape) < 0.5
    # geometric branch
    c = hit.copy()
    px = qx + om.sigma_p * rng.standard_normal(shape)
    py = qy + om.sigma_p * rng.standard_normal(shape)
    n = wrap(qn + om.sigma_n * rng.standard_normal(shape))
    # uniform branch: uniform point in the workspace disc, uniform normal
    r = RHO * np.sqrt(rng.random(shape))
    a = rng.uniform(-np.pi, np.pi, shape)
    ux, uy, un = r * np.cos(a), r * np.sin(a), rng.uniform(-np.pi, np.pi, shape)
    c = np.where(u_branch, u_contact, c)
    px = np.where(u_branch, ux, px)
    py = np.where(u_branch, uy, py)
    n = np.where(u_branch, un, n)
    px, py, n = np.where(c, px, 0.0), np.where(c, py, 0.0), np.where(c, n, 0.0)
    return c, px, py, n
