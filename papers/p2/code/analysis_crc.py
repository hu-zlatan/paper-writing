"""08c read-out of the CRC route (H2a / H2b primary, sigma curve, H4e, per-seed D): conformal risk control on the
monotonised physical slip loss, per disturbance stratum, and relative excess at the chosen lambda.

Inputs: results/v1/crc_grids.json (arms, grids, instance list), results/v1/crc/*.jsonl (main.py crc replays), labels
(F*_lo / F*_mid / F*_hi, unavoidable) from results/v1/labels. Refuses to compute anything unless every grid instance
has exactly one replay line (prints counts only), so a partial read is impossible.

Per arm and stratum: L~_i(lambda_j) = max_{j' >= j} L_i(lambda_j'); lambda-hat = the smallest grid point with
(n R~_n + 1)/(n + 1) <= alpha, else the largest (flagged). Test: F_i = the replayed grid force at lambda-hat of i's
stratum; RE = mean (F - F*_ref)/F*_ref over avoidable test instances (ref = mid primary, lo / hi robustness);
physical slip = mean L_i(lambda-hat) over all test instances (unavoidable instances count as slips at every lambda);
label slip = mean 1{F < F*_hi}. D = 1 - RE(target)/RE(comparator), paired on the same instances and calibration draw.
Bootstrap: 2,000 draws resampling calibration objects and test objects within family (the four instances of an
object move together), lambda-hat recomputed per draw; CI** = 1.25 / 98.75 percentiles (08b §4).
Decisions (07_hypotheses H2 at the 08b level 0.0125): H2a superiority iff D >= 0.10 and lower > 0 for mid, lo and hi;
equivalence iff CI** inside (-0.10, 0.10); inferiority iff upper < 0; else not confirmed. H2b likewise (TOST ±0.10).
sigma* = the smallest sigma whose D(H2a) lower limit is < 0.10 (descriptive).
Writes results/v1/crc_analysis.json.  usage (from papers/p2/code): python analysis_crc.py [--check] [--draws 2000]
"""
import argparse
import glob
import json
import os

import numpy as np

from certgrip.io import ROOT, key, load_rows

ALPHA, SESOI, LO_P, HI_P = 0.10, 0.10, 1.25, 98.75
TARGET = "full_rd@0.2#0"
SIGMAS = (0.0, 0.1, 0.2, 0.4)


def contrasts():
    c = {"H2a": (TARGET, "CSF-1"), "H2b": (TARGET, "CSF-muhat@0.2"), "H4e_vs_onset_only": (TARGET, "P_onset@0.2#0")}
    for s in SIGMAS:
        c[f"H2a_sigma@{s}"] = (f"full_rd@{s}#0", "CSF-1")
        c[f"H2b_sigma@{s}"] = (f"full_rd@{s}#0", f"CSF-muhat@{s}")
    for k in (1, 2, 3, 4):
        c[f"H2a_seed{k}"] = (f"full_rd@0.2#{k}", "CSF-1")
        c[f"H2b_seed{k}"] = (f"full_rd@0.2#{k}", "CSF-muhat@0.2")
    return c


def lam_index(Lcal, alpha=ALPHA):
    """Lcal: (n, J) bool physical losses on the grid (ascending lambda). Returns (j_hat, at_max)."""
    Lt = np.maximum.accumulate(Lcal[:, ::-1].astype(float), axis=1)[:, ::-1]   # monotonised, non-increasing in j
    n = Lt.shape[0]
    ok = (n * Lt.mean(axis=0) + 1) / (n + 1) <= alpha
    if not ok.any():
        return Lt.shape[1] - 1, True
    return int(np.argmax(ok)), False


def evaluate(D, cal_idx, test_idx):
    """D: dict with L[arm] (N, J) bool, F[arm] (N, J), strata (N,), ref{mid,lo,hi} (N,), avoid (N,), fhi (N,).
    cal_idx / test_idx: instance index arrays (repeats allowed). Returns per-arm metrics."""
    out = {}
    st_c, st_t = D["strata"][cal_idx], D["strata"][test_idx]
    for arm in D["L"]:
        L, F = D["L"][arm], D["F"][arm]
        j_t = np.empty(len(test_idx), dtype=int)
        lam, atmax = {}, {}
        for s in np.unique(D["strata"]):
            j, m = lam_index(L[cal_idx[st_c == s]])
            j_t[st_t == s] = j
            lam[str(s)], atmax[str(s)] = j, m
        Ft = F[test_idx, j_t]
        av = D["avoid"][test_idx]
        r = {"lam_idx": lam, "at_max": atmax,
             "slip_phys": float(L[test_idx, j_t].mean()),
             "slip_label": float(np.mean(np.where(av, Ft < D["fhi"][test_idx], True)))}
        for k, ref in D["ref"].items():
            rr = ref[test_idx][av]
            r[f"RE_{k}"] = float(np.mean((Ft[av] - rr) / rr))
        out[arm] = r
    return out


def decide(d, lo, hi, d_lohi=None):
    if d >= SESOI and lo > 0 and (d_lohi is None or all(x[0] >= SESOI and x[1] > 0 for x in d_lohi)):
        return "superiority"
    if lo > -SESOI and hi < SESOI:
        return "equivalence"
    if hi < 0:
        return "inferiority"
    return "not confirmed"


