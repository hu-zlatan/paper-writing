"""Physics-formula comparators (07_hypotheses §1.3): nominal force for CSF-1 / Mondrian-CSF.

F_nom = m (g + a_cmd) / (2 mu_bar) for the self-generated motions D1 (a_cmd = commanded lift acceleration) and D2
(a_cmd = peak shake acceleration A (2 pi f)^2), and m g / (2 mu_bar) for the external disturbances D3 / D4, whose
amplitude the robot does not know. mu_bar = geometric mean of the design mu range [0.3, 1.0].
"""
from __future__ import annotations

import math

G = 9.81
MU_BAR = math.sqrt(0.3 * 1.0)


def commanded_acc(dist: str, amp: float, freq: float) -> float:
    if dist == "D1":
        return amp
    if dist == "D2":
        return amp * (2 * math.pi * freq) ** 2
    return 0.0


def f_nom(mass: float, dist: str, amp: float, freq: float) -> float:
    return mass * (G + commanded_acc(dist, amp, freq)) / (2 * MU_BAR)


MU_HAT_CLIP = (0.1, 3.0)   # amendment 08a: keeps a censored (not found) onset from giving an unbounded estimate


def mu_hat(mass: float, F_onset_noisy: float) -> float:
    """Friction estimate from the noisy ramp-down onset force (static load m g shared by two pads)."""
    return min(max(mass * G / (2 * F_onset_noisy), MU_HAT_CLIP[0]), MU_HAT_CLIP[1])


def f_nom_muhat(mass: float, dist: str, amp: float, freq: float, F_onset_noisy: float) -> float:
    """CSF-mu-hat (amendment 08a): the CSF-1 formula with mu_bar replaced by the same noisy onset estimate."""
    return mass * (G + commanded_acc(dist, amp, freq)) / (2 * mu_hat(mass, F_onset_noisy))
