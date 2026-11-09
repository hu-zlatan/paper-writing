"""Addendum 08h: H1c, H3-S, H4b, D-FID, H2-M mass-noise (secondary). Writes results/v1/sec08h_<part>.json.
usage (from papers/p2/code): python secondaries_08h.py {h1c,h3s,h4b,dfid,massnoise} [--draws N]
"""
import argparse
import copy
import json
import os
from statistics import NormalDist

import numpy as np

import comp_selection
from certgrip.baselines import f_nom
from certgrip.featsets import noisy_mass, touch_only
from certgrip.io import ROOT
from secondaries_08f import F_MAX, PRED, Data, ci, resample
from secondaries_08g import forces, re

PRED.update({"RAWQ@0.01": "a001_full_rd_s0.2_seed0", "RAWQ@0.05": "a005_full_rd_s0.2_seed0",
             "RAWQ@0.1": "a010_full_rd_s0.2_seed0", "RAWQ@0.2": "a020_full_rd_s0.2_seed0",
             "P_fid#0": "a010_P_fid_seed0", "full_rd_fid#0": "a010_full_rd_fid_s0.2_seed0",
             "P_mn#0": "a010_P_mn_seed0", "full_rd_mn#0": "a010_full_rd_mn_s0.2_seed0"})
ALPHAS = (0.01, 0.05, 0.10, 0.20)


def idsplit(D, sp):
    return D.sel(lambda r: r["pool"] == "id" and r["shift"] is None and r["split"] == sp)


# ---------------------------------------------------------------- H1c
def part_h1c(draws, seed=2040):
    D = Data([f"RAWQ@{a}" for a in (0.01, 0.05, 0.1, 0.2)])
    g = json.load(open(os.path.join(ROOT, "v1/preds/g_full_rd_s0.2_seed0.json")))
    mu, sd = np.array(g["mu"]), np.array(g["sigma_hat"])
    sel, tst = idsplit(D, "select"), idsplit(D, "test")
    sel = sel[~D.unav[sel]]
    bs_, bt = D.by_obj(sel), D.by_obj(tst)

    def slips(si, ti):
        out = {}
        for al in ALPHAS:
            lq = D.lg[f"RAWQ@{al:g}" if al != 0.10 else "RAWQ@0.1"]
            fq = np.minimum(F_MAX, np.exp(lq[ti]))
            fg_ = np.minimum(F_MAX, np.exp(mu[ti] + NormalDist().inv_cdf(1 - al) * sd[ti]))
            c = np.quantile(np.log(D.fhi[si]) - lq[si], 1 - al)
            fv = np.minimum(F_MAX, np.exp(lq[ti] + c))
            out[al] = {k: float(np.mean(F < D.fhi[ti])) for k, F in (("RAW-Q", fq), ("RAW-G", fg_), ("RAW-Qv", fv))}
        return out
    pt = slips(sel, tst)
    rng = np.random.default_rng(seed)
    boot = [slips(resample(bs_, rng), resample(bt, rng)) for _ in range(draws)]
    res = {}
    for al in ALPHAS:
        res[f"alpha_{al}"] = {}
        for m in ("RAW-Q", "RAW-G", "RAW-Qv"):
            d = np.array([b[al][m] - al for b in boot]); lo, hi = ci(d)
            res[f"alpha_{al}"][m] = {"slip": pt[al][m], "slip_minus_alpha": pt[al][m] - al, "CI**": [lo, hi],
                                     "outside_pm_0.5alpha": bool(lo > 0.5 * al or hi < -0.5 * al),
                                     "inside_pm_0.25alpha": bool(-0.25 * al < lo and hi < 0.25 * al)}
    miss = {m: res["alpha_0.05"][m]["outside_pm_0.5alpha"] for m in ("RAW-Q", "RAW-G")}
    allin = all(res[f"alpha_{al}"][m]["inside_pm_0.25alpha"] for al in ALPHAS for m in ("RAW-Q", "RAW-G", "RAW-Qv"))
    return {"purpose": "08h §1 H1c uncalibrated targeters (CertGrip-full features), label slip on id test",
            "results": res, "miss_at_0.05": miss,
            "decision": ("failure (all inside ±0.25 alpha)" if allin else
                         ("confirmed (RAW-Q and RAW-G miss at alpha 0.05)" if all(miss.values()) else "partly confirmed / not confirmed")),
            "draws": draws}


