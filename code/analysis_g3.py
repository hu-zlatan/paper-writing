"""Gate G3 (ii) + (iv) read-out (docs/07_hypotheses_v2.md §4) at (S, kappa_hi = 12), grid evaluation (B8).
(ii) seed-mean validation success of the 3 pilot seeds >= success(G*) - 5 pp on the same validation episodes;
plateau within the E_train cap and objective saturation < 10 % are read from the training logs.
(iv) ball-sPCE (training objective, last logged validation value) vs grid BI of the same policy is reported.
Writes results/v2/12_g3_analysis.json."""
import glob
import json
import os

import numpy as np

base = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "results", "v2")


def load(pat):
    d = {}
    for f in glob.glob(os.path.join(base, "grid_g3_val", pat)):
        for line in open(f):
            r = json.loads(line)
            if "episode" in r:
                d[r["episode"]] = r
    return d


g = load("S_k12_gstar_sh*.jsonl")
out = {"gstar": {"n": len(g), "success": float(np.mean([r["success"] for r in g.values()])),
                 "bi": float(np.mean([r["ball_info"] for r in g.values()])),
                 "probes": float(np.mean([len(r["actions"]) for r in g.values()]))}, "seeds": {}}
for sd in (200, 201, 202):
    p = load(f"S_k12_sd{sd}_sh*.jsonl")
    common = sorted(set(p) & set(g))
    s = {"n": len(p), "n_paired": len(common),
         "success": float(np.mean([p[e]["success"] for e in common])) if common else None,
         "gstar_success_paired": float(np.mean([g[e]["success"] for e in common])) if common else None,
         "bi": float(np.mean([p[e]["ball_info"] for e in common])) if common else None,
         "probes": float(np.mean([len(p[e]["actions"]) for e in common])) if common else None}
    log = os.path.join(base, "g3", f"pilot_S_k12_sd{sd}.json")
    if os.path.exists(log):
        L = json.load(open(log))
        s["train_status"] = L.get("status")
        h = L.get("history", [])
        if h:
            last = h[-1]
            s["last_log"] = {k: last[k] for k in last if not isinstance(last[k], (list, dict))}
    out["seeds"][sd] = s
vals = [s["success"] for s in out["seeds"].values() if s["success"] is not None]
paired_g = [s["gstar_success_paired"] for s in out["seeds"].values() if s["success"] is not None]
out["seed_mean_success"] = float(np.mean(vals))
out["gstar_success_paired_mean"] = float(np.mean(paired_g))
out["rule_ii_success_pass"] = bool(out["seed_mean_success"] >= out["gstar_success_paired_mean"] - 0.05)
json.dump(out, open(os.path.join(base, "12_g3_analysis.json"), "w"), indent=1)
print(json.dumps(out, indent=1))
