"""p2 v4 POST-HOC, REPORT-ONLY rows requested by the stage-18 [v4] reviewers (run 48, 2026-11-12).

Written after v4_analysis.json was read; not pre-registered; no decision depends on it. It re-reads the same committed
v4 replays and labels with analysis_v4.load and the same split / CRC / matched-slip recipe (analysis_v4.arm_eval), and
adds only quantities the confirmatory read-out did not report:
  P1 absolute excess hold force AE = mean (F - F*_mid) in newtons on avoidable test rows, at the CRC point and at
     matched test slip 0.10 (same interpolation as RE_match); D_abs(a vs b) = 1 - AE(a) / AE(b) with CI** from
     object-cluster draws (analysis_v3_a.boot_draws, seed 2027; --draws, default 500, fewer than the 2,000 of record).
  P2 mean hold force per arm and its difference to CSF-1 (N and %), CRC point, f4 test split.
  P3 test-slip by friction tercile (terciles of the f4 test instances' mu), per arm, CRC point.
  P4 count of unavoidable instances per pool / split.
Writes results/v4/v4_posthoc.json.  usage (from papers/p2/code): python analysis_v4_posthoc.py [--draws N]"""
import argparse
import json
import os

import numpy as np

import analysis_v3_a as V
import analysis_v4 as A4
from certgrip.io import ROOT, key, load_rows

ARMS_F = (A4.FULL, A4.MUHAT, A4.SHR, A4.COMP)
ARMS_C = (A4.FULL, A4.MUHAT, A4.FAM, A4.COMP)


def ae_eval(D, arm, ci, ti):
    e = A4.arm_eval(D, arm, ci, ti)
    L, F = D["L"][arm], D["F"][arm]
    J = L.shape[1]
    av = D["avoid"][ti]
    rr = D["ref"]["mid"][ti][av]

    def at(jj):
        return float(L[ti, jj].mean()), float(np.mean(F[ti, jj][av] - rr))

    s, ae = at(e["j_t"])
    front = [at(np.clip(e["j_t"] + k, 0, J - 1)) for k in A4.KS]
    match = None
    for (s0, r0), (s1, r1) in zip(front[:-1], front[1:]):
        if (s0 - A4.SLIP_MATCH) * (s1 - A4.SLIP_MATCH) <= 0 and s0 != s1:
            match = r0 + (s0 - A4.SLIP_MATCH) / (s0 - s1) * (r1 - r0)
            break
    return {"slip": s, "AE_N": ae, "AE_match_N": match, "edge": e["edge"], "e": e}


def contrasts(D, ci, ti, pairs):
    m = {a: ae_eval(D, a, ci, ti) for a in {x for p in pairs.values() for x in p[:2]}}
    key_ = {"match": "AE_match_N", "crc": "AE_N"}
    return {k: A4.dd(m[t][key_[kind]], m[c][key_[kind]]) for k, (t, c, kind) in pairs.items()}, m


def pool(D, pairs, draws):
    co, to = V.groups_of(D)
    ci0, ti0 = V.split_idx(D, co), V.split_idx(D, to)
    pt, m = contrasts(D, ci0, ti0, pairs)
    boot = {k: [] for k in pairs}
    for ci, ti in V.boot_draws(D, co, to, draws, 2027):
        v, _ = contrasts(D, ci, ti, pairs)
        for k in pairs:
            boot[k].append(v[k])
    rows = {k: {"target": t, "comparator": c, "kind": kind, "point": pt[k], "CI**": V.ci_of(boot[k]),
                "valid_draws": int(sum(x is not None for x in boot[k]))} for k, (t, c, kind) in pairs.items()}
    arms = {a: {"slip": x["slip"], "AE_N": x["AE_N"], "AE_match_N": x["AE_match_N"], "edge": x["edge"]}
            for a, x in m.items()}
    return rows, arms, m, (ci0, ti0)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--draws", type=int, default=500)
    a = ap.parse_args()
    labs = {key(r): r for r in load_rows("v4/labels/*.jsonl")}
    Df = A4.load("f4", labs, )[4]
    Dc = A4.load("c4", labs)[4]
    assert Df is not None and Dc is not None
    res = {"purpose": "p2 v4 post-hoc report-only rows (stage-18 v4 reviewers); not pre-registered; no decision",
           "draws": a.draws, "seed": 2027}
    pf = {"P1_C1_abs_match": (A4.MUHAT, A4.COMP, "match"), "P1_C2_abs_match": (A4.FULL, A4.MUHAT, "match"),
          "P1_C3_abs_crc": (A4.FULL, A4.COMP, "crc"), "P1_C1_abs_crc": (A4.MUHAT, A4.COMP, "crc"),
          "P1_C2_abs_crc": (A4.FULL, A4.MUHAT, "crc"), "P1_shrunk_vs_full_abs_match": (A4.SHR, A4.FULL, "match")}
    rows, arms, m, (ci, ti) = pool(Df, pf, a.draws)
    av = Df["avoid"][ti]
    hold = {x: float(np.mean(m[x]["e"]["F_t"][av])) for x in m}
    res["f4"] = {"rows": rows, "arms": arms,
                 "P2_hold_force_N": {x: {"mean": hold[x], "minus_CSF1_N": hold[x] - hold[A4.COMP],
                                         "minus_CSF1_pct": 100 * (hold[x] - hold[A4.COMP]) / hold[A4.COMP]}
                                     for x in hold}}
    mu_t = Df["mu"][ti]
    q = np.quantile(mu_t, [1 / 3, 2 / 3])
    terc = np.digitize(mu_t, q)
    res["f4"]["P3_slip_by_mu_tercile"] = {
        "edges_mu": [float(q[0]), float(q[1])],
        "n": [int((terc == t).sum()) for t in range(3)],
        "slip": {x: [float(Df["L"][x][ti, m[x]["e"]["j_t"]][terc == t].mean()) for t in range(3)] for x in m}}
    pc = {"P1_C4_abs_match": (A4.MUHAT, A4.FAM, "match"), "P1_C5_abs_match": (A4.FULL, A4.FAM, "match")}
    rows_c, arms_c, _, _ = pool(Dc, pc, a.draws)
    res["c4"] = {"rows": rows_c, "arms": arms_c}
    res["P4_unavoidable"] = {}
    for n, D in (("f4", Df), ("c4", Dc)):
        sp = np.array(D["split"])
        res["P4_unavoidable"][n] = {s: int((~D["avoid"][sp == s]).sum()) for s in np.unique(sp)}
        res["P4_unavoidable"][n]["n_instances"] = len(D["keys"])
    json.dump(res, open(os.path.join(ROOT, "v4", "v4_posthoc.json"), "w"), indent=1)
    print(json.dumps({k: v["point"] for k, v in {**rows, **rows_c}.items()}, indent=1))


if __name__ == "__main__":
    main()
