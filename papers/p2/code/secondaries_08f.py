"""Addendum 08f: remaining secondaries / diagnostics of p2 (all reported as secondary, CI** = 1.25 / 98.75 percentiles).

Parts (each writes results/v1/sec08f_<part>.json):
  tail   H2-T  P95 ratio T = P95(RE CertGrip-full s0.2) / P95(RE CSF-1), routes CRC 08c, CRC 08e, label rule.
  label  H4c   D = 1 - RE(full_rd_shuf)/RE(P);  H2-M  D_nm = 1 - RE(full_rd no mass)/RE(P no mass), with the
               with-mass label-route D(full_rd vs P) on the same draws.
  h3b    H3-B  p_obs vs location prediction p_pred = 1 - F_ID(q - Delta) on S1 / S1m; S3 and S2 p_obs.
  dmu    D-mu  CV R^2 of log mu -> residual (5-fold by object), 500-draw object bootstrap 95 % interval.
  ut3    UT3   1,000 object-level re-splits of the id cal+test pool, label-rule coverage band per cell.
Bootstrap (tail / label / h3b): cal objects and test objects resampled within family, q-hat / lambda-hat refitted.
usage (from papers/p2/code): python secondaries_08f.py <part> [--draws N]
"""
import argparse
import hashlib
import json
import math
import os
from statistics import NormalDist

import numpy as np

from certgrip.baselines import f_nom, f_nom_muhat
from certgrip.featsets import onset_log_force
from certgrip.io import ROOT, key, load_rows

ALPHA, F_MAX, LO_P, HI_P = 0.10, 100.0, 1.25, 98.75
DISTS = ("D1", "D2", "D3", "D4")
PRED = {"P#0": "a010_P_seed0", "S#0": "a010_S_seed0", "full#0": "a010_full_seed0", "oracle#0": "a010_oracle_seed0",
        "full_rd@0.2#0": "a010_full_rd_s0.2_seed0", "P_onset@0.2#0": "a010_P_onset_s0.2_seed0",
        "full_rd_shuf@0.2#0": "a010_full_rd_shuf_s0.2_seed0", "P_nomass#0": "a010_P_nomass_seed0",
        "full_rd_nomass@0.2#0": "a010_full_rd_nomass_s0.2_seed0"}
for _s in (0.0, 0.1, 0.4):
    PRED[f"full_rd@{_s}#0"] = f"a010_full_rd_s{_s}_seed0"


def qhat(scores, alpha=ALPHA):
    sc = np.sort(scores); n = len(sc); k = math.ceil((n + 1) * (1 - alpha))
    return sc[k - 1] if k <= n else np.inf


def ci(v):
    return [float(np.percentile(v, LO_P)), float(np.percentile(v, HI_P))]


class Data:
    def __init__(self, arms):
        self.rows = load_rows("v1/labels/*.jsonl")
        ks = hashlib.sha256(json.dumps([list(key(r)) for r in self.rows]).encode()).hexdigest()
        self.lg = {}
        for a in arms:
            if a == "CSF-1":
                self.lg[a] = np.log([f_nom(r["inst"]["mass"], r["dist"], r["inst"]["amp"], r["inst"]["freq"]) for r in self.rows])
            elif a.startswith("CSF-muhat@"):
                s = float(a.split("@")[1])
                self.lg[a] = np.log([f_nom_muhat(r["inst"]["mass"], r["dist"], r["inst"]["amp"], r["inst"]["freq"],
                                                 math.exp(onset_log_force(r, s))) for r in self.rows])
            else:
                p = json.load(open(os.path.join(ROOT, "v1/preds", PRED[a] + ".json")))
                assert p["keys_sha256"] == ks, a
                self.lg[a] = np.asarray(p["log_pred"], dtype=float)
        nan = float("nan")
        g = lambda f: np.array([r[f] if r[f] is not None else nan for r in self.rows], dtype=float)
        self.fhi, self.fmid = g("F_hi"), g("F_mid")
        self.unav = np.array([r["unavoidable"] for r in self.rows])
        self.st = np.array([r["dist"] for r in self.rows])
        self.obj = [(r["pool"], r["family"], r["obj"]) for r in self.rows]
        self.sel = lambda f: np.array([i for i, r in enumerate(self.rows) if f(r)])

    def by_obj(self, idx):
        d = {}
        for i in idx:
            d.setdefault(self.obj[i], []).append(i)
        return d


