"""H2 (07_hypotheses_v3 §2.2, 08 plan v3 claim H2): on the first 500 S12 test3 episodes with the same per-episode
contrastive draws (L = 4095, J = 16), one-sided 95% crossed-bootstrap LB of g_T(student, seeds 501-503) -
g_T(RL-relative, seeds 511-513) > +0.10 nats. Inputs: gt3 outputs results/v3/h2/S_k12_<method>_s<seed>*.jsonl.
Usage: python analysis_h2_v3.py [--student-tag rem] [--n 500]. Writes results/v3/14_h2_analysis.json."""
import glob
import json
import os
import sys

import numpy as np

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from touchbed.stats import crossed_bootstrap_diff  # noqa: E402

base = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "results", "v3")
tag = sys.argv[sys.argv.index("--student-tag") + 1] if "--student-tag" in sys.argv else "rem"
n_ep = int(sys.argv[sys.argv.index("--n") + 1]) if "--n" in sys.argv else 500


def load(pat):
    d = {}
    for f in glob.glob(os.path.join(base, "h2", pat)):
        for line in open(f):
            r = json.loads(line)
            if "episode" in r:
                d[r["episode"]] = r["g_T"]
    return d


st = {s: load(f"S_k12_student_{tag}_s{s}*.jsonl") for s in (501, 502, 503)}
rl = {s: load(f"S_k12_rl_s{s}*.jsonl") for s in (511, 512, 513)}
eps = [e for e in range(n_ep) if all(e in d for d in list(st.values()) + list(rl.values()))]
out = {"student_tag": tag, "n_episodes": len(eps), "complete": len(eps) == n_ep, "threshold_nats": 0.10}
if eps:
    A = np.array([[st[s][e] for s in st] for e in eps])
    B = np.array([[rl[s][e] for s in rl] for e in eps])
    r = crossed_bootstrap_diff(A, B)
    out.update({"student_mean": float(A.mean()), "rl_mean": float(B.mean()), "bootstrap": r,
                "per_seed_student": {str(s): float(A[:, i].mean()) for i, s in enumerate(st)},
                "per_seed_rl": {str(s): float(B[:, i].mean()) for i, s in enumerate(rl)},
                "passes": bool(r["lower"] > 0.10)})
print(json.dumps(out, indent=1))
json.dump(out, open(os.path.join(base, "14_h2_analysis.json"), "w"), indent=1)
