"""Gate Cal′ (amendment v3.0 C4; rule of 07_hypotheses_v2 §1.2 on 64 x 8).
n*: G* success on the 200 cal3 episodes at kappa = 0, tau = 4 (grid read-out): > 0.88 -> 3, < 0.20 -> 5, else 4.
tau_12 = n* + mean travel time of G* run without a budget for n* probes on the 200 cal3 episodes, rounded to 0.1.
Verification (results/v3/cal/verify_*): with the budget enforced, G*'s mean executed probe count within n* +- 0.3.
Writes results/v3/12_cal_analysis.json."""
import glob
import json
import os

import numpy as np

base = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "results", "v3")


def rows(pattern):
    out = []
    for f in sorted(glob.glob(os.path.join(base, "cal", pattern))):
        for line in open(f):
            r = json.loads(line)
            if "episode" in r:
                out.append(r)
    return out


out = {"n_star": {}, "tau": {}, "verify": {}}
for s in ("S", "A"):
    ns = rows(f"nstar_{s}_sh*.jsonl")
    if ns:
        p = float(np.mean([r["success"] for r in ns]))
        n_star = 3 if p > 0.88 else (5 if p < 0.20 else 4)
        out["n_star"][s] = {"n_star": n_star, "gstar_success": p, "n_episodes": len(ns),
                            "mean_probes": float(np.mean([r["n_probes"] for r in ns])),
                            "mean_ball_info": float(np.mean([r["ball_info"] for r in ns])), "complete": len(ns) == 200}
    for k in (12.0,):
        cal = rows(f"tau_{s}_k{k:g}_sh*.jsonl") + rows(f"tau_{s}_k{k:g}_n*_sh*.jsonl")
        if cal:
            byn = {}
            for r in cal:
                byn.setdefault(r["n_star"], []).append(r["travel_time"])
            for n, v in byn.items():
                v = np.array(v)
                out["tau"][f"{s}_k{k:g}_nstar{n}"] = {"n_star": n, "n_episodes": len(v), "mean_travel_time": float(v.mean()),
                                                     "sd_travel_time": float(v.std(ddof=1)) if len(v) > 1 else None,
                                                     "tau": round(n + float(v.mean()), 1), "complete": len(v) == 200}
    out["tau"][f"{s}_k0"] = {"tau": float(out["n_star"].get(s, {}).get("n_star", 4))}
for f in sorted(glob.glob(os.path.join(base, "cal", "verify_*_sh*.jsonl"))):
    cell = os.path.basename(f).split("_sh")[0].replace("verify_", "")
    for line in open(f):
        r = json.loads(line)
        if "episode" in r:
            out["verify"].setdefault(cell, []).append(r["n_probes"])
for cell, v in list(out["verify"].items()):
    out["verify"][cell] = {"n_episodes": len(v), "mean_probes": float(np.mean(v))}
print(json.dumps(out, indent=1))
json.dump(out, open(os.path.join(base, "12_cal_analysis.json"), "w"), indent=1)