def resample(byo, rng):
    """Within-family object bootstrap of an {obj: [rows]} map; returns a row-index array (repeats allowed)."""
    fams = sorted({o[:2] for o in byo})
    out = []
    for f in fams:
        os_ = [o for o in byo if o[:2] == f]
        for j in rng.integers(0, len(os_), len(os_)):
            out += byo[os_[j]]
    return np.array(out)


def label_forces(D, a, ci_, ti):
    F = np.empty(len(ti))
    q = {}
    for s in DISTS:
        c = ci_[D.st[ci_] == s]
        q[s] = qhat(np.log(D.fhi[c]) - D.lg[a][c])
        m = D.st[ti] == s
        F[m] = np.minimum(F_MAX, np.exp(D.lg[a][ti][m] + q[s]))
    return F, q


# ---------------------------------------------------------------- H2-T
def part_tail(draws, seed=2028):
    import analysis_crc as AC
    D = Data(["CSF-1", "full_rd@0.2#0"])
    cal = D.sel(lambda r: r["pool"] == "id" and r["shift"] is None and r["split"] == "cal")
    tst = D.sel(lambda r: r["pool"] == "id" and r["shift"] is None and r["split"] == "test")
    T, C = "full_rd@0.2#0", "CSF-1"

    def p95_label(ci_, ti):
        out = {}
        for a in (T, C):
            F, _ = label_forces(D, a, ci_, ti)
            ok = ~D.unav[ti]
            out[a] = float(np.percentile((F[ok] - D.fmid[ti][ok]) / D.fmid[ti][ok], 95))
        return out

    routes = {}
    rng = np.random.default_rng(seed)
    bc, bt = D.by_obj(cal), D.by_obj(tst)
    pt = p95_label(cal, tst)
    bs = []
    for _ in range(draws):
        m = p95_label(resample(bc, rng), resample(bt, rng)); bs.append(m[T] / m[C])
    routes["label"] = {"P95": pt, "T": pt[T] / pt[C], "CI**": ci(bs)}
    for v2 in (False, True):
        AC.V2 = v2
        G, keys, _, rep, missing, dup = AC.load_real()
        assert not missing and not dup
        X = AC.build(G, keys, rep)
        objs = X["obj"]; split = np.array(X["split"])
        byo = {}
        for i, o in enumerate(objs):
            byo.setdefault(("id",) + tuple(o), []).append(i)
        bcal = {o: v for o, v in byo.items() if split[v[0]] == "cal"}; btst = {o: v for o, v in byo.items() if split[v[0]] == "test"}

        def p95_crc(ci_, ti):
            out = {}
            for a in (T, C):
                j_t = np.empty(len(ti), dtype=int)
                for s in np.unique(X["strata"]):
                    j, _ = AC.lam_index(X["L"][a][ci_[X["strata"][ci_] == s]])
                    j_t[X["strata"][ti] == s] = j
                Ft = X["F"][a][ti, j_t]; av = X["avoid"][ti]; rr = X["ref"]["mid"][ti][av]
                out[a] = float(np.percentile((Ft[av] - rr) / rr, 95))
            return out
        ci0 = np.array([i for v in bcal.values() for i in v]); ti0 = np.array([i for v in btst.values() for i in v])
        pt = p95_crc(ci0, ti0)
        bs = []
        for _ in range(draws):
            m = p95_crc(resample(bcal, rng), resample(btst, rng)); bs.append(m[T] / m[C])
        routes["crc_08e" if v2 else "crc_08c"] = {"P95": pt, "T": pt[T] / pt[C], "CI**": ci(bs)}
    for r in routes.values():
        lo, hi = r["CI**"]
        r["decision"] = "pass (upper < 1.10)" if hi < 1.10 else ("failure (lower > 1.10)" if lo > 1.10 else "inconclusive")
    return {"purpose": "08f §1 H2-T: P95 relative-excess ratio CertGrip-full s0.2 / CSF-1", "routes": routes,
            "primary_route": "crc_08c", "draws": draws}


