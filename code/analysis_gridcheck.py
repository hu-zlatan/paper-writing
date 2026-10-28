"""B8 self-check: adaptive grid sub 4 vs sub 8 on the same episodes (mean |dBI| <= 0.02; no success flips outside the
true-identity-mass tie band [0.45, 0.55]). Writes results/v2/12_gridcheck_analysis.json."""
import glob
import json
import os

import numpy as np

base = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "results", "v2", "grid_check")
rows = {}
for f in glob.glob(os.path.join(base, "*.jsonl")):
    sub = int(os.path.basename(f).split("_sub")[1].split(".")[0])
    for line in open(f):
        r = json.loads(line)
        rows[(r["set"], r["kappa"], r["method"], r["episode"], sub)] = r
pairs = [(k[:4]) for k in rows if k[4] == 4 and k[:4] + (8,) in rows]
d = [abs(rows[p + (4,)]["ball_info"] - rows[p + (8,)]["ball_info"]) for p in pairs]
flips = [p for p in pairs if rows[p + (4,)]["success"] != rows[p + (8,)]["success"]]
outside = [p for p in flips if not all(0.45 <= rows[p + (s,)]["identity_mass_true"] <= 0.55 for s in (4, 8))]
out = {"n_episodes": len(pairs), "mean_abs_dBI": float(np.mean(d)), "max_abs_dBI": float(np.max(d)), "flips": len(flips),
       "flips_outside_tie_band": len(outside), "passes": bool(np.mean(d) <= 0.02 and not outside)}
print(out)
json.dump(out, open(os.path.join(base, "..", "12_gridcheck_analysis.json"), "w"), indent=1)
