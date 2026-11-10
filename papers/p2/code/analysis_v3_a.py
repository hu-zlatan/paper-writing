"""Amendment 10 part A (p2 v3): analyses of the existing 08c / 08e CRC replays, no new simulation.
A1 repeated object re-splits (R = 200, seed 3031, within family with the v1 cal / test object counts): CRC and LTT
   lambda-hat refitted on each split's cal part; test physical slip overall and per stratum.
A2 slip / RE tables per stratum, family x stratum cell, friction quintile (true mu of test rows), per seed.
A4 losing sub-pool (08g H2-R definition: mu in [0.5, 0.8] and amplitude inside the per-stratum inter-quartile range of
   the avoidable cal + test rows) and the two restrictions separately, on the CRC route (CRC refitted inside the
   sub-pool's cal rows).
A5 empirically tuned per-stratum margin: smallest grid lambda with monotonised calibration slip <= alpha (no (n+1)).
A6 direct learned vs plug-in: D(full_rd@0.2#0 vs CSF-muhat@0.2) at matched slip and under LTT.
A7 force in newtons at the CRC lambda-hat; shared protocol phases (preload, squeeze, ramp-down) force-time.
CI** as code/analysis_crc.py (2,000 object-cluster draws within family, seed 2026, 1.25 / 98.75 percentiles).
Writes results/v3/a_analysis[_08e].json.  usage (from papers/p2/code): python analysis_v3_a.py [--v2] [--draws N]
[--splits R]"""
import argparse
import json
import math
import os

import numpy as np

import analysis_crc as A
import analysis_v2_a as B
from certgrip.io import key, load_rows
from certgrip.sim import DT, T_PRELOAD, T_PROBE, RD2

ALPHA = 0.10
FULL, MUHAT, COMP = "full_rd@0.2#0", "CSF-muhat@0.2", "CSF-1"
SPLIT_ARMS = (FULL, MUHAT, COMP)
F0 = 32.7


def lam_emp(Lcal, alpha=ALPHA):
    Lt = np.maximum.accumulate(Lcal[:, ::-1].astype(float), axis=1)[:, ::-1]
    ok = Lt.mean(axis=0) <= alpha
    return (Lt.shape[1] - 1, True) if not ok.any() else (int(np.argmax(ok)), False)


RULES = {"crc": A.lam_index, "ltt": B.lam_ltt, "emp": lam_emp}


def chosen(D, arm, cal_idx, test_idx, rule="crc"):
    L = D["L"][arm]
    st_c, st_t = D["strata"][cal_idx], D["strata"][test_idx]
    j_t = np.empty(len(test_idx), dtype=int)
    for s in np.unique(D["strata"]):
        sel = cal_idx[st_c == s]
        j, _ = RULES[rule](L[sel]) if len(sel) else (L.shape[1] - 1, True)
        j_t[st_t == s] = j
    return j_t


def metrics(D, arm, cal_idx, test_idx, rule="crc"):
    j_t = chosen(D, arm, cal_idx, test_idx, rule)
    L, F = D["L"][arm], D["F"][arm]
    av = D["avoid"][test_idx]
    Ft = F[test_idx, j_t]
    rr = D["ref"]["mid"][test_idx][av]
    return {"slip_phys": float(L[test_idx, j_t].mean()), "RE_mid": float(np.mean((Ft[av] - rr) / rr)),
            "j_t": j_t, "F_t": Ft}


def split_idx(D, objs):
    by = D["by_obj"]
    return np.array([i for o in objs for i in by[o]], dtype=int)


def groups_of(D):
    cal_objs = sorted({o for o, s in zip(D["obj"], D["split"]) if s == "cal"})
    test_objs = sorted({o for o, s in zip(D["obj"], D["split"]) if s == "test"})
    return cal_objs, test_objs


def boot_draws(D, cal_objs, test_objs, draws, seed=2026):
    g = {}
    for part, objs in (("cal", cal_objs), ("test", test_objs)):
        for o in objs:
            g.setdefault((part, o[0]), []).append(o)
    rng = np.random.default_rng(seed)
    for _ in range(draws):
        ci, ti = [], []
        for (part, _f), objs in g.items():
            pick = rng.integers(0, len(objs), len(objs))
            (ci if part == "cal" else ti).extend(i for p in pick for i in D["by_obj"][objs[p]])
        yield np.array(ci, dtype=int), np.array(ti, dtype=int)


