"""v5 E5 evaluator check (amendment v5.0 E5): sub-8 -> sub-16 re-read of test5 0-199, G* and student 701, S2 / S12
(regrid3 outputs results/v5/e5/<tag>_<method>_sub16_*.jsonl; tools_v5_e5.py). Per (cell, method): success flip rate
(share of episodes whose success differs between the sub-8 record and the sub-16 re-read, with the direction counts),
mean |Delta BI| and mean Delta BI (sub 16 - sub 8), and the success means at both settings; plus, per cell, the change
of the student - G* success contrast (sub 16 minus sub 8) on the same episodes. Report-only: every test5 success
contrast is printed next to the measured flip rate. Complete iff all 200 episodes of every row are present.
Writes results/v5/14_e5_analysis.json."""
import glob
import json
import os

import numpy as np

ROOT = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "results", "v5")
ROWS = {"S2": "S_k2", "S12": "S_k12"}
METHODS, N = ("gstar", "student_s701"), 200


def load(tag, m):
    d = {}
    for f in glob.glob(os.path.join(ROOT, "e5", f"{tag}_{m}_sub16_*.jsonl")):
        for line in open(f):
            r = json.loads(line)
            if "episode" in r and "header" not in r and "success" in r:
                d[r["episode"]] = r
    return d


def main():
    out = {}
    for c, tag in ROWS.items():
        rows = {m: load(tag, m) for m in METHODS}
        res = {"n_episodes": {m: len(v) for m, v in rows.items()}}
        res["complete"] = all(all(e in rows[m] for e in range(N)) for m in METHODS)
        if res["complete"]:
            for m in METHODS:
                r = [rows[m][e] for e in range(N)]
                s8 = np.array([bool(x["orig_success"]) for x in r]); s16 = np.array([bool(x["success"]) for x in r])
                b8 = np.array([x["orig_ball_info"] for x in r], float); b16 = np.array([x["ball_info"] for x in r], float)
                res[m] = {"flip_rate": float(np.mean(s8 != s16)), "flips_8to16_gain": int(np.sum(~s8 & s16)),
                          "flips_8to16_loss": int(np.sum(s8 & ~s16)), "success_sub8": float(s8.mean()),
                          "success_sub16": float(s16.mean()), "mean_abs_dBI": float(np.mean(np.abs(b16 - b8))),
                          "mean_dBI": float(np.mean(b16 - b8))}
            res["contrast_change_student_minus_gstar"] = (
                (res["student_s701"]["success_sub16"] - res["gstar"]["success_sub16"])
                - (res["student_s701"]["success_sub8"] - res["gstar"]["success_sub8"]))
        out[c] = res
    json.dump(out, open(os.path.join(ROOT, "14_e5_analysis.json"), "w"), indent=1)
    print({c: (r["n_episodes"], r["complete"]) for c, r in out.items()})


if __name__ == "__main__":
    main()
