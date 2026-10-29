"""Label-fit diagnosis (07_hypotheses_v3 §3.3, encoder sentence): for every final (round-2) student, training-set and
held-out R-bar (floored normalised regret, distill.mean_regret) and top-1 agreement with the teacher's action.
under-fit := training-set R-bar > 0.25 or training top-1 agreement < 0.50 at the end of round 2.
Writes results/v3/14_labelfit.json."""
import glob
import json
import os
import sys

import numpy as np

here = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, here)
os.environ.setdefault("TOUCHBED_NPHI", "64")
from touchbed.cli3 import load_student  # noqa: E402
from touchbed.distill import decision_logits, load_shards, mean_regret  # noqa: E402

base = os.path.join(here, "..", "results", "v3")


def top1(st, D, chunk=256):
    hit, n = 0, 0
    for c in range(0, len(D["valid"]), chunk):
        j = np.arange(c, min(c + chunk, len(D["valid"])))
        out, _ = decision_logits(st, D, j)
        a = np.argmax(np.where(D["MASK"][j], out, -np.inf), axis=-1)
        V = D["valid"][j]
        hit += int(((a == D["AT"][j]) & V).sum()); n += int(V.sum())
    return hit / max(n, 1)


groups = {"first_attempt": "d3/S_k12_hp0_s50?_r2.json", "remedy": "d3rem/S_k12_hp0_s50?_r2.json",
          "belief_input": "d3b/S_k12_belief_hp0_s52?_r2.json"}
out = {"rule": "under-fit := train R_bar > 0.25 or train top-1 < 0.50 (end of round 2)", "groups": {}}
for g, pat in groups.items():
    rows = []
    for f in sorted(glob.glob(os.path.join(base, pat))):
        meta = json.load(open(f))
        st, _ = load_student(f.replace(".json", ".npz"))
        cwd = os.getcwd(); os.chdir(here)
        D, V = load_shards(meta["shards"]), load_shards(meta["val_shards"])
        os.chdir(cwd)
        tr, va = mean_regret(st, D), mean_regret(st, V)
        rows.append({"student": os.path.basename(f)[:-5], "train_R_bar": tr["R_bar"], "train_top1": top1(st, D),
                     "train_decisions": tr["n_decisions"], "heldout_R_bar": va["R_bar"], "heldout_top1": top1(st, V),
                     "under_fit": bool(tr["R_bar"] > 0.25 or top1(st, D) < 0.50)})
    out["groups"][g] = rows
print(json.dumps(out, indent=1))
json.dump(out, open(os.path.join(base, "14_labelfit.json"), "w"), indent=1)
