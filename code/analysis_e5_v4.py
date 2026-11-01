"""E5 (docs/07c_amendment_v4_0.md): reduced-G* rows g125_512_16 and g500_512_4 on test3 0-299, S12, sub 8, paired with
the v3 S12 test3 sub-8 rows (full G*, remedied students s501-503, long-training students s501-503). Reading fixed in the
amendment: reduced-G* - student success / BI with ci95, reported; no claim beyond "at its logged latency" (median of
the per-decision latencies logged by eval3 on the free runners, not the Lat' protocol). Exploratory, no multiplicity
correction. Episodes are those every row has (nothing selected). Writes results/v4/14_e5_analysis.json."""
import glob
import json
import os
import sys

import numpy as np

here = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, here)
from touchbed.stats import crossed_bootstrap_diff  # noqa: E402

v3 = os.path.join(here, "..", "results", "v3", "test3_sub8")
v4 = os.path.join(here, "..", "results", "v4")
N = 300


def load(d, pat):
    out = {}
    for f in sorted(glob.glob(os.path.join(d, pat))):
        for line in open(f):
            r = json.loads(line)
            if "episode" in r and "header" not in r and r["episode"] < N:
                out[r["episode"]] = r
    return out


meth = {"g125_512_16": [load(os.path.join(v4, "e5"), "S_k12_g125_512_16_*.jsonl")],
        "g500_512_4": [load(os.path.join(v4, "e5"), "S_k12_g500_512_4_*.jsonl")],
        "gstar": [load(v3, "S_k12_gstar_*.jsonl")],
        "student_rem": [load(v3, f"S_k12_student_rem_s{s}_*.jsonl") for s in (501, 502, 503)],
        "student_long": [load(v3, f"S_k12_student_long_s{s}_*.jsonl") for s in (501, 502, 503)]}
eps = [e for e in range(N) if all(e in d for ds in meth.values() for d in ds)]
out = {"note": "E5, exploratory: reduced G* on S12 test3 0-299 sub 8, paired with v3 rows; ci95 two-sided, no "
               "multiplicity correction; latency = median of eval3-logged per-decision latencies (free runners)",
       "n_episodes": len(eps), "complete": len(eps) == N,
       "n_per_row": {m: [len(d) for d in ds] for m, ds in meth.items()}, "rows": {}, "diffs": {}}


def arr(m, key):
    return np.array([[float(d[e][key]) for d in meth[m]] for e in eps])


if eps:
    for m in meth:
        lat = [x for d in meth[m] for e in eps for x in d[e].get("latencies_s", [])]
        out["rows"][m] = {"success": float(arr(m, "success").mean()), "ball_info": float(arr(m, "ball_info").mean()),
                          "probes": float(np.mean([[len(d[e]["actions"]) for d in meth[m]] for e in eps])),
                          "decision_latency_median_s": float(np.median(lat)) if lat else None}
    for a in ("g125_512_16", "g500_512_4"):
        for b in ("student_rem", "student_long", "gstar"):
            for key in ("success", "ball_info"):
                r = crossed_bootstrap_diff(arr(a, key), arr(b, key), alpha=0.025)
                out["diffs"][f"{a}-{b}:{key}"] = {"diff": r["diff"], "ci95": [r["lower"], r["upper"]]}
os.makedirs(v4, exist_ok=True)
json.dump(out, open(os.path.join(v4, "14_e5_analysis.json"), "w"), indent=1)
print(json.dumps(out, indent=1))