# ---------------------------------------------------------------- H3-S
def part_h3s(draws):
    import h3_streams as H

    def cum_metrics(F, slip, cap, fmid, avoid):
        c = (slip[:, H.T_PRE:H.T_PRE + 500].astype(float) - H.ALPHA).sum(1)
        return {"RE_window": c, "slip_label_window": c, "capped_window": c, "slip_label_all": c}
    H.metrics = cum_metrics
    pools = H.load_pools(); qoff, eta = H.offline(pools["cal"])
    res = {}
    for s in ("S1", "S2", "S3", "S1m"):
        point, *_ = H.shift_summary(pools, s, qoff, eta)
        bs = H.bootstrap(pools, s, qoff, eta, draws)
        d = bs["OQTdecay-CertGrip"][:, 0] - bs["OQT-CertGrip"][:, 0]
        dc = point["OQTdecay-CertGrip"]["RE_window"] - point["OQT-CertGrip"]["RE_window"]
        lo, hi = ci(d)
        res[s] = {"C_constant": point["OQT-CertGrip"]["RE_window"], "C_decay": point["OQTdecay-CertGrip"]["RE_window"],
                  "Delta_C": dc, "CI**": [lo, hi],
                  "decision": "confirmed (lower > 0)" if lo > 0 else ("failure (upper <= 0)" if hi <= 0 else "inconclusive")}
    return {"purpose": "08h §2 H3-S cumulative (slip - alpha) over shifted steps 1-500, decay minus constant eta",
            "eta": eta, "results": res, "draws": draws}


# ---------------------------------------------------------------- H4b
def part_h4b(draws, seed=2041):
    arms = ["P#0", "full_rd@0.2#0", "P_fid#0", "full_rd_fid#0"]
    D = Data(arms)
    cal, tst = idsplit(D, "cal"), idsplit(D, "test")
    bc, bt = D.by_obj(cal), D.by_obj(tst)

    def ev(ci_, ti):
        R = {a: re(D, forces(D, a, ci_, ti), ti) for a in arms}
        dfid = 1 - R["full_rd_fid#0"] / R["P_fid#0"]; d = 1 - R["full_rd@0.2#0"] / R["P#0"]
        return {"RE": R, "D_FID": dfid, "D": d, "D_FID_minus_half_D": dfid - 0.5 * d}
    pt = ev(cal, tst)
    rng = np.random.default_rng(seed)
    boot = [ev(resample(bc, rng), resample(bt, rng)) for _ in range(draws)]
    out = {"RE": pt["RE"]}
    for k in ("D_FID", "D", "D_FID_minus_half_D"):
        out[k] = {"value": pt[k], "CI**": ci([b[k] for b in boot])}
    lo, hi = out["D_FID"]["CI**"]
    out["decision"] = ("failure (D_FID inside ±0.05)" if -0.05 < lo and hi < 0.05 else
                       ("confirmed (D_FID >= 0.5 D, lower > 0)" if out["D_FID_minus_half_D"]["CI**"][0] > 0 else "not confirmed"))
    return {"purpose": "08h §3 H4b identifier control (label route)", "results": out, "draws": draws}


