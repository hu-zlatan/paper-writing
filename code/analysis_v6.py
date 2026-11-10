"""v6 read-out (docs/07c_amendment_v6_0.md 'Decision rules' + addendum v6.1). Written and committed before any E8-E12
record was read (2026-11-10).

Inputs (sub-8 eval3 records on split test5):
  results/v5/test5/<tag>_<m>_<start>.jsonl   episodes 0-299 (v5), m in gstar, b_fan, b_spread, b_cov, student_s70x,
                                             rl_s71x, rlsucc_s71x (S2/S12)
  results/v6/test5/<tag>_<m>_<start>.jsonl   E8: the same methods on 300-499;  E9: g125_512_16, g500_512_4 on 0-499;
                                             E10: gstar2 (eval3 --run-salt r1) on 0-499;  E11: r0student_s70x on 0-499
  results/v5/test5_gt/, results/v6/test5_gt/ g_T (gt3, J 16, L 4095) of the same records
  results/v5/e5/, results/v6/e12/            regrid3 --sub 16 re-reads (E12, episodes 0-99)
  results/v5/12_base_hstar.json              H* per cell (pilot3; unchanged)
  results/v5/lat/ via results/v5/14_e6_analysis.json   E6 job-1 median latencies (frontier; no new timing)
Rules (amendment v6.0), each on WINDOWS = {"0-499" (primary), "300-499" (fresh check)}:
  H6a  student(5 seeds) - G*(runs 1 + 2 as two seeds), success and BI: two-sided ci95 (Holm over 5 cells, success);
       TOST at delta 0.04: p_TOST = max(p of 'diff <= -delta', p of 'diff >= +delta') from the crossed bootstrap of the
       difference; Holm over 5 cells; "equivalent within 4 pp" only where Holm rejects.
  H6b  student - g125_512_16 and student - g500_512_4 success, two-sided ci95, Holm over the 10 contrasts.
  H6c  student r2 - student r0 success (5 seeds each), two-sided ci95, Holm over 5 cells.
  E12  sub-8 -> sub-16 success flip rates (G* run 1, each student seed) and student - G* success on 0-99 at sub 8 and
       sub 16 (ci95), report-only.
  Report-only v6 updates of v5 rows on 0-499: student - H*, student - RL, student - rl_success (S2/S12), H2-v5 g_T
  contrasts + inversion (v5 code path), H5b slope (v5 rule, G* = run 1 as registered in v5).
  First-decision agreement of G* run 2 with run 1 (actions[0], same state), report-only.
A window is analysed only when every method it needs has every episode (nothing is selected).
usage: python analysis_v6.py [--check]     --check prints completeness only (no outcome numbers).
Writes results/v6/14_v6_analysis.json."""
import glob
import json
import os
import sys

import numpy as np

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
from touchbed.stats import crossed_bootstrap_diff, holm  # noqa: E402

R5 = os.environ.get("V5_RESULTS", os.path.join(HERE, "..", "results", "v5"))
R6 = os.environ.get("V6_RESULTS", os.path.join(HERE, "..", "results", "v6"))
CELLS = {"S2": "S_k2", "S4": "S_k4", "S8": "S_k8", "S12": "S_k12", "A16-2": "A16_k2"}
SEEDS_S, SEEDS_R = range(701, 706), range(711, 716)
STUDENTS = [f"student_s{s}" for s in SEEDS_S]
R0 = [f"r0student_s{s}" for s in SEEDS_S]
RLS = [f"rl_s{s}" for s in SEEDS_R]
RLSUCC = [f"rlsucc_s{s}" for s in SEEDS_R]
HEUR = ["b_fan", "b_spread", "b_cov"]
REDUCED = ["g125_512_16", "g500_512_4"]
WINDOWS = {"0-499": range(0, 500), "300-499": range(300, 500)}
DELTA, ALPHA2, N_BOOT = 0.04, 0.025, 10000
E12_EPS = range(0, 100)


def _load_dir(d, tag, m):
    out = {}
    for f in glob.glob(os.path.join(d, f"{tag}_{m}_*.jsonl")):
        for line in open(f):
            r = json.loads(line)
            if "episode" in r and "header" not in r:
                out[r["episode"]] = r
    return out


def load(kind, tag, m):
    """kind 'test5' or 'test5_gt': v5 records (0-299) merged with v6 records; v6 wins only where v5 has none."""
    d = _load_dir(os.path.join(R6, kind), tag, m)
    d.update({e: r for e, r in _load_dir(os.path.join(R5, kind), tag, m).items() if e < 300})
    return d


def methods(c):
    return ["gstar", "gstar2"] + HEUR + STUDENTS + R0 + RLS + REDUCED + (RLSUCC if c in ("S2", "S12") else [])


def gt_methods(c):
    return ["gstar"] + STUDENTS + RLS + (RLSUCC if c in ("S2", "S12") else [])


