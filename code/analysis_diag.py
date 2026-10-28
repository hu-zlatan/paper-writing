"""EXPLORATORY diagnostics for the v2 stage-15 decision (experiments/v2_diag_k0k6.json, v2_dev_rel.json): learned
policy vs G* on the same validation episodes of S, grid evaluation (B8). Not a gate; no pre-registered threshold.
Paired bootstrap 95 % CI of the success difference over episodes. Writes results/v2/12_diag_analysis.json."""
import glob
import json
import os

import numpy as np

base = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "results", "v2")


def load(pat):
    d = {}
    for f in glob.glob(os.path.join(base, pat)):
        for line in open(f):
            r = json.loads(line)
            if "episode" in r:
                d[r["episode"]] = r
    return d


def boot(x, n=10000, seed=0):
    rng = np.random.default_rng(seed)
    i = rng.integers(0, len(x), (n, len(x)))
    m = x[i].mean(1)
    return [float(np.quantile(m, 0.025)), float(np.quantile(m, 0.975))]


out = {}
cells = {"k0": ("diag/val_S_k0_gstar_sh*_grid.jsonl", {f"abs_sd{s}": f"diag/val_S_k0_sd{s}_grid.jsonl" for s in (300, 301)}),
         "k6": ("diag/val_S_k6_gstar_sh*_grid.jsonl", {f"abs_sd{s}": f"diag/val_S_k6_sd{s}_grid.jsonl" for s in (200, 201, 202)}),
         "k12": ("grid_g3_val/S_k12_gstar_sh*.jsonl", {**{f"abs_sd{s}": f"grid_g3_val/S_k12_sd{s}_sh*.jsonl" for s in (200, 201, 202)},
                                                    **{f"rel_sd{s}": f"dev_rel/val_rel_S_k12_sd{s}_grid.jsonl" for s in (400, 401, 402)}})}
for c, (gp, pols) in cells.items():
    g = load(gp)
    out[c] = {}
    for name, pp in pols.items():
        p = load(pp)
        e = sorted(set(p) & set(g))
        if not e:
            continue
        d = np.array([float(p[i]["success"]) - float(g[i]["success"]) for i in e])
        out[c][name] = {"n": len(e), "success": float(np.mean([p[i]["success"] for i in e])),
                        "gstar_success": float(np.mean([g[i]["success"] for i in e])), "d_success": float(d.mean()),
                        "d_success_ci95": boot(d), "bi": float(np.mean([p[i]["ball_info"] for i in e])),
                        "gstar_bi": float(np.mean([g[i]["ball_info"] for i in e])),
                        "probes": float(np.mean([len(p[i]["actions"]) for i in e])),
                        "gstar_probes": float(np.mean([len(g[i]["actions"]) for i in e])),
                        "distinct_first_phi": len({p[i]["actions"][0] // 8 for i in e})}
json.dump(out, open(os.path.join(base, "12_diag_analysis.json"), "w"), indent=1)
for c in out:
    for k, v in out[c].items():
        print(c, k, "n=%d succ %.3f vs G* %.3f  d=%+.3f [%+.3f,%+.3f]  BI %.2f vs %.2f  probes %.2f vs %.2f  firstphi %d" % (
            v["n"], v["success"], v["gstar_success"], v["d_success"], *v["d_success_ci95"], v["bi"], v["gstar_bi"],
            v["probes"], v["gstar_probes"], v["distinct_first_phi"]))
