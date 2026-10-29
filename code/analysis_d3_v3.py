"""Gate D3 (07_hypotheses_v3 §4): S12, student seeds 501-503 (final DAgger round), first 500 val3 episodes paired with
G*, grid read-out sub 8 (E' failed). Margins delta_S12, eps_S12 from results/v3/12_g5_analysis.json (sub 8).
(i)  Delta_succ >= max(-0.02, -delta + 1.645 * SE_s * sqrt(500/1000))
(ii) Delta_BI   >= max(-0.15, -eps   + 1.645 * SE_BI * sqrt(500/1000))
(iii) every seed's point Delta_succ > -delta
Delta = mean over episodes of (seed-mean student - G*); SE = SD of the crossed bootstrap (episodes and seeds resampled,
B = 10,000, the scheme of stats.crossed_bootstrap_diff). Usage: python analysis_d3_v3.py [--kind student|belief_student]
[--tag r2]. Writes results/v3/12_d3_analysis[_<kind>][_<tag> if tag != r2].json."""
import glob
import json
import math
import os
import sys

import numpy as np

base = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "results", "v3")
kind = sys.argv[sys.argv.index("--kind") + 1] if "--kind" in sys.argv else "student"
tag = sys.argv[sys.argv.index("--tag") + 1] if "--tag" in sys.argv else "r2"
seeds = (501, 502, 503) if kind == "student" else (521, 522, 523)
n_ep = 500 if kind == "student" else 300


def load(pat):
    d = {}
    for f in glob.glob(os.path.join(base, "d3_val", pat)):
        for line in open(f):
            r = json.loads(line)
            if "episode" in r:
                d[r["episode"]] = r
    return d


def boot_sd(A, B, n_boot=10000, seed=0):
    rng = np.random.default_rng(seed)
    n = A.shape[0]
    st = np.empty(n_boot)
    for b in range(n_boot):
        ei = rng.integers(0, n, n)
        sa = rng.integers(0, A.shape[1], A.shape[1])
        st[b] = np.mean(A[ei][:, sa].mean(1) - B[ei])
    return float(st.std(ddof=1))


g = load("S_k12_gstar_*.jsonl")
st = {s: load(f"S_k12_{kind}_s{s}_{tag}_*.jsonl") for s in seeds}
eps = [e for e in range(n_ep) if e in g and all(e in st[s] for s in seeds)]
g5 = json.load(open(os.path.join(base, "12_g5_analysis.json")))["cells"]["S12"]
delta, epsc = g5["delta_c"], g5["eps_c"]
out = {"kind": kind, "tag": tag, "n_episodes": len(eps), "complete": len(eps) == n_ep, "delta_S12": delta, "eps_S12": epsc}
if eps:
    for metric, key, floor, margin in (("succ", "success", -0.02, delta), ("bi", "ball_info", -0.15, epsc)):
        A = np.array([[float(st[s][e][key]) for s in seeds] for e in eps])
        B = np.array([float(g[e][key]) for e in eps])
        d = float(np.mean(A.mean(1) - B))
        se = boot_sd(A, B)
        thr = max(floor, -margin + 1.645 * se * math.sqrt(500 / 1000))
        out[metric] = {"delta_hat": d, "se": se, "threshold": thr, "passes": bool(d >= thr),
                       "student_mean": float(A.mean()), "gstar_mean": float(B.mean()),
                       "per_seed": {str(s): float(np.mean(A[:, i] - B)) for i, s in enumerate(seeds)}}
    out["seeds_ok"] = {s: v > -delta for s, v in out["succ"]["per_seed"].items()}
    out["passes"] = bool(out["succ"]["passes"] and out["bi"]["passes"] and all(out["seeds_ok"].values()))
print(json.dumps(out, indent=1))
name = "12_d3_analysis" + ("" if kind == "student" else f"_{kind}") + ("" if tag == "r2" else f"_{tag}") + ".json"
json.dump(out, open(os.path.join(base, name), "w"), indent=1)
