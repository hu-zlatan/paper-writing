"""Amendment 09 part A (p2 v2): analyses of the existing 08c / 08e CRC replays, no new simulation.
A1 risk-efficiency frontier: shift every stratum's CRC lambda-hat index by k in -4..+4 (clipped); matched-slip RE at
   test physical slip 0.10 by linear interpolation between adjacent k; D_match = 1 - RE_arm / RE_CSF-1.
A2 Learn-then-Test fixed sequence: per stratum scan the grid from the top down, keep lambda while the one-sided
   Clopper-Pearson (1 - delta) upper bound of the calibration (monotonised) physical risk is <= alpha; delta = 0.10.
A3 contrasts on the CRC route: CSF-mu-hat sigma 0.2 vs CSF-1, onset-only sigma 0.2 vs CSF-1.
Bootstrap and CI** exactly as code/analysis_crc.py (object clusters within family, 2,000 draws, seed 2026,
1.25 / 98.75 percentiles; lambda-hat refitted per draw).
Writes results/v2/a_analysis.json (08c grids) and results/v2/a_analysis_08e.json (--v2: 08e grids).
usage (from papers/p2/code): python analysis_v2_a.py [--v2] [--draws 2000]"""
import argparse
import json
import os

import numpy as np
from scipy.stats import beta

import analysis_crc as A

ALPHA, DELTA, SHIFTS, SLIP_MATCH = 0.10, 0.10, tuple(range(-4, 5)), 0.10
ARMS = ("full_rd@0.2#0", "P_onset@0.2#0", "CSF-muhat@0.2", "CSF-1")
COMP = "CSF-1"


def cp_upper(k, n, delta=DELTA):
    return 1.0 if k >= n else float(beta.ppf(1 - delta, k + 1, n - k))


def lam_ltt(Lcal, alpha=ALPHA, delta=DELTA):
    """Fixed-sequence LTT from the largest lambda down; returns (j_hat, fallback_flag)."""
    Lt = np.maximum.accumulate(Lcal[:, ::-1].astype(float), axis=1)[:, ::-1]
    n, J = Lt.shape
    k = Lt.sum(axis=0)
    j_hat = None
    for j in range(J - 1, -1, -1):
        if cp_upper(int(round(k[j])), n, delta) <= alpha:
            j_hat = j
        else:
            break
    return (J - 1, True) if j_hat is None else (j_hat, False)


def evaluate(D, cal_idx, test_idx, rule="crc", shift=0):
    out = {}
    st_c, st_t = D["strata"][cal_idx], D["strata"][test_idx]
    for arm in D["L"]:
        L, F = D["L"][arm], D["F"][arm]
        J = L.shape[1]
        j_t = np.empty(len(test_idx), dtype=int)
        flags = {}
        for s in np.unique(D["strata"]):
            Lc = L[cal_idx[st_c == s]]
            j, f = A.lam_index(Lc) if rule == "crc" else lam_ltt(Lc)
            j_t[st_t == s] = min(max(j + shift, 0), J - 1)
            flags[str(s)] = [int(j), bool(f)]
        av = D["avoid"][test_idx]
        Ft = F[test_idx, j_t]
        rr = D["ref"]["mid"][test_idx][av]
        out[arm] = {"lam": flags, "slip_phys": float(L[test_idx, j_t].mean()),
                    "RE_mid": float(np.mean((Ft[av] - rr) / rr))}
    return out


def matched_re(front):
    """front: list of (slip, RE) over SHIFTS (slip non-increasing in k). RE at slip SLIP_MATCH or None."""
    for (s0, r0), (s1, r1) in zip(front[:-1], front[1:]):
        if (s0 - SLIP_MATCH) * (s1 - SLIP_MATCH) <= 0 and s0 != s1:
            w = (s0 - SLIP_MATCH) / (s0 - s1)
            return r0 + w * (r1 - r0)
    return None