def analyse(D, draws=2000, seed=2026):
    cal_objs = sorted({o for o, s in zip(D["obj"], D["split"]) if s == "cal"})
    test_objs = sorted({o for o, s in zip(D["obj"], D["split"]) if s == "test"})
    by_obj = {}
    for i, o in enumerate(D["obj"]):
        by_obj.setdefault(o, []).append(i)
    cal_idx = np.array([i for o in cal_objs for i in by_obj[o]])
    test_idx = np.array([i for o in test_objs for i in by_obj[o]])
    point = evaluate(D, cal_idx, test_idx)
    C = contrasts()
    C = {k: v for k, v in C.items() if v[0] in D["L"] and v[1] in D["L"]}
    refs = list(D["ref"])

    def dvals(m):
        return {k: {r: 1 - m[t][f"RE_{r}"] / m[c][f"RE_{r}"] for r in refs} for k, (t, c) in C.items()}

    rng = np.random.default_rng(seed)
    fam = lambda o: o[0]
    groups = {}
    for part, objs in (("cal", cal_objs), ("test", test_objs)):
        for o in objs:
            groups.setdefault((part, fam(o)), []).append(o)
    boot = {k: {r: [] for r in refs} for k in C}
    boot_re = {a: [] for a in D["L"]}
    for _ in range(draws):
        ci, ti = [], []
        for (part, _f), objs in groups.items():
            pick = rng.integers(0, len(objs), len(objs))
            idx = [i for p in pick for i in by_obj[objs[p]]]
            (ci if part == "cal" else ti).extend(idx)
        m = evaluate(D, np.array(ci), np.array(ti))
        for k, v in dvals(m).items():
            for r in refs:
                boot[k][r].append(v[r])
        for a in D["L"]:
            boot_re[a].append(m[a]["RE_mid"])
    pd = dvals(point)
    res = {}
    for k in C:
        ci = {r: [float(np.percentile(boot[k][r], LO_P)), float(np.percentile(boot[k][r], HI_P))] for r in refs}
        lohi = [(pd[k][r], ci[r][0]) for r in refs if r != "mid"]
        res[k] = {"target": C[k][0], "comparator": C[k][1], "D": {r: float(pd[k][r]) for r in refs}, "CI**": ci,
                  "decision": decide(pd[k]["mid"], *ci["mid"], d_lohi=lohi if k.startswith("H2a") else None)}
    sig = [s for s in SIGMAS if f"H2a_sigma@{s}" in res and res[f"H2a_sigma@{s}"]["CI**"]["mid"][0] < SESOI]
    arms = {a: dict(point[a], RE_mid_CI=[float(np.percentile(boot_re[a], LO_P)), float(np.percentile(boot_re[a], HI_P))])
            for a in point}
    return {"arms": arms, "contrasts": res, "sigma_star": (min(sig) if sig else None),
            "n_cal_instances": int(len(cal_idx)), "n_test_instances": int(len(test_idx)), "draws": draws}


V2 = False


def load_real():
    G = json.load(open(os.path.join(ROOT, "v1/crc_grids_v2.json" if V2 else "v1/crc_grids.json")))
    keys = [tuple(k) for k in G["instances"]]
    idx = {k: i for i, k in enumerate(keys)}
    rep = {}
    for f in sorted(glob.glob(os.path.join(ROOT, "v1/crc_v2/*.jsonl" if V2 else "v1/crc/*.jsonl"))):
        for line in open(f):
            r = json.loads(line)
            if "key" in r:
                rep.setdefault(tuple(r["key"]), []).append(r)
    missing = [k for k in keys if k not in rep]
    dup = sum(1 for k in keys if len(rep.get(k, [])) > 1)
    return G, keys, idx, rep, missing, dup


def build(G, keys, rep):
    lab = {key(r): r for r in load_rows("v1/labels/*.jsonl")}
    N, arms = len(keys), list(G["arms"])
    D = {"L": {}, "F": {}, "strata": np.array([k[3] for k in keys]), "obj": [(k[1], k[2]) for k in keys],
         "split": [lab[k]["split"] for k in keys], "avoid": np.array([not lab[k]["unavoidable"] for k in keys])}
    for a in arms:
        D["L"][a] = np.array([rep[k][-1]["slip"][a] for k in keys], dtype=bool)
        D["F"][a] = np.array([rep[k][-1]["F"][a] for k in keys], dtype=float)
        D["L"][a][~D["avoid"]] = True
    nan = float("nan")
    D["ref"] = {r: np.array([lab[k][f"F_{r}"] if lab[k][f"F_{r}"] is not None else nan for k in keys])
                for r in ("mid", "lo", "hi")}
    D["fhi"] = D["ref"]["hi"]
    return D


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--check", action="store_true")
    ap.add_argument("--draws", type=int, default=2000)
    ap.add_argument("--v2", action="store_true", help="addendum 08e per-stratum grids")
    a = ap.parse_args()
    global V2
    V2 = a.v2
    G, keys, idx, rep, missing, dup = load_real()
    print(f"instances: {len(keys)}, with replays: {len(keys) - len(missing)}, duplicates: {dup}")
    if a.check or missing:
        if missing and not a.check:
            print("incomplete: refusing to analyse")
        return
    res = analyse(build(G, keys, rep), draws=a.draws)
    res["purpose"] = "p2 08c CRC read-out (H2a / H2b primary, sigma curve, H4e, per-seed D)"
    json.dump(res, open(os.path.join(ROOT, "v1/crc_analysis_v2.json" if V2 else "v1/crc_analysis.json"), "w"), indent=1)
    for k in ("H2a", "H2b", "H4e_vs_onset_only"):
        c = res["contrasts"][k]
        print(f"{k}: D {c['D']['mid']:.3f} CI** {c['CI**']['mid'][0]:.3f}..{c['CI**']['mid'][1]:.3f} -> {c['decision']}")


if __name__ == "__main__":
    main()
