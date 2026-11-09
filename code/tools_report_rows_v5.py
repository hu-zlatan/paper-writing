"""Report-only rows for stage 17 [v5] (no new runs; reads existing training logs).

(1) Amendment v5.1c: training-episode count of every time-guard-saved `rl_success` model (results/v5/rl/*rlsucc*.json,
    last logged history entry), to be printed next to every rl_success number.
(2) Amendment v5.0 E2: last-checkpoint sensitivity row for students -- held-out label regret R_bar of the kept
    (lowest-R_bar) checkpoint vs the last-epoch checkpoint, per cell / seed / round (results/v5/d5/<cell>_s<seed>_r<k>.json).
    This is the logged sensitivity quantity (R_bar on the held-out label shards); no success evaluation of last
    checkpoints exists and none is run.
Output: results/v5/16_report_rows.json.
"""
import glob
import json
import os
import re

here = os.path.dirname(os.path.abspath(__file__))
b = os.path.join(here, "..", "results", "v5")
out = {"provenance": "extracted unchanged from training logs; report-only, not a hypothesis test", "rl_success": {},
       "student_checkpoint_sensitivity": {}}
for p in sorted(glob.glob(os.path.join(b, "rl", "*_rlsucc_*.json"))):
    r = json.load(open(p))
    name = os.path.basename(p)[:-5]
    out["rl_success"][name] = {"status": r.get("status"), "episodes_trained": r["history"][-1]["episodes"],
                               "plateau_at": r.get("plateau_at"), "wall_s": r.get("wall_s")}
pat = re.compile(r"^(.+)_s(7\d\d)_r(\d)\.json$")
for p in sorted(glob.glob(os.path.join(b, "d5", "*.json"))):
    m = pat.match(os.path.basename(p))
    if not m:
        continue
    r = json.load(open(p))
    if "last_val" not in r:
        continue
    cell, seed, rnd = m.groups()
    row = {"keep": r.get("checkpoint"), "best_epoch": r.get("best_epoch"), "status": r.get("status"),
           "R_bar_kept": r["final_val"]["R_bar"], "R_bar_last": r["last_val"]["R_bar"],
           "n_val_decisions": r["final_val"]["n_decisions"]}
    row["R_bar_last_minus_kept"] = row["R_bar_last"] - row["R_bar_kept"]
    out["student_checkpoint_sensitivity"].setdefault(cell, {}).setdefault(seed, {})["r" + rnd] = row
json.dump(out, open(os.path.join(b, "16_report_rows.json"), "w"), indent=1)
for k, v in out["rl_success"].items():
    print(k, v["status"], v["episodes_trained"])
for c, s in out["student_checkpoint_sensitivity"].items():
    print(c, {seed: {r: (round(x["R_bar_kept"], 4), round(x["R_bar_last"], 4), x["best_epoch"]) for r, x in rr.items()}
              for seed, rr in s.items()})
