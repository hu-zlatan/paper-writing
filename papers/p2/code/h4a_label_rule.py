"""H4a (07_hypotheses §H4a as changed by 08b §6): static vs probe, in steps P -> S -> S+squeeze (full) -> +onset (full_rd).
Secondary; 08c: arms other than the H2 / H4e set are reported under the label rule only. Same label-rule split conformal
route, object-cluster bootstrap and CI** (1.25 / 98.75, 2,000 draws) as h2_label_rule.py, on the 2,800 id test
instances (cal n = 500 per stratum). Arms: seed-0 predictors a010_P, a010_S, a010_full, a010_full_rd_s0.2 (alpha 0.10).
Decisions (07_hypotheses H4a): step S vs P -> superiority iff D >= 0.05 and lower > 0, equivalence iff CI** inside
+-0.05; step full vs S -> the same with 0.03; step full_rd vs full (+onset) has no registered margin -> D and CI** only.
Written and committed before it is run (run 41). Writes results/v1/h4a_label_rule.json.
usage (from papers/p2/code): python h4a_label_rule.py
"""
import hashlib
import json
import math
import os

import numpy as np

from certgrip.io import ROOT, key, load_rows

ALPHA, F_MAX = 0.10, 100.0
ARMS = {"P#0": "a010_P_seed0", "S#0": "a010_S_seed0", "full#0": "a010_full_seed0", "full_rd@0.2#0": "a010_full_rd_s0.2_seed0"}
STEPS = {"H4a_S_vs_P": ("S#0", "P#0", 0.05), "H4a_squeeze_full_vs_S": ("full#0", "S#0", 0.03),
         "H4a_onset_full_rd_vs_full": ("full_rd@0.2#0", "full#0", None)}


def decide(d, lo, hi, m):
    if m is None:
        return "report only (no registered margin)"
    if d >= m and lo > 0:
        return "superiority"
    if lo > -m and hi < m:
        return "equivalence"
    if hi < 0:
        return "inferiority"
    return "not confirmed"


def main(draws=2000, seed=2027):
    rows = load_rows("v1/labels/*.jsonl")
    ks = hashlib.sha256(json.dumps([list(key(r)) for r in rows]).encode()).hexdigest()
    base = [i for i, r in enumerate(rows) if r["pool"] == "id" and r["shift"] is None and r["split"] in ("cal", "test")]
    rs = [rows[i] for i in base]
    assert not any(r["unavoidable"] for r in rs)
    lg = {}
    for a, f in ARMS.items():
        p = json.load(open(os.path.join(ROOT, "v1/preds", f + ".json")))
        assert p["keys_sha256"] == ks, f
        lg[a] = np.asarray(p["log_pred"], dtype=float)[base]
    fhi = np.array([r["F_hi"] for r in rs]); ref = {k: np.array([r[f"F_{k}"] for r in rs]) for k in ("mid", "lo", "hi")}
    st = np.array([r["dist"] for r in rs]); split = np.array([r["split"] for r in rs])
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
    rng = np.random.default_rng(seed)
    fams = sorted({o[0] for o in objs})
    boot = {k: {r: [] for r in ref} for k in STEPS}
    cf = {f: [o for o in cal_o if o[0] == f] for f in fams}; tf = {f: [o for o in test_o if o[0] == f] for f in fams}
    for _ in range(draws):
        ci = idx([cf[f][j] for f in fams for j in rng.integers(0, len(cf[f]), len(cf[f]))])
        ti = idx([tf[f][j] for f in fams for j in rng.integers(0, len(tf[f]), len(tf[f]))])
        m = ev(ci, ti)
        for k, (t, c, _) in STEPS.items():
            for r in ref:
                boot[k][r].append(1 - m[t][f"RE_{r}"] / m[c][f"RE_{r}"])
    res = {}
    for k, (t, c, mg) in STEPS.items():
        D = {r: 1 - point[t][f"RE_{r}"] / point[c][f"RE_{r}"] for r in ref}
        ci = {r: [float(np.percentile(boot[k][r], 1.25)), float(np.percentile(boot[k][r], 98.75))] for r in ref}
        res[k] = {"target": t, "comparator": c, "margin": mg, "D": D, "CI**": ci, "decision": decide(D["mid"], *ci["mid"], mg)}
    out = {"purpose": "p2 H4a steps P -> S -> full -> full_rd under the label-rule route (secondary)",
           "arms": point, "contrasts": res, "draws": draws, "n_test_instances": int((split == "test").sum())}
    json.dump(out, open(os.path.join(ROOT, "v1/h4a_label_rule.json"), "w"), indent=1)
    for k, v in res.items():
        print(f"{k}: D {v['D']['mid']:.3f} CI** [{v['CI**']['mid'][0]:.3f}, {v['CI**']['mid'][1]:.3f}] -> {v['decision']}")
    for a, v in point.items():
        print(a, {x: round(y, 4) for x, y in v.items()})


if __name__ == "__main__":
    main()
