"""Gradient-boosted quantile predictors of log F*_hi with an equal tuning budget for every input set
(07_hypotheses §1.4): the same 30-config random search, 4-fold CV grouped by object on the train objects, pinball
loss at tau. RAW-G: Gaussian heteroscedastic model (mean of log F*_hi, then mean of the absolute residual).
"""
from __future__ import annotations

import numpy as np
from sklearn.ensemble import HistGradientBoostingRegressor
from sklearn.model_selection import GroupKFold

N_CONFIGS = 30


def configs(seed: int = 0, n: int = N_CONFIGS):
    rng = np.random.default_rng([seed, 777])
    out = []
    for _ in range(n):
        out.append({"learning_rate": float(np.exp(rng.uniform(np.log(0.02), np.log(0.3)))),
                    "max_iter": int(rng.choice([100, 200, 400, 800])),
                    "max_leaf_nodes": int(rng.choice([7, 15, 31, 63])),
                    "min_samples_leaf": int(rng.choice([5, 10, 20, 40])),
                    "l2_regularization": float(rng.choice([0.0, 0.1, 1.0]))})
    return out


def pinball(y, p, tau):
    d = y - p
    return float(np.mean(np.maximum(tau * d, (tau - 1) * d)))


def fit_quantile(X, y, groups, tau: float, seed: int = 0, n_configs: int = N_CONFIGS):
    """Random search (same configs for every input set given the seed) -> refit on all train objects."""
    cv = GroupKFold(n_splits=4)
    best, best_loss, log = None, np.inf, []
    for c in configs(seed, n_configs):
        losses = []
        for tr, va in cv.split(X, y, groups):
            m = HistGradientBoostingRegressor(loss="quantile", quantile=tau, random_state=seed, **c)
            m.fit(X[tr], y[tr])
            losses.append(pinball(y[va], m.predict(X[va]), tau))
        loss = float(np.mean(losses))
        log.append({"config": c, "cv_pinball": loss})
        if loss < best_loss:
            best, best_loss = c, loss
    m = HistGradientBoostingRegressor(loss="quantile", quantile=tau, random_state=seed, **best)
    m.fit(X, y)
    return m, {"best": best, "cv_pinball": best_loss, "search": log}


class GaussianModel:
    """RAW-G: mu(x) by squared error, sigma(x) = sqrt(pi/2) E|resid| (Gaussian), F = exp(mu + z sigma)."""

    def __init__(self, seed: int = 0, **cfg):
        self.mu = HistGradientBoostingRegressor(random_state=seed, **cfg)
        self.sd = HistGradientBoostingRegressor(random_state=seed, **cfg)

    def fit(self, X, y):
        self.mu.fit(X, y)
        self.sd.fit(X, np.abs(y - self.mu.predict(X)))
        return self

    def predict(self, X, z: float):
        return self.mu.predict(X) + z * np.sqrt(np.pi / 2) * np.maximum(self.sd.predict(X), 1e-6)
