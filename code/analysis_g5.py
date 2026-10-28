"""Gate G5 + non-degeneracy (docs/07_hypotheses_v2.md §1.5, §1.7, §4) on the adopted grid evaluation (B8).
Cells: A0 (tau 3), S0 (tau 4; G4 runs, first 300), A/S at kappa 6 and 12. Rules: G* >= random + 10 pp (300 pilot eps);
non-degeneracy on the first 200: success(G*) in [0.15, 0.90], D = success(G*) - success(random) >= 20 pp, BI
saturation of G* (BI > cap - 0.5 nats) < 50 %. Flatness at (S, kappa): |dsuccess| <= 2 pp and |dBI| <= 0.10 (fine grid
64x16 minus 32x8, paired point estimates). Writes results/v2/12_g5_analysis.json."""
import glob
import json
import math
import os

import numpy as np

base = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "results", "v2")


def load(folder, pat):
    d = {}
    for f in glob.glob(os.path.join(base, folder, pat)):
        for line in open(f):
            r = json.loads(line)
            if "episode" in r:
                d[r["episode"]] = r
    return d


def cap(r):
    return r.get("ball_cap", None)


out = {"cells": {}, "flatness": {}}
cells = {"A0": ("grid_g5", "A_k0"), "A6": ("grid_g5", "A_k6"), "A12": ("grid_g5", "A_k12"),
         "S0": ("grid_ref", "S_k0"), "S6": ("grid_g5", "S_k6"), "S12": ("grid_g5", "S_k12")}
for name, (folder, pre) in cells.items():
    g = load(folder, f"{pre}_gstar_*.jsonl"); r = load(folder, f"{pre}_random_*.jsonl")
    caps = {}
    src = "g4" if name == "S0" else "g5"
    for e, row in load(src, f"{pre}_gstar_{'N32000_' if name == 'S0' else ''}sh*.jsonl").items():
        caps[e] = row["ball_cap"]
    e300 = [e for e in sorted(set(g) & set(r)) if e < 300]
    e200 = [e for e in e300 if e < 200]
    if not e200:
        continue
    sg3, sr3 = (float(np.mean([d[e]["success"] for e in e300])) for d in (g, r))
    sg2, sr2 = (float(np.mean([d[e]["success"] for e in e200])) for d in (g, r))
    sat = float(np.mean([g[e]["ball_info"] > caps[e] - 0.5 for e in e200 if e in caps]))
    out["cells"][name] = {"n300": len(e300), "gstar_success_300": sg3, "random_success_300": sr3,
                          "plus10pp_ok": bool(sg3 >= sr3 + 0.10), "gstar_success_200": sg2, "D_200": sg2 - sr2,
                          "sat_200": sat, "nondegenerate": bool(0.15 <= sg2 <= 0.90 and sg2 - sr2 >= 0.20 and sat < 0.5),
                          "gstar_bi_300": float(np.mean([g[e]["ball_info"] for e in e300]))}
    print(name, out["cells"][name])
for k in (6, 12):
    a = load("grid_g5", f"S_k{k}_gstar_sh*.jsonl"); b = load("grid_g5_flat", f"S_k{k}_gstar_fine_*.jsonl")
    e = sorted(set(a) & set(b))
    if not e:
        continue
    ds = float(np.mean([b[i]["success"] for i in e]) - np.mean([a[i]["success"] for i in e]))
    db = float(np.mean([b[i]["ball_info"] - a[i]["ball_info"] for i in e]))
    out["flatness"][f"S{k}"] = {"n": len(e), "d_success": ds, "d_bi": db, "passes": bool(abs(ds) <= 0.02 and abs(db) <= 0.10)}
    print("flatness", k, out["flatness"][f"S{k}"])
json.dump(out, open(os.path.join(base, "12_g5_analysis.json"), "w"), indent=1)
