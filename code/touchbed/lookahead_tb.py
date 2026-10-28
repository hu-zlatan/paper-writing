"""Touchbed adapter of the fixed look-ahead estimator (gate G2, H2b-P1; amendment B6).

Belief = N_LA = 500 equally weighted particles resampled from G*'s decision PF (ladder rung R3 size); rollout belief
updates re-weight these particles exactly with the shared likelihood (no MH inside rollouts). Target = ball information
around the (particle) true state. Greedy completion = G* at rung R3 (128 candidates = 16 phi' x 8 psi, M = 16),
cost-aware (EIG_B / c) and restricted to feasible actions. Budget = a copy of the travel state.
Structured set-up moves: antipodal travel (the feasible action nearest to phi_t + pi), travel to the region of maximal
mode disagreement (the feasible action whose predicted contact differs most between the two heaviest identity-pose
modes), and the action of maximal full-state EIG (B6)."""
import copy
import math

import numpy as np

from .ball import ball_eig, in_ball, neighbours
from .geometry import cast
from .likelihood import loglik, sample_obs
from .policies import eig_candidates
from .travel import A, PHI, PSI, rung_subset, wrap


class _PFView:
    def __init__(self, lib, om, k, x, y, th, w):
        self.lib, self.om, self.k, self.x, self.y, self.th, self._w = lib, om, k, x, y, th, w

    def weights(self):
        return self._w


class TouchbedProblem:
    n_actions = A

    def __init__(self, lib, om, k, x, y, th, M: int = 16, rung=(16, 8)):
        self.lib, self.om = lib, om
        self.k, self.x, self.y, self.th = k, x, y, th
        self.M = M
        self.subset = rung_subset(*rung)
        self.nb = neighbours(lib, k, x, y, th)

    @classmethod
    def from_pf(cls, pf, n: int, rng, **kw):
        w = pf.weights()
        idx = rng.choice(len(w), size=n, p=w)
        return cls(pf.lib, pf.om, pf.k[idx].copy(), pf.x[idx].copy(), pf.y[idx].copy(), pf.th[idx].copy(), **kw)

    def sample_obs(self, a, s, rng):
        return tuple(v[0] for v in sample_obs(self.om, self.lib, rng, np.array([self.k[s]]), self.x[s], self.y[s],
                                               self.th[s], float(PHI[a]), float(PSI[a])))

    def loglik(self, a, obs):
        return loglik(self.om, self.lib, obs, self.k, self.x, self.y, self.th, float(PHI[a]), float(PSI[a]))

    def target_logmass(self, logw, s):
        m = in_ball(self.lib, self.k, self.x, self.y, self.th, self.k[s], self.x[s], self.y[s], self.th[s])
        mx = logw.max()
        return float(math.log(np.exp(logw[m] - mx).sum()) - math.log(np.exp(logw - mx).sum()))

    def _w(self, logw):
        w = np.exp(logw - logw.max())
        return w / w.sum()

    def greedy(self, logw, ts, rng, M=None):
        feas = ts.feasible()
        cand = self.subset[feas[self.subset]]
        if len(cand) == 0:
            cand = np.flatnonzero(feas)
        w = self._w(logw)
        view = _PFView(self.lib, self.om, self.k, self.x, self.y, self.th, w)
        e = ball_eig(view, PHI[cand], PSI[cand], M or self.M, rng, particles=(self.k, self.x, self.y, self.th, w), nb=self.nb)
        return int(cand[int(np.argmax(e / ts.costs()[cand]))])

    def setup_moves(self, logw, ts):
        feas = np.flatnonzero(ts.feasible())
        out = []
        if len(feas) == 0:
            return out
        # antipodal travel
        d = np.abs(wrap(PHI[feas] - (ts.phi + math.pi)))
        out.append(int(feas[np.argmin(d)]))
        # maximal mode disagreement: two heaviest (identity, coarse pose) modes, predicted contact distance
        w = self._w(logw)
        key = self.k * 1000 + np.round(wrap(self.th) / math.radians(30)).astype(int)
        uk, inv = np.unique(key, return_inverse=True)
        mass = np.bincount(inv, weights=w)
        if len(uk) >= 2:
            top = np.argsort(-mass)[:2]
            reps = [int(np.flatnonzero(inv == t)[np.argmax(w[inv == t])]) for t in top]
            hit, qx, qy, _ = cast(self.lib, self.k[reps][:, None], self.x[reps][:, None], self.y[reps][:, None],
                                  self.th[reps][:, None], PHI[feas][None, :], PSI[feas][None, :])
            dist = np.where(hit[0] != hit[1], 1e3, np.hypot(qx[0] - qx[1], qy[0] - qy[1]))
            dist = np.where(hit[0] | hit[1], dist, 0.0)
            out.append(int(feas[np.argmax(dist)]))
        # maximal full-state EIG (B6)
        view = _PFView(self.lib, self.om, self.k, self.x, self.y, self.th, w)
        e = eig_candidates(view, PHI[feas], PSI[feas], self.M, np.random.default_rng(12345),
                           particles=(self.k, self.x, self.y, self.th, w))
        out.append(int(feas[np.argmax(e)]))
        return out

    def feasible(self, ts):
        return ts.feasible()

    def step_budget(self, ts, a):
        t2 = copy.deepcopy(ts)
        t2.step(int(a))
        return t2

    def budget_left(self, ts):
        return not ts.done()
