"""Collect every v5 analysis JSON unchanged into results/v5/results_v5.json (input of stage 14 v5). Earlier versions'
numbers stay in results/v<N>/results_v<N>.json."""
import json
import os

here = os.path.dirname(os.path.abspath(__file__))
b = os.path.join(here, "..", "results", "v5")
out = {"note": "v5 (docs/07c_amendment_v5_0.md + addenda v5.1*); every block is the unchanged content of the named file"}
for name in ("12_rl_sweep_selection.json", "12_cal_analysis.json", "12_e7_analysis.json", "12_base_hstar.json",
             "12_d5_analysis.json", "13_freeze.json", "14_test5_analysis.json", "14_e5_analysis.json",
             "14_e6_analysis.json", "15_posthoc_derived.json", "16_report_rows.json"):
    p = os.path.join(b, name)
    out[name] = json.load(open(p)) if os.path.exists(p) else None
json.dump(out, open(os.path.join(b, "results_v5.json"), "w"), indent=1)
print({k: v is not None for k, v in out.items() if k != "note"})
