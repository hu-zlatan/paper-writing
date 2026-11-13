"""Derived (report-only) v6 values requested by stage 15 [v6] §4.1, from results/v6/14_v6_analysis.json only.

Arithmetic on existing fields: NOT pre-registered, no CI. Writes results/v6/15_derived_v6.json.
- student mean = mean of the 5 student seeds' success; r0 mean likewise; RL mean over rl_s71x.
- strongest non-oracle comparator per cell = max success among heuristics (b_fan, b_spread, b_cov), reduced planners
  (g125_512_16, g500_512_4) and RL seeds' mean; margin = student mean - that value.
- best-heuristic margin = student mean - max heuristic success.
- latency ratios = latency_median_s ratios from the 'frontier' block (v5 E6 job-1 point medians, no dispersion).
"""
import json, os
import numpy as np

HERE = os.path.dirname(os.path.abspath(__file__))
R6 = os.path.join(HERE, "..", "results", "v6")
d = json.load(open(os.path.join(R6, "14_v6_analysis.json")))
out = {"note": "derived arithmetic on results/v6/14_v6_analysis.json; not pre-registered; no CI", "cells": {}}
for c, cd in d["cells"].items():
    row = {}
    for w in ("0-499", "300-499"):
        m = cd[w]["means"]
        mean = lambda pre: float(np.mean([v["success"] for k, v in m.items() if k.startswith(pre)]))
        stu, r0 = mean("student_s"), mean("r0student_s")
        rl = mean("rl_s") if any(k.startswith("rl_s") for k in m) else None
        heur = {k: m[k]["success"] for k in ("b_fan", "b_spread", "b_cov") if k in m}
        comps = dict(heur)
        for k in ("g125_512_16", "g500_512_4"):
            if k in m:
                comps[k] = m[k]["success"]
        if rl is not None:
            comps["rl_mean"] = rl
        best_c = max(comps, key=comps.get); best_h = max(heur, key=heur.get)
        row[w] = {"student_mean": stu, "r0student_mean": r0, "rl_mean": rl,
                  "gstar_run1": m["gstar"]["success"], "gstar_run2": m.get("gstar2", {}).get("success"),
                  "strongest_non_oracle": best_c, "strongest_value": comps[best_c],
                  "margin_vs_strongest": stu - comps[best_c],
                  "best_heuristic": best_h, "registered_H_star": cd[w]["v5_row_updates"]["H_star"],
                  "margin_vs_best_heuristic": stu - heur[best_h]}
    lat = cd["frontier"]["latency_median_s"]
    row["latency_ratio"] = {f"{k}_over_student": lat[k] / lat["student"] for k in lat if k != "student"}
    out["cells"][c] = row
p = os.path.join(R6, "15_derived_v6.json"); json.dump(out, open(p, "w"), indent=1); print("written", p)
for c, r in out["cells"].items():
    a = r["0-499"]
    print(c, round(a["student_mean"], 4), a["strongest_non_oracle"], round(a["strongest_value"], 4),
          f"{100*a['margin_vs_strongest']:+.2f}pp", a["best_heuristic"], a["registered_H_star"],
          f"{100*a['margin_vs_best_heuristic']:+.2f}pp",
          {k: round(v) for k, v in r["latency_ratio"].items()})
