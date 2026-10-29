"""Reduced-G* rows (R_b candidates; v3.1, dropped from the row-4 main set as H1-only, runs cancelled part-way) read out
as a REPORT-ONLY, INCOMPLETE accuracy-vs-latency frontier (stage 18 v3 pass-2 review). pilot3 split, S12, sub 8, paired
with full G* on the same pilot3 episodes (G5' sub-8 re-reads). Episodes are those both rows have; nothing is selected.
Latency: median of the per-decision latencies logged by eval3 (same runner type, not the Lat' protocol).
Writes results/v3/14_rb_frontier.json."""
import glob
import json
import os
import sys

import numpy as np

here = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, here)
from touchbed.stats import crossed_bootstrap_diff  # noqa: E402

b = os.path.join(here, "..", "results", "v3")


def load(pat):
    d = {}
    for f in glob.glob(os.path.join(b, pat)):
        for line in open(f):
            r = json.loads(line)
            if "episode" in r and "header" not in r:
                d[r["episode"]] = r
    return d


gs = load("g5_sub8/S_k12_gstar_*.jsonl")
rb = {}
for f in glob.glob(os.path.join(b, "rb", "*.jsonl")):
    for line in open(f):
        r = json.loads(line)
        if "episode" in r and "header" not in r:
            rb.setdefault(r["method"], {})[r["episode"]] = r
out = {"note": "report-only, incomplete (runs cancelled part-way; 200 pilot3 episodes planned per row); pilot3, S12, sub 8",
       "gstar_pilot3_episodes": len(gs), "rows": {}}
for m in sorted(rb):
    eps = sorted(e for e in rb[m] if e in gs)
    if not eps:
        continue
    A = np.array([float(rb[m][e]["success"]) for e in eps]); G = np.array([float(gs[e]["success"]) for e in eps])
    Ab = np.array([float(rb[m][e]["ball_info"]) for e in eps]); Gb = np.array([float(gs[e]["ball_info"]) for e in eps])
    lat = [x for e in eps for x in rb[m][e]["latencies_s"]]
    ds = crossed_bootstrap_diff(A, G, alpha=0.025); db = crossed_bootstrap_diff(Ab, Gb, alpha=0.025)
    out["rows"][m] = {"n_paired": len(eps), "n_run": len(rb[m]), "success": float(A.mean()), "gstar_success_same_eps": float(G.mean()),
                      "ball_info": float(Ab.mean()), "decision_latency_median_s": float(np.median(lat)),
                      "minus_gstar:success": {"diff": ds["diff"], "ci95": [ds["lower"], ds["upper"]]},
                      "minus_gstar:ball_info": {"diff": db["diff"], "ci95": [db["lower"], db["upper"]]}}
json.dump(out, open(os.path.join(b, "14_rb_frontier.json"), "w"), indent=1)
print(json.dumps(out, indent=1))
