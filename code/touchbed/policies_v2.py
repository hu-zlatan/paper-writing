"""v2 selectors over the shared, feasibility-masked action set (docs/07_hypotheses_v2.md §2.2):
random, coverage, G* (cost-aware ball greedy; ladder rungs via candidate subsets), full-state cost-aware greedy."""
from __future__ import annotations

import numpy as np

from .ball import ball_eig, neighbours
from .geometry import cast
from .policies import eig_candidates
from .travel import PHI, PSI, A


class RandomV2:
    name = "random"

    def __init__(self, rng):
        self.rng = rng

    def act(self, pf, ts):
        return int(self.rng.choice(np.flatnonzero(ts.feasible())))


class CoverageV2:
    name = "coverage"

    def __init__(self, rng):
        self.rng = rng

    def act(self, pf, ts):
        feas = np.flatnonzero(ts.feasible())
        mass = pf.identity_mass()
        kh = int(np.argmax(mass))
        sel = np.flatnonzero(pf.k == kh)
        i = sel[np.argmax(pf.loglik_hist[sel])] if len(sel) else 0
        hit, qx, qy, _ = cast(pf.lib, kh, pf.x[i], pf.y[i], pf.th[i], PHI[feas], PSI[feas])
        contacts = np.array([[o[1], o[2]] for _, _, o in pf.hist if o[0]]).reshape(-1, 2)
        c = ts.costs()[feas]
        if not hit.any():
            return int(feas[int(self.rng.integers(len(feas)))])
        if len(contacts) == 0:
            d = np.where(hit, 0.0, -np.inf)
        else:
            d = np.min(np.hypot(qx[:, None] - contacts[None, :, 0], qy[:, None] - contacts[None, :, 1]), axis=1)
            d = np.where(hit, d, -np.inf)
        best = np.flatnonzero(d == d.max())
        return int(feas[best[np.argmin(c[best])]])  # ties -> lower cost


class GStar:
    """argmax over feasible candidates of EIG_B(a; b) / c(a) (ball target) or full-state EIG / c (target='state')."""
    name = "gstar"

    def __init__(self, rng, M: int = 64, subset=None, target: str = "ball", actions=None):
        self.rng, self.M, self.target = rng, M, target
        self.phis, self.psis = (PHI, PSI) if actions is None else actions
        self.subset = np.arange(len(self.phis)) if subset is None else np.asarray(subset)

    def _scores(self, pf, ts):
        feas = ts.feasible()
        cand = self.subset[feas[self.subset]]
        if len(cand) == 0:
            cand = np.flatnonzero(feas)
        if self.target == "ball":
            w = pf.weights()
            nb = neighbours(pf.lib, pf.k, pf.x, pf.y, pf.th)
            e = ball_eig(pf, self.phis[cand], self.psis[cand], self.M, self.rng, particles=(pf.k, pf.x, pf.y, pf.th, w), nb=nb)
        else:
            e = eig_candidates(pf, self.phis[cand], self.psis[cand], self.M, self.rng)
        return cand, e, ts.costs()[cand]

    def act(self, pf, ts):
        cand, e, c = self._scores(pf, ts)
        score = e / c
        j = int(np.argmax(score))
        self.last_score = float(score[j])
        return int(cand[j])

    def score_vector(self, pf, ts):
        """Teacher label of amendment v3.0 C7: s(a) = max(0, EIG_B(a; b)) / c(a) on the scored feasible candidates, 0
        elsewhere (float32, length |A|), the scored mask, and the action `act` would take from the same RNG state (it
        consumes the RNG exactly like `act`). argmax s == action whenever max s > 0."""
        cand, e, c = self._scores(pf, ts)
        score = e / c
        j = int(np.argmax(score))
        self.last_score = float(score[j])
        s = np.zeros(len(self.phis), dtype=np.float32)
        s[cand] = (np.maximum(e, 0.0) / c).astype(np.float32)
        mask = np.zeros(len(self.phis), dtype=bool)
        mask[cand] = True
        return s, mask, int(cand[j])