def ci_of(vals):
    v = [x for x in vals if x is not None and np.isfinite(x)]
    if not v:
        return None
    return [float(np.percentile(v, A.LO_P)), float(np.percentile(v, A.HI_P))]


def label(c):
    if c is None:
        return None
    return "superiority" if c[0] > 0 else ("inferiority" if c[1] < 0 else "not shown")


# ---------------- A1
def a1_resplits(D, cal_objs, test_objs, R, seed=3031):
    fam_all = {}
    for o in cal_objs + test_objs:
        fam_all.setdefault(o[0], []).append(o)
    n_cal = {f: sum(1 for o in cal_objs if o[0] == f) for f in fam_all}
    rng = np.random.default_rng(seed)
    strata = [str(s) for s in np.unique(D["strata"])]
    rec = {r: {a: [] for a in SPLIT_ARMS} for r in ("crc", "ltt")}
    for _ in range(R):
        co, to = [], []
        for f, objs in sorted(fam_all.items()):
            perm = rng.permutation(len(objs))
            co += [objs[p] for p in perm[:n_cal[f]]]
            to += [objs[p] for p in perm[n_cal[f]:]]
        ci, ti = split_idx(D, co), split_idx(D, to)
        st_t = D["strata"][ti]
        for r in rec:
            for a in SPLIT_ARMS:
                j_t = chosen(D, a, ci, ti, r)
                l = D["L"][a][ti, j_t]
                rec[r][a].append({"all": float(l.mean()), **{s: float(l[st_t == s].mean()) for s in strata}})
    out = {}
    for r in rec:
        out[r] = {}
        for a in SPLIT_ARMS:
            rows = rec[r][a]
            allv = np.array([x["all"] for x in rows])
            per = {s: np.array([x[s] for x in rows]) for s in strata}
            anyst = np.mean([any(x[s] > ALPHA for s in strata) for x in rows])
            out[r][a] = {"mean_slip": float(allv.mean()), "share_above_alpha": float(np.mean(allv > ALPHA)),
                         "q90_slip": float(np.quantile(allv, 0.9)), "min_slip": float(allv.min()),
                         "max_slip": float(allv.max()), "share_any_stratum_above_alpha": float(anyst),
                         "per_stratum": {s: {"mean_slip": float(per[s].mean()),
                                             "share_above_alpha": float(np.mean(per[s] > ALPHA)),
                                             "q90_slip": float(np.quantile(per[s], 0.9))} for s in strata}}
    return {"R": R, "seed": seed, "rules": out}


# ---------------- A2
def a2_tables(D, cal_idx, test_idx, mu):
    st_t = D["strata"][test_idx]
    fam_t = np.array([D["obj"][i][0] for i in test_idx])
    mu_t = mu[test_idx]
    qs = np.quantile(mu_t, [0.2, 0.4, 0.6, 0.8])
    qbin = np.searchsorted(qs, mu_t, side="right")
    av = D["avoid"][test_idx]
    rr = D["ref"]["mid"][test_idx]
    out = {"mu_quintile_edges": [float(x) for x in qs], "arms": {}}
    for a in D["L"]:
        m = metrics(D, a, cal_idx, test_idx, "crc")
        l = D["L"][a][test_idx, m["j_t"]]
        ex = np.where(av, (m["F_t"] - rr) / np.where(av, rr, 1.0), np.nan)

        def cell(mask):
            return {"n": int(mask.sum()), "slip_phys": float(l[mask].mean()) if mask.any() else None,
                    "RE_mid": (float(np.nanmean(ex[mask & av])) if (mask & av).any() else None)}
        out["arms"][a] = {
            "overall": cell(np.ones(len(test_idx), bool)),
            "stratum": {str(s): cell(st_t == s) for s in np.unique(st_t)},
            "family_x_stratum": {f"{f}{s}": cell((fam_t == f) & (st_t == s))
                                 for f in sorted(set(fam_t)) for s in np.unique(st_t)},
            "mu_quintile": {str(q + 1): cell(qbin == q) for q in range(5)},
            "lam_idx": {str(s): int(m["j_t"][st_t == s][0]) for s in np.unique(st_t)}}
    return out


