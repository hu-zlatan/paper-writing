"""Row-4 main read-out M4 (plans/stage_12_experiment_run_v3_main_row4.md; 07_hypotheses_v3 §3.3 'reported with the
test'): success / BI / executed probes on test3 0-299, S12, sub-8 grid re-read, for G*, the remedied students
(501-503) and RL-relative (511-513). Paired crossed-bootstrap differences (two-sided 90% and 95% intervals):
student - G*, student - RL, G* - RL; gap closure [succ(student) - succ(RL)] / [succ(G*) - succ(RL)] only if
LB95(succ(G*) - succ(RL)) > delta_S12. Writes results/v3/14_m4_analysis.json."""
import glob
import json
import os
import sys

import numpy as np

here = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, here)
from touchbed.stats import crossed_bootstrap_diff  # noqa: E402

base = os.path.join(here, "..", "results", "v3")
N = 300


def load(pat):
    d = {}
    for f in glob.glob(os.path.join(base, "test3_sub8", pat)):
        for line in open(f):
            r = json.loads(line)
            if "episode" in r and r["episode"] < N:
                d[r["episode"]] = r
    return d


meth = {"gstar": [load("S_k12_gstar_*.jsonl")],
        "student": [load(f"S_k12_student_rem_s{s}_*.jsonl") for s in (501, 502, 503)],
        "rl": [load(f"S_k12_rl_s{s}_*.jsonl") for s in (511, 512, 513)]}
eps = [e for e in range(N) if all(e in d for ds in meth.values() for d in ds)]
g5 = json.load(open(os.path.join(base, "12_g5_analysis.json")))["cells"]["S12"]
out = {"n_episodes": len(eps), "complete": len(eps) == N, "delta_S12": g5["delta_c"], "rows": {}, "diffs": {}}


def arr(m, key):
    return np.array([[float(d[e][key]) for d in meth[m]] for e in eps])


if eps:
    for m in meth:
        out["rows"][m] = {"success": float(arr(m, "success").mean()), "ball_info": float(arr(m, "ball_info").mean()),
                          "probes": float(np.mean([[len(d[e]["actions"]) for d in meth[m]] for e in eps])),
                          "per_seed_success": [float(arr(m, "success")[:, i].mean()) for i in range(len(meth[m]))]}
    for a, b in (("student", "gstar"), ("student", "rl"), ("gstar", "rl")):
        for key in ("success", "ball_info"):
            r90 = crossed_bootstrap_diff(arr(a, key), arr(b, key), alpha=0.05)
            r95 = crossed_bootstrap_diff(arr(a, key), arr(b, key), alpha=0.025)
            out["diffs"][f"{a}-{b}:{key}"] = {"diff": r90["diff"], "ci90": [r90["lower"], r90["upper"]],
                                              "ci95": [r95["lower"], r95["upper"]]}
    lb = out["diffs"]["gstar-rl:success"]["ci90"][0]          # one-sided 95% LB
    out["gap_closure_reported"] = bool(lb > g5["delta_c"])
    if out["gap_closure_reported"]:
        s = out["rows"]
        out["gap_closure"] = (s["student"]["success"] - s["rl"]["success"]) / (s["gstar"]["success"] - s["rl"]["success"])
print(json.dumps(out, indent=1))
json.dump(out, open(os.path.join(base, "14_m4_analysis.json"), "w"), indent=1)
