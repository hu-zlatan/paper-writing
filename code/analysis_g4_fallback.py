"""Gate G4 pre-registered fallback (docs/07_hypotheses_v2.md §4): 32k particles with 10 MH steps per move vs the
reference 32k x 30 MH steps on the same pilot episodes, same pass rule as G4. Also compares the 10-MH and 3-MH (G4)
32k runs with the 128k x 3-MH reference where the episodes overlap. Writes results/v2/12_g4_fallback_analysis.json."""
import glob
import json
import os
import sys

import numpy as np

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from touchbed.stats import crossed_bootstrap_diff  # noqa: E402

base = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "results", "v2")
rows = {}
for sub in ("g4", "g4_fallback"):
    for f in glob.glob(os.path.join(base, sub, "*.jsonl")):
        for line in open(f):
            r = json.loads(line)
            if "episode" in r:
                rows[(r["set"], r["kappa"], r["method"], r["n_eval"], r.get("mh_steps", 3), r["episode"])] = r


def compare(s, k, m, ref, cand):
    eps = sorted(e for (s2, k2, m2, n, mh, e) in rows if (s2, k2, m2, n, mh) == (s, k, m) + cand
                 and (s, k, m) + ref + (e,) in rows)
    if not eps:
        return None
    res = {"n_episodes": len(eps), "reference": list(ref), "candidate": list(cand)}
    for metric in ("success", "ball_info", "identity_ok"):
        a = np.array([float(rows[(s, k, m) + ref + (e,)][metric]) for e in eps])
        b = np.array([float(rows[(s, k, m) + cand + (e,)][metric]) for e in eps])
        bs = crossed_bootstrap_diff(a, b, n_boot=4000, seed=1, alpha=0.025)
        res[metric] = {"mean_candidate": float(b.mean()), "mean_reference": float(a.mean()),
                       "diff_ref_minus_cand": bs["diff"], "ci95": [bs["lower"], bs["upper"]]}
    res["passes_G4_rule"] = bool(abs(res["ball_info"]["diff_ref_minus_cand"]) <= 0.05
                                 and abs(res["success"]["diff_ref_minus_cand"]) <= 0.01
                                 and res["success"]["ci95"][0] >= -0.02 and res["success"]["ci95"][1] <= 0.02)
    return res


out = {}
for s in ("A", "S"):
    for k in (0.0,):
        for m in ("random",):
            for name, ref, cand in (("fallback_10mh_vs_30mh", (32000, 30), (32000, 10)),
                                    ("10mh_vs_128k3mh", (128000, 3), (32000, 10)),
                                    ("30mh_vs_128k3mh", (128000, 3), (32000, 30)),
                                    ("3mh_vs_10mh_32k", (32000, 10), (32000, 3))):
                r = compare(s, k, m, ref, cand)
                if r is None:
                    continue
                out[f"{s}_k{k:g}_{m}_{name}"] = r
                print(s, k, m, name, r["n_episodes"],
                      {mm: (round(v["mean_candidate"], 3), round(v["mean_reference"], 3), [round(x, 3) for x in v["ci95"]])
                       for mm, v in r.items() if isinstance(v, dict)}, "PASS" if r["passes_G4_rule"] else "FAIL")
json.dump(out, open(os.path.join(base, "12_g4_fallback_analysis.json"), "w"), indent=1)
