"""G4 re-check under amendment B5: candidates r10 / r30 (32k x 3 MH + R final MH) vs reference (32k x 30 MH + 60
final), paired pilot episodes, same rule as G4. Writes results/v2/12_g4_b5_analysis.json."""
import glob
import json
import os
import sys

import numpy as np

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from touchbed.stats import crossed_bootstrap_diff  # noqa: E402

base = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "results", "v2")
sub = sys.argv[1] if len(sys.argv) > 1 else "g4_b5"
rows = {}
for f in glob.glob(os.path.join(base, sub, "*.jsonl")):
    cfg = os.path.basename(f).rsplit("_sh", 1)[0].split("_")[-1]
    for line in open(f):
        r = json.loads(line)
        if "episode" in r:
            rows[(r["set"], r["kappa"], r["method"], cfg, r["episode"])] = r
out = {}
cells = sorted({(s, k, m) for (s, k, m, c, e) in rows})
for s, k, m in cells:
    for cand in ("r10", "r30"):
        eps = sorted(e for (s2, k2, m2, c, e) in rows if (s2, k2, m2, c) == (s, k, m, cand) and (s, k, m, "ref", e) in rows)
        if not eps:
            continue
        res = {"n_episodes": len(eps)}
        for metric in ("success", "ball_info", "identity_ok"):
            a = np.array([float(rows[(s, k, m, "ref", e)][metric]) for e in eps])
            b = np.array([float(rows[(s, k, m, cand, e)][metric]) for e in eps])
            bs = crossed_bootstrap_diff(a, b, n_boot=4000, seed=1, alpha=0.025)
            res[metric] = {"mean_cand": float(b.mean()), "mean_ref": float(a.mean()), "diff_ref_minus_cand": bs["diff"],
                           "ci95": [bs["lower"], bs["upper"]]}
        res["passes_G4_rule"] = bool(abs(res["ball_info"]["diff_ref_minus_cand"]) <= 0.05
                                     and abs(res["success"]["diff_ref_minus_cand"]) <= 0.01
                                     and res["success"]["ci95"][0] >= -0.02 and res["success"]["ci95"][1] <= 0.02)
        res["ci_only_fails"] = bool(not res["passes_G4_rule"] and abs(res["ball_info"]["diff_ref_minus_cand"]) <= 0.05
                                    and abs(res["success"]["diff_ref_minus_cand"]) <= 0.01)
        out[f"{s}_k{k:g}_{m}_{cand}"] = res
        print(f"{s} k{k:g} {m:6s} {cand} n={len(eps)} succ {b.mean():.3f}/{a.mean():.3f} "
              f"dS={res['success']['diff_ref_minus_cand']:+.3f} {np.round(res['success']['ci95'], 3)} "
              f"dBI={res['ball_info']['diff_ref_minus_cand']:+.3f} {np.round(res['ball_info']['ci95'], 3)} "
              + ("PASS" if res["passes_G4_rule"] else ("FAIL(CI only)" if res["ci_only_fails"] else "FAIL")))
json.dump(out, open(os.path.join(base, f"12_{sub}_analysis.json"), "w"), indent=1)
