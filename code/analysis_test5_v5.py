"""v5 test5 read-out (docs/07c_amendment_v5_0.md 'Decision rules'; addendum v5.1e: test5 0-299 per cell).
Written in run 35 before any test5 number was read (the S2/S12 test5 jobs were still running; S4/S8/A16-2 not frozen).

Inputs (all sub-8 grid read-out by eval3 on split test5):
  results/v5/test5/<tag>_<method>_<start>.jsonl   method in gstar, random, b_fan, b_spread, b_cov, student_s70x,
                                                   rl_s71x (cfg 6, spce_total), rlsucc_s71x (S2/S12 only)
  results/v5/test5_gt/<tag>_<method>_*.jsonl       g_T (gt3, J 16, L 4095) of the same records, for H2-v5
  results/v5/12_d5_analysis.json                   D5 on val3 (H5a's "m of 5 cells")
  results/v5/12_base_hstar.json                    H* per cell (pilot3 0-199, never test5)
Rules, as frozen in amendment v5.0:
  H5a   per cell test5 Delta_succ and Delta_BI (student - G*), crossed episode x seed bootstrap, two-sided ci95;
        reported with the validation count m (cells passing D5).
  H5b   slope of test5 Delta_succ(student - G*) on the cell's mean G* travel on test5 (radians -> reported per 100 deg),
        weighted least squares over the 5 cells, ci95 from the crossed bootstrap. Weights (fixed here): 1 / bootstrap
        variance of each cell's Delta_succ, held fixed across replicates. In each replicate every cell resamples its
        episodes (shared by student, G* and the G* travel of that cell) and student seeds independently. "The gap grows
        with travel" only if the ci95 excludes 0; otherwise "no trend detected over 5 cells". Needs all 5 cells.
  H2-v5 per cell g_T(student) - g_T(RL) one-sided 95 % LB > +0.10 nats. Also g_T(G*) - g_T(student), g_T(G*) - g_T(RL)
        (ci95) and the success ordering student - RL (ci95). "Inversion" (RL higher g_T, lower success) is claimed in a
        cell only if g_T(RL) - g_T(student) and success(student) - success(RL) both have ci95 above 0; in S2/S12 the
        same two contrasts are reported for rl_success vs student as the check.
  Baselines student - H* (success, BI) per cell with ci95.
  Holm (alpha 0.05, two-sided bootstrap p) across the 5 cells, separately for student - G* success and student - H*
        success.
Episodes: a cell is analysed only when every required method has all 300 episodes (nothing is selected).
usage: python analysis_test5_v5.py [--check]     --check prints completeness only (no outcome numbers).
Writes results/v5/14_test5_analysis.json."""
import glob
import json
import os
import sys

import numpy as np

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from touchbed.stats import crossed_bootstrap_diff, holm  # noqa: E402

ROOT = os.environ.get("V5_RESULTS", os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "results", "v5"))
CELLS = {"S2": "S_k2", "S4": "S_k4", "S8": "S_k8", "S12": "S_k12", "A16-2": "A16_k2"}
STUDENTS, RLS = [f"student_s{s}" for s in range(701, 706)], [f"rl_s{s}" for s in range(711, 716)]
RLSUCC = [f"rlsucc_s{s}" for s in range(711, 716)]
SINGLE = ["gstar", "random", "b_fan", "b_spread", "b_cov"]
N_EP, ALPHA2, N_BOOT = 300, 0.025, 10000


def methods(c):
    return SINGLE + STUDENTS + RLS + (RLSUCC if c in ("S2", "S12") else [])


def load(sub, tag, m):
    d = {}
    for f in glob.glob(os.path.join(ROOT, sub, f"{tag}_{m}_*.jsonl")):
        for line in open(f):
            r = json.loads(line)
            if "episode" in r and "header" not in r:
                d[r["episode"]] = r
    return d


def col(recs, names, key, eps):
    return np.array([[float(recs[n][e][key]) for n in names] for e in eps])


