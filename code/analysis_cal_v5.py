"""P0 calibration for v5 (amendment v5.0 'P0'): the unchanged v3 Cal' rule applied to the new cells.
n*(A16): G* success on the 200 cal3 episodes at kappa = 0, tau = 4, sub-8 grid read-out: > 0.88 -> 3, < 0.20 -> 5, else 4.
A16-2 is kept only if G* sub-8 success at that n* is in [0.30, 0.90] (at n* = 4 this is the same 200 episodes).
tau for S kappa 4 / 8 = n* + mean travel time of G* run without a budget for n* probes on the 200 cal3 episodes, rounded to 0.1.
Writes results/v5/12_cal_analysis.json."""
import glob
import json
import os

import numpy as np

base = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "results", "v5")


def rows(pattern):
    out = {}
    for f in sorted(glob.glob(os.path.join(base, "cal", pattern))):
        for line in open(f):
            r = json.loads(line)
            if "episode" in r:
                out[r["episode"]] = r
    return list(out.values())


out = {"n_star": {}, "tau": {}, "keep": {}}
ns = rows("nstar_A16_sh*.jsonl")
if ns:
    p = float(np.mean([r["success"] for r in ns]))
    n_star = 3 if p > 0.88 else (5 if p < 0.20 else 4)
    out["n_star"]["A16"] = {"n_star": n_star, "gstar_success_sub8": p, "n_episodes": len(ns), "complete": len(ns) == 200,
                            "mean_probes": float(np.mean([r["n_probes"] for r in ns])),
                            "mean_ball_info": float(np.mean([r["ball_info"] for r in ns]))}
    if n_star == 4:
        out["keep"]["A16"] = {"gstar_success_sub8_at_nstar": p, "keep": bool(0.30 <= p <= 0.90),
                              "note": "n* = 4 equals the tau = 4, kappa = 0 run, so the keep check uses the same episodes"}
    else:
        kp = rows(f"keep_A16_n{n_star}_sh*.jsonl")
        if kp:
            q = float(np.mean([r["success"] for r in kp]))
            out["keep"]["A16"] = {"gstar_success_sub8_at_nstar": q, "n_episodes": len(kp), "complete": len(kp) == 200,
                                  "keep": bool(0.30 <= q <= 0.90) if len(kp) == 200 else None,
                                  "conditions": f"kappa 0, tau = n* = {n_star}, cal3 0-199, sub 8 (amendment v5.1)"}
        else:
            out["keep"]["A16"] = {"note": f"n* = {n_star}: needs 200 cal3 episodes at tau = {n_star} before the keep check"}
for setname, k in (("S", 4), ("S", 8), ("A16", 2)):
    cal = rows(f"tau_{setname}_k{k}_sh*.jsonl")
    if cal:
        v = np.array([r["travel_time"] for r in cal])
        n = cal[0]["n_star"]
        out["tau"][f"{setname}_k{k}"] = {"n_star": n, "n_episodes": len(v), "mean_travel_time": float(v.mean()),
                                 "sd_travel_time": float(v.std(ddof=1)), "mean_travel_rad": float(np.mean([r["travel_rad"] for r in cal])),
                                 "tau": round(n + float(v.mean()), 1), "complete": len(v) == 200}
print(json.dumps(out, indent=1))
json.dump(out, open(os.path.join(base, "12_cal_analysis.json"), "w"), indent=1)
