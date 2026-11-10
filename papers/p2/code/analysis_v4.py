"""Amendment 11 (p2 v4) read-out. Written and committed before any v4 replay result exists.

Inputs: results/v4/crc_grids_11_{f4,c4,np}.json, replays results/v4/crc_{f4,c4,np}/*.jsonl (main.py crc), labels
results/v4/labels/*.jsonl. Refuses to compute unless every grid instance has exactly one replay line (--check prints
counts only).
Per arm and stratum: per-stratum CRC on the monotonised physical slip loss (analysis_crc.lam_index), alpha 0.10;
RE = mean (F - F*_mid) / F*_mid on avoidable test rows. Matched slip (09 A1 recipe on the wide grid W): shift every
stratum's lambda-hat index by k in -8..+8 (clipped to 0..80), RE interpolated at test physical slip 0.10 (None if not
bracketed). D(a vs b) = 1 - RE(a) / RE(b). CI** = 1.25 / 98.75 percentiles of 2,000 object-cluster draws within family
(cal and test objects resampled, lambda-hat refitted), seed 2027.
Confirmatory C1-C5 (Holm at 5 % over the five p-values):
  C1 f4 D_match(CSF-muhat@0.2 vs CSF-1)       superiority iff Holm p < 0.05 and point > 0
  C2 f4 D_match(full_rd@0.2#0 vs CSF-muhat@0.2) equivalence iff Holm-adjusted TOST p (max of the two one-sided
                                                 shares at -0.10 / +0.10) < 0.05
  C3 f4 D_crc(full_rd@0.2#0 vs CSF-1)          superiority as C1
  C4 c4 D_match(CSF-muhat@0.2 vs CSF-fam)      superiority as C1
  C5 c4 D_match(full_rd@0.2#0 vs CSF-fam)      superiority as C1
  p (two-sided) = min(1, 2 min(share <= 0, share >= 0)) over the valid draws. Any arm of a decision with lambda-hat on
  grid index 0 or 80 in any stratum (point estimate) -> that decision is "grid floor / ceiling - not interpretable".
Secondary (CI**, unadjusted): S1 sigma band (C1-C3 at sigma 0.1 / 0.4); S2 shrunk plug-in; S3 friction-width sweep on
f4 (centred log-mu windows of relative width 1.0 / 0.75 / 0.5 / 0.25 of log(1.0 / 0.3), CRC refitted inside);
S4 per-family CRC-route D on c4; S5 CRC-route versions of C1, C2, C4, C5 and c4 contrasts vs CSF-1; S6 no-probe CSF-1
grasp (lambda-hat, slip, hold force, integrated force-time, measured break-even, point values); S7 200 re-splits (A1
recipe) on f4.
Writes results/v4/v4_analysis.json.  usage (from papers/p2/code): python analysis_v4.py [--check] [--draws N]"""
import argparse
import glob
import json
import math
import os

import numpy as np

import analysis_crc as A
import analysis_v3_a as V
from certgrip.io import ROOT, key, load_rows
from certgrip.sim import DT, T_PRELOAD, T_PROBE, T_RAMP, RD2

ALPHA, SESOI, SLIP_MATCH, KS = 0.10, 0.10, 0.10, tuple(range(-8, 9))
F0 = 32.7
FULL, MUHAT, COMP, SHR, FAM = "full_rd@0.2#0", "CSF-muhat@0.2", "CSF-1", "CSF-shrunk@0.2", "CSF-fam"


def load(name, labs):
    G = json.load(open(os.path.join(ROOT, f"v4/crc_grids_11_{name}.json")))
    keys = [tuple(k) for k in G["instances"]]
    rep = {}
    for f in sorted(glob.glob(os.path.join(ROOT, f"v4/crc_{name}/*.jsonl"))):
        for line in open(f):
            r = json.loads(line)
            if "key" in r:
                rep.setdefault(tuple(r["key"]), []).append(r)
    missing = [k for k in keys if k not in rep]
    dup = sum(1 for k in keys if len(rep.get(k, [])) > 1)
    D = None
    if not missing and not dup:
        D = {"L": {}, "F": {}, "strata": np.array([k[3] for k in keys]), "obj": [(k[1], k[2]) for k in keys],
             "split": [labs[k]["split"] for k in keys], "avoid": np.array([not labs[k]["unavoidable"] for k in keys]),
             "mu": np.array([labs[k]["inst"]["mu"] for k in keys]), "keys": keys}
        for a in G["arms"]:
            D["L"][a] = np.array([rep[k][0]["slip"][a] for k in keys], dtype=bool)
            D["F"][a] = np.array([rep[k][0]["F"][a] for k in keys], dtype=float)
            D["L"][a][~D["avoid"]] = True
        nan = float("nan")
        D["ref"] = {"mid": np.array([labs[k]["F_mid"] if labs[k]["F_mid"] is not None else nan for k in keys])}
        D["by_obj"] = {}
        for i, o in enumerate(D["obj"]):
            D["by_obj"].setdefault(o, []).append(i)
    return G, keys, missing, dup, D


