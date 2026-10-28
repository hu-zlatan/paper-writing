"""Gate G4 (docs/07_hypotheses_v2.md §4): evaluation PF 32k vs 128k on paired pilot episodes.
Pass per cell: |d BI| <= 0.05 nats; |d success| <= 1 pp (point) with 95% CI inside +-2 pp. Writes results/v2/12_g4_analysis.json."""
import glob
import json
import os
import sys

import numpy as np

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from touchbed.stats import crossed_bootstrap_diff  # noqa: E402

root = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "results", "v2", "g4")
rows = {}
for f in glob.glob(os.path.join(root, "*.jsonl")):
    for line in open(f):
        r = json.loads(line)
        if "episode" in r:
            rows[(r["set"], r["kappa"], r["method"], r["n_eval"], r["episode"])] = r
out = {}
for s in ("A", "S"):
    for k in (0.0, 6.0, 12.0):
        for m in ("random", "gstar", "spce_total"):
            eps = sorted(e for (s2, k2, m2, n, e) in rows if (s2, k2, m2, n) == (s, k, m, 32000)
                         and (s, k, m, 128000, e) in rows)
            if not eps:
                continue
            res = {"n_episodes": len(eps)}
            for metric in ("success", "ball_info", "identity_ok"):
                a = np.array([float(rows[(s, k, m, 128000, e)][metric]) for e in eps])
                b = np.array([float(rows[(s, k, m, 32000, e)][metric]) for e in eps])
                bs = crossed_bootstrap_diff(a, b, n_boot=4000, seed=1, alpha=0.025)
                res[metric] = {"mean_32k": float(b.mean()), "mean_128k": float(a.mean()), "diff_128k_minus_32k": bs["diff"],
                               "ci95": [bs["lower"], bs["upper"]]}
            res["passes_G4"] = bool(abs(res["ball_info"]["diff_128k_minus_32k"]) <= 0.05
                                    and abs(res["success"]["diff_128k_minus_32k"]) <= 0.01
                                    and res["success"]["ci95"][0] >= -0.02 and res["success"]["ci95"][1] <= 0.02)
            out[f"{s}_k{k:g}_{m}"] = res
            print(s, k, m, len(eps), {mm: (round(v["mean_32k"], 3), round(v["mean_128k"], 3)) for mm, v in res.items()
                                      if isinstance(v, dict)}, "PASS" if res["passes_G4"] else "FAIL")
os.makedirs(os.path.join(root, ".."), exist_ok=True)
json.dump(out, open(os.path.join(root, "..", "12_g4_analysis.json"), "w"), indent=1)