# ---------------------------------------------------------------- H4c, H2-M (label route)
def part_label(draws, seed=2029):
    arms = ["P#0", "full_rd@0.2#0", "full_rd_shuf@0.2#0", "P_nomass#0", "full_rd_nomass@0.2#0"]
    D = Data(arms)
    cal = D.sel(lambda r: r["pool"] == "id" and r["shift"] is None and r["split"] == "cal")
    tst = D.sel(lambda r: r["pool"] == "id" and r["shift"] is None and r["split"] == "test")
    assert not D.unav[cal].any() and not D.unav[tst].any()
    C = {"H4c_shuf_vs_P": ("full_rd_shuf@0.2#0", "P#0", 0.05),
         "H2M_nomass_full_rd_vs_P": ("full_rd_nomass@0.2#0", "P_nomass#0", None),
         "H2M_ref_withmass_full_rd_vs_P": ("full_rd@0.2#0", "P#0", None)}

    def ev(ci_, ti):
        out = {}
        for a in arms:
            F, _ = label_forces(D, a, ci_, ti)
            out[a] = {"RE": float(np.mean((F - D.fmid[ti]) / D.fmid[ti])), "slip_label": float(np.mean(F < D.fhi[ti]))}
        return out
    pt = ev(cal, tst)
    rng = np.random.default_rng(seed); bc, bt = D.by_obj(cal), D.by_obj(tst)
    boot = {k: [] for k in C}; bdiff = []
    for _ in range(draws):
        m = ev(resample(bc, rng), resample(bt, rng))
        for k, (t, c, _) in C.items():
            boot[k].append(1 - m[t]["RE"] / m[c]["RE"])
        bdiff.append(boot["H2M_nomass_full_rd_vs_P"][-1] - boot["H2M_ref_withmass_full_rd_vs_P"][-1])
    res = {}
    for k, (t, c, mg) in C.items():
        d = 1 - pt[t]["RE"] / pt[c]["RE"]; lo, hi = ci(boot[k])
        if mg is None:
            dec = "report only"
        elif -mg < lo and hi < mg:
            dec = "equivalence (pass)"
        elif lo > mg:
            dec = "failure (shuffled beats P by > 5 %)"
        else:
            dec = "inconclusive"
        res[k] = {"target": t, "comparator": c, "margin": mg, "D": d, "CI**": [lo, hi], "decision": dec}
    pd = res["H2M_nomass_full_rd_vs_P"]["D"] - res["H2M_ref_withmass_full_rd_vs_P"]["D"]
    res["H2M_change_nomass_minus_withmass"] = {"value": pd, "CI**": ci(bdiff)}
    return {"purpose": "08f §2-3 H4c shuffled-touch and H2-M no-mass (label route)", "arms": pt, "contrasts": res,
            "draws": draws}


