"""Stage-10/12 pilot read-out for paper 2 (07_hypotheses §8). Pilot pool only (salt 3003, disjoint from every main
pool), so nothing here touches calibration or test data. Not a paper result; it sets the pre-registration constants.

Reads results/pilot/labels/*.jsonl and results/pilot/mono/*.jsonl, writes results/pilot/pilot_analysis.json:
  H1-M pilot look (non-monotone count), UT5 range check, UT8 unavoidable rate per pool (none / S1 / S3 / F5),
  F* spread, paired shift effect (S1, S3) in log F*, preload-slip rate;
  cross-fitted (5-fold by object) quantile predictors for every input set (equal 5-config search; the main study
  uses 30) -> conformal RE and label slip rate by repeated random cal/eval object splits, CSF-1 and Mondrian-CSF,
  paired differences for the power inputs, eta = 0.1 x IQR of the CertGrip scores, and D-mu (does the residual of
  each predictor still correlate with log mu?).
usage (from papers/p2/code): python pilot_analysis.py [--configs 5] [--splits 200]
"""
import argparse
import glob
import json
import math
import os

import numpy as np
from sklearn.ensemble import HistGradientBoostingRegressor
from sklearn.model_selection import GroupKFold

from certgrip.baselines import f_nom
from certgrip.conformal import qhat
from certgrip.featsets import matrix
from certgrip.models import fit_quantile

ROOT = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "results", "pilot")
ALPHA, TAU, F_MAX = 0.10, 0.90, 100.0


