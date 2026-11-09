"""Addendum 08g (part 1): H2-C, H2-n, H2-H, H2-R, H4d, D-loc, oracle decomposition (label route, secondary).
Writes results/v1/sec08g.json.  usage (from papers/p2/code): python secondaries_08g.py [--draws 2000]
"""
import argparse
import json
import math
import os
from statistics import NormalDist

import numpy as np

from certgrip.io import ROOT
from secondaries_08f import DISTS, F_MAX, Data, ci, qhat, resample

CG, CSF, P, FULL, S, OR = "full_rd@0.2#0", "CSF-1", "P#0", "full#0", "S#0", "oracle#0"
ARMS = [CG, CSF, P, FULL, S, OR]
FAMS = ("F1", "F2", "F3", "F4")


def forces(D, a, ci_, ti, cell=False):
    """Label-rule F on ti with q-hat per stratum (dist, or family x dist when cell) from ci_."""
    lab = (lambda i: D.fam[i] + D.st[i]) if cell else (lambda i: D.st[i])
    lc, lt = np.array([lab(i) for i in ci_]), np.array([lab(i) for i in ti])
    F = np.empty(len(ti))
    for s in np.unique(lt):
        c = ci_[lc == s]
        q = qhat(np.log(D.fhi[c]) - D.lg[a][c])
        m = lt == s
        F[m] = np.minimum(F_MAX, np.exp(D.lg[a][ti][m] + q))
    return F


def re(D, F, ti):
    return float(np.mean((F - D.fmid[ti]) / D.fmid[ti]))


def decide_h2(d, lo, hi, m=0.10):
    if d >= m and lo > 0:
        return "superiority"
    if -m < lo and hi < m:
        return "equivalence"
    if hi < 0:
        return "inferiority"
    return "not confirmed"


def main(draws, seed=2032):
    D = Data(ARMS)
    D.fam = np.array([r["family"] for r in D.rows])
    idr = lambda sp: D.sel(lambda r: r["pool"] == "id" and r["shift"] is None and r["split"] == sp)
    cal, tst = idr("cal"), idr("test")
    assert not D.unav[cal].any() and not D.unav[tst].any()
    bc, bt = D.by_obj(cal), D.by_obj(tst)
    rng = np.random.default_rng(seed)
    out = {"purpose": "p2 addendum 08g part 1 (label route, secondary)", "draws": draws}

    # sub-pool for H2-R
    mu = np.array([r["inst"]["mu"] for r in D.rows]); amp = np.array([r["inst"]["amp"] for r in D.rows])
    pool = np.concatenate([cal, tst])
    keep = np.zeros(len(D.rows), bool)
    for s in DISTS:
        m = pool[D.st[pool] == s]
        lo_a, hi_a = np.percentile(amp[m], [25, 75])
        keep[m] = (mu[m] >= 0.5) & (mu[m] <= 0.8) & (amp[m] >= lo_a) & (amp[m] <= hi_a)
    rcal, rtst = cal[keep[cal]], tst[keep[tst]]

    def stats(ci_, ti, rci, rti):
        F = {a: forces(D, a, ci_, ti) for a in ARMS}
        R = {a: re(D, F[a], ti) for a in ARMS}
        v = {"H2C": 1 - R[CG] / re(D, forces(D, CSF, ci_, ti, cell=True), ti),
             "oracle_share": (R[CSF] - R[CG]) / (R[CSF] - R[OR])}
        for f in FAMS:
            m = D.fam[ti] == f
            v[f"H4d_full_rd_{f}"] = 1 - re(D, F[CG][m], ti[m]) / re(D, F[P][m], ti[m])
            v[f"H4d_full_{f}"] = 1 - re(D, F[FULL][m], ti[m]) / re(D, F[P][m], ti[m])
            for s in DISTS:
                mm = m & (D.st[ti] == s)
                v[f"cell_{f}{s}"] = 1 - re(D, F[CG][mm], ti[mm]) / re(D, F[CSF][mm], ti[mm])
        v["H4d_full_rd_F4-F1"] = v["H4d_full_rd_F4"] - v["H4d_full_rd_F1"]
        v["H4d_full_F4-F1"] = v["H4d_full_F4"] - v["H4d_full_F1"]
        v["H2R"] = 1 - re(D, forces(D, CG, rci, rti), rti) / re(D, forces(D, CSF, rci, rti), rti)
        v["RE"] = R
        return v

    pt = stats(cal, tst, rcal, rtst)
    brc, brt = D.by_obj(rcal), D.by_obj(rtst)
    boot = []
    for _ in range(draws):
        boot.append(stats(resample(bc, rng), resample(bt, rng), resample(brc, rng), resample(brt, rng)))
    B = lambda k: np.array([b[k] for b in boot])
    out["RE_point"] = pt["RE"]
    out["H2C_vs_Mondrian"] = {"D": pt["H2C"], "CI**": ci(B("H2C")), "decision": decide_h2(pt["H2C"], *ci(B("H2C")))}
    out["oracle_decomposition"] = {"share_of_CSF1_to_oracle_gap_closed": pt["oracle_share"], "CI**": ci(B("oracle_share")),
                                   "RE": {a: pt["RE"][a] for a in (CSF, CG, OR)}}
    h4 = {}
    for arm in ("full_rd", "full"):
        k = f"H4d_{arm}_F4-F1"; lo, hi = ci(B(k))
        h4[arm] = {"D_by_family": {f: pt[f"H4d_{arm}_{f}"] for f in FAMS}, "F4_minus_F1": pt[k], "CI**": [lo, hi],
                   "decision": "confirmed (lower > 0)" if lo > 0 else ("failure (upper <= 0)" if hi <= 0 else "inconclusive")}
    out["H4d"] = h4
    out["H2R"] = {"D": pt["H2R"], "CI**": ci(B("H2R")), "n_cal": int(len(rcal)), "n_test": int(len(rtst))}

    # H2-H: DerSimonian-Laird over the 16 cells, Holm guard
    cells = [f"cell_{f}{s}" for f in FAMS for s in DISTS]
    d = np.array([pt[c] for c in cells]); se = np.array([B(c).std(ddof=1) for c in cells]); w = 1 / se ** 2
    dfix = np.sum(w * d) / np.sum(w); Q = np.sum(w * (d - dfix) ** 2); k = len(d)
    tau2 = max(0.0, (Q - (k - 1)) / (np.sum(w) - np.sum(w ** 2) / np.sum(w)))
    ws = 1 / (se ** 2 + tau2); dre = np.sum(ws * d) / np.sum(ws); sre = math.sqrt(1 / np.sum(ws))
    # Holm on H0_c: -D_c <= 0.10 vs -D_c > 0.10 (CertGrip worse than COMP by > 10 %), one-sided
    pz = np.array([1 - NormalDist().cdf((-dc - 0.10) / s) for dc, s in zip(d, se)])
    order = np.argsort(pz); rej = np.zeros(k, bool)
    for r, j in enumerate(order):
        if pz[j] <= 0.05 / (k - r):
            rej[j] = True
        else:
            break
    out["H2H"] = {"pooled_D_RE": dre, "pooled_95CI": [dre - 1.96 * sre, dre + 1.96 * sre], "tau": math.sqrt(tau2), "Q": Q,
                  "cells": {c[5:]: {"D": float(pt[c]), "CI**": ci(B(c)), "se": float(s)} for c, s in zip(cells, se)},
                  "guard_cells_flagged": [cells[j][5:] for j in range(k) if rej[j]],
                  "decision": "pass (no cell worse by > 10 %)" if not rej.any() else "failure"}

    # D-loc (no bootstrap)
    ix = {(r["family"], r["obj"], r["dist"], r["shift"]): i for i, r in enumerate(D.rows) if r["pool"] == "id"}
    pairs = [(ix[(f, o, s, None)], i) for (f, o, s, sh), i in ix.items() if sh == "S1" and (f, o, s, None) in ix]
    pairs = [(a, b) for a, b in pairs if not D.unav[a] and not D.unav[b]]
    a_, b_ = np.array([p[0] for p in pairs]), np.array([p[1] for p in pairs])
    dl = np.log(D.fmid[b_]) - np.log(D.fmid[a_])
    out["D_loc"] = {"n_pairs": len(pairs), "dlogF_mean": float(dl.mean()), "dlogF_sd": float(dl.std()),
                    "mean_abs_dg_over_g": {a: float(np.mean(np.abs(np.exp(D.lg[a][b_] - D.lg[a][a_]) - 1)))
                                           for a in (P, S, FULL, CG)},
                    "preload_slip_rate": {}}
    for name, f in {"id": lambda r: r["pool"] == "id" and r["shift"] is None, "S1": lambda r: r["shift"] == "S1",
                    "S1m": lambda r: r["shift"] == "S1m", "S3": lambda r: r["shift"] == "S3", "s2": lambda r: r["pool"] == "s2"}.items():
        rr = [r for r in D.rows if f(r)]
        out["D_loc"]["preload_slip_rate"][name] = float(np.mean([r["preload_slip"] for r in rr]))
    return out