# ---------------------------------------------------------------- H3-B
def part_h3b(draws, seed=2030):
    arms = ["P#0", "S#0", "full#0", "CSF-1", "full_rd@0.2#0"]
    tested = arms[:4]
    D = Data(arms)
    cal = D.sel(lambda r: r["pool"] == "id" and r["shift"] is None and r["split"] == "cal")
    tid = D.sel(lambda r: r["pool"] == "id" and r["shift"] is None and r["split"] == "test")
    pools = {sh: D.sel(lambda r, sh=sh: r["pool"] == "id" and r["shift"] == sh) for sh in ("S1", "S1m", "S3")}
    s2 = D.sel(lambda r: r["pool"] == "s2")
    DELTA = {"S1": 0.511, "S1m": 0.105}

    def ev(ci_, ti_id, sh_idx):
        out = {}
        for a in arms:
            q = {s: qhat(np.log(D.fhi[ci_[D.st[ci_] == s]]) - D.lg[a][ci_[D.st[ci_] == s]]) for s in DISTS}
            r = {}
            for sh, idx in sh_idx.items():
                qq = np.array([q[s] for s in D.st[idx]])
                F = np.minimum(F_MAX, np.exp(D.lg[a][idx] + qq))
                slip = np.where(D.unav[idx], True, F < np.nan_to_num(D.fhi[idx], nan=np.inf))
                r[sh] = {"p_obs": float(slip.mean())}
                if sh in DELTA:
                    sid = np.log(D.fhi[ti_id]) - D.lg[a][ti_id]
                    pp = [np.mean(sid[D.st[ti_id] == s] > q[s] - DELTA[sh]) * np.sum(D.st[idx] == s) for s in DISTS]
                    r[sh]["p_pred"] = float(np.sum(pp) / len(idx))
                    r[sh]["diff"] = r[sh]["p_obs"] - r[sh]["p_pred"]
            out[a] = r
        return out

    # the shift-pool instances belong to id test objects; S2 objects are resampled within the s2 pool
    sh_all = dict(pools); sh_all["S2"] = s2
    pt = ev(cal, tid, sh_all)
    rng = np.random.default_rng(seed)
    bc, bt, b2 = D.by_obj(cal), D.by_obj(tid), D.by_obj(s2)
    bsh = {sh: D.by_obj(idx) for sh, idx in pools.items()}
    boot = {a: {sh: [] for sh in sh_all} for a in arms}
    for _ in range(draws):
        ci_ = resample(bc, rng)
        # resample id test objects once; the same objects carry their shifted copies
        fams = sorted({o[:2] for o in bt}); chosen = []
        for f in fams:
            os_ = [o for o in bt if o[:2] == f]
            chosen += [os_[j] for j in rng.integers(0, len(os_), len(os_))]
        ti = np.array([i for o in chosen for i in bt[o]])
        sh_idx = {sh: np.array([i for o in chosen for i in bsh[sh].get(o, [])]) for sh in pools}
        sh_idx["S2"] = resample(b2, rng)
        m = ev(ci_, ti, sh_idx)
        for a in arms:
            for sh in sh_all:
                boot[a][sh].append(m[a][sh]["diff"] if sh in DELTA else m[a][sh]["p_obs"])
    res = {}
    for a in arms:
        res[a] = {}
        for sh in sh_all:
            r = dict(pt[a][sh]); lo, hi = ci(boot[a][sh])
            if sh in DELTA:
                r["diff_CI**"] = [lo, hi]
                if a not in tested:
                    r["decision"] = "not tested (08b §6: probe-arm predictions never specified)"
                elif -0.02 < lo and hi < 0.02:
                    r["decision"] = "pass (|p_obs - p_pred| <= 0.02)"
                elif lo > 0.02 or hi < -0.02:
                    r["decision"] = "failure (not a pure location shift)"
                else:
                    r["decision"] = "inconclusive"
            else:
                r["p_obs_CI**"] = [lo, hi]
                if sh == "S2":
                    r["decision"] = ("break (|p_obs - alpha| >= 0.05)" if lo - ALPHA > 0.05 or hi - ALPHA < -0.05
                                     else "no break shown")
                else:
                    r["decision"] = "report (predicted direction: up)"
            r["n"] = int(len(sh_all[sh]))
            res[a][sh] = r
    return {"purpose": "08f §4 H3-B offline breakage magnitude (label rule, frozen offline q-hat)", "Delta": DELTA,
            "results": res, "draws": draws}


# ---------------------------------------------------------------- D-mu
def cv_r2(resid, logmu, groups):
    """Cross-validated R^2 of a linear fit of log mu -> residual (5-fold by object) — the pilot's cv_r2."""
    from sklearn.linear_model import LinearRegression
    from sklearn.model_selection import GroupKFold
    pred = np.zeros(len(resid))
    for tr, te in GroupKFold(n_splits=5).split(resid, resid, groups):
        lr = LinearRegression().fit(logmu[tr, None], resid[tr])
        pred[te] = lr.predict(logmu[te, None])
    return float(1 - np.sum((resid - pred) ** 2) / np.sum((resid - resid.mean()) ** 2))


def part_dmu(draws, seed=2031):
    arms = ["P#0", "S#0", "full#0", "full_rd@0.0#0", "full_rd@0.1#0", "full_rd@0.2#0", "full_rd@0.4#0",
            "P_onset@0.2#0", "CSF-1", "CSF-muhat@0.0", "CSF-muhat@0.1", "CSF-muhat@0.2", "CSF-muhat@0.4", "oracle#0"]
    D = Data(arms)
    idx = D.sel(lambda r: r["pool"] == "id" and r["shift"] is None and r["split"] in ("cal", "test"))
    logmu = np.log([D.rows[i]["inst"]["mu"] for i in idx])
    objs = [D.obj[i] for i in idx]
    byo = {}
    for p, o in enumerate(objs):
        byo.setdefault(o, []).append(p)
    rng = np.random.default_rng(seed)
    draws_idx = []
    for _ in range(draws):
        fams = sorted({o[:2] for o in byo}); pos, grp = [], []
        for f in fams:
            os_ = [o for o in byo if o[:2] == f]
            for n_, j in enumerate(rng.integers(0, len(os_), len(os_))):
                pos += byo[os_[j]]; grp += [f"{f}_{n_}"] * len(byo[os_[j]])
        draws_idx.append((np.array(pos), grp))
    res = {}
    for a in arms:
        r = np.log(D.fhi[idx]) - D.lg[a][idx]
        g = [f"{o[1]}_{o[2]}" for o in objs]
        pt = cv_r2(r, logmu, g)
        bs = [cv_r2(r[p], logmu[p], gr) for p, gr in draws_idx]
        res[a] = {"cvR2": pt, "CI95": [float(np.percentile(bs, 2.5)), float(np.percentile(bs, 97.5))],
                  "le_0.05": bool(pt <= 0.05)}
    return {"purpose": "08f §5 D-mu: grouped 5-fold CV R^2 of log mu -> residual on the 4,800 id cal+test instances",
            "results": res, "draws": draws, "n": int(len(idx))}