# ---------------- A4 / A5 / A6 (bootstrap)
def subpools(D, mu, amp, cal_idx, test_idx):
    pool = np.concatenate([cal_idx, test_idx])
    keep_mu = (mu >= 0.5) & (mu <= 0.8)
    keep_amp = np.zeros(len(mu), bool)
    for s in np.unique(D["strata"]):
        m = pool[(D["strata"][pool] == s) & D["avoid"][pool]]
        lo, hi = np.percentile(amp[m], [25, 75])
        ms = D["strata"] == s
        keep_amp[ms] = (amp[ms] >= lo) & (amp[ms] <= hi)
    return {"mu_and_amp": keep_mu & keep_amp, "mu_only": keep_mu, "amp_only": keep_amp}


def stat_set(D, ci, ti, pools):
    v = {}
    re = {}
    for a in (FULL, MUHAT, COMP):
        for r in ("crc", "emp", "ltt"):
            m = metrics(D, a, ci, ti, r)
            re[(a, r)] = m["RE_mid"]
            v[f"slip:{r}:{a}"] = m["slip_phys"]
            v[f"RE:{r}:{a}"] = m["RE_mid"]
    for a in (FULL, MUHAT):
        v[f"D_emp:{a}_vs_CSF-1crc"] = 1 - re[(a, "emp")] / re[(COMP, "crc")]
        v[f"D_emp:{a}_vs_CSF-1emp"] = 1 - re[(a, "emp")] / re[(COMP, "emp")]
    v["D_ltt:full_vs_muhat"] = 1 - re[(FULL, "ltt")] / re[(MUHAT, "ltt")]
    v["D_crc:full_vs_muhat"] = 1 - re[(FULL, "crc")] / re[(MUHAT, "crc")]
    # matched slip (09 A1 recipe) full vs muhat
    fr = {}
    for a in (FULL, MUHAT):
        pts = []
        for k in B.SHIFTS:
            j_t = np.clip(chosen(D, a, ci, ti, "crc") + k, 0, D["L"][a].shape[1] - 1)
            av = D["avoid"][ti]
            Ft = D["F"][a][ti, j_t]
            rr = D["ref"]["mid"][ti][av]
            pts.append((float(D["L"][a][ti, j_t].mean()), float(np.mean((Ft[av] - rr) / rr))))
        fr[a] = B.matched_re(pts)
    v["D_match:full_vs_muhat"] = (None if fr[FULL] is None or fr[MUHAT] is None else 1 - fr[FULL] / fr[MUHAT])
    # sub-pools on the CRC route
    for name, keep in pools.items():
        cs, ts = ci[keep[ci]], ti[keep[ti]]
        r = {a: metrics(D, a, cs, ts, "crc") for a in (FULL, MUHAT, COMP)}
        for a in r:
            v[f"sub:{name}:slip:{a}"] = r[a]["slip_phys"]
            v[f"sub:{name}:RE:{a}"] = r[a]["RE_mid"]
        v[f"sub:{name}:D:full_vs_CSF-1"] = 1 - r[FULL]["RE_mid"] / r[COMP]["RE_mid"]
        v[f"sub:{name}:D:muhat_vs_CSF-1"] = 1 - r[MUHAT]["RE_mid"] / r[COMP]["RE_mid"]
    return v