def arm_eval(D, arm, ci, ti):
    """CRC lambda-hat per stratum on ci; returns point metrics, floor flag and the matched-slip RE."""
    L, F = D["L"][arm], D["F"][arm]
    J = L.shape[1]
    st_c, st_t = D["strata"][ci], D["strata"][ti]
    j_t = np.empty(len(ti), dtype=int)
    edge = False
    for s in np.unique(D["strata"]):
        j, _ = A.lam_index(L[ci[st_c == s]])
        edge |= j in (0, J - 1)
        j_t[st_t == s] = j
    av = D["avoid"][ti]
    rr = D["ref"]["mid"][ti][av]

    def at(jj):
        Ft = F[ti, jj]
        return float(L[ti, jj].mean()), float(np.mean((Ft[av] - rr) / rr)), Ft

    slip, re_, Ft = at(j_t)
    front = [at(np.clip(j_t + k, 0, J - 1))[:2] for k in KS]          # slip non-increasing in k
    match = None
    for (s0, r0), (s1, r1) in zip(front[:-1], front[1:]):
        if (s0 - SLIP_MATCH) * (s1 - SLIP_MATCH) <= 0 and s0 != s1:
            match = r0 + (s0 - SLIP_MATCH) / (s0 - s1) * (r1 - r0)
            break
    return {"slip": slip, "RE": re_, "RE_match": match, "edge": bool(edge), "F_t": Ft, "j_t": j_t}


def dd(a, b):
    return None if a is None or b is None or b == 0 else 1 - a / b


def pool_stats(D, ci, ti, contrasts):
    m = {a: arm_eval(D, a, ci, ti) for a in {x for c in contrasts.values() for x in c[:2]}}
    v = {}
    for name, (t, c, kind) in contrasts.items():
        v[name] = dd(m[t]["RE_match"], m[c]["RE_match"]) if kind == "match" else dd(m[t]["RE"], m[c]["RE"])
    return v, m


def p_two(vals):
    x = np.array([u for u in vals if u is not None])
    return float(min(1.0, 2 * min(np.mean(x <= 0), np.mean(x >= 0)))) if len(x) else None


def p_tost(vals):
    x = np.array([u for u in vals if u is not None])
    return float(max(np.mean(x <= -SESOI), np.mean(x >= SESOI))) if len(x) else None


def holm(ps):
    order = np.argsort(ps); m = len(ps); adj = np.empty(m); run = 0.0
    for r, i in enumerate(order):
        run = max(run, min(1.0, (m - r) * ps[i])); adj[i] = run
    return adj


def run_pool(D, contrasts, draws, seed=2027, sub=None):
    """sub: optional boolean mask over instances (object-level, e.g. a mu window)."""
    cal_objs, test_objs = V.groups_of(D)
    if sub is not None:
        keep = {D["obj"][i] for i in np.where(sub)[0]}
        cal_objs = [o for o in cal_objs if o in keep]
        test_objs = [o for o in test_objs if o in keep]
    ci0, ti0 = V.split_idx(D, cal_objs), V.split_idx(D, test_objs)
    point, m = pool_stats(D, ci0, ti0, contrasts)
    boot = {k: [] for k in contrasts}
    for ci, ti in V.boot_draws(D, cal_objs, test_objs, draws, seed):
        v, _ = pool_stats(D, ci, ti, contrasts)
        for k in contrasts:
            boot[k].append(v[k])
    rows = {}
    for k, (t, c, kind) in contrasts.items():
        rows[k] = {"target": t, "comparator": c, "kind": kind, "point": point[k], "CI**": V.ci_of(boot[k]),
                   "valid_draws": int(sum(x is not None for x in boot[k])), "p_two_sided": p_two(boot[k]),
                   "p_tost": p_tost(boot[k]), "edge": bool(m[t]["edge"] or m[c]["edge"])}
    arms = {a: {"slip": x["slip"], "RE": x["RE"], "RE_match": x["RE_match"], "edge": x["edge"],
                "hold_F_N_mean": float(np.mean(x["F_t"][D["avoid"][ti0]]))} for a, x in m.items()}
    return {"n_cal_objects": len(cal_objs), "n_test_objects": len(test_objs), "rows": rows, "arms": arms}, (ci0, ti0)


