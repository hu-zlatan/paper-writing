"""Travel-notch control for gate G1′ (c) (docs/07_hypotheses_v3.md §3.4, §4; amendment v3.0 C12).

The exact notch problem of `notch.py` (identity of a notched vs plain 80 x 30 mm rectangle, unknown offset x) with its
actions placed on the stand-off circle and the v2 travel model c(a | phi) = 1 + kappa |wrap(phi_a - phi)| / pi:
  * the horizontal probe (the cheap set-up action that localises x; identity EIG 0) sits at phi = 0, the start;
  * all 71 vertical probes (the only actions that can see the notch, i.e. the identity feature) sit at phi = pi, far
    from the cheap action;
  * time budget tau = 2 + kappa: exactly two probes are possible on every path that can carry information
    (H -> V costs 1 + (1 + kappa); V -> V costs (1 + kappa) + 1; V -> H is infeasible).
G* is the cost-aware ratio greedy argmax_a EIG(a) / c(a) over feasible actions. Because every vertical probe shares one
angle, the last-step ratio choice equals the last-step EIG maximiser, so the exact one-step-deviation value of a first
action (a1, then G*) equals its exact optimal two-step value; the exact relative gap is
(max_a1 v(a1) - v(a1_G*)) / max_a1 v(a1), computed by enumeration with the notch tables (quadrature as `notch.two_step`).
This control checks that the look-ahead estimator handles travel costs, feasibility and the budget correctly; it does
not by itself show that travel creates headroom on the touchbed task.
"""
from __future__ import annotations

import math

import numpy as np

from . import notch as N

KAPPA = 12.0
PHI_ACT = np.where(np.arange(N.N_ACT) == N.H_ACT, 0.0, math.pi)


def costs(phi: float, kappa: float = KAPPA) -> np.ndarray:
    d = np.abs((PHI_ACT - phi + math.pi) % (2 * math.pi) - math.pi)
    return 1.0 + kappa * d / math.pi


class Budget:
    __slots__ = ("phi", "tau_rem")

    def __init__(self, phi: float, tau_rem: float):
        self.phi, self.tau_rem = float(phi), float(tau_rem)


class TravelNotchProblem(N.NotchProblem):
    """NotchProblem with a travel budget state; greedy = cost-aware ratio greedy over feasible actions."""

    def __init__(self, kappa: float = KAPPA):
        super().__init__()
        self.kappa = kappa

    def start(self):
        return Budget(0.0, 2.0 + self.kappa)

    def feasible(self, budget) -> np.ndarray:
        return costs(budget.phi, self.kappa) <= budget.tau_rem + 1e-12

    def step_budget(self, budget, a):
        c = float(costs(budget.phi, self.kappa)[a])
        return Budget(PHI_ACT[a], budget.tau_rem - c)

    def budget_left(self, budget) -> bool:
        return budget.tau_rem >= 1.0 - 1e-12 and bool(self.feasible(budget).any())

    def greedy(self, logw, budget, rng, M: int = 64):
        feas = np.flatnonzero(self.feasible(budget))
        e = self.mc_eig(logw, feas, M, rng)
        return int(feas[int(np.argmax(e / costs(budget.phi, self.kappa)[feas]))])


def exact_values(kappa: float = KAPPA, chunk: int = 512):
    """Exact two-step values from the prior at phi = 0, tau = 2 + kappa: v(a1) for every feasible first action
    (a1 then the cost-aware greedy last step), the G* first action, and the relative gap."""
    T = N._Tables()
    w = N.prior_belief()
    c1 = costs(0.0, kappa)
    tau = 2.0 + kappa
    eig1 = N.eig_batch(w[None, :], T)[0]
    v = np.full(N.N_ACT, np.nan)
    for a in range(N.N_ACT):
        if c1[a] > tau + 1e-12:
            continue
        rem = tau - c1[a]
        c2 = costs(PHI_ACT[a], kappa)
        feas2 = c2 <= rem + 1e-12
        P, pr = N.posteriors(w, a, T)
        best = np.empty(len(P))
        for i in range(0, len(P), chunk):
            E = N.eig_batch(P[i:i + chunk], T)
            R = np.where(feas2[None, :], E / c2[None, :], -np.inf)
            j = np.argmax(R, axis=1)
            best[i:i + chunk] = E[np.arange(len(j)), j] if feas2.any() else 0.0
        v[a] = eig1[a] + float((pr * best).sum())
    feas1 = c1 <= tau + 1e-12
    ag = int(np.flatnonzero(feas1)[np.argmax(eig1[feas1] / c1[feas1])])
    ao = int(np.nanargmax(v))
    return {"kappa": kappa, "tau": tau, "v": v.tolist(), "eig1": eig1.tolist(), "a_opt": ao, "v_opt": float(v[ao]),
            "a_greedy": ag, "v_greedy": float(v[ag]), "gap_rel": float((v[ao] - v[ag]) / v[ao]),
            "a_opt_is_horizontal": ao == N.H_ACT}
