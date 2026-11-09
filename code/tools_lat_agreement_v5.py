"""Report-only (stage 19 [v5], prompted by stage-18 pass-2 review): first-choice action agreement with full G*
(g2000_512_64) on the E6 job-1 latency records (same pilot3 decision states, results/v5/lat/<tag>_s701_gstar[_d1000].jsonl,
the same file analysis_e6_v5.py reads). Agreement = fraction of timed decisions where a method's recorded action equals
full G*'s. Not pre-registered, no CI, no test. Writes results/v5/19_lat_agreement.json."""
import json
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from analysis_e6_v5 import CELLS, ROOT, rows  # noqa: E402

out = {"provenance": "report-only; agreement of recorded actions with g2000_512_64 on E6 job-1 states; no CI", "cells": {}}
for c, tag in CELLS.items():
    p = os.path.join(ROOT, "lat", f"{tag}_s701_gstar_d1000.jsonl")
    if not os.path.exists(p):
        p = os.path.join(ROOT, "lat", f"{tag}_s701_gstar.jsonl")
    recs, _ = rows(p)
    ref = [r["actions"]["g2000_512_64"] for r in recs]
    res = {"source": os.path.basename(p), "n_decisions": len(recs)}
    for m in ("student", "g125_512_16", "g500_512_4"):
        res[m] = sum(r["actions"][m] == a for r, a in zip(recs, ref)) / len(recs)
    out["cells"][c] = res
json.dump(out, open(os.path.join(ROOT, "19_lat_agreement.json"), "w"), indent=1)
for c, v in out["cells"].items():
    print(c, v["n_decisions"], {k: round(v[k], 3) for k in ("student", "g125_512_16", "g500_512_4")})