def probe_phases(labs, keys_test):
    """Shared rd-protocol force-time per avoidable test instance, as analysis_v3_a.a7_force (incl. return + re-hold)."""
    pre, sq, rd, ret, reh = [], [], [], [], []
    floor, T = RD2["floor"], RD2["T"]
    for k in keys_test:
        rec = labs[k]["rec"]
        pre.append(F0 * T_PRELOAD)
        sq.append(float(np.mean([fr[0] for fr in rec["touch_probe"]])) * T_PROBE)
        on = rec.get("onset") or {}
        t_on = (on.get("frames") or int(T / DT)) * DT * RD2["frame_steps"] if on.get("found") else T
        t_on = min(t_on, T)
        rd.append(F0 * T / math.log(floor) * (floor ** (t_on / T) - 1))
        ret.append(0.5 * (F0 * floor ** (t_on / T) + F0) * RD2["t_up"])
        reh.append(F0 * 0.1)
    return {"preload": float(np.mean(pre)), "squeeze": float(np.mean(sq)), "rampdown": float(np.mean(rd)),
            "return": float(np.mean(ret)), "rehold": float(np.mean(reh))}


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--check", action="store_true")
    ap.add_argument("--draws", type=int, default=2000)
    a = ap.parse_args()
    labs = {key(r): r for r in load_rows("v4/labels/*.jsonl")}
    pools = {n: load(n, labs) for n in ("f4", "c4", "np")}
    for n, (G, keys, missing, dup, _) in pools.items():
        print(f"{n}: instances {len(keys)}, with replays {len(keys) - len(missing)}, duplicates {dup}")
    if a.check or any(p[2] or p[3] for p in pools.values()):
        if not a.check:
            print("incomplete: refusing to analyse")
        return
    Df, Dc, Dn = pools["f4"][4], pools["c4"][4], pools["np"][4]
    res = {"purpose": "p2 amendment 11 (v4) read-out", "draws": a.draws, "alpha": ALPHA}
    # ---- f4: C1-C3, S1, S2, S5
    cf = {"C1": (MUHAT, COMP, "match"), "C2": (FULL, MUHAT, "match"), "C3": (FULL, COMP, "crc"),
          "S2_shrunk_vs_muhat": (SHR, MUHAT, "match"), "S2_shrunk_vs_CSF1": (SHR, COMP, "match"),
          "S5_C1_crc": (MUHAT, COMP, "crc"), "S5_C2_crc": (FULL, MUHAT, "crc")}
    for s in (0.1, 0.4):
        cf[f"S1_C1@{s}"] = (f"CSF-muhat@{s}", COMP, "match")
        cf[f"S1_C2@{s}"] = (f"full_rd@{s}#0", f"CSF-muhat@{s}", "match")
        cf[f"S1_C3@{s}"] = (f"full_rd@{s}#0", COMP, "crc")
    res["f4"], (ci_f, ti_f) = run_pool(Df, cf, a.draws)
    # ---- c4: C4, C5, S4, S5
    cc = {"C4": (MUHAT, FAM, "match"), "C5": (FULL, FAM, "match"), "S5_C4_crc": (MUHAT, FAM, "crc"),
          "S5_C5_crc": (FULL, FAM, "crc"), "S5_muhat_vs_CSF1_match": (MUHAT, COMP, "match"),
          "S5_full_vs_CSF1_match": (FULL, COMP, "match"), "S5_fam_vs_CSF1_match": (FAM, COMP, "match")}
    res["c4"], (ci_c, ti_c) = run_pool(Dc, cc, a.draws)
    # S4 per-family CRC-route D on c4 (pooled lambda-hat, family test rows)
    s4 = {}
    m = {x: arm_eval(Dc, x, ci_c, ti_c) for x in (FULL, MUHAT, FAM, COMP)}
    fam_t = np.array([Dc["obj"][i][0] for i in ti_c])
    av_t = Dc["avoid"][ti_c]
    rr = Dc["ref"]["mid"][ti_c]
    for f in ("F1", "F2", "F3", "F4"):
        mk = (fam_t == f) & av_t
        re_f = {x: float(np.mean((m[x]["F_t"][mk] - rr[mk]) / rr[mk])) for x in m}
        sl_f = {x: float(Dc["L"][x][ti_c, m[x]["j_t"]][fam_t == f].mean()) for x in m}
        s4[f] = {"RE": re_f, "slip": sl_f, "D_muhat_vs_fam": dd(re_f[MUHAT], re_f[FAM]),
                 "D_full_vs_fam": dd(re_f[FULL], re_f[FAM])}
    res["c4"]["S4_per_family_point"] = s4
    # ---- Holm over C1-C5
    rows = {"C1": res["f4"]["rows"]["C1"], "C2": res["f4"]["rows"]["C2"], "C3": res["f4"]["rows"]["C3"],
            "C4": res["c4"]["rows"]["C4"], "C5": res["c4"]["rows"]["C5"]}
    ps = [rows[k]["p_tost"] if k == "C2" else rows[k]["p_two_sided"] for k in rows]
    adj = holm(np.array([1.0 if p is None else p for p in ps]))
    dec = {}
    for (k, r), pa in zip(rows.items(), adj):
        if r["edge"]:
            d = "grid floor / ceiling - not interpretable"
        elif k == "C2":
            d = "equivalence" if pa < 0.05 else ("superiority" if r["CI**"] and r["CI**"][0] > 0 else
                                                 "inferiority" if r["CI**"] and r["CI**"][1] < 0 else "not shown")
        else:
            d = "superiority" if (pa < 0.05 and r["point"] is not None and r["point"] > 0) else (
                "inferiority" if (pa < 0.05 and r["point"] is not None and r["point"] < 0) else "not shown")
        dec[k] = {"point": r["point"], "CI**": r["CI**"], "p": r["p_tost"] if k == "C2" else r["p_two_sided"],
                  "p_holm": float(pa), "decision": d}
    res["confirmatory"] = dec
    # ---- S3 friction-width sweep on f4
    lo, hi = math.log(0.3), math.log(1.0)
    c0, half = 0.5 * (lo + hi), 0.5 * (hi - lo)
    sweep = {}
    for w in (1.0, 0.75, 0.5, 0.25):
        mask = np.abs(np.log(Df["mu"]) - c0) <= w * half + 1e-12
        r, _ = run_pool(Df, {"D_muhat_vs_CSF1": (MUHAT, COMP, "match"), "D_full_vs_CSF1": (FULL, COMP, "match")},
                        a.draws, sub=mask)
        r["mu_window"] = [float(math.exp(c0 - w * half)), float(math.exp(c0 + w * half))]
        sweep[str(w)] = r
    res["S3_width_sweep"] = sweep
    # ---- S6 no-probe CSF-1 grasp vs rd arms (f4 test split)
    mn = arm_eval(Dn, COMP, ci_f, ti_f)
    avn = Dn["avoid"][ti_f]
    Fn = float(np.mean(mn["F_t"][avn]))
    keys_t = [Df["keys"][i] for i in ti_f[Df["avoid"][ti_f]]]
    ph = probe_phases(labs, keys_t)
    rd_shared = sum(ph.values())
    s6 = {"noprobe_CSF1": {"slip": mn["slip"], "edge": mn["edge"], "hold_F_N_mean": Fn,
                           "lam_idx_by_stratum": {str(s): int(mn["j_t"][Dn["strata"][ti_f] == s][0])
                                                  for s in np.unique(Dn["strata"])}},
          "rd_shared_phases_Ns": ph, "arms": {}}
    np_fixed = F0 * T_PRELOAD
    for x in (FULL, MUHAT, COMP):
        e = arm_eval(Df, x, ci_f, ti_f)
        Fx = float(np.mean(e["F_t"][Df["avoid"][ti_f]]))
        integ = lambda fixed, F, T: fixed + 0.5 * (F0 + F) * T_RAMP + F * T
        row = {"hold_F_N_mean": Fx, "slip": e["slip"],
               "integrated_Ns": {str(T): integ(rd_shared, Fx, T) for T in (1, 5, 30)},
               "noprobe_integrated_Ns": {str(T): integ(np_fixed, Fn, T) for T in (1, 5, 30)}}
        gap = (rd_shared + 0.5 * (F0 + Fx) * T_RAMP) - (np_fixed + 0.5 * (F0 + Fn) * T_RAMP)
        row["break_even_T_s"] = gap / (Fn - Fx) if Fn > Fx else None
        s6["arms"][x] = row
    res["S6_noprobe"] = s6
    # ---- S7 re-splits on f4 (A1 recipe: CRC and LTT, arms full / muhat / CSF-1)
    co, to = V.groups_of(Df)
    res["S7_resplits"] = V.a1_resplits(Df, co, to, 200)
    os.makedirs(os.path.join(ROOT, "v4"), exist_ok=True)
    json.dump(res, open(os.path.join(ROOT, "v4", "v4_analysis.json"), "w"), indent=1)
    print(json.dumps(res["confirmatory"], indent=1))


if __name__ == "__main__":
    main()
