"""v5 'Baselines' rule (docs/07c_amendment_v5_0.md, Decision rules): per cell, H* = the heuristic among B-spread /
B-fan / B-cov with the highest success on pilot3 episodes 0-199 (sub-8 grid read-out). Tie-break inherited unchanged
from v3 G5' (code/analysis_g5_v3.py): B-spread < B-fan < B-cov in priority order. test5 is not read here.
Also reports BI (ball_info) and mean travel per heuristic for context. Writes results/v5/12_base_hstar.json."""
import glob
import json
import math
import os

import numpy as np

base = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "results", "v5")
CELLS = {"S2": "S_k2", "S4": "S_k4", "S8": "S_k8", "S12": "S_k12", "A16-2": "A16_k2"}
HEUR = ("b_spread", "b_fan", "b_cov")
N = 200


def load(pre, method):
    d = {}
    for f in glob.glob(os.path.join(base, "base_pilot", f"{pre}_{method}_*.jsonl")):
        for line in open(f):
            r = json.loads(line)
            if "episode" in r:
                d[r["episode"]] = r
    return d


def summ(d):
    e = sorted(i for i in d if i < N)
    s = np.array([d[i]["success"] for i in e], float)
    b = np.array([d[i]["ball_info"] for i in e], float)
    tr = np.array([d[i]["travel_rad"] for i in e], float)
    return {"n": len(e), "success": float(s.mean()) if e else None,
            "se_success": float(s.std(ddof=1) / math.sqrt(len(e))) if len(e) > 1 else None,
            "bi": float(b.mean()) if e else None, "travel_deg": float(np.degrees(tr).mean()) if e else None}


out = {"rule": "H* = argmax success on pilot3 0-199, sub 8; ties B-spread < B-fan < B-cov", "cells": {}}
for name, pre in CELLS.items():
    c = {h: summ(load(pre, h)) for h in HEUR}
    c["complete"] = all(c[h]["n"] == N for h in HEUR)
    best = max((c[h]["success"] if c[h]["n"] else -1.0, -i, h) for i, h in enumerate(HEUR))
    c["H_star"], c["H_star_success"] = best[2], best[0]
    out["cells"][name] = c
print(json.dumps(out, indent=1))
json.dump(out, open(os.path.join(base, "12_base_hstar.json"), "w"), indent=1)
