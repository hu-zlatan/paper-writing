"""Non-random heuristic baselines of docs/07_hypotheses_v3.md §1.7 (frozen by amendment v3.0 C10).

All share the feasibility mask and the budget reservation rule: action a is *allowed* iff
    c(a) <= tau_rem - max(0, n* - t - 1),   t = probes executed so far,
so a heuristic cannot strand itself before n* probes; if no action is allowed, the cheapest feasible action is taken
(ties -> lower index).

Implementation choices where §1.7 is silent (recorded here, fixed before any v3 run):
* B-spread: "probe angle" = the target angle phi' of the executed action; the start angle phi0 is included.
* B-fan: "stay" = the grid angle nearest to the current finger angle phi_t (phi0 is continuous). If (stay, psi_t) is not
  allowed, the allowed action with psi_t nearest to phi_t is taken; if no allowed action has psi_t, the nearest allowed
  action over all psi (ties -> lower index).
"""
from __future__ import annotations

import numpy as np

from .geometry import cast
from .travel import PHI, PSI, wrap

PSI_DEG = np.rint(np.rad2deg(PSI)).astype(int)
FAN_CYCLE = (5, -5, 15, -15, 25, -25, 35, -35)


def allowed_mask(ts, n_star: int) -> np.ndarray:
    reserve = max(0, n_star - ts.n_probes - 1)
    return ts.feasible() & (ts.costs() <= ts.tau_rem - reserve + 1e-12)


def _fallback(ts) -> int:
    feas = np.flatnonzero(ts.feasible())
    c = ts.costs()[feas]
    return int(feas[np.flatnonzero(c == c.min())[0]])


class BSpread:
    """Belief-free: phi' maximising the minimum wrap distance to {phi0} ∪ previous probe angles; psi = +5°;
    ties -> lower cost, then lower index."""
    name = "b_spread"
    needs_belief = False

    def __init__(self, rng, n_star: int):
        self.n_star = n_star
        self.angles = None

    def act(self, _pf, ts):
        if self.angles is None:                  # first call: finger is at phi0
            self.angles = [ts.phi]
        allowed = allowed_mask(ts, self.n_star)
        cand = np.flatnonzero(allowed & (PSI_DEG == 5))
        if len(cand) == 0:
            cand = np.flatnonzero(allowed)
        if len(cand) == 0:
            a = _fallback(ts)
        else:
            d = np.min(np.abs(wrap(PHI[cand][:, None] - np.array(self.angles)[None, :])), axis=1)
            best = cand[np.isclose(d, d.max(), rtol=0, atol=1e-12)]
            c = ts.costs()[best]
            a = int(best[np.flatnonzero(np.isclose(c, c.min(), rtol=0, atol=1e-12))[0]])
        self.angles.append(float(PHI[a]))
        return a


class BFan:
    """Belief-free, travel-nearest: stay at the current angle, psi cycles +5, -5, +15, -15, +25, -25, +35, -35."""
    name = "b_fan"
    needs_belief = False

    def __init__(self, rng, n_star: int):
        self.n_star = n_star

    def act(self, _pf, ts):
        allowed = allowed_mask(ts, self.n_star)
        if not allowed.any():
            return _fallback(ts)
        psi_t = FAN_CYCLE[ts.n_probes % len(FAN_CYCLE)]
        dist = np.abs(wrap(PHI - ts.phi))
        cand = np.flatnonzero(allowed & (PSI_DEG == psi_t))
        if len(cand) == 0:
            cand = np.flatnonzero(allowed)
        d = dist[cand]
        return int(cand[np.flatnonzero(np.isclose(d, d.min(), rtol=0, atol=1e-12))[0]])


class BCov:
    """Belief-using: v2 coverage (`CoverageV2`: max-min distance from the MAP particle's predicted contact to previous
    contacts; ties -> lower cost; random allowed action if no predicted hit) restricted to allowed actions."""
    name = "b_cov"
    needs_belief = True

    def __init__(self, rng, n_star: int):
        self.rng, self.n_star = rng, n_star

    def act(self, pf, ts):
        allowed = np.flatnonzero(allowed_mask(ts, self.n_star))
        if len(allowed) == 0:
            return _fallback(ts)
        mass = pf.identity_mass()
        kh = int(np.argmax(mass))
        sel = np.flatnonzero(pf.k == kh)
        i = sel[np.argmax(pf.loglik_hist[sel])] if len(sel) else 0
        hit, qx, qy, _ = cast(pf.lib, kh, pf.x[i], pf.y[i], pf.th[i], PHI[allowed], PSI[allowed])
        contacts = np.array([[o[1], o[2]] for _, _, o in pf.hist if o[0]]).reshape(-1, 2)
        c = ts.costs()[allowed]
        if not hit.any():
            return int(allowed[int(self.rng.integers(len(allowed)))])
        if len(contacts) == 0:
            d = np.where(hit, 0.0, -np.inf)
        else:
            d = np.min(np.hypot(qx[:, None] - contacts[None, :, 0], qy[:, None] - contacts[None, :, 1]), axis=1)
            d = np.where(hit, d, -np.inf)
        best = np.flatnonzero(d == d.max())
        return int(allowed[best[np.argmin(c[best])]])


HEURISTICS = {"b_spread": BSpread, "b_fan": BFan, "b_cov": BCov}
