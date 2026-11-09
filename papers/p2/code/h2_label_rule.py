"""08c §3 secondary: H2a / H2b under the label-rule split conformal route (the pre-H1-M plan) — per disturbance
stratum q-hat = the ceil((n+1)(1-alpha))-th smallest label score log F*_hi - log g on the id cal split (n = 500),
F = min(F_max, g exp(q-hat)) on the 2,800 id test instances, RE against F*_mid (lo / hi robustness), label slip.
No lambda-grid, so it is not limited by the CRC grid range. Same object-cluster bootstrap as analysis_crc.py (cal and
test objects within family, q-hat refitted per draw, 2,000 draws, CI** 1.25 / 98.75).
Writes results/v1/h2_label_rule.json.  usage (from papers/p2/code): python h2_label_rule.py
"""
import json
import math
import os

import numpy as np

from analysis_crc import contrasts, decide
from certgrip.io import ROOT, load_rows

ALPHA, F_MAX = 0.10, 100.0


def main(draws=2000, seed=2027):
    rows = load_rows("v1/labels/*.jsonl")
    G = json.load(open(os.path.join(ROOT, "v1/crc_grids.json")))
    base = [i for i, r in enumerate(rows) if r["pool"] == "id" and r["shift"] is None and r["split"] in ("cal", "test")]
    rs = [rows[i] for i in base]
    assert [[r["pool"], r["family"], r["obj"], r["dist"], r["shift"]] for r in rs] == G["instances"]
    lg = {a: np.asarray(v["log_g"]) for a, v in G["arms"].items()}          # same base predictors as the CRC route
    fhi = np.array([r["F_hi"] for r in rs]); ref = {k: np.array([r[f"F_{k}"] for r in rs]) for k in ("mid", "lo", "hi")}
    st = np.array([r["dist"] for r in rs]); split = np.array([r["split"] for r in rs])
    assert not any(r["unavoidable"] for r in rs)
    objs = [(r["family"], r["obj"]) for r in rs]
    by = {}
    for i, o in enumerate(objs):
        by.setdefault(o, []).append(i)
    cal_o = sorted({o for o, s in zip(objs, split) if s == "cal"}); test_o = sorted({o for o, s in zip(objs, split) if s == "test"})

    def ev(ci, ti):
        out = {}
        for a, g in lg.items():
            F = np.empty(len(ti))
            for s in ("D1", "D2", "D3", "D4"):
                c = ci[st[ci] == s]
                sc = np.sort(np.log(fhi[c]) - g[c]); n = len(sc); k = math.ceil((n + 1) * (1 - ALPHA))
                q = sc[k - 1] if k <= n else np.inf
                m = st[ti] == s
                F[m] = np.minimum(F_MAX, np.exp(g[ti][m] + q))
            out[a] = {f"RE_{k}": float(np.mean((F - v[ti]) / v[ti])) for k, v in ref.items()}
            out[a]["slip_label"] = float(np.mean(F < fhi[ti]))
        return out

    idx = lambda os_: np.array([i for o in os_ for i in by[o]])
    point = ev(idx(cal_o), idx(test_o))
    C = {k: v for k, v in contrasts().items() if v[0] in lg and v[1] in lg}
    rng = np.random.default_rng(seed)
    fams = sorted({o[0] for o in objs})
    boot = {k: {r: [] for r in ref} for k in C}
    cf = {f: [o for o in cal_o if o[0] == f] for f in fams}; tf = {f: [o for o in test_o if o[0] == f] for f in fams}
    for _ in range(draws):
        ci = idx([cf[f][j] for f in fams for j in rng.integers(0, len(cf[f]), len(cf[f]))])
        ti = idx([tf[f][j] for f in fams for j in rng.integers(0, len(tf[f]), len(tf[f]))])
        m = ev(ci, ti)
        for k, (t, c) in C.items():
            for r in ref:
                boot[k][r].append(1 - m[t][f"RE_{r}"] / m[c][f"RE_{r}"])
    res = {}
    for k, (t, c) in C.items():
        D = {r: 1 - point[t][f"RE_{r}"] / point[c][f"RE_{r}"] for r in ref}
        ci = {r: [float(np.percentile(boot[k][r], 1.25)), float(np.percentile(boot[k][r], 98.75))] for r in ref}
        res[k] = {"target": t, "comparator": c, "D": D, "CI**": ci,
                  "decision": decide(D["mid"], *ci["mid"], d_lohi=[(D[r], ci[r][0]) for r in ("lo", "hi")] if k.startswith("H2a") else None)}
    out = {"purpose": "p2 08c §3 secondary: H2 contrasts under label-rule split conformal (no lambda-grid)",
           "arms": point, "contrasts": res, "draws": draws}
    json.dump(out, open(os.path.join(ROOT, "v1/h2_label_rule.json"), "w"), indent=1)
    for k in ("H2a", "H2b", "H4e_vs_onset_only", "H2b_sigma@0.0", "H2b_sigma@0.1"):
        print(f"{k}: D {res[k]['D']['mid']:.3f} CI** {res[k]['CI**']['mid']} -> {res[k]['decision']}")


if __name__ == "__main__":
    main()
