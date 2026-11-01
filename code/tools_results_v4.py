"""Collect every v4 analysis JSON unchanged into results/v4/results_v4.json (input of stage 14 v4), plus the round-wise
held-out R-bar of the S2 students (from results/v4/d4/S_k2_s<seed>_r<k>.json). v3 numbers stay in results/v3/results_v3.json."""
import json
import os

here = os.path.dirname(os.path.abspath(__file__))
b = os.path.join(here, "..", "results", "v4")
out = {"note": "v4 (docs/07c_amendment_v4_0.md); every block is the unchanged content of the named file"}
for name in ("12_d4_analysis.json", "14_s2_analysis.json", "14_e5_analysis.json", "14_travel_split.json"):
    p = os.path.join(b, name)
    out[name] = json.load(open(p)) if os.path.exists(p) else None
rb = {}
for s in (601, 602, 603):
    for k in (0, 1, 2):
        p = os.path.join(b, "d4", f"S_k2_s{s}_r{k}.json")
        if os.path.exists(p):
            m = json.load(open(p))
            rb[f"s{s}_r{k}"] = {"val_R_bar": m["final_val"]["R_bar"], "n_train_episodes": m["n_train_episodes"],
                                "n_train_decisions": m["n_train_decisions"], "status": m["status"]}
out["students_S2_training"] = rb
json.dump(out, open(os.path.join(b, "results_v4.json"), "w"), indent=1)
print(json.dumps({k: (v is not None) for k, v in out.items() if k.endswith(".json")}))