def col(recs, names, key, eps):
    return np.array([[float(recs[n][e][key]) for n in names] for e in eps])


def two_sided(A, B):
    r = crossed_bootstrap_diff(A, B, n_boot=N_BOOT, alpha=ALPHA2)
    return {"diff": r["diff"], "ci95": [r["lower"], r["upper"]],
            "p_two_sided": min(1.0, 2 * min(r["p_greater"], r["p_less"])), "n_episodes": r["n_episodes"],
            "n_seeds": r["n_seeds"]}


def tost(A, B, delta=DELTA):
    """Bootstrap TOST: p_lo = P*(diff <= -delta), p_hi = P*(diff >= +delta) over the crossed-bootstrap replicates of
    the difference (same scheme and seed as crossed_bootstrap_diff, with the replicates shifted by the margin)."""
    lo = crossed_bootstrap_diff(A, B - delta, n_boot=N_BOOT, alpha=0.05)      # replicates of diff + delta
    hi = crossed_bootstrap_diff(A, B + delta, n_boot=N_BOOT, alpha=0.05)      # replicates of diff - delta
    p_lo, p_hi = lo["p_greater"], hi["p_less"]                                  # P*(diff+delta <= 0), P*(diff-delta >= 0)
    return {"delta": delta, "p_lower_margin": p_lo, "p_upper_margin": p_hi, "p_tost": max(p_lo, p_hi),
            "ci90": [lo["lower"] - delta, hi["upper"] + delta]}


def completeness(c, eps):
    tag = CELLS[c]
    rec = {m: load("test5", tag, m) for m in methods(c)}
    gt = {m: load("test5_gt", tag, m) for m in gt_methods(c)}
    have = {m: sum(e in rec[m] for e in eps) for m in rec}
    have_gt = {m: sum(e in gt[m] for e in eps) for m in gt}
    return rec, gt, have, have_gt


def window_result(c, win, eps, hstar):
    rec, gt, have, have_gt = completeness(c, eps)
    n = len(eps)
    out = {"window": win, "n_required": n, "episodes_per_method": have, "complete": all(v == n for v in have.values()),
           "gt_episodes_per_method": have_gt, "gt_complete": all(v == n for v in have_gt.values())}
    if not out["complete"]:
        return out, None
    eps = list(eps)
    out["means"] = {m: {k: float(np.mean([float(rec[m][e][k]) for e in eps])) for k in ("success", "ball_info",
                                                                                         "travel_rad", "n_probes")}
                    for m in rec}
    X = lambda names, k: col(rec, names, k, eps)
    S = {k: X(STUDENTS, k) for k in ("success", "ball_info")}
    G2 = {k: X(["gstar", "gstar2"], k) for k in ("success", "ball_info")}
    out["H6a"] = {"success": two_sided(S["success"], G2["success"]) | {"tost": tost(S["success"], G2["success"])},
                  "ball_info": two_sided(S["ball_info"], G2["ball_info"]),
                  "gstar_run2_minus_run1_success": two_sided(X(["gstar2"], "success"), X(["gstar"], "success"))}
    out["H6b"] = {g: two_sided(S["success"], X([g], "success")) for g in REDUCED}
    out["H6c"] = {"success": two_sided(S["success"], X(R0, "success")),
                  "ball_info": two_sided(S["ball_info"], X(R0, "ball_info"))}
    h = hstar["cells"][c]["H_star"]
    upd = {"H_star": h, "student_minus_hstar_success": two_sided(S["success"], X([h], "success")),
           "student_minus_gstar_run1_success": two_sided(S["success"], X(["gstar"], "success")),
           "student_minus_rl_success": two_sided(S["success"], X(RLS, "success"))}
    if c in ("S2", "S12"):
        upd["student_minus_rlsucc_success"] = two_sided(S["success"], X(RLSUCC, "success"))
    if out["gt_complete"]:
        gS, gR, gG = col(gt, STUDENTS, "g_T", eps), col(gt, RLS, "g_T", eps), col(gt, ["gstar"], "g_T", eps)
        lb = crossed_bootstrap_diff(gS, gR, n_boot=N_BOOT, alpha=0.05)
        inv_g = two_sided(gR, gS)
        upd["H2_v5_update"] = {"student_minus_rl_gT": {"diff": lb["diff"], "lower_one_sided_95": lb["lower"]},
                               "claim_student_higher_on_rl_objective": bool(lb["lower"] > 0.10),
                               "gstar_minus_student_gT": two_sided(gG, gS), "rl_minus_student_gT": inv_g,
                               "inversion": bool(inv_g["ci95"][0] > 0 and upd["student_minus_rl_success"]["ci95"][0] > 0)}
    out["v5_row_updates"] = upd
    a0 = [rec["gstar"][e]["actions"][:1] == rec["gstar2"][e]["actions"][:1] for e in eps]
    out["gstar_first_decision_agreement_run2_vs_run1"] = float(np.mean(a0))
    arrays = {"S": S["success"], "G": X(["gstar"], "success")[:, 0], "travel": X(["gstar"], "travel_rad")[:, 0]}
    return out, arrays


