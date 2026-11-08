"""Re-pilot read-out under amendment 08a (protocol "rd"; pilot pool objects 125-224 only, salt 3003 — disjoint from
every main pool). Not a paper result: it sets the pre-registration constants of docs/08b_preregistration.md.

Reads results/pilot/rd/labels/*.jsonl and results/pilot/rd/mono/*.jsonl, writes results/pilot/rd/pilot_analysis_rd.json:
  H1-M look and UT8 under the probe protocol (probe-induced unavoidable instances counted per pool), onset detector
  quality (found rate, log mu-hat vs log mu at each sigma), paired shift effects;
  cross-fitted (5-fold by object) quantile predictors with the equal --configs search for P, S, full (squeeze),
  full_rd and P_onset (onset arms at every sigma in --sigmas), oracle; physics plug-ins CSF-1 and CSF-mu-hat (per sigma);
  conformal RE / label slip by repeated random cal / eval object splits; paired differences D(H2a) = RE(comparator)
  - RE(full_rd) vs CSF-1 and vs P (COMP proxies) and D(H2b) vs CSF-mu-hat at the same sigma (power inputs);
  D-mu = cross-validated R^2 of log mu on each arm's OOF residual (linear, 5-fold by object); eta = 0.1 x IQR.
Unavoidable instances (F_max slips, incl. probe-induced slip) have no F*: excluded from training and RE, counted as a
slip for every method in the label slip rate.
usage (from papers/p2/code): python pilot_analysis_rd.py [--configs 30] [--splits 200] [--jobs 2]
"""
import argparse
import glob
import json
import math
import os

import numpy as np
from joblib import Parallel, delayed
from sklearn.linear_model import LinearRegression
from sklearn.model_selection import GroupKFold

from certgrip.baselines import f_nom, f_nom_muhat, mu_hat
from certgrip.conformal import qhat
from certgrip.featsets import matrix, onset_log_force
from certgrip.models import fit_quantile

ROOT = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "results", "pilot", "rd")
ALPHA, TAU, F_MAX = 0.10, 0.90, 100.0


def load(pattern):
    rows = []
    for f in sorted(glob.glob(os.path.join(ROOT, pattern))):
        rows += [json.loads(l) for l in open(f) if l.strip()]
    return [r for r in rows if "header" not in r and "EARLY_STOP_AT_80_PCT_BUDGET" not in r]


def oof_predict(X, y, groups, configs, seed=0):
    def fold(tr, te):
        m, info = fit_quantile(X[tr], y[tr], groups[tr], TAU, seed=seed, n_configs=configs)
        return te, m.predict(X[te]), info["cv_pinball"]
    res = [fold(tr, te) for tr, te in GroupKFold(n_splits=5).split(X, y, groups)]
    p = np.zeros(len(y))
    for te, pr, _ in res:
        p[te] = pr
    return p