def two_sided(A, B):
    r = crossed_bootstrap_diff(A, B, n_boot=N_BOOT, alpha=ALPHA2)
    return {"diff": r["diff"], "ci95": [r["lower"], r["upper"]], "p_two_sided": min(1.0, 2 * min(r["p_greater"], r["p_less"])),
            "n_episodes": r["n_episodes"], "n_seeds": r["n_seeds"]}


def completeness(c):
    tag = CELLS[c]
    rec = {m: load("test5", tag, m) for m in methods(c)}
    have = {m: sum(e in rec[m] for e in range(N_EP)) for m in rec}
    gt = {m: load("test5_gt", tag, m) for m in ["gstar"] + STUDENTS + RLS + (RLSUCC if c in ("S2", "S12") else [])}
    have_gt = {m: sum(e in gt[m] for e in range(N_EP)) for m in gt}
    return rec, gt, have, have_gt


def cell_result(c, hstar):
    rec, gt, have, have_gt = completeness(c)
    out = {"cell": c, "n_required": N_EP, "episodes_per_method": have, "complete": all(v == N_EP for v in have.values()),
           "gt_episodes_per_method": have_gt, "gt_complete": all(v == N_EP for v in have_gt.values())}
    if not out["complete"]:
        return out, None
    eps = list(range(N_EP))
    out["means"] = {m: {k: float(np.mean([float(rec[m][e][k]) for e in eps])) for k in ("success", "ball_info", "travel_rad",
                                                                                         "n_probes")}
                    for m in rec}
    for m in out["means"]:
        out["means"][m]["travel_deg"] = float(np.degrees(out["means"][m]["travel_rad"]))
    S, G = {k: col(rec, STUDENTS, k, eps) for k in ("success", "ball_info")}, {k: col(rec, ["gstar"], k, eps) for k in ("success", "ball_info")}
    out["student_minus_gstar"] = {"success": two_sided(S["success"], G["success"]), "ball_info": two_sided(S["ball_info"], G["ball_info"])}
    h = hstar["cells"][c]["H_star"]
    H = {k: col(rec, [h], k, eps) for k in ("success", "ball_info")}
    out["H_star"] = h
    out["student_minus_hstar"] = {"success": two_sided(S["success"], H["success"]), "ball_info": two_sided(S["ball_info"], H["ball_info"])}
    R = {k: col(rec, RLS, k, eps) for k in ("success", "ball_info")}
    out["student_minus_rl"] = {"success": two_sided(S["success"], R["success"]), "ball_info": two_sided(S["ball_info"], R["ball_info"])}
    if c in ("S2", "S12"):
        RS = {k: col(rec, RLSUCC, k, eps) for k in ("success", "ball_info")}
        out["student_minus_rlsucc"] = {"success": two_sided(S["success"], RS["success"]), "ball_info": two_sided(S["ball_info"], RS["ball_info"])}
    # H5b inputs: per-episode arrays kept for the cross-cell bootstrap (not written to JSON)
    arrays = {"S": S["success"], "G": G["success"][:, 0], "travel": col(rec, ["gstar"], "travel_rad", eps)[:, 0]}
    if out["gt_complete"]:
        gS, gR, gG = col(gt, STUDENTS, "g_T", eps), col(gt, RLS, "g_T", eps), col(gt, ["gstar"], "g_T", eps)
        lb = crossed_bootstrap_diff(gS, gR, n_boot=N_BOOT, alpha=0.05)
        h2 = {"student_minus_rl_gT": {"diff": lb["diff"], "lower_one_sided_95": lb["lower"]},
              "claim_student_higher_on_rl_objective": bool(lb["lower"] > 0.10),
              "gstar_minus_student_gT": two_sided(gG, gS), "gstar_minus_rl_gT": two_sided(gG, gR),
              "means_gT": {"student": float(gS.mean()), "rl": float(gR.mean()), "gstar": float(gG.mean())}}
        inv_g, inv_s = two_sided(gR, gS), out["student_minus_rl"]["success"]
        h2["rl_minus_student_gT"] = inv_g
        h2["inversion"] = bool(inv_g["ci95"][0] > 0 and inv_s["ci95"][0] > 0)
        if c in ("S2", "S12"):
            gRS = col(gt, RLSUCC, "g_T", eps)
            c_g, c_s = two_sided(gRS, gS), out["student_minus_rlsucc"]["success"]
            h2["check_rlsucc"] = {"rlsucc_minus_student_gT": c_g, "student_minus_rlsucc_success": c_s,
                                  "inversion": bool(c_g["ci95"][0] > 0 and c_s["ci95"][0] > 0), "means_gT_rlsucc": float(gRS.mean())}
        out["H2_v5"] = h2
    return out, arrays


