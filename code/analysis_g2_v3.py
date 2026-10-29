"""Gate G2' / H3 (07_hypotheses_v3 §3.4; amendment v3.0 C12) on results/v3/g2 (g2v3 beliefs, S, kappa in {0, 2, 12}).
G(kappa) = (mean V_LA - mean V_G*) / mean V_LA over the 100 beliefs (ratio of means; no-budget beliefs contribute 0 to
both means), one-sided 95 % bootstrap bounds over beliefs (B = 10,000). Regions at kappa = 12 (kill takes precedence):
Kill LB95 > 0.05; Hold UB95 < 0.03; Inconclusive otherwise. Instrument conditions: G1' (a)(b) pass (else untested),
G1' (c) pass and bias ratio <= 1.02 (else Hold downgraded to Inconclusive). Bias check: mean estimator V_G* over
g2v3 S12 beliefs 0-19 / mean full-G* reference V_ref (touchbed/bias3.py) on the same beliefs.
kappa = 0 and 2 are descriptive. Writes results/v3/12_g2_analysis.json."""
import glob
import json
import os

import numpy as np

base = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "results", "v3")
d, bias = {}, {}
for f in glob.glob(os.path.join(base, "g2", "*.jsonl")):
    for line in open(f):
        r = json.loads(line)
        if "index" not in r:
            continue
        if "v_ref" in r:
            bias[r["index"]] = r
        else:
            d.setdefault(float(r["kappa"]), {})[r["index"]] = r
rng = np.random.default_rng(7)
out = {}
for k in sorted(d):
    rs = [d[k][i] for i in sorted(d[k])]
    la = np.array([r["v_la"] for r in rs]); g = np.array([r["v_greedy"] for r in rs])
    G = (la.mean() - g.mean()) / la.mean()
    bs = np.empty(10000)
    for b in range(10000):
        j = rng.integers(0, len(la), len(la))
        bs[b] = (la[j].mean() - g[j].mean()) / la[j].mean()
    out[f"k{k:g}"] = {"n_beliefs": len(la), "complete": len(la) == 100, "G": float(G),
                      "lb95": float(np.quantile(bs, 0.05)), "ub95": float(np.quantile(bs, 0.95)),
                      "abs_gap_nats": float(la.mean() - g.mean()), "mean_v_la": float(la.mean()),
                      "mean_v_greedy": float(g.mean()),
                      "frac_la_differs": float(np.mean([r["a_la"] != r["a_greedy"] for r in rs])),
                      "n_no_budget_left": int(sum(bool(r.get("no_budget_left")) for r in rs))}
g1 = json.load(open(os.path.join(base, "12_g1_analysis.json")))
if bias:
    idx = sorted(i for i in bias if i in d.get(12.0, {}))
    est = np.array([d[12.0][i]["v_greedy"] for i in idx]); ref = np.array([bias[i]["v_ref"] for i in idx])
    out["bias_check"] = {"n_beliefs": len(idx), "complete": len(idx) == 20, "mean_estimator_v_greedy": float(est.mean()),
                         "mean_reference_v": float(ref.mean()), "ratio": float(est.mean() / ref.mean()),
                         "n_floored_rollouts": int(sum(bias[i]["n_floored"] for i in idx)),
                         "hold_available": bool(est.mean() / ref.mean() <= 1.02)}
if "k12" in out:
    k12 = out["k12"]
    region = "Kill" if k12["lb95"] > 0.05 else ("Hold" if k12["ub95"] < 0.03 else "Inconclusive")
    tested = g1["a"]["passes"] and g1["b"]["passes"]
    downgrade = region == "Hold" and (not g1["c"]["passes"] or not out.get("bias_check", {}).get("hold_available", False))
    out["H3"] = {"region_raw": region, "tested_on_64x8": bool(tested),
                 "region": "untested" if not tested else ("Inconclusive" if downgrade else region),
                 "downgraded": bool(downgrade),
                 "ordering_G0<=G2<=G12": bool(all(f"k{k}" in out for k in (0, 2)) and out["k0"]["G"] <= out["k2"]["G"] <= k12["G"]),
                 "complete": bool(k12["complete"] and out.get("bias_check", {}).get("complete", False))}
print(json.dumps(out, indent=1))
json.dump(out, open(os.path.join(base, "12_g2_analysis.json"), "w"), indent=1)
