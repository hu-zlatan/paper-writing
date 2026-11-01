"""Report-only checks for the second stage-18 v4 pass (no test, no gate):
(1) S2 student training curves (results/v4/d4/S_k2_s60x_r{0,1,2}.json): per round, epoch of the lowest held-out R-bar,
    that minimum, the kept epoch-200 value and the rise, and whether the training loss still falls over the last 20 epochs.
(2) S12 G* fraction of between-probe moves of zero phi grid steps on test3 0-299 (v3 14_behaviour uses 0-499).
Writes results/v4/14_review2_checks.json."""
import glob
import json
import os

import numpy as np

here = os.path.dirname(os.path.abspath(__file__))
r4 = os.path.join(here, "..", "results", "v4")
r3 = os.path.join(here, "..", "results", "v3")
out = {"note": "report-only (stage 18 v4 pass 2)", "students_S2_curves": {}}
for s in (601, 602, 603):
    for k in (0, 1, 2):
        m = json.load(open(os.path.join(r4, "d4", f"S_k2_s{s}_r{k}.json")))
        lg = m["log"]
        v = np.array([x["val_R_bar"] for x in lg])
        tl = np.array([x["train_loss"] for x in lg])
        i = int(np.argmin(v))
        out["students_S2_curves"][f"s{s}_r{k}"] = {
            "n_epochs_logged": len(lg), "best_epoch": int(lg[i]["epoch"]), "best_val_R_bar": float(v[i]),
            "final_val_R_bar": float(m["final_val"]["R_bar"]), "rise_to_final": float(m["final_val"]["R_bar"] - v[i]),
            "train_loss_last": float(tl[-1]), "train_loss_minus20": float(tl[-21]),
            "train_loss_falling_last20": bool(tl[-1] < tl[-21])}
c = out["students_S2_curves"].values()
out["students_S2_curves_summary"] = {"best_epoch_range": [min(x["best_epoch"] for x in c), max(x["best_epoch"] for x in c)],
                                     "rise_range": [min(x["rise_to_final"] for x in c), max(x["rise_to_final"] for x in c)],
                                     "all_train_loss_falling_last20": all(x["train_loss_falling_last20"] for x in c)}
N_PHI, N_PSI = 64, 8
rows = {}
for f in sorted(glob.glob(os.path.join(r3, "test3", "S_k12_gstar_*.jsonl"))):
    for line in open(f):
        d = json.loads(line)
        if "episode" in d and "header" not in d and "actions" in d and d["episode"] < 300:
            rows[d["episode"]] = d
mv = []
for e in sorted(rows):
    idx = [a // N_PSI for a in rows[e]["actions"]]
    for i in range(1, len(idx)):
        dd = abs(idx[i] - idx[i - 1]) % N_PHI
        mv.append(min(dd, N_PHI - dd))
out["S12_gstar_test3_0_299"] = {"n_episodes": len(rows), "n_between_probe_moves": len(mv),
                                "frac_between_probe_moves_eq_0": float(np.mean(np.array(mv) == 0))}
json.dump(out, open(os.path.join(r4, "14_review2_checks.json"), "w"), indent=1)
print(json.dumps(out["students_S2_curves_summary"]), json.dumps(out["S12_gstar_test3_0_299"]))
