"""Amendment B8: every candidate evaluation method vs the adaptive grid reference on the same recorded episodes, G4 rule
(|dBI| <= 0.05 nats; |dsuccess| <= 1 pp with 95 % CI inside +-2 pp). Writes results/v2/12_b8_analysis.json."""
import glob
import json
import os
import sys

import numpy as np

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from touchbed.stats import crossed_bootstrap_diff  # noqa: E402

base = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "results", "v2")


def load(pattern, label_fn):
    out = {}
    for f in glob.glob(os.path.join(base, pattern)):
        lab = label_fn(os.path.basename(f))
        for line in open(f):
            r = json.loads(line)
            if "episode" in r:
                out[(lab, r["set"], float(r["kappa"]), r["method"], r["episode"])] = r
    return out


rows = {}
rows.update(load("g4/*.jsonl", lambda b: "pf32k_3mh" if "N32000" in b else "pf128k_3mh"))
rows.update(load("g4_fallback/*.jsonl", lambda b: "pf32k_" + b.split("_")[3]))           # mh10 / mh30
rows.update(load("g4_b5/*.jsonl", lambda b: "b5_" + b.rsplit("_sh", 1)[0].split("_")[-1]))  # r10 / r30 / ref
rows.update(load("grid_ref/*.jsonl", lambda b: "grid"))
for extra in sys.argv[1:]:   # more candidate folders, e.g. evalpf re-reads: name=folder
    name, folder = extra.split("=")
    rows.update(load(folder + "/*.jsonl", lambda b, n=name: n))
cands = sorted({c for (c, *_rest) in rows if c != "grid"})
cells = sorted({(s, k, m) for (c, s, k, m, e) in rows if c == "grid"})
out = {}
for s, k, m in cells:
    for c in cands:
        eps = sorted(e for (c2, s2, k2, m2, e) in rows if (c2, s2, k2, m2) == (c, s, k, m) and ("grid", s, k, m, e) in rows)
        if len(eps) < 20:
            continue
        res = {"n_episodes": len(eps)}
        for metric in ("success", "ball_info", "identity_ok"):
            a = np.array([float(rows[("grid", s, k, m, e)][metric]) for e in eps])
            b = np.array([float(rows[(c, s, k, m, e)][metric]) for e in eps])
            bs = crossed_bootstrap_diff(a, b, n_boot=4000, seed=1, alpha=0.025)
            res[metric] = {"mean_cand": float(b.mean()), "mean_grid": float(a.mean()), "diff_grid_minus_cand": bs["diff"],
                           "ci95": [bs["lower"], bs["upper"]]}
        res["passes_G4_rule"] = bool(abs(res["ball_info"]["diff_grid_minus_cand"]) <= 0.05
                                     and abs(res["success"]["diff_grid_minus_cand"]) <= 0.01
                                     and res["success"]["ci95"][0] >= -0.02 and res["success"]["ci95"][1] <= 0.02)
        out[f"{s}_k{k:g}_{m}_{c}"] = res
        print(f"{s} k{k:g} {m:6s} {c:11s} n={len(eps):3d} succ {res['success']['mean_cand']:.3f}/{res['success']['mean_grid']:.3f} "
              f"dS={res['success']['diff_grid_minus_cand']:+.3f} [{res['success']['ci95'][0]:+.3f},{res['success']['ci95'][1]:+.3f}] "
              f"dBI={res['ball_info']['diff_grid_minus_cand']:+.3f} [{res['ball_info']['ci95'][0]:+.3f},{res['ball_info']['ci95'][1]:+.3f}] "
              + ("PASS" if res["passes_G4_rule"] else "FAIL"))
json.dump(out, open(os.path.join(base, "12_b8_analysis.json"), "w"), indent=1)
