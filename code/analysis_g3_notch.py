"""Provenance script for results/v2/12_g3_notch_analysis.json (amendment v3.0 C14 item 4).
G3 (iii) rule (07_hypotheses_v2): seed-mean exact value v_pi of the learned argmax policy on the exact notch control
>= 0.8 * v_opt. v_pi = `final.v_pi` of results/v2/g3/notch_spce_total{,_2x}_sd*.json (exact enumeration done by
touchbed/train_notch.py at the end of training); v_opt, v_greedy from touchbed.notch.two_step at the prior.
Writes results/v2/12_g3_notch_analysis.regen.json and a field-by-field comparison with the original to
results/v2/12_g3_provenance_notch.json (the original file is not modified)."""
import glob
import json
import os

import numpy as np

from touchbed import notch as N

base = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "results", "v2")
ex = N.two_step(N.prior_belief(), N._Tables())
runs = []
for f in sorted(glob.glob(os.path.join(base, "g3", "notch_spce_total*_sd*.json"))):
    d = json.load(open(f))
    fin = d["final"]
    runs.append({"file": os.path.basename(f), "episodes": d["episodes"], "v_pi": fin["v_pi"],
                 "frac_of_opt": fin["v_pi"] / ex["v_opt"], "horizontal_first": bool(fin["a1_is_horizontal"])})
out = {"exact_v_opt": ex["v_opt"], "exact_v_greedy": ex["v_greedy"], "rule": "seed-mean v_pi >= 0.8 * v_opt",
       "runs": runs}
for tag in ("notch_spce_total_2x", "notch_spce_total"):
    v = [r["v_pi"] for r in runs if r["file"].startswith(tag + "_sd")]
    if v:
        out[f"{tag}_seed_mean"] = float(np.mean(v))
key = "notch_spce_total_2x_seed_mean" if "notch_spce_total_2x_seed_mean" in out else "notch_spce_total_seed_mean"
out["passes"] = bool(out[key] >= 0.8 * ex["v_opt"])
json.dump(out, open(os.path.join(base, "12_g3_notch_analysis.regen.json"), "w"), indent=1)

orig_path = os.path.join(base, "12_g3_notch_analysis.json")
orig = json.load(open(orig_path))


def same(a, b):
    if isinstance(a, float) or isinstance(b, float):
        return abs(float(a) - float(b)) <= 1e-12 * max(1.0, abs(float(a)))
    if isinstance(a, dict) and isinstance(b, dict):
        return a.keys() == b.keys() and all(same(a[k], b[k]) for k in a)
    if isinstance(a, list) and isinstance(b, list):
        return len(a) == len(b) and all(same(x, y) for x, y in zip(a, b))
    return a == b


diff = {k: {"original": orig.get(k), "regenerated": out.get(k)} for k in set(orig) | set(out)
        if not same(orig.get(k), out.get(k))}
# The 1x and 2x runs of each seed report identical v_pi and the same first action per seed (sd100: 20, sd101: 17,
# sd102: 18): the exact value of the final deterministic argmax policy is the same after 1x and 2x training. Recorded
# (with the first actions) so it is not read as a copy error; whether the full policies coincide is not checked here.
same_policy = {r["file"]: [r["v_pi"], json.load(open(os.path.join(base, "g3", r["file"])))["final"]["a1"]] for r in runs}
rec = {"identical": not diff, "differences": diff, "note_identical_1x_2x_values": same_policy}
json.dump(rec, open(os.path.join(base, "12_g3_provenance_notch.json"), "w"), indent=1)
print(json.dumps({"identical": rec["identical"], "differences": list(diff)}, indent=1))
