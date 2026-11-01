"""Report-only diagnostics after the stage-18 v4 review (no test, no gate):
(1) Cal' verification for S2 (review M2): G*'s mean executed probes with the tau = 4.7 budget enforced on cal3 0-199
    (results/v4/cal/verify_S_k2_sh*.jsonl); rule as v3 C4: within n* +- 0.3 (n* = 4).
(2) Val/test pipeline check (review M6): val3 0-49 no-grid actions (results/v4/pipe/val3_nogrid, the test3 pipeline)
    vs the inline-scored D4 val3 rows (results/v4/d4_val, eval3 sub 8): identical action sequences, and after the
    regrid3 sub-8 re-read (results/v4/pipe/val3_sub8) identical success and |BI difference| per episode.
Writes results/v4/14_diag_s2.json."""
import glob
import json
import os

import numpy as np

b = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "results", "v4")


def rows(pattern):
    r = {}
    for f in sorted(glob.glob(os.path.join(b, pattern))):
        for line in open(f):
            d = json.loads(line)
            if "episode" in d and "header" not in d:
                r[d["episode"]] = d
    return r


out = {"note": "report-only diagnostics (stage 18 v4 review M2, M6); no gate"}
v = rows("cal/verify_S_k2_sh*.jsonl")
if v:
    p = [v[e]["n_probes"] for e in sorted(v)]
    out["cal_verify_S_k2"] = {"n_episodes": len(p), "complete": len(p) == 200, "mean_probes": float(np.mean(p)),
                              "rule": "mean probes within 4 +- 0.3", "passes": bool(abs(np.mean(p) - 4) <= 0.3)}
pc = {}
for m, a, inline, rg in (("gstar", "S_k2_gstar_*", "S_k2_gstar_*", "S_k2_gstar_*"),
                         ("student_s601", "S_k2_student_s601_r2_*", "S_k2_student_s601_r2_*", "S_k2_student_s601_r2_*")):
    A = rows(f"pipe/val3_nogrid/{a}.jsonl")
    B = rows(f"d4_val/{inline}.jsonl")
    R = rows(f"pipe/val3_sub8/{rg}.jsonl")
    e = [i for i in range(50) if i in A and i in B]
    r = {"n_episodes": len(e), "identical_actions": int(sum(A[i]["actions"] == B[i]["actions"] for i in e))}
    er = [i for i in e if i in R]
    if er:
        r["n_reread"] = len(er)
        r["same_success"] = int(sum(bool(R[i]["success"]) == bool(B[i]["success"]) for i in er))
        r["max_abs_bi_diff"] = float(max(abs(R[i]["ball_info"] - B[i]["ball_info"]) for i in er))
        r["success_inline"] = float(np.mean([B[i]["success"] for i in er]))
        r["success_reread"] = float(np.mean([R[i]["success"] for i in er]))
    pc[m] = r
out["pipe_check_val3_0_49"] = pc
json.dump(out, open(os.path.join(b, "14_diag_s2.json"), "w"), indent=1)
print(json.dumps(out, indent=1))
