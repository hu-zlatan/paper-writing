"""Gate E' (amendment v3.0 C2): grid evaluator sub 4 (original eval3 read-out) vs sub 8 (regrid3) on the same episodes.
Pass: mean |Delta BI| <= 0.02 nats AND no success flip outside the tie band, where a flip counts only if the
true-identity mass is outside [0.45, 0.55] under both settings. Writes results/v3/12_e_analysis.json."""
import glob
import json
import os

import numpy as np

base = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "results", "v3")
rows = [json.loads(l) for f in sorted(glob.glob(os.path.join(base, "e", "*_sub8.jsonl"))) for l in open(f)]
rows = [r for r in rows if "episode" in r]
d_bi, flips, counted = [], [], []
for r in rows:
    d_bi.append(abs(r["ball_info"] - r["orig_ball_info"]))
    if bool(r["success"]) != bool(r["orig_success"]):
        m4, m8 = r["orig_identity_mass_true"], r["identity_mass_true"]
        outside = not (0.45 <= m4 <= 0.55) and not (0.45 <= m8 <= 0.55)
        flips.append({"set": r["set"], "method": r["method"], "episode": r["episode"], "mass_sub4": m4, "mass_sub8": m8,
                      "counts": outside})
        counted.append(outside)
out = {"n_episodes": len(rows), "by_cell_method": {}, "mean_abs_dBI": float(np.mean(d_bi)) if rows else None,
       "max_abs_dBI": float(np.max(d_bi)) if rows else None, "flips": flips, "counted_flips": int(sum(counted)),
       "mean_wall_s_sub8": float(np.mean([r["wall_s"] for r in rows])) if rows else None}
for r in rows:
    out["by_cell_method"].setdefault(f'{r["set"]}{int(r["kappa"])}_{r["method"]}', 0)
    out["by_cell_method"][f'{r["set"]}{int(r["kappa"])}_{r["method"]}'] += 1
out["passes"] = bool(rows and out["mean_abs_dBI"] <= 0.02 and out["counted_flips"] == 0)
out["complete"] = len(rows) == 16
print(json.dumps(out, indent=1))
json.dump(out, open(os.path.join(base, "12_e_analysis.json"), "w"), indent=1)
