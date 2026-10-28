"""v2 action model (docs/07_hypotheses_v2.md §1.2, §1.5): finger on the 100 mm stand-off circle, shared discrete
action set of 32 target angles x 8 offsets, travel cost c(a | phi_t) = 1 + kappa |wrap(phi' - phi_t)| / pi strokes,
time budget tau with feasibility c(a) <= tau_rem; the episode ends when tau_rem < 1."""
from __future__ import annotations

import math

import numpy as np

N_PHI, N_PSI = 32, 8
PHI_GRID = np.arange(N_PHI) * (2 * math.pi / N_PHI)                 # 0, 11.25°, ...
PSI_GRID = np.deg2rad(np.arange(-35, 36, 10, dtype=float))          # -35, -25, ..., 35 degrees
PHI = np.repeat(PHI_GRID, N_PSI)                                    # action index a = i_phi * 8 + i_psi
PSI = np.tile(PSI_GRID, N_PHI)
A = N_PHI * N_PSI


def wrap(a):
    return (np.asarray(a) + np.pi) % (2 * np.pi) - np.pi


def rung_subset(n_phi: int, n_psi: int) -> np.ndarray:
    """Nested candidate subsets for the greedy ladder: every (32/n_phi)-th angle and an evenly spread psi subset."""
    sp = N_PHI // n_phi
    psi_idx = {8: range(8), 4: (0, 2, 5, 7), 2: (2, 5)}[n_psi]
    return np.array([i * N_PSI + j for i in range(0, N_PHI, sp) for j in psi_idx])


def cost(phi_t: float, kappa: float) -> np.ndarray:
    return 1.0 + kappa * np.abs(wrap(PHI - phi_t)) / math.pi


class TravelState:
    def __init__(self, phi0: float, kappa: float, tau: float):
        self.phi, self.kappa, self.tau_rem, self.tau = float(phi0), float(kappa), float(tau), float(tau)
        self.travel = 0.0
        self.n_probes = 0

    def costs(self) -> np.ndarray:
        return cost(self.phi, self.kappa)

    def feasible(self) -> np.ndarray:
        return self.costs() <= self.tau_rem + 1e-12

    def done(self) -> bool:
        return self.tau_rem < 1.0 - 1e-12

    def step(self, a: int) -> float:
        c = float(self.costs()[a])
        assert c <= self.tau_rem + 1e-12, "infeasible action"
        self.travel += abs(float(wrap(PHI[a] - self.phi)))
        self.tau_rem -= c
        self.phi = float(PHI[a])
        self.n_probes += 1
        return c
