"""Gate G5' (07_hypotheses_v3 §1.4, §1.5, §1.7, §4) on the v3 pilot (pilot3, grid read-out sub 4).
Per primary cell (S0 tau 4, S12 tau 4.9, A12 tau 3.3): G* 500, random 200, B-spread / B-fan / B-cov 200 episodes.
Pass rule per cell: success(G*) >= success(random) + 10 pp AND v2 §1.7 non-degeneracy: success(G*) in [0.15, 0.90],
D_c = success(G*) - success(random) >= 20 pp, BI saturation of G* < 50 % (BI > cap - 0.5 nats, cap = -log prior ball
mass, i.e. posterior ball mass > exp(-0.5); computed from the recorded ball_mass). Margins (§1.5): delta_c = min(4 pp,
0.15 D_c); eps_c = min(0.05 BI_c(G*), 0.15 D_c^BI) nats. H-star(c) = heuristic with the highest success on its 200
episodes (ties -> B-spread < B-fan < B-cov). Flat' screen: H-star success >= success(G*) - delta_c in >= 2 cells.
Episode sets are used in full (G* 0-499, others 0-199); incomplete files are reported as such.
Writes results/v3/12_g5_analysis.json."""
import glob
import json
import math
import os

import numpy as np

base = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "results", "v3")
CELLS = {"S0": "S_k0", "S12": "S_k12", "A12": "A_k12"}
N_EXPECT = {"gstar": 500, "random": 200, "b_spread": 200, "b_fan": 200, "b_cov": 200}
HEUR = ("b_spread", "b_fan", "b_cov")


def load(pre, method):
    d = {}
    for f in glob.glob(os.path.join(base, "g5", f"{pre}_{method}_*.jsonl")):
        for line in open(f):
            r = json.loads(line)
            if "episode" in r:
                d[r["episode"]] = r
    return d


def summ(d):
    e = sorted(d)
    s = np.array([d[i]["success"] for i in e], float)
    b = np.array([d[i]["ball_info"] for i in e], float)
    sat = np.array([d[i]["ball_mass"] > math.exp(-0.5) for i in e], float)
    return {"n": len(e), "success": float(s.mean()) if len(e) else None,
            "se_success": float(s.std(ddof=1) / math.sqrt(len(e))) if len(e) > 1 else None,
            "bi": float(b.mean()) if len(e) else None, "sd_bi": float(b.std(ddof=1)) if len(e) > 1 else None,
            "sat": float(sat.mean()) if len(e) else None}


out = {"cells": {}}
flat_count = 0
for name, pre in CELLS.items():
    m = {k: load(pre, k) for k in N_EXPECT}
    if not m["gstar"] or not m["random"]:
        continue
    c = {k: summ(v) for k, v in m.items()}
    c["complete"] = {k: len(m[k]) == n for k, n in N_EXPECT.items()}
    g, r = c["gstar"], c["random"]
    D = g["success"] - r["success"]
    DBI = g["bi"] - r["bi"]
    eg = sorted(m["gstar"])
    c["gstar_first200_success"] = float(np.mean([m["gstar"][i]["success"] for i in eg if i < 200]))
    c["gstar_last300_success"] = float(np.mean([m["gstar"][i]["success"] for i in eg if i >= 200])) if any(i >= 200 for i in eg) else None
    c["D_c"], c["D_c_BI"] = D, DBI
    c["plus10pp_ok"] = bool(g["success"] >= r["success"] + 0.10)
    c["nondegenerate"] = {"gstar_in_[0.15,0.90]": bool(0.15 <= g["success"] <= 0.90), "D_c>=0.20": bool(D >= 0.20),
                          "sat<0.5": bool(g["sat"] < 0.5)}
    c["passes"] = bool(c["plus10pp_ok"] and all(c["nondegenerate"].values()))
    c["delta_c"] = float(min(0.04, 0.15 * D))
    c["eps_c"] = float(min(0.05 * g["bi"], 0.15 * DBI))
    hs = [(c[h]["success"] if c[h]["n"] else -1.0, -i, h) for i, h in enumerate(HEUR)]
    best = max(hs)
    c["H_star"] = best[2]
    c["H_star_success"] = best[0]
    c["flat_screen"] = bool(best[0] >= g["success"] - c["delta_c"])
    flat_count += int(c["flat_screen"])
    out["cells"][name] = c
out["flat_screen_cells"] = flat_count
out["flat_prime_likely"] = bool(flat_count >= 2)
out["surviving_cells"] = [k for k, v in out["cells"].items() if v["passes"]]
print(json.dumps(out, indent=1))
json.dump(out, open(os.path.join(base, "12_g5_analysis.json"), "w"), indent=1)