# ---------------- A7
def a7_force(D, cal_idx, test_idx, labs, keys):
    av = D["avoid"][test_idx]
    fmid = D["ref"]["mid"][test_idx][av]
    out = {"F_mid_N_quantiles_avoidable_test": {q: float(np.quantile(fmid, float(q))) for q in ("0.1", "0.5", "0.9")},
           "F_mid_N_max": float(fmid.max()), "F_mid_N_mean": float(fmid.mean()),
           "share_F_mid_above_preload": float(np.mean(fmid > F0)),
           "share_F_mid_above_squeeze_peak": float(np.mean(fmid > 1.5 * F0)),
           "n_avoidable_test": int(av.sum()), "arms": {}}
    for a in D["L"]:
        m = metrics(D, a, cal_idx, test_idx, "crc")
        F = m["F_t"][av]
        out["arms"][a] = {"hold_F_N_mean": float(F.mean()), "hold_F_N_median": float(np.median(F)),
                          "excess_N_mean": float(np.mean(F - fmid)), "excess_N_median": float(np.median(F - fmid))}
    # shared protocol phases (all arms are replayed with the same protocol before the hold)
    pre, sq, rd, ret, reh = [], [], [], [], []
    floor, T = RD2["floor"], RD2["T"]
    for i in test_idx[av]:
        rec = labs[keys[i]]["rec"]
        pre.append(F0 * T_PRELOAD)
        tp = rec["touch_probe"]
        sq.append(float(np.mean([fr[0] for fr in tp])) * T_PROBE)
        on = rec.get("onset") or {}
        t_on = (on.get("frames") or int(T / DT)) * DT * RD2["frame_steps"] if on.get("found") else T
        t_on = min(t_on, T)
        rd.append(F0 * T / math.log(floor) * (floor ** (t_on / T) - 1))
        # sim.py::_rd_touch_probe after the ramp-down: linear return F_end -> F0 over t_up, then F0 held 0.1 s
        # (added run 46 after stage-18 v3 review: these segments were omitted from the first A7 read-out)
        f_end = F0 * floor ** (t_on / T)
        ret.append(0.5 * (f_end + F0) * RD2["t_up"])
        reh.append(F0 * 0.1)
    out["shared_phase_force_time_Ns"] = {"preload_mean": float(np.mean(pre)), "squeeze_mean": float(np.mean(sq)),
                                         "rampdown_mean": float(np.mean(rd)), "return_mean": float(np.mean(ret)),
                                         "rehold_mean": float(np.mean(reh)),
                                         "note": "common to every arm in these replays; arms differ only in the hold"}
    return out


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--v2", action="store_true")
    ap.add_argument("--draws", type=int, default=2000)
    ap.add_argument("--splits", type=int, default=200)
    a = ap.parse_args()
    A.V2 = a.v2
    G, keys, idx, rep, missing, dup = A.load_real()
    assert not missing, "incomplete replays"
    D = A.build(G, keys, rep)
    labs = {key(r): r for r in load_rows("v1/labels/*.jsonl")}
    mu = np.array([labs[k]["inst"]["mu"] for k in keys])
    amp = np.array([labs[k]["inst"]["amp"] for k in keys])
    D["by_obj"] = {}
    for i, o in enumerate(D["obj"]):
        D["by_obj"].setdefault(o, []).append(i)
    cal_objs, test_objs = groups_of(D)
    cal_idx, test_idx = split_idx(D, cal_objs), split_idx(D, test_objs)
    pools = subpools(D, mu, amp, cal_idx, test_idx)
    res = {"purpose": "p2 v3 amendment 10 part A (secondary, existing replays)", "grids": "08e" if a.v2 else "08c",
           "alpha": ALPHA, "draws": a.draws,
           "subpool_sizes": {n: {"cal": int(p[cal_idx].sum()), "test": int(p[test_idx].sum())} for n, p in pools.items()}}
    res["A2_tables"] = a2_tables(D, cal_idx, test_idx, mu)
    res["A7_force"] = a7_force(D, cal_idx, test_idx, labs, keys)
    point = stat_set(D, cal_idx, test_idx, pools)
    boot = {k: [] for k in point}
    for ci, ti in boot_draws(D, cal_objs, test_objs, a.draws):
        v = stat_set(D, ci, ti, pools)
        for k in point:
            boot[k].append(v[k])
    res["A4_A5_A6"] = {k: {"point": point[k], "CI**": ci_of(boot[k]),
                           **({"decision": label(ci_of(boot[k]))} if ":D" in k or k.startswith("D_") else {})}
                       for k in point}
    res["A1_resplits"] = a1_resplits(D, cal_objs, test_objs, a.splits)
    os.makedirs(os.path.join(A.ROOT, "v3"), exist_ok=True)
    out = os.path.join(A.ROOT, "v3", "a_analysis_08e.json" if a.v2 else "a_analysis.json")
    json.dump(res, open(out, "w"), indent=1)
    print("wrote", out)


if __name__ == "__main__":
    main()
