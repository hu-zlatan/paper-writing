"""Post-hoc, report-only checks requested by the stage-18 [v6] reviewers (NOT pre-registered; no decision).

Uses the frozen read-out's own loaders and statistics (analysis_v6.py, touchbed/stats.py) unchanged.
  P1  E12 grid shift with uncertainty: per episode 0-99, shift = (student - G*)_sub16 - (student - G*)_sub8, i.e.
      crossed bootstrap of A = S16 - S8 (episode x 5 student seeds) against B = G16 - G8 (episode x G* run 1);
      two-sided ci95, same scheme / n_boot / seed 0 as the read-out.
  P2  H6b bootstrap-seed sensitivity: the registered H6b family (5 cells x 2 reduced planners, Holm over 10) re-run
      with bootstrap seeds 0 (registered) .. 10; reports the number of Holm rejections per seed and per window.
  P3  DAgger checkpoint epochs (descriptive): best_epoch of the kept student checkpoints per round, read from
      results/v5/results_v5.json > 16_report_rows.json > student_checkpoint_sensitivity.
Writes results/v6/18_posthoc_v6.json.  usage: python analysis_v6_posthoc.py
"""
import json
import os
import sys

import numpy as np

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import analysis_v6 as A  # noqa: E402
from touchbed.stats import crossed_bootstrap_diff, holm  # noqa: E402


def two_sided_seed(X, Y, seed):
    r = crossed_bootstrap_diff(X, Y, n_boot=A.N_BOOT, alpha=A.ALPHA2, seed=seed)
    return {"diff": r["diff"], "ci95": [r["lower"], r["upper"]],
            "p_two_sided": min(1.0, 2 * min(r["p_greater"], r["p_less"]))}


def p1(c):
    tag = A.CELLS[c]; eps = list(A.E12_EPS)
    res = {}
    for m in ["gstar"] + A.STUDENTS:
        d = {}
        for dd in (os.path.join(A.R5, "e5"), os.path.join(A.R6, "e12")):
            d.update(A._load_dir(dd, tag, m + "_sub16"))
        res[m] = d
    t5 = {m: A.load("test5", tag, m) for m in ["gstar"] + A.STUDENTS}
    S8, G8 = A.col(t5, A.STUDENTS, "success", eps), A.col(t5, ["gstar"], "success", eps)
    S16, G16 = A.col(res, A.STUDENTS, "success", eps), A.col(res, ["gstar"], "success", eps)
    return two_sided_seed(S16 - S8, G16 - G8, 0)


def p2():
    out = {}
    recs = {}
    for c in A.CELLS:
        rec, _, _, _ = A.completeness(c, A.WINDOWS["0-499"])
        recs[c] = rec
    for win, eps in A.WINDOWS.items():
        eps = list(eps); per_seed = {}
        for seed in range(0, 11):
            names, ps = [], []
            for c in A.CELLS:
                S = A.col(recs[c], A.STUDENTS, "success", eps)
                for g in A.REDUCED:
                    names.append(f"{c}:{g}")
                    ps.append(two_sided_seed(S, A.col(recs[c], [g], "success", eps), seed)["p_two_sided"])
            rej = holm(ps)
            per_seed[str(seed)] = {"n_rejected": int(sum(rej)), "rejected": [n for n, r in zip(names, rej) if r],
                                   "p": dict(zip(names, ps))}
        out[win] = per_seed
    return out


def p3():
    r5 = json.load(open(os.path.join(A.R5, "results_v5.json")))
    return r5["16_report_rows.json"].get("student_checkpoint_sensitivity")


def main():
    res = {"note": "post hoc, report-only, not pre-registered (stage 18 [v6] reviewer requests); no decision",
           "P1_e12_shift_ci95": {c: p1(c) for c in A.CELLS},
           "P2_h6b_bootstrap_seed_sensitivity": p2(),
           "P3_checkpoint_epochs_source": "results_v5.json > 16_report_rows.json > student_checkpoint_sensitivity",
           "P3_checkpoint_epochs": p3()}
    p = os.path.join(A.R6, "18_posthoc_v6.json")
    json.dump(res, open(p, "w"), indent=1)
    for c, r in res["P1_e12_shift_ci95"].items():
        print("P1", c, round(r["diff"], 4), [round(x, 4) for x in r["ci95"]], r["p_two_sided"])
    for w, d in res["P2_h6b_bootstrap_seed_sensitivity"].items():
        print("P2", w, {s: v["n_rejected"] for s, v in d.items()})
    print("written", p)


if __name__ == "__main__":
    main()
