"""Provenance script for results/v2/12_g3_hp_selection.txt (amendment v3.0 C14 item 4).
Rule (amendment v2.0 B9): final validation ball-sPCE of the argmax policy = `val_ball_spce` of the last history entry
that has it, per results/v2/g3/hp*_S_k6.json; selected = highest (ties -> lower index). Writes the regenerated text to
results/v2/12_g3_hp_selection.regen.txt and a comparison record to results/v2/12_g3_provenance_hp.json (the original file
is not modified)."""
import glob
import json
import os

base = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "results", "v2")
rows = []
for f in sorted(glob.glob(os.path.join(base, "g3", "hp*_S_k6.json"))):
    d = json.load(open(f))
    v = [h["val_ball_spce"] for h in d["history"] if "val_ball_spce" in h]
    rows.append((os.path.basename(f), v[-1] if v else float("nan")))
best = max(range(len(rows)), key=lambda i: (rows[i][1], -i))
lines = [f"{n} {v:.3f}" for n, v in rows] + [f"selected: {rows[best][0].split('_')[0]} (B9: final validation ball-sPCE of "
                                              "the argmax policy)"]
regen = "\n".join(lines) + "\n"
open(os.path.join(base, "12_g3_hp_selection.regen.txt"), "w").write(regen)
orig_path = os.path.join(base, "12_g3_hp_selection.txt")
orig = open(orig_path).read() if os.path.exists(orig_path) else None
rec = {"original": orig, "regenerated": regen, "identical": orig == regen,
       "values": {n: v for n, v in rows}, "selected": rows[best][0]}
json.dump(rec, open(os.path.join(base, "12_g3_provenance_hp.json"), "w"), indent=1)
print(json.dumps({k: rec[k] for k in ("identical", "selected", "values")}, indent=1))
