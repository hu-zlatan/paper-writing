"""Stage 15 [v5] decision section 4.1 task 1: post-hoc derived values, arithmetic on existing fields only.

Not pre-registered, no CI, no new test. Inputs: results/v5/14_test5_analysis.json, results/v5/14_e6_analysis.json.
Output: results/v5/15_posthoc_derived.json (collected into results_v5.json by tools_results_v5.py).
"""
import json
import os

here = os.path.dirname(os.path.abspath(__file__))
b = os.path.join(here, "..", "results", "v5")
t5 = json.load(open(os.path.join(b, "14_test5_analysis.json")))
e6 = json.load(open(os.path.join(b, "14_e6_analysis.json")))
CELLS = ["S2", "S4", "S8", "S12", "A16-2"]
HEUR = ["b_fan", "b_spread", "b_cov"]

out = {"provenance": "arithmetic on existing fields of 14_test5_analysis.json / 14_e6_analysis.json; "
                     "post hoc, not pre-registered, no CI, no test (results/v5/15_decision.md section 4.1)",
       "cells": {}}
for c in CELLS:
    m = t5[c]["means"]
    sd = t5[c]["student_minus_gstar"]["success"]["diff"]
    student_from_diff = m["gstar"]["success"] + sd
    student_seeds = [m[k]["success"] for k in m if k.startswith("student_s")]
    rl_seeds = {k: m[k]["success"] for k in m if k.startswith("rl_s")}
    rl_from_diff = student_from_diff - t5[c]["student_minus_rl"]["success"]["diff"]
    heur = {h: m[h]["success"] for h in HEUR}
    best_h = max(heur, key=heur.get)
    out["cells"][c] = {
        "student_success_mean_from_diff": student_from_diff,
        "student_success_mean_of_listed_seed_means": sum(student_seeds) / len(student_seeds),
        "rl_success_mean_from_diff": rl_from_diff,
        "rl_seed_means_listed": rl_seeds,
        "heuristic_success": heur,
        "H_star_preregistered": t5[c]["H_star"],
        "best_test5_heuristic": best_h,
        "margin_student_minus_best_test5_heuristic": student_from_diff - heur[best_h],
        "margin_student_minus_H_star": t5[c]["student_minus_hstar"]["success"]["diff"],
    }
    j1 = e6[c]["job1"]
    full = j1["g2000_512_64"]["median"]
    j2 = {s: v["median"] for s, v in e6[c].get("job2", {}).items()}
    out["cells"][c]["latency"] = {
        "ratio_full_gstar_over_student_s701_median": j1["ratio_full_gstar_over_student"]["median"],
        "ratio_full_gstar_median_over_job2_student_medians": {s: full / v for s, v in j2.items()},
        "note": "ratio of medians, not paired; job-2 students timed in a different job",
    }

h = t5["H5b"]
tr = h["gstar_mean_travel_rad"]
span = max(tr) - min(tr)
out["H5b_span_translation"] = {
    "travel_span_rad": [min(tr), max(tr)],
    "span_rad": span,
    "slope_times_span": h["slope_per_rad"] * span,
    "ci95_times_span": [x * span for x in h["ci95_per_rad"]],
}
json.dump(out, open(os.path.join(b, "15_posthoc_derived.json"), "w"), indent=1)
for c, v in out["cells"].items():
    print(c, round(v["student_success_mean_from_diff"], 4), v["best_test5_heuristic"],
          round(100 * v["margin_student_minus_best_test5_heuristic"], 2), "pp",
          {s: round(r) for s, r in v["latency"]["ratio_full_gstar_median_over_job2_student_medians"].items()})
print(out["H5b_span_translation"])
