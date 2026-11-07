"""v5 E4: freeze record + test5 manifests (amendment v5.0 E4). test5 is evaluated once per (method, cell), only after
every student and RL policy of that cell is frozen; the freeze record (results/v5/13_freeze.json, sha256 of every
weight file) must be committed and logged in PROGRESS before the first test5 job.

usage: python tools_v5_test5.py freeze <cell> [<cell> ...]     write/extend the freeze record (refuses if a weight is missing)
       python tools_v5_test5.py manifest <cell>                 test5 eval3 manifest(s) for one cell (refuses unless frozen
                                                                and every hash still matches; split at 250 jobs per file)
Methods per cell: gstar, random, b_fan, b_spread, b_cov, student x 5 (round-2 best checkpoint), rl x 5 (cfg 6, spce_total)
and in S2/S12 rl_success x 5. test5 0-299 (addendum v5.1e), sub 8 grid read-out (g_T is read post hoc with gt3 on the same records).
Shard size: about 15 min of mean per-episode wall time measured on pilot3/val3 in the same cell (sizing only)."""
import glob
import hashlib
import json
import math
import os
import sys

ROOT = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..")
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from tools_v5_manifests import cell  # noqa: E402

FREEZE = os.path.join(ROOT, "results/v5/13_freeze.json")
STUDENT_SEEDS, RL_SEEDS = range(701, 706), range(711, 716)
N_EP, TARGET_S = 300, 900   # 300: addendum v5.1e (reduction order step 2)


def weights(c):
    s, k, _ = cell(c)
    w = {f"student_s{sd}": f"results/v5/d5/{s}_k{k}_s{sd}_r2.npz" for sd in STUDENT_SEEDS}
    w |= {f"rl_s{sd}": f"results/v5/rl/{s}_k{k}_rel_cfg6_sd{sd}.npz" for sd in RL_SEEDS}
    if c in ("S2", "S12"):
        w |= {f"rlsucc_s{sd}": f"results/v5/rl/{s}_k{k}_rlsucc_cfg6_sd{sd}.npz" for sd in RL_SEEDS}
    return w


def sha(p):
    return hashlib.sha256(open(os.path.join(ROOT, p), "rb").read()).hexdigest()


def mean_wall(s, k, method):
    v = []
    for d in ("results/v5/base_pilot", "results/v5/d5_val", "results/v4/d4_val", "results/v3/d3_val*"):  # S2/S12 G* val3 = v4/v3
        for f in glob.glob(os.path.join(ROOT, d, f"{s}_k{k}_*.jsonl")):
            for line in open(f):
                r = json.loads(line)
                if r.get("method") == method and "wall_s" in r:
                    v.append(r["wall_s"])
    return sum(v) / len(v) if v else None


def jobs_for(c):
    s, k, tau = cell(c)
    n_star = 3 if s == "A16" else 4
    fz = json.load(open(FREEZE))["cells"].get(c)
    assert fz, f"{c} not frozen"
    for p, h in fz["sha256"].items():
        assert sha(p) == h, f"{p} changed since the freeze"
    g = mean_wall(s, k, "gstar")
    assert g, "no G* wall-time record for sizing"
    rows = [("gstar", "gstar", None), ("random", "random", None)] + [(m, m, None) for m in ("b_fan", "b_spread", "b_cov")]
    for name, p in weights(c).items():
        rows.append((name, "student" if name.startswith("student") else "rl", p))
    out = []
    for name, method, w in rows:
        mw = mean_wall(s, k, method) or g        # students/RL/random without a record in the cell: G* time (conservative)
        n = max(1, min(25, math.floor(TARGET_S / mw)))
        wa = f" --weights ../{w}" if w else ""
        for st in range(0, N_EP, n):
            cnt = min(n, N_EP - st)
            out.append({"id": f"v5_t5_{c}_{name}_{st:03d}", "cmd": f"python main.py eval3 --set {s} --kappa {k} --tau {tau} "
                        f"--n-star {n_star} --method {method}{wa} --split test5 --start {st} --count {cnt} --sub 8 "
                        f"--budget-minutes 25 --out ../results/v5/test5/{s}_k{k}_{name}_{st:03d}"})
    return out


if __name__ == "__main__":
    step, cells = sys.argv[1], sys.argv[2:]
    if step == "freeze":
        rec = json.load(open(FREEZE)) if os.path.exists(FREEZE) else {
            "rule": "amendment v5.0 E4: no test5 job for a cell before its weights are recorded here", "cells": {}}
        for c in cells:
            assert c not in rec["cells"], f"{c} already frozen (a freeze is never rewritten)"
            w = weights(c)
            miss = [p for p in w.values() if not os.path.exists(os.path.join(ROOT, p))]
            assert not miss, f"missing: {miss}"
            rec["cells"][c] = {"sha256": {p: sha(p) for p in w.values()}}
        json.dump(rec, open(FREEZE, "w"), indent=1)
        print("frozen", cells)
    elif step == "manifest":
        (c,) = cells
        jobs = jobs_for(c)
        parts = [jobs[i:i + 250] for i in range(0, len(jobs), 250)]
        for i, part in enumerate(parts):
            name = f"v5_test5_{c.replace('-', '')}" + (f"_p{i}" if len(parts) > 1 else "")
            json.dump({"purpose": f"v5 E4 test5 0-299 (addendum v5.1e) for {c}, every method once (code/tools_v5_test5.py; freeze "
                       f"results/v5/13_freeze.json)", "jobs": part},
                      open(os.path.join(ROOT, "experiments", name + ".json"), "w"), indent=1)
            print(name, len(part))
