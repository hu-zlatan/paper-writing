"""Travel decomposition on test3 0-299 (stage 18 v4 review item M4; report-only, no test). Logged travel_rad starts at
the episode's continuous start angle phi0, so the first probe always includes a move onto the 5.625 deg phi grid.
Splits the logged total into the first leg |wrap(phi(a_0) - phi0)| and the between-probe travel (sum over later legs),
and reports the first leg's grid-snap floor min_j |wrap(PHI_GRID_j - phi0)| (the travel no policy can avoid).
Cells: S12 (results/v3/test3, no-grid, kappa 12) and S2 (results/v4/test3, no-grid, kappa 2); B-fan in S12 from
results/v3/test3_sub8 (its no-grid file set). Writes results/v4/14_travel_split.json."""
import glob
import json
import math
import os
import sys

here = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, here)
os.environ.setdefault("TOUCHBED_NPHI", "64")                       # every v3/v4 job ran the 64 x 8 action set
import numpy as np  # noqa: E402
from touchbed.travel import PHI, PHI_GRID, wrap  # noqa: E402
from touchbed.v3 import state_v3  # noqa: E402

root = os.path.join(here, "..", "results")
N = 300
CELLS = {
    "S12": ("v3", 12.0, {"gstar": ["test3/S_k12_gstar_*.jsonl"], "b_fan": ["test3_sub8/S_k12_b_fan_*.jsonl"],
                         "random": ["test3/S_k12_random_*.jsonl"],
                         "student_rem": [f"test3/S_k12_student_rem_s{s}_*.jsonl" for s in (501, 502, 503)],
                         "rl": [f"test3/S_k12_rl_s{s}_*.jsonl" for s in (511, 512, 513)]}),
    "S2": ("v4", 2.0, {"gstar": ["test3/S_k2_gstar_*.jsonl"], "b_fan": ["test3/S_k2_b_fan_*.jsonl"],
                       "random": ["test3/S_k2_random_*.jsonl"],
                       "student": [f"test3/S_k2_student_s{s}_*.jsonl" for s in (601, 602, 603)],
                       "rl": [f"test3/S_k2_rl_s{s}_*.jsonl" for s in (611, 612, 613)]}),
}


def rows(ver, pattern):
    r = {}
    for f in sorted(glob.glob(os.path.join(root, ver, pattern))):
        for line in open(f):
            d = json.loads(line)
            if "episode" in d and "header" not in d and "actions" in d and d["episode"] < N:
                r[d["episode"]] = d
    return r


out = {"note": "report-only (stage 18 v4 M4); degrees; test3 episodes 0-299; seeds pooled for learners",
       "grid_step_deg": math.degrees(PHI_GRID[1]), "cells": {}}
for cell, (ver, kappa, groups) in CELLS.items():
    c = {}
    phi0 = {}
    for name, pats in groups.items():
        first, between, total, snap, n = [], [], [], [], 0
        for pat in pats:
            r = rows(ver, pat)
            for e, d in r.items():
                if e not in phi0:
                    phi0[e] = state_v3("S", "test3", e, kappa=kappa)[1]
                p0 = phi0[e]
                phis = [float(PHI[a]) for a in d["actions"]]
                legs = [abs(float(wrap(phis[0] - p0)))] + [abs(float(wrap(phis[i] - phis[i - 1])))
                                                           for i in range(1, len(phis))]
                tot = math.degrees(d["travel_rad"])
                assert abs(math.degrees(sum(legs)) - tot) < 1e-6, (cell, name, e)
                first.append(math.degrees(legs[0]))
                between.append(math.degrees(sum(legs[1:])))
                total.append(tot)
                snap.append(math.degrees(float(np.min(np.abs(wrap(PHI_GRID - p0))))))
                n += 1
        if n:
            c[name] = {"n_episode_seed": n, "travel_deg_mean": float(np.mean(total)),
                       "first_leg_deg_mean": float(np.mean(first)), "between_probe_deg_mean": float(np.mean(between)),
                       "snap_floor_deg_mean": float(np.mean(snap)),
                       "frac_first_leg_is_snap": float(np.mean(np.isclose(first, snap, atol=1e-9)))}
    out["cells"][cell] = c
p = os.path.join(root, "v4", "14_travel_split.json")
json.dump(out, open(p, "w"), indent=1)
print(json.dumps(out, indent=1))