def load(pattern):
    rows = []
    for f in sorted(glob.glob(os.path.join(ROOT, pattern))):
        rows += [json.loads(l) for l in open(f) if l.strip()]
    return [r for r in rows if "header" not in r and "EARLY_STOP_AT_80_PCT_BUDGET" not in r]


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--configs", type=int, default=5)
    ap.add_argument("--splits", type=int, default=200)
    a = ap.parse_args()
    out = {"purpose": "p2 pilot read-out (pilot pool only; not a paper result)", "alpha": ALPHA}

    mono = load("mono/*.jsonl")
    out["H1M_pilot"] = {"n": len(mono), "non_monotone": int(sum(r["non_monotone"] for r in mono)),
                        "by_family": {f: [int(sum(r["non_monotone"] for r in mono if r["family"] == f)),
                                          sum(r["family"] == f for r in mono)] for f in sorted({r["family"] for r in mono})}}
    pools = {"ID F1-F4": "labels/pilot_F[1-4].jsonl", "S1": "labels/pilot_F*_S1.jsonl",
             "S3": "labels/pilot_F*_S3.jsonl", "F5 (S2 family)": "labels/pilot_F5.jsonl"}
    out["UT8"], out["fstar"] = {}, {}
    for k, p in pools.items():
        rs = load(p)
        fh = np.array([r["F_hi"] for r in rs if not r["unavoidable"]])
        out["UT8"][k] = {"n": len(rs), "unavoidable": int(sum(r["unavoidable"] for r in rs)),
                         "max_F_hi": float(fh.max()), "preload_slips": int(sum(r["preload_slip"] for r in rs)),
                         "F_lo_at_F_min (never observed slipping)": int(sum(r["F_lo"] <= 0.1 + 1e-9 for r in rs))}
        out["fstar"][k] = {q: float(np.percentile(fh, q)) for q in (1, 10, 50, 90, 99)}
    base = {(r["family"], r["obj"], r["dist"]): r for r in load("labels/pilot_F[1-4].jsonl")}
    for sh, pred in (("S1", math.log(1 / 0.6)), ("S3", None)):
        d = [math.log(r["F_mid"]) - math.log(base[(r["family"], r["obj"], r["dist"])]["F_mid"])
             for r in load(f"labels/pilot_F*_{sh}.jsonl") if not r["unavoidable"]]
        out[f"shift_{sh}_dlogF"] = {"mean": float(np.mean(d)), "sd": float(np.std(d)), "coulomb_prediction": pred,
                                    "by_dist": {}}
        for dist in ("D1", "D2", "D3", "D4"):
            dd = [math.log(r["F_mid"]) - math.log(base[(r["family"], r["obj"], r["dist"])]["F_mid"])
                  for r in load(f"labels/pilot_F*_{sh}.jsonl") if r["dist"] == dist]
            out[f"shift_{sh}_dlogF"]["by_dist"][dist] = float(np.mean(dd))

    # ---- cross-fitted predictors on the ID pilot pool
    rows = [base[k] for k in sorted(base)]
    y = np.log([r["F_hi"] for r in rows])
    ymid = np.array([r["F_mid"] for r in rows])
    fhi = np.array([r["F_hi"] for r in rows])
    groups = np.array([f"{r['family']}_{r['obj']}" for r in rows])
    dist = np.array([r["dist"] for r in rows])
    famdist = np.array([f"{r['family']}{r['dist']}" for r in rows])
    logmu = np.log([r["inst"]["mu"] for r in rows])
    oof, search = {}, {}
    for fs in ("base", "P", "S", "full", "oracle"):
        X = matrix(rows, fs)
        p = np.zeros(len(y))
        for tr, te in GroupKFold(n_splits=5).split(X, y, groups):
            m, info = fit_quantile(X[tr], y[tr], groups[tr], TAU, seed=0, n_configs=a.configs)
            p[te] = m.predict(X[te])
        oof[fs] = p
        search[fs] = {"dim": int(X.shape[1])}
    oof["CSF-1"] = np.log([f_nom(r["inst"]["mass"], r["dist"], r["inst"]["amp"], r["inst"]["freq"]) for r in rows])
    oof["Mondrian-CSF"] = oof["CSF-1"]
    strata = {k: (famdist if k == "Mondrian-CSF" else dist) for k in oof}

    # residual vs log mu (D-mu): mean-model residual on the OOF median would be cleaner; the quantile residual is a
    # pilot proxy
    out["D_mu_corr_resid_logmu"] = {k: float(np.corrcoef(y - oof[k], logmu)[0, 1]) for k in oof}
    out["oof_pinball"] = {k: float(np.mean(np.maximum(TAU * (y - oof[k]), (TAU - 1) * (y - oof[k])))) for k in oof
                          if k not in ("CSF-1", "Mondrian-CSF")}

    objs = np.unique(groups)
    rng = np.random.default_rng(12)
    res = {k: {"RE": [], "slip": []} for k in oof}
    dpair = {k: [] for k in oof}
    for _ in range(a.splits):
        cal_objs = set(rng.choice(objs, size=len(objs) // 2, replace=False))
        cal = np.array([g in cal_objs for g in groups])
        ev = ~cal
        re_k = {}
        for k, p in oof.items():
            s = y - p
            F = np.empty(len(y))
            for st in np.unique(strata[k]):
                idx = strata[k] == st
                q = qhat(s[cal & idx], ALPHA)
                F[idx] = np.minimum(np.exp(p[idx] + q), F_MAX)
            re_k[k] = (F[ev] - ymid[ev]) / ymid[ev]
            res[k]["RE"].append(float(re_k[k].mean()))
            res[k]["slip"].append(float(np.mean(F[ev] < fhi[ev])))
        for k in oof:
            dpair[k].append(float(re_k[k].mean() - re_k["full"].mean()))
    out["conformal_pilot"] = {k: {"RE_mean": float(np.mean(v["RE"])), "RE_sd_over_splits": float(np.std(v["RE"])),
                                  "slip_label_mean": float(np.mean(v["slip"]))} for k, v in res.items()}
    out["paired_RE_minus_full"] = {k: {"mean": float(np.mean(v)), "sd": float(np.std(v))} for k, v in dpair.items()}
    s_full = y - oof["full"]
    q25, q75 = np.percentile(s_full, [25, 75])
    out["eta_pilot"] = {"IQR_scores_full": float(q75 - q25), "eta": float(0.1 * (q75 - q25)),
                        "note": "pilot value; the frozen eta uses the main in-distribution calibration scores (§1.4)"}
    out["n_rows_ID"] = len(rows)
    out["feature_dims"] = search
    json.dump(out, open(os.path.join(ROOT, "pilot_analysis.json"), "w"), indent=1)
    print(json.dumps({k: out[k] for k in ("H1M_pilot", "UT8", "conformal_pilot", "D_mu_corr_resid_logmu",
                                          "eta_pilot")}, indent=1))


if __name__ == "__main__":
    main()
