"""Pre-registered statistics (docs/07_hypotheses.md §1.5, §6): paired comparison over shared test episodes with a
crossed (episode x seed) bootstrap, one-sided percentile bounds, Holm correction and seed-robustness counts."""
from __future__ import annotations

import numpy as np


def _as2d(a):
    a = np.asarray(a, dtype=float)
    return a[:, None] if a.ndim == 1 else a


def crossed_bootstrap_diff(A, B, n_boot: int = 10000, seed: int = 0, alpha: float = 0.05):
    """A, B: per-episode outcomes, shape (n_episodes,) or (n_episodes, n_seeds) on the SAME episodes (paired).
    Statistic: mean over episodes of (seed-mean of A - seed-mean of B). Each resample draws episodes with replacement
    (same indices for A and B) and, independently per method, seeds with replacement.
    Returns dict with point estimate, one-sided lower/upper (1 - alpha) bounds and bootstrap p-values."""
    A, B = _as2d(A), _as2d(B)
    assert A.shape[0] == B.shape[0], "paired design requires the same episodes"
    rng = np.random.default_rng(seed)
    n = A.shape[0]
    point = float(np.mean(A.mean(1) - B.mean(1)))
    stats = np.empty(n_boot)
    for b in range(n_boot):
        ei = rng.integers(0, n, n)
        sa = rng.integers(0, A.shape[1], A.shape[1])
        sb = rng.integers(0, B.shape[1], B.shape[1])
        stats[b] = np.mean(A[ei][:, sa].mean(1) - B[ei][:, sb].mean(1))
    return {"diff": point, "lower": float(np.quantile(stats, alpha)), "upper": float(np.quantile(stats, 1 - alpha)),
            "p_greater": float(np.mean(stats <= 0.0)), "p_less": float(np.mean(stats >= 0.0)), "n_episodes": n,
            "n_seeds": [A.shape[1], B.shape[1]], "n_boot": n_boot}


def holm(pvals, alpha: float = 0.05):
    """Holm step-down; returns list of booleans (rejected) in the input order."""
    p = np.asarray(pvals, dtype=float)
    order = np.argsort(p)
    rej = np.zeros(len(p), dtype=bool)
    for i, j in enumerate(order):
        if p[j] <= alpha / (len(p) - i):
            rej[j] = True
        else:
            break
    return rej.tolist()


def seed_robustness(A, B):
    """Number of treatment seeds whose mean paired difference to the seed-averaged comparator is > 0."""
    A, B = _as2d(A), _as2d(B)
    bm = B.mean(1)
    return int(np.sum([(A[:, s] - bm).mean() > 0 for s in range(A.shape[1])])), A.shape[1]


def tost(A, B, margin: float, n_boot: int = 10000, seed: int = 0, alpha: float = 0.05):
    """Two one-sided tests via the crossed bootstrap: equivalence of mean(A - B) within (-margin, +margin) is declared
    when the (1 - 2*alpha) bootstrap interval lies inside the margins (equivalently both one-sided bounds)."""
    r = crossed_bootstrap_diff(A, B, n_boot=n_boot, seed=seed, alpha=alpha)
    r["equivalent"] = bool(r["lower"] > -margin and r["upper"] < margin)
    r["margin"] = margin
    return r
