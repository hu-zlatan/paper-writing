"""v4 E4 test read-outs for S2 (S, kappa 2, tau 4.7; docs/07c_amendment_v4_0.md), exploratory, one cell, ci95, no
multiplicity correction:
- test3 0-299 sub 8 (regrid3 re-reads in results/v4/test3_sub8/): success / BI rows for G*, students (seeds 601-603,
  final round r2), RL-relative (seeds 611-613), B-fan, random; paired diffs student-G*, student-RL, G*-RL, student-B-fan.
- H2-S2 on test3 0-499 (gt3 outputs in results/v4/h2/): one-sided 95 % crossed-bootstrap LB of g_T(student) - g_T(RL)
  > +0.10 nats -> "distillation scores higher on RL's own objective", else "not detected".
- behaviour (no-grid test3 0-299 actions in results/v4/test3/): probes and logged travel per episode (degrees).
Episodes are those every row has; nothing is selected. Writes results/v4/14_s2_analysis.json."""
import glob
import json
import math
import os
import sys

import numpy as np

here = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, here)
from touchbed.stats import crossed_bootstrap_diff  # noqa: E402

base = os.path.join(here, "..", "results", "v4")
N_SUB, N_H2 = 300, 500
ST, RL = (601, 602, 603), (611, 612, 613)


def load(sub, pat, n, key=None):
    d = {}
    for f in sorted(glob.glob(os.path.join(base, sub, pat))):
        for line in open(f):
            r = json.loads(line)
            if "episode" in r and "header" not in r and r["episode"] < n:
                d[r["episode"]] = r[key] if key else r
    return d


def rows(sub, n, key=None):
    return {"gstar": [load(sub, "S_k2_gstar*.jsonl", n, key)],
            "student": [load(sub, f"S_k2_student_s{s}*.jsonl", n, key) for s in ST],
            "rl": [load(sub, f"S_k2_rl_s{s}*.jsonl", n, key) for s in RL],
            "b_fan": [load(sub, "S_k2_b_fan*.jsonl", n, key)],
            "random": [load(sub, "S_k2_random*.jsonl", n, key)]}


def common(meth, n, skip=()):
    return [e for e in range(n) if all(e in d for m, ds in meth.items() if m not in skip for d in ds)]


out = {"cell": "S2", "note": "exploratory, one cell; ci95 two-sided; no multiplicity correction"}
meth = rows("test3_sub8", N_SUB)
eps = common(meth, N_SUB, skip=("random",))     # random (an anchor, in no paired contrast) does not restrict the set
out["test3_sub8"] = {"n_episodes": len(eps), "complete": len(eps) == N_SUB,
                     "n_per_row": {m: [len(d) for d in ds] for m, ds in meth.items()}, "rows": {}, "diffs": {}}
if eps:
    def arr(m, key, ee=None):
        return np.array([[float(d[e][key]) for d in meth[m]] for e in (eps if ee is None else ee)])
    er = [e for e in eps if e in meth["random"][0]]
    out["test3_sub8"]["random_on_available"] = {"n": len(er), "success": float(arr("random", "success", er).mean()),
                                                 "ball_info": float(arr("random", "ball_info", er).mean())} if er else None
    for m in [k for k in meth if k != "random"]:
        out["test3_sub8"]["rows"][m] = {"success": float(arr(m, "success").mean()),
                                        "ball_info": float(arr(m, "ball_info").mean()),
                                        "per_seed_success": [float(x) for x in arr(m, "success").mean(0)]}
    for a, b in (("student", "gstar"), ("student", "rl"), ("gstar", "rl"), ("student", "b_fan"), ("b_fan", "gstar")):
        for key in ("success", "ball_info"):
            r = crossed_bootstrap_diff(arr(a, key), arr(b, key), alpha=0.025)
            out["test3_sub8"]["diffs"][f"{a}-{b}:{key}"] = {"diff": r["diff"], "ci95": [r["lower"], r["upper"]]}

g = rows("h2", N_H2, "g_T")
e2 = [e for e in range(N_H2) if all(e in d for d in g["student"] + g["rl"])]
out["h2"] = {"n_episodes": len(e2), "complete": len(e2) == N_H2, "threshold_nats": 0.10}
if e2:
    A = np.array([[d[e] for d in g["student"]] for e in e2])
    B = np.array([[d[e] for d in g["rl"]] for e in e2])
    r = crossed_bootstrap_diff(A, B)
    out["h2"].update({"student_mean": float(A.mean()), "rl_mean": float(B.mean()), "bootstrap": r,
                      "passes": bool(r["lower"] > 0.10)})
    for m in ("gstar", "b_fan", "random"):
        if all(e in g[m][0] for e in e2):
            out["h2"][f"g_T_{m}"] = float(np.mean([g[m][0][e] for e in e2]))

beh = rows("test3", N_SUB)
e3 = common(beh, N_SUB)
out["behaviour"] = {"n_episodes": len(e3)}
if e3:
    for m in beh:
        tr = [math.degrees(d[e]["travel_rad"]) for d in beh[m] for e in e3]
        pr = [len(d[e]["actions"]) for d in beh[m] for e in e3]
        out["behaviour"][m] = {"travel_deg_mean": float(np.mean(tr)), "probes_mean": float(np.mean(pr))}
    # stage 14 v4 pass 2 (S3): per-episode coupling of student and G* travel, and identical action sequences
    tg = np.array([math.degrees(beh["gstar"][0][e]["travel_rad"]) for e in e3])
    out["behaviour"]["student_vs_gstar_travel_pearson_r"] = [
        float(np.corrcoef(tg, [math.degrees(d[e]["travel_rad"]) for e in e3])[0, 1]) for d in beh["student"]]
    out["behaviour"]["student_identical_action_sequence_to_gstar"] = [
        int(sum(d[e]["actions"] == beh["gstar"][0][e]["actions"] for e in e3)) for d in beh["student"]]
if e2:
    out["h2"]["per_seed_student"] = {str(s): float(np.mean([g["student"][i][e] for e in e2])) for i, s in enumerate(ST)}
    out["h2"]["per_seed_rl"] = {str(s): float(np.mean([g["rl"][i][e] for e in e2])) for i, s in enumerate(RL)}
out["rl_training"] = {}
for s in RL:
    f = os.path.join(base, "rl", f"S_k2_rel_cfg2_sd{s}.json")
    if os.path.exists(f):
        m = json.load(open(f))
        out["rl_training"][str(s)] = {"status": m["status"], "plateau_at": m.get("plateau_at"),
                                      "episodes": m["history"][-1]["episodes"],
                                      "g_T_mean_last": m["history"][-1]["g_T_mean"], "wall_s": m.get("wall_s")}
json.dump(out, open(os.path.join(base, "14_s2_analysis.json"), "w"), indent=1)
print(json.dumps(out, indent=1))