def cv_r2(resid, logmu, groups):
    """Cross-validated R^2 of a linear fit of log mu -> residual (5-fold by object)."""
    pred = np.zeros(len(resid))
    for tr, te in GroupKFold(n_splits=5).split(resid, resid, groups):
        lr = LinearRegression().fit(logmu[tr, None], resid[tr])
        pred[te] = lr.predict(logmu[te, None])
    return float(1 - np.sum((resid - pred) ** 2) / np.sum((resid - resid.mean()) ** 2))


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--configs", type=int, default=30)
    ap.add_argument("--splits", type=int, default=200)
    ap.add_argument("--jobs", type=int, default=2)
    ap.add_argument("--sigmas", default="0,0.1,0.2,0.4")
    a = ap.parse_args()
    sigmas = [float(s) for s in a.sigmas.split(",")]
    out = {"purpose": "p2 re-pilot read-out under amendment 08a (pilot objects 125-224; not a paper result)",
           "alpha": ALPHA, "configs": a.configs, "splits": a.splits, "sigmas": sigmas}

    mono = load("mono/*.jsonl")
    out["H1M_pilot_rd"] = {"n": len(mono), "non_monotone": int(sum(r["non_monotone"] for r in mono)),
                           "all_slip_on_grid": int(sum(all(r["slip_grid"]) for r in mono))}
    pools = {"ID F1-F4": "labels/pilot_F[1-4].jsonl", "S1": "labels/pilot_F*_S1.jsonl",
             "S3": "labels/pilot_F*_S3.jsonl", "F5 (S2 family)": "labels/pilot_F5.jsonl"}
    out["UT8_rd"], out["onset_quality"] = {}, {}
    for k, p in pools.items():
        rs = load(p)
        fh = np.array([r["F_hi"] for r in rs if not r["unavoidable"]])
        out["UT8_rd"][k] = {"n": len(rs), "unavoidable": int(sum(r["unavoidable"] for r in rs)),
                            "unavoidable_by_dist": {d: int(sum(r["unavoidable"] for r in rs if r["dist"] == d))
                                                    for d in ("D1", "D2", "D3", "D4")},
                            "max_F_hi": float(fh.max()), "preload_slips": int(sum(r["preload_slip"] for r in rs)),
                            "onset_disp_mm_p50_p99": [float(np.percentile([r["rec"]["onset"]["disp_at_onset_mm"]
                                                                           for r in rs], q)) for q in (50, 99)]}
        oq = {"found_rate": float(np.mean([r["rec"]["onset"]["found"] for r in rs]))}
        lm = np.log([r["inst"]["mu"] for r in rs])
        for s in sigmas:
            est = np.log([mu_hat(r["inst"]["mass"], math.exp(onset_log_force(r, s))) for r in rs])
            oq[f"sigma_{s}"] = {"corr_logmuhat_logmu": float(np.corrcoef(est, lm)[0, 1]),
                                "err_mean": float(np.mean(est - lm)), "err_sd": float(np.std(est - lm))}
        out["onset_quality"][k] = oq
    base = {(r["family"], r["obj"], r["dist"]): r for r in load("labels/pilot_F[1-4].jsonl")}
    for sh in ("S1", "S3"):
        d = [math.log(r["F_mid"]) - math.log(base[(r["family"], r["obj"], r["dist"])]["F_mid"])
             for r in load(f"labels/pilot_F*_{sh}.jsonl")
             if not r["unavoidable"] and not base[(r["family"], r["obj"], r["dist"])]["unavoidable"]]
        out[f"shift_{sh}_dlogF"] = {"mean": float(np.mean(d)), "sd": float(np.std(d)), "n": len(d)}

    # ---- cross-fitted predictors on the ID pilot pool (avoidable instances)
    allrows = [base[k] for k in sorted(base)]
    rows = [r for r in allrows if not r["unavoidable"]]
    n_unav = len(allrows) - len(rows)
    y = np.log([r["F_hi"] for r in rows])
    ymid = np.array([r["F_mid"] for r in rows])
    fhi = np.array([r["F_hi"] for r in rows])
    groups = np.array([f"{r['family']}_{r['obj']}" for r in rows])
    dist = np.array([r["dist"] for r in rows])
    logmu = np.log([r["inst"]["mu"] for r in rows])
    arms = [("P", 0.0), ("S", 0.0), ("full", 0.0), ("oracle", 0.0)]
    arms += [("full_rd", s) for s in sigmas] + [("P_onset", s) for s in sigmas]
    names = [f"{fs}" if fs in ("P", "S", "full", "oracle") else f"{fs}@{s}" for fs, s in arms]
    preds = Parallel(n_jobs=a.jobs)(delayed(oof_predict)(matrix(rows, fs, sigma=s), y, groups, a.configs)
                                    for fs, s in arms)
    oof = dict(zip(names, preds))
    oof["CSF-1"] = np.log([f_nom(r["inst"]["mass"], r["dist"], r["inst"]["amp"], r["inst"]["freq"]) for r in rows])
    for s in sigmas:
        oof[f"CSF-muhat@{s}"] = np.log([f_nom_muhat(r["inst"]["mass"], r["dist"], r["inst"]["amp"], r["inst"]["freq"],
                                                    math.exp(onset_log_force(r, s))) for r in rows])
    out["D_mu_cvR2"] = {k: cv_r2(y - p, logmu, groups) for k, p in oof.items()}
    out["oof_pinball"] = {k: float(np.mean(np.maximum(TAU * (y - p), (TAU - 1) * (y - p)))) for k, p in oof.items()}

    objs = np.unique(groups)
    rng = np.random.default_rng(12)
    res = {k: {"RE": [], "slip": []} for k in oof}
    pairs = {}
    for s in sigmas:
        pairs[f"H2a_vs_CSF-1@{s}"] = ("CSF-1", f"full_rd@{s}")
        pairs[f"H2a_vs_P@{s}"] = ("P", f"full_rd@{s}")
        pairs[f"H2b_vs_CSF-muhat@{s}"] = (f"CSF-muhat@{s}", f"full_rd@{s}")
        pairs[f"H4e_onset_only@{s}"] = (f"P_onset@{s}", f"full_rd@{s}")
    pairs["squeeze_vs_S"] = ("S", "full")
    dpair = {k: [] for k in pairs}
    for _ in range(a.splits):
        cal_objs = set(rng.choice(objs, size=len(objs) // 2, replace=False))
        cal = np.array([g in cal_objs for g in groups])
        ev = ~cal
        re_k = {}
        for k, p in oof.items():
            sc = y - p
            F = np.empty(len(y))
            for st in np.unique(dist):
                idx = dist == st
                F[idx] = np.minimum(np.exp(p[idx] + qhat(sc[cal & idx], ALPHA)), F_MAX)
            re_k[k] = float(((F[ev] - ymid[ev]) / ymid[ev]).mean())
            res[k]["RE"].append(re_k[k])
            res[k]["slip"].append(float(np.mean(F[ev] < fhi[ev])))
        for k, (c, t) in pairs.items():
            dpair[k].append(re_k[c] - re_k[t])
    out["conformal_pilot_rd"] = {k: {"RE_mean": float(np.mean(v["RE"])), "RE_sd_over_splits": float(np.std(v["RE"])),
                                     "slip_label_mean_avoidable": float(np.mean(v["slip"]))} for k, v in res.items()}
    out["paired_D"] = {k: {"mean": float(np.mean(v)), "sd_over_splits": float(np.std(v))} for k, v in dpair.items()}
    s_full = y - oof[f"full_rd@{0.2 if 0.2 in sigmas else sigmas[0]}"]
    q25, q75 = np.percentile(s_full, [25, 75])
    out["eta_pilot_rd"] = {"IQR_scores_full_rd": float(q75 - q25), "eta": float(0.1 * (q75 - q25))}
    out["n_rows_ID"] = len(allrows)
    out["n_unavoidable_ID"] = n_unav
    out["feature_dims"] = {n: int(matrix(rows[:1], fs, sigma=s).shape[1]) for n, (fs, s) in zip(names, arms)}
    json.dump(out, open(os.path.join(ROOT, "pilot_analysis_rd.json"), "w"), indent=1)
    print(json.dumps({k: out[k] for k in ("H1M_pilot_rd", "UT8_rd", "conformal_pilot_rd", "paired_D", "D_mu_cvR2")},
                     indent=1))


if __name__ == "__main__":
    main()
