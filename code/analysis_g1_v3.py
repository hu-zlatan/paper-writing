"""Gate G1′ (07_hypotheses_v3 §4): (a) mean of 5 notch estimator runs in [0.573, 0.860] (= [0.8, 1.2] x 0.717);
(b) zero-gap bank: mean estimated relative gap in [-0.01, 0.02] and one-sided 95 % bootstrap UB < 0.03;
(c) travel-notch: exact relative gap >= 0.10 and the mean of 5 estimates within +-20 % of it.
Writes results/v3/12_g1_analysis.json."""
import glob
import json
import os

import numpy as np

base = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "results", "v3")


def load(p):
    return [json.loads(l) for f in sorted(glob.glob(os.path.join(base, "g1", p))) for l in open(f) if l.strip()]


A, B, C = load("a_sd*.jsonl"), load("b_*.jsonl"), load("c_sd*.jsonl")
out = {}
if A:
    m = float(np.mean([r["gap_rel"] for r in A]))
    out["a"] = {"n_runs": len(A), "estimates": [r["gap_rel"] for r in A], "mean": m, "exact": A[0]["exact_gap_rel"],
                "band": [0.573, 0.860], "passes": bool(0.573 <= m <= 0.860), "complete": len(A) == 5}
if B:
    g = np.array([r["gap_rel"] for r in B])
    rng = np.random.default_rng(1)
    bs = np.array([g[rng.integers(0, len(g), len(g))].mean() for _ in range(10000)])
    ub = float(np.quantile(bs, 0.95))
    out["b"] = {"n_beliefs": len(g), "mean": float(g.mean()), "ub95": ub, "passes": bool(-0.01 <= g.mean() <= 0.02 and ub < 0.03),
                "complete": len(g) == 100}
if C:
    ex = C[0]["exact_gap_rel"]
    m = float(np.mean([r["gap_rel"] for r in C]))
    out["c"] = {"n_runs": len(C), "estimates": [r["gap_rel"] for r in C], "mean": m, "exact": ex,
                "band": [0.8 * ex, 1.2 * ex], "passes": bool(ex >= 0.10 and 0.8 * ex <= m <= 1.2 * ex),
                "complete": len(C) == 5}
print(json.dumps(out, indent=1))
json.dump(out, open(os.path.join(base, "12_g1_analysis.json"), "w"), indent=1)
