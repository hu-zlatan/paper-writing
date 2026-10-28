"""Gate G1 (amendment B6): (a) mean of 5 estimator runs at the notch prior within [0.8, 1.2] x exact relative gap;
(b) zero-gap bank: mean estimated relative gap in [-0.01, 0.02] and one-sided 95 % bootstrap UB < 0.03.
Writes results/v2/12_g1_analysis.json."""
import glob
import json
import os

import numpy as np

base = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "results", "v2")
A = [json.loads(l) for f in sorted(glob.glob(os.path.join(base, "g1", "a_sd*.jsonl"))) for l in open(f)]
B = [json.loads(l) for f in sorted(glob.glob(os.path.join(base, "g1", "b_*.jsonl"))) for l in open(f)]
out = {}
if A:
    ex = A[0]["exact_gap_rel"]
    m = float(np.mean([r["gap_rel"] for r in A]))
    out["a"] = {"n_runs": len(A), "estimates": [r["gap_rel"] for r in A], "mean": m, "exact": ex,
                "band": [0.8 * ex, 1.2 * ex], "passes": bool(0.8 * ex <= m <= 1.2 * ex),
                "v_la": [r["v_la"] for r in A], "v_greedy": [r["v_greedy"] for r in A],
                "exact_v_opt": A[0]["exact_v_opt"], "exact_v_greedy": A[0]["exact_v_greedy"],
                "a_la": [r["a_la"] for r in A], "a_greedy": [r["a_greedy"] for r in A]}
if B:
    g = np.array([r["gap_rel"] for r in B])
    rng = np.random.default_rng(1)
    bs = np.array([g[rng.integers(0, len(g), len(g))].mean() for _ in range(10000)])
    ub = float(np.quantile(bs, 0.95))
    out["b"] = {"n_beliefs": len(g), "mean": float(g.mean()), "ub95": ub, "frac_positive": float(np.mean(g > 0)),
                "passes": bool(-0.01 <= g.mean() <= 0.02 and ub < 0.03), "complete": len(g) == 100}
print(json.dumps(out, indent=1))
json.dump(out, open(os.path.join(base, "12_g1_analysis.json"), "w"), indent=1)
