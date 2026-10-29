"""Derived descriptives quoted in the paper (stage 17 v3): per-seed spreads (H2, M4) and the RL-sweep selection margin.
Pure arithmetic on existing analysis outputs; writes results/v3/14_derived.json. Nothing here is a test."""
import json
import os
import statistics as st

b = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "results", "v3")
h2 = json.load(open(os.path.join(b, "14_h2_analysis.json")))
m4 = json.load(open(os.path.join(b, "14_m4_analysis.json")))
rl = json.load(open(os.path.join(b, "12_rl_sweep_selection.json")))
out = {}
for k in ("student", "rl"):
    v = list(h2[f"per_seed_{k}"].values())
    out[f"h2_gT_per_seed_{k}"] = {"sd": st.stdev(v), "range": max(v) - min(v)}
out["h2_gT_sd_ratio_rl_over_student"] = out["h2_gT_per_seed_rl"]["sd"] / out["h2_gT_per_seed_student"]["sd"]
out["h2_gT_range_ratio_rl_over_student"] = out["h2_gT_per_seed_rl"]["range"] / out["h2_gT_per_seed_student"]["range"]
for k in ("student", "rl"):
    v = m4["rows"][k]["per_seed_success"]
    out[f"m4_success_range_{k}"] = max(v) - min(v)
vals = sorted(r["final_val_ball_spce"] for r in rl["rows"])
out["rl_sweep_margin_best_minus_second"] = vals[-1] - vals[-2]
json.dump(out, open(os.path.join(b, "14_derived.json"), "w"), indent=1)
print(json.dumps(out, indent=1))