def h2n(draws, seed=2033):
    D = Data([CG, CSF])
    idr = lambda sp: D.sel(lambda r: r["pool"] == "id" and r["shift"] is None and r["split"] == sp)
    cal, tst = idr("cal"), idr("test")
    bc, bt = D.by_obj(cal), D.by_obj(tst)
    cobj = list(bc)
    rng = np.random.default_rng(seed)
    res = {}
    for al in (0.10, 0.20):
        ds = []
        for _ in range(draws):
            ch = [cobj[j] for j in rng.permutation(len(cobj))[:50]]
            ci_ = np.array([i for o in ch for i in bc[o]]); ti = resample(bt, rng)
            R = {}
            for a in (CG, CSF):
                F = np.empty(len(ti))
                for s in DISTS:
                    c = ci_[D.st[ci_] == s]
                    q = qhat(np.log(D.fhi[c]) - D.lg[a][c], al)
                    m = D.st[ti] == s
                    F[m] = np.minimum(F_MAX, np.exp(D.lg[a][ti][m] + q))
                R[a] = re(D, F, ti)
            ds.append(1 - R[CG] / R[CSF])
        lo, hi = ci(ds)
        res[f"alpha_{al}"] = {"D_mean": float(np.mean(ds)), "interval": [lo, hi],
                              "decision": "confirmed (lower > 0)" if lo > 0 else ("failure (inside ±0.10)" if -0.1 < lo and hi < 0.1 else "inconclusive")}
    return res


if __name__ == "__main__":
    ap = argparse.ArgumentParser(); ap.add_argument("--draws", type=int, default=2000); a = ap.parse_args()
    res = main(a.draws)
    res["H2n"] = h2n(a.draws)
    json.dump(res, open(os.path.join(ROOT, "v1/sec08g.json"), "w"), indent=1)
    print(json.dumps({k: v for k, v in res.items() if k != "H2H"}, indent=1)[:5000])
    print(json.dumps({k: v for k, v in res["H2H"].items() if k != "cells"}, indent=1))