def wls_slope(x, y, w):
    X = np.column_stack([np.ones_like(x), x])
    W = np.diag(w)
    beta = np.linalg.solve(X.T @ W @ X, X.T @ W @ y)
    return float(beta[1])


def h5b(arrays, rng_seed=0):
    rng = np.random.default_rng(rng_seed)
    cs = list(CELLS)
    d = np.array([np.mean(arrays[c]["S"].mean(1) - arrays[c]["G"]) for c in cs])
    x = np.array([np.mean(arrays[c]["travel"]) for c in cs])
    reps = np.empty((N_BOOT, len(cs), 2))
    for b in range(N_BOOT):
        for i, c in enumerate(cs):
            A = arrays[c]
            n, k = A["S"].shape
            ei, si = rng.integers(0, n, n), rng.integers(0, k, k)
            reps[b, i, 0] = np.mean(A["S"][ei][:, si].mean(1) - A["G"][ei])
            reps[b, i, 1] = np.mean(A["travel"][ei])
    w = 1.0 / reps[:, :, 0].var(axis=0, ddof=1)
    slope = wls_slope(x, d, w)
    bs = np.array([wls_slope(reps[b, :, 1], reps[b, :, 0], w) for b in range(N_BOOT)])
    lo, hi = float(np.quantile(bs, ALPHA2)), float(np.quantile(bs, 1 - ALPHA2))
    per100 = np.radians(100.0)
    verdict = ("gap grows with travel" if lo > 0 else "gap shrinks with travel" if hi < 0 else
               "no trend detected over 5 cells")
    return {"cells": cs, "delta_succ": d.tolist(), "gstar_mean_travel_rad": x.tolist(), "weights": w.tolist(),
            "slope_per_rad": slope, "ci95_per_rad": [lo, hi], "slope_per_100deg": slope * per100,
            "ci95_per_100deg": [lo * per100, hi * per100], "verdict": verdict}


def main():
    if "--check" in sys.argv:
        for c in CELLS:
            _, _, have, have_gt = completeness(c)
            print(c, "test5", sum(have.values()), "/", N_EP * len(have), "g_T", sum(have_gt.values()), "/", N_EP * len(have_gt))
        return
    hstar = json.load(open(os.path.join(ROOT, "12_base_hstar.json")))
    d5 = json.load(open(os.path.join(ROOT, "12_d5_analysis.json")))
    res, arrays = {}, {}
    for c in CELLS:
        res[c], a = cell_result(c, hstar)
        if a is not None:
            arrays[c] = a
    done = [c for c in CELLS if res[c]["complete"]]
    res["H5a"] = {"validation_cells_complete": d5.get("H5a_validation", {}).get("cells_complete"),
                  "validation_cells_within_delta": d5.get("H5a_validation", {}).get("cells_pass"),
                  "test5_cells_complete": done}
    if len(done) == len(CELLS):
        for name in ("student_minus_gstar", "student_minus_hstar"):
            p = [res[c][name]["success"]["p_two_sided"] for c in CELLS]
            rej = holm(p)
            for c, r in zip(CELLS, rej):
                res[c][name]["success"]["holm_reject_5cells"] = bool(r)
        res["H5b"] = h5b(arrays)
    json.dump(res, open(os.path.join(ROOT, "14_test5_analysis.json"), "w"), indent=1)
    print("cells complete:", done, "| H5b:", res.get("H5b", {}).get("verdict", "pending (needs all 5 cells)"))


if __name__ == "__main__":
    main()
