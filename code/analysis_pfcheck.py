"""Analyse the evaluation-PF convergence check (amendment A3): N=8000 vs N=32000 on identical episodes/probes for
random (probes identical by construction) and greedy (probes chosen by a decision PF of 2,000 particles, also identical
across N_eval because N_eval does not affect decisions). Paired bootstrap on per-episode differences."""
import glob
import json
import os
import sys

import numpy as np

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from touchbed.stats import crossed_bootstrap_diff  # noqa: E402

root = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "results", "v1", "pfcheck")
rows = {}
for f in glob.glob(os.path.join(root, "*.jsonl")):
    for line in open(f):
        r = json.loads(line)
        if "episode" not in r:
            continue
        rows[(r["set"], r["T"], r["method"], r["n_eval"], r["episode"])] = r
out = {}
for s in ("A", "S"):
    for T in (3, 10):
        for m in ("random", "greedy"):
            eps = sorted(e for (s2, T2, m2, n, e) in rows if (s2, T2, m2, n) == (s, T, m, 8000)
                         and (s, T, m, 32000, e) in rows)
            if not eps:
                continue
            res = {"n_episodes": len(eps)}
            for metric in ("success", "identity_ok", "ball_info", "ig"):
                a = np.array([float(rows[(s, T, m, 32000, e)][metric]) for e in eps])
                b = np.array([float(rows[(s, T, m, 8000, e)][metric]) for e in eps])
                bs = crossed_bootstrap_diff(a, b, n_boot=4000, seed=1)
                res[metric] = {"mean_N8000": float(b.mean()), "mean_N32000": float(a.mean()), "diff": bs["diff"],
                               "ci90": [bs["lower"], bs["upper"]]}
            ok = (abs(res["success"]["diff"]) <= 0.01 and -0.02 <= res["success"]["ci90"][0]
                  and res["success"]["ci90"][1] <= 0.02 and abs(res["ball_info"]["diff"]) <= 0.05)
            res["passes_A3_rule"] = bool(ok)
            out[f"{s}_T{T}_{m}"] = res
            print(s, T, m, len(eps), {k: (round(v["mean_N8000"], 3), round(v["mean_N32000"], 3)) for k, v in res.items()
                                     if isinstance(v, dict)}, "PASS" if ok else "FAIL")
json.dump(out, open(os.path.join(root, "..", "12_pfcheck_analysis.json"), "w"), indent=1)