def e12(c):
    tag = CELLS[c]
    res = {}
    for m in ["gstar"] + STUDENTS:
        sub16 = {}
        for d in (os.path.join(R5, "e5"), os.path.join(R6, "e12")):
            sub16.update(_load_dir(d, tag, m + "_sub16"))
        res[m] = sub16
    have = {m: sum(e in res[m] for e in E12_EPS) for m in res}
    out = {"episodes_per_method": have, "complete": all(v == len(E12_EPS) for v in have.values())}
    if not out["complete"]:
        return out
    t5 = {m: load("test5", tag, m) for m in ["gstar"] + STUDENTS}
    eps = list(E12_EPS)
    for m in res:                                          # the sub-16 re-read must be of the same recorded episode
        assert all(res[m][e]["actions"] == t5[m][e]["actions"] for e in eps), (c, m)
    out["flip_rate"] = {m: float(np.mean([bool(res[m][e]["success"]) != bool(t5[m][e]["success"]) for e in eps]))
                        for m in res}
    S8, G8 = col(t5, STUDENTS, "success", eps), col(t5, ["gstar"], "success", eps)
    S16, G16 = col(res, STUDENTS, "success", eps), col(res, ["gstar"], "success", eps)
    out["student_minus_gstar_success_sub8"] = two_sided(S8, G8)
    out["student_minus_gstar_success_sub16"] = two_sided(S16, G16)
    return out


def frontier(c, means):
    e6 = json.load(open(os.path.join(R5, "14_e6_analysis.json")))[c]["job1"]
    lat = {"gstar": e6["g2000_512_64"]["median"], "student": e6["student"]["median"],
           "g125_512_16": e6["g125_512_16"]["median"], "g500_512_4": e6["g500_512_4"]["median"]}
    succ = {"gstar": means["gstar"]["success"], "g125_512_16": means["g125_512_16"]["success"],
            "g500_512_4": means["g500_512_4"]["success"],
            "student": float(np.mean([means[s]["success"] for s in STUDENTS]))}
    return {"latency_median_s": lat, "success_0_499": succ, "note": "latency: v5 E6 job 1 (unchanged); success: test5 0-499"}


def h5b(arrays):
    from analysis_test5_v5 import h5b as h5b_v5
    return h5b_v5(arrays)


def main():
    if "--check" in sys.argv:
        for c in CELLS:
            for w, eps in WINDOWS.items():
                _, _, have, have_gt = completeness(c, eps)
                print(c, w, "test5", sum(have.values()), "/", len(eps) * len(have),
                      "g_T", sum(have_gt.values()), "/", len(eps) * len(have_gt))
            print(c, "E12", e12(c)["episodes_per_method"])
        return
    hstar = json.load(open(os.path.join(R5, "12_base_hstar.json")))
    res = {"amendment": "docs/07c_amendment_v6_0.md", "cells": {}}
    arrays = {}
    for c in CELLS:
        res["cells"][c] = {}
        for w, eps in WINDOWS.items():
            r, a = window_result(c, w, eps, hstar)
            res["cells"][c][w] = r
            if a is not None and w == "0-499":
                arrays[c] = a
                res["cells"][c]["frontier"] = frontier(c, r["means"])
        res["cells"][c]["E12"] = e12(c)
    for w in WINDOWS:
        if not all(res["cells"][c][w]["complete"] for c in CELLS):
            continue
        fam = {"H6a_difference": [res["cells"][c][w]["H6a"]["success"]["p_two_sided"] for c in CELLS],
               "H6a_tost": [res["cells"][c][w]["H6a"]["success"]["tost"]["p_tost"] for c in CELLS],
               "H6c": [res["cells"][c][w]["H6c"]["success"]["p_two_sided"] for c in CELLS]}
        for k, p in fam.items():
            for c, rj in zip(CELLS, holm(p)):
                res["cells"][c][w].setdefault("holm", {})[k] = bool(rj)
        p6b = [res["cells"][c][w]["H6b"][g]["p_two_sided"] for c in CELLS for g in REDUCED]
        rj = holm(p6b)
        for i, (c, g) in enumerate([(c, g) for c in CELLS for g in REDUCED]):
            res["cells"][c][w].setdefault("holm", {})[f"H6b_{g}"] = bool(rj[i])
    if len(arrays) == len(CELLS):
        res["H5b_update_0_499"] = h5b(arrays)
    os.makedirs(R6, exist_ok=True)
    json.dump(res, open(os.path.join(R6, "14_v6_analysis.json"), "w"), indent=1)
    print("written", os.path.join(R6, "14_v6_analysis.json"))


if __name__ == "__main__":
    main()