# ---------------------------------------------------------------- UT3
def part_ut3(draws, seed=3):
    arms = ["P#0", "S#0", "full#0", "full_rd@0.2#0", "CSF-1"]
    alphas, ns = (0.01, 0.05, 0.10, 0.20), (50, 500)
    D = Data(arms)
    idx = D.sel(lambda r: r["pool"] == "id" and r["shift"] is None and r["split"] in ("cal", "test"))
    assert not D.unav[idx].any()
    objs = sorted({D.obj[i] for i in idx})
    pos = {o: {} for o in objs}
    for i in idx:
        pos[D.obj[i]][D.st[i]] = i
    M = {s: np.array([pos[o][s] for o in objs]) for s in DISTS}     # (n_obj,) row index per stratum
    S = {a: {s: np.log(D.fhi[M[s]]) - D.lg[a][M[s]] for s in DISTS} for a in arms}
    K = len(arms) * len(DISTS) * len(alphas) * len(ns)
    z = NormalDist().inv_cdf(1 - 0.05 / (2 * K))
    rng = np.random.default_rng(seed)
    miss = {(a, s, al, n): [] for a in arms for s in DISTS for al in alphas for n in ns}
    for _ in range(draws):
        perm = rng.permutation(len(objs))
        for n in ns:
            c, t = perm[:n], perm[n:]
            for a in arms:
                for s in DISTS:
                    sc = S[a][s]; cs = np.sort(sc[c])
                    for al in alphas:
                        k = math.ceil((n + 1) * (1 - al)); q = cs[k - 1] if k <= n else np.inf
                        miss[(a, s, al, n)].append(float(np.mean(sc[t] > q)))
    cells, n_pass, worst = [], 0, None
    for (a, s, al, n), v in miss.items():
        v = np.array(v); m, sd = float(v.mean()), float(v.std(ddof=1)); se = sd / math.sqrt(len(v))
        lo_b, hi_b = al - 1 / (n + 1) - z * se, al + z * se
        ok = lo_b <= m <= hi_b
        n_pass += ok
        dev = max(lo_b - m, m - hi_b)
        cells.append({"arm": a, "stratum": s, "alpha": al, "n": n, "mean_miss": m, "sd": sd, "band": [lo_b, hi_b], "pass": bool(ok)})
        if worst is None or dev > worst[0]:
            worst = (dev, cells[-1])
    return {"purpose": "08f §6 UT3: label-rule split conformal coverage over 1,000 object-level re-splits",
            "K": K, "z": z, "n_pass": int(n_pass), "worst_cell": worst[1], "cells": cells, "draws": draws,
            "n_objects": len(objs)}


PARTS = {"tail": part_tail, "label": part_label, "h3b": part_h3b, "dmu": part_dmu, "ut3": part_ut3}

if __name__ == "__main__":
    ap = argparse.ArgumentParser()
    ap.add_argument("part", choices=list(PARTS))
    ap.add_argument("--draws", type=int, default=None)
    a = ap.parse_args()
    dflt = {"dmu": 500, "ut3": 1000}.get(a.part, 2000)
    res = PARTS[a.part](a.draws or dflt)
    out = os.path.join(ROOT, f"v1/sec08f_{a.part}.json")
    json.dump(res, open(out, "w"), indent=1)
    print(json.dumps({k: v for k, v in res.items() if k not in ("cells",)}, indent=1)[:6000])