def stats(D, cal_idx, test_idx):
    crc = {k: evaluate(D, cal_idx, test_idx, "crc", k) for k in SHIFTS}
    ltt = evaluate(D, cal_idx, test_idx, "ltt", 0)
    v = {}
    for a in ARMS:
        fr = [(crc[k][a]["slip_phys"], crc[k][a]["RE_mid"]) for k in SHIFTS]
        v[f"RE_match@{a}"] = matched_re(fr)
    for a in ARMS[:-1]:
        rm, rc = v[f"RE_match@{a}"], v[f"RE_match@{COMP}"]
        v[f"D_match:{a}"] = None if rm is None or rc is None else 1 - rm / rc
        v[f"D_ltt:{a}"] = 1 - ltt[a]["RE_mid"] / ltt[COMP]["RE_mid"]
        v[f"D_crc:{a}"] = 1 - crc[0][a]["RE_mid"] / crc[0][COMP]["RE_mid"]
    return v, crc, ltt


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--v2", action="store_true")
    ap.add_argument("--draws", type=int, default=2000)
    a = ap.parse_args()
    A.V2 = a.v2
    G, keys, idx, rep, missing, dup = A.load_real()
    assert not missing, "incomplete replays"
    D = A.build(G, keys, rep)
    D["L"] = {k: D["L"][k] for k in ARMS}
    D["F"] = {k: D["F"][k] for k in ARMS}
    cal_objs = sorted({o for o, s in zip(D["obj"], D["split"]) if s == "cal"})
    test_objs = sorted({o for o, s in zip(D["obj"], D["split"]) if s == "test"})
    by_obj = {}
    for i, o in enumerate(D["obj"]):
        by_obj.setdefault(o, []).append(i)
    cal_idx = np.array([i for o in cal_objs for i in by_obj[o]])
    test_idx = np.array([i for o in test_objs for i in by_obj[o]])
    point, crc, ltt = stats(D, cal_idx, test_idx)
    groups = {}
    for part, objs in (("cal", cal_objs), ("test", test_objs)):
        for o in objs:
            groups.setdefault((part, o[0]), []).append(o)
    rng = np.random.default_rng(2026)
    boot = {k: [] for k in point}
    for _ in range(a.draws):
        ci, ti = [], []
        for (part, _f), objs in groups.items():
            pick = rng.integers(0, len(objs), len(objs))
            (ci if part == "cal" else ti).extend(i for p in pick for i in by_obj[objs[p]])
        v, _, _ = stats(D, np.array(ci), np.array(ti))
        for k in point:
            boot[k].append(v[k])
    res = {"purpose": "p2 v2 amendment 09 part A (frontier, LTT, extra contrasts); secondary",
           "grids": "08e" if a.v2 else "08c", "alpha": ALPHA, "delta": DELTA, "slip_match": SLIP_MATCH,
           "draws": a.draws, "frontier": {arm: [{"k": k, "slip_phys": crc[k][arm]["slip_phys"],
                                                 "RE_mid": crc[k][arm]["RE_mid"]} for k in SHIFTS] for arm in ARMS},
           "ltt_arms": ltt, "point": point, "CI**": {}}
    for k, b in boot.items():
        vals = [x for x in b if x is not None]
        res["CI**"][k] = {"n_valid": len(vals), "ci": ([float(np.percentile(vals, A.LO_P)), float(np.percentile(vals, A.HI_P))]
                                                      if vals else None)}
    for k in point:
        if k.startswith("D_") and res["CI**"][k]["ci"]:
            lo, hi = res["CI**"][k]["ci"]
            res["CI**"][k]["decision"] = "superiority" if lo > 0 else ("inferiority" if hi < 0 else "not shown")
    out = os.path.join(A.ROOT, "v2", "a_analysis_08e.json" if a.v2 else "a_analysis.json")
    json.dump(res, open(out, "w"), indent=1)
    for k in point:
        print(k, None if point[k] is None else round(point[k], 4), res["CI**"][k])


if __name__ == "__main__":
    main()
