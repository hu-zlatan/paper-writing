"""One-sided multiplicative conformal calibration (CQR-style) and online quantile tracking (07_hypotheses §1.4).

Score  s = log F*_hi - log g(x);  decision  F = min(F_max, g(x) exp(q)).
Offline q_hat = the ceil((n+1)(1-alpha))-th smallest calibration score of the stratum (+inf if that exceeds n).
Online (OQT): q_{t+1} = q_t + eta (slip_t - alpha), no update on steps where F_t was capped at F_max (anti-windup);
the tracker only sees the binary slip outcome. Decaying-step variant: eta_t = eta / sqrt(t) (H3-S arm).
"""
from __future__ import annotations

import math

import numpy as np


def qhat(scores, alpha: float) -> float:
    s = np.sort(np.asarray(scores, dtype=float))
    n = len(s)
    k = math.ceil((n + 1) * (1 - alpha))
    return float("inf") if k > n else float(s[k - 1])


def scores(log_f_hi, log_pred):
    return np.asarray(log_f_hi, dtype=float) - np.asarray(log_pred, dtype=float)


def calibrate(log_f_hi, log_pred, strata, alpha: float) -> dict:
    """Mondrian (per-stratum) q_hat; strata is any hashable label per calibration point."""
    s = scores(log_f_hi, log_pred)
    strata = np.asarray(strata)
    return {k: qhat(s[strata == k], alpha) for k in np.unique(strata)}


def decide(log_pred, q, f_max: float):
    """Force F = min(F_max, g exp(q)), and whether it was capped."""
    F = np.exp(np.asarray(log_pred, dtype=float) + q)
    capped = F >= f_max
    return np.minimum(F, f_max), capped


class OQT:
    """Score-space online quantile tracker with anti-windup; keeps the books for the UT4 identity."""

    def __init__(self, q1: float, eta: float, alpha: float, f_max: float, decay: bool = False):
        self.q, self.q1, self.eta, self.alpha, self.f_max, self.decay = q1, q1, eta, alpha, f_max, decay
        self.t = 0
        self.sum_uncapped = 0.0       # sum over uncapped steps of (slip - alpha)  [constant-step identity]
        self.n_uncapped = 0
        self.qs = [q1]

    def force(self, log_pred: float):
        F = math.exp(log_pred + self.q)
        return (self.f_max, True) if F >= self.f_max else (F, False)

    def update(self, slip: bool, capped: bool):
        self.t += 1
        if capped:
            self.qs.append(self.q)
            return
        err = float(slip) - self.alpha
        step = self.eta / math.sqrt(self.n_uncapped + 1) if self.decay else self.eta
        self.q += step * err
        self.sum_uncapped += err
        self.n_uncapped += 1
        self.qs.append(self.q)

    def identity_residual(self) -> float:
        """UT4(a): sum_{uncapped}(slip - alpha) - (q_{T+1} - q_1)/eta  (0 up to float error; constant step only)."""
        return self.sum_uncapped - (self.q - self.q1) / self.eta

    def rate_bound(self) -> float:
        """UT4(b): |rate over uncapped steps - alpha| <= (max q - min q) / (eta T_uncapped)."""
        return (max(self.qs) - min(self.qs)) / (self.eta * max(1, self.n_uncapped))