# ---------------------------------------------------------------- D-FID
def part_dfid(draws, seed=2042):
    from sklearn.ensemble import HistGradientBoostingClassifier
    D = Data([])
    tr = [D.rows[i] for i in idsplit(D, "train")]
    ti = idsplit(D, "test"); te = [D.rows[i] for i in ti]
    out = {}
    for name, onset in (("touch_only", False), ("touch_plus_onset", True)):
        Xtr = np.array([touch_only(r, onset) for r in tr]); ytr = [r["family"] for r in tr]
        clf = HistGradientBoostingClassifier(random_state=0).fit(Xtr, ytr)
        ok = clf.predict(np.array([touch_only(r, onset) for r in te])) == np.array([r["family"] for r in te])
        bt = D.by_obj(ti); pos = {i: p for p, i in enumerate(ti)}
        rng = np.random.default_rng(seed)
        bs = [ok[[pos[i] for i in resample(bt, rng)]].mean() for _ in range(draws)]
        out[name] = {"accuracy": float(ok.mean()), "CI95": [float(np.percentile(bs, 2.5)), float(np.percentile(bs, 97.5))],
                     "chance": 0.25, "n_test": len(te)}
    return {"purpose": "08h §4 D-FID family classification from touch-only features", "results": out, "draws": draws}


# ---------------------------------------------------------------- H2-M mass-noise
def part_massnoise(draws, seed=2043):
    D = Data(["P_mn#0", "full_rd_mn#0", "full_rd@0.2#0", "CSF-1"])
    D.lg["CSF-1-mn"] = np.log([f_nom(noisy_mass(r), r["dist"], r["inst"]["amp"], r["inst"]["freq"]) for r in D.rows])
    D.fam = np.array([r["family"] for r in D.rows])
    sel = idsplit(D, "select")
    rows_mn = []
    for i in sel:
        r = copy.deepcopy(D.rows[i]); r["inst"]["mass"] = noisy_mass(D.rows[i]); rows_mn.append(r)
    cand, winner, _, _ = comp_selection.select(rows_mn, D.lg["P_mn#0"][sel])
    comp = {"CSF-1": "CSF-1-mn", "Mondrian-CSF": "CSF-1-mn", "CertGrip-P": "P_mn#0"}[winner]
    cell = winner == "Mondrian-CSF"
    cal, tst = idsplit(D, "cal"), idsplit(D, "test")
    bc, bt = D.by_obj(cal), D.by_obj(tst)

    def ev(ci_, ti):
        R = {"full_rd_mn": re(D, forces(D, "full_rd_mn#0", ci_, ti), ti),
             "COMP_mn": re(D, forces(D, comp, ci_, ti, cell=cell), ti),
             "full_rd": re(D, forces(D, "full_rd@0.2#0", ci_, ti), ti), "CSF-1": re(D, forces(D, "CSF-1", ci_, ti), ti)}
        return {"RE": R, "D_mn": 1 - R["full_rd_mn"] / R["COMP_mn"], "D_H2a": 1 - R["full_rd"] / R["CSF-1"]}
    pt = ev(cal, tst)
    rng = np.random.default_rng(seed)
    boot = [ev(resample(bc, rng), resample(bt, rng)) for _ in range(draws)]
    out = {"COMP_selection_mn": {"candidates": cand, "winner": winner}, "RE": pt["RE"]}
    for k in ("D_mn", "D_H2a"):
        out[k] = {"value": pt[k], "CI**": ci([b[k] for b in boot])}
    out["change"] = {"value": pt["D_mn"] - pt["D_H2a"], "CI**": ci([b["D_mn"] - b["D_H2a"] for b in boot])}
    return {"purpose": "08h §5 H2-M mass-noise (10 % multiplicative, per object)", "results": out, "draws": draws}


PARTS = {"h1c": part_h1c, "h3s": part_h3s, "h4b": part_h4b, "dfid": part_dfid, "massnoise": part_massnoise}

if __name__ == "__main__":
    ap = argparse.ArgumentParser(); ap.add_argument("part", choices=list(PARTS)); ap.add_argument("--draws", type=int)
    a = ap.parse_args()
    res = PARTS[a.part](a.draws or {"dfid": 500}.get(a.part, 2000))
    json.dump(res, open(os.path.join(ROOT, f"v1/sec08h_{a.part}.json"), "w"), indent=1)
    print(json.dumps(res, indent=1)[:5000])
