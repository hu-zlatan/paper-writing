"""Gate G5 n* and tau calibration (docs/07_hypotheses_v2.md §1.2).
n*: from G* success on the first 200 pilot episodes at kappa = 0, tau = 4 (G4 runs): > 0.88 -> 3, < 0.20 -> 5, else 4.
tau_kappa = n* + mean travel time of G* run without a budget for n* probes on 200 pilot episodes (results/v2/calib),
rounded to 0.1. Writes results/v2/12_calib_analysis.json (the budget-enforced verification is a separate run)."""
import glob
import json
import os

import numpy as np

base = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "results", "v2")
g4 = {}
for f in glob.glob(os.path.join(base, "g4", "*_gstar_*.jsonl")):
    for line in open(f):
        r = json.loads(line)
        if "episode" in r and r["episode"] < 200:
            g4.setdefault((r["set"], r["n_eval"]), []).append(float(r["success"]))
cal = {}
for f in glob.glob(os.path.join(base, "calib", "*.jsonl")):
    for line in open(f):
        r = json.loads(line)
        if "episode" in r:
            cal.setdefault((r["set"], r["kappa"], r["n_star"]), {})[r["episode"]] = r["travel_time"]
out = {"n_star": {}, "tau": {}}
for s in ("A", "S"):
    succ = {n: float(np.mean(v)) for (s2, n), v in g4.items() if s2 == s}
    counts = {n: len(v) for (s2, n), v in g4.items() if s2 == s}
    p = succ[32000]
    n_star = 3 if p > 0.88 else (5 if p < 0.20 else 4)
    robust = all((3 if q > 0.88 else (5 if q < 0.20 else 4)) == n_star for q in succ.values())
    out["n_star"][s] = {"n_star": n_star, "gstar_success_first200": succ, "n_episodes": counts, "same_rule_outcome_at_128k": robust}
    for k in (2.0, 6.0, 12.0):
        tt = cal.get((s, k, n_star))
        if not tt:
            continue
        v = np.array([tt[e] for e in sorted(tt)])
        out["tau"][f"{s}_k{k:g}"] = {"n_star": n_star, "n_episodes": len(v), "mean_travel_time": float(v.mean()),
                                    "sd_travel_time": float(v.std(ddof=1)), "tau": round(n_star + float(v.mean()), 1),
                                    "other_n_star_tau": {str(n): round(n + float(np.mean(list(cal[(s, k, n)].values()))), 1)
                                                         for n in (3, 4, 5) if (s, k, n) in cal}}
    out["tau"][f"{s}_k0"] = {"n_star": n_star, "tau": float(n_star)}
print(json.dumps(out, indent=1))
json.dump(out, open(os.path.join(base, "12_calib_analysis.json"), "w"), indent=1)

# budget-enforced verification (results/v2/calib_verify): mean executed probes within n* +- 0.3
ver = {}
for f in glob.glob(os.path.join(base, "calib_verify", "*.jsonl")):
    cell = os.path.basename(f).rsplit("_sh", 1)[0]
    for line in open(f):
        r = json.loads(line)
        if "episode" in r:
            ver.setdefault(cell, []).append(r["n_probes"])
out["verify"] = {}
for cell, v in sorted(ver.items()):
    s, rest = cell.split("_k")
    n_star = out["n_star"][s]["n_star"]
    m = float(np.mean(v))
    out["verify"][cell] = {"n_episodes": len(v), "mean_probes": m, "n_star": n_star, "passes": bool(abs(m - n_star) <= 0.3)}
    print(cell, len(v), round(m, 3), "PASS" if abs(m - n_star) <= 0.3 else "FAIL")
json.dump(out, open(os.path.join(base, "12_calib_analysis.json"), "w"), indent=1)
