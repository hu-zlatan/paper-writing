"""Gate D5 per cell (docs/07c_amendment_v5_0.md 'Decision rules'): the D4 rule with delta = 4 pp on val3 0-499, sub-8
grid read-out, best-checkpoint round-2 students, seeds 701-705, paired with G*:
(i)   Delta_succ(student - G*) >= max(-0.02, -delta + 1.645 * SE_s * sqrt(0.5))
(ii)  Delta_BI >= -0.15 nats
(iii) >= 4 of 5 seeds have point Delta_succ > -delta
SE = SD of the crossed (episode x seed) bootstrap, as analysis_d4_v4.boot_sd.
G* val3 records: S2 re-uses results/v4/d4_val (v4 D4), S12 re-uses results/v3/d3_val (v3 D3) — same split, episodes,
(set, kappa, tau), sub 8 and G* code path (amendment v5.1 addendum b); new cells read results/v5/d5_val.
Students: results/v5/d5_val/<cell>_student_s<seed>_r2_*.jsonl. Writes results/v5/12_d5_analysis.json."""
import glob
import json
import math
import os

import numpy as np

from analysis_d4_v4 import boot_sd

ROOT = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "results")
SEEDS, N_EP, DELTA = (701, 702, 703, 704, 705), 500, 0.04
CELLS = {"S2": "S_k2", "S4": "S_k4", "S8": "S_k8", "S12": "S_k12", "A16-2": "A16_k2"}
GSTAR = {"S2": "v4/d4_val/S_k2_gstar_*.jsonl", "S12": "v3/d3_val/S_k12_gstar_*.jsonl"}


def load(pat):
    d = {}
    for f in glob.glob(os.path.join(ROOT, pat)):
        for line in open(f):
            r = json.loads(line)
            if "episode" in r and "header" not in r:
                d[r["episode"]] = r
    return d


def cell_result(c):
    tag = CELLS[c]
    g = load(GSTAR.get(c, f"v5/d5_val/{tag}_gstar_*.jsonl"))
    st = {s: load(f"v5/d5_val/{tag}_student_s{s}_r2_*.jsonl") for s in SEEDS}
    eps = [e for e in range(N_EP) if e in g and all(e in st[s] for s in SEEDS)]
    out = {"cell": c, "n_episodes": len(eps), "complete": len(eps) == N_EP, "delta": DELTA,
           "gstar_source": GSTAR.get(c, "v5/d5_val")}
    if not eps:
        return out
    for metric, key in (("succ", "success"), ("bi", "ball_info")):
        A = np.array([[float(st[s][e][key]) for s in SEEDS] for e in eps])
        B = np.array([float(g[e][key]) for e in eps])
        d = float(np.mean(A.mean(1) - B))
        se = boot_sd(A, B)
        thr = max(-0.02, -DELTA + 1.645 * se * math.sqrt(0.5)) if metric == "succ" else -0.15
        out[metric] = {"delta_hat": d, "se": se, "threshold": thr, "passes": bool(d >= thr),
                       "student_mean": float(A.mean()), "gstar_mean": float(B.mean()),
                       "per_seed": {str(s): float(np.mean(A[:, i] - B)) for i, s in enumerate(SEEDS)}}
    ok = {s: v > -DELTA for s, v in out["succ"]["per_seed"].items()}
    out["seeds_ok"] = ok
    out["passes"] = bool(out["succ"]["passes"] and out["bi"]["passes"] and sum(ok.values()) >= 4)
    out["gstar_mean_travel_rad"] = float(np.mean([g[e]["travel_rad"] for e in eps]))
    return out


def main():
    res = {c: cell_result(c) for c in CELLS}
    done = [c for c, r in res.items() if r.get("complete")]
    res["H5a_validation"] = {"cells_complete": done, "cells_pass": [c for c in done if res[c]["passes"]]}
    json.dump(res, open(os.path.join(ROOT, "v5", "12_d5_analysis.json"), "w"), indent=1)
    print(json.dumps({c: (r.get("n_episodes"), r.get("passes")) for c, r in res.items() if c in CELLS}, indent=1))


if __name__ == "__main__":
    main()
