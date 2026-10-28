"""Gate G2 (docs/07_hypotheses_v2.md §4): G(kappa) = (mean V_LA - mean V_G*) / mean V_LA over the belief bank (ratio of
means), one-sided 95 % bootstrap bounds over beliefs; absolute gap in nats. Pass: G(kappa_hi) >= 0.10 with LB > 0.05,
G(0) <= 0.03 (point; UB reported), G(0) <= G(2) <= G(kappa_hi) (point). Writes results/v2/12_g2_analysis.json."""
import glob
import json
import os

import numpy as np

base = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "results", "v2")
d = {}
for f in glob.glob(os.path.join(base, "g2", "*.jsonl")):
    for line in open(f):
        r = json.loads(line)
        if "index" in r:
            d.setdefault(float(r["kappa"]), {})[r["index"]] = r
out = {}
rng = np.random.default_rng(7)
for k in sorted(d):
    rs = [d[k][i] for i in sorted(d[k])]
    la = np.array([r["v_la"] for r in rs]); g = np.array([r["v_greedy"] for r in rs])
    G = (la.mean() - g.mean()) / la.mean()
    bs = []
    for _ in range(10000):
        j = rng.integers(0, len(la), len(la))
        bs.append((la[j].mean() - g[j].mean()) / la[j].mean())
    bs = np.array(bs)
    out[f"k{k:g}"] = {"n_beliefs": len(la), "G": float(G), "lb95": float(np.quantile(bs, 0.05)), "ub95": float(np.quantile(bs, 0.95)),
                      "abs_gap_nats": float(la.mean() - g.mean()), "mean_v_la": float(la.mean()), "mean_v_greedy": float(g.mean()),
                      "frac_la_differs": float(np.mean([r["a_la"] != r["a_greedy"] for r in rs])),
                      "mean_steps_before": float(np.mean([r["steps_before"] for r in rs])),
                      "n_no_budget_left": int(sum(bool(r.get("no_budget_left")) for r in rs))}
    print(k, out[f"k{k:g}"])
kh = 12.0 if "k12" in out and out["k12"]["n_beliefs"] == 100 else 6.0
if all(f"k{k:g}" in out for k in (0.0, 2.0, kh)):
    g0, g2, gh = (out[f"k{k:g}"]["G"] for k in (0.0, 2.0, kh))
    out["decision"] = {"kappa_hi": kh, "magnitude_ok": bool(gh >= 0.10 and out[f"k{kh:g}"]["lb95"] > 0.05),
                       "g0_ok": bool(g0 <= 0.03), "ordering_ok": bool(g0 <= g2 <= gh),
                       "complete": all(out[f"k{k:g}"]["n_beliefs"] == 100 for k in (0.0, 2.0, kh))}
    out["decision"]["passes"] = all(out["decision"][x] for x in ("magnitude_ok", "g0_ok", "ordering_ok"))
    print(out["decision"])
json.dump(out, open(os.path.join(base, "12_g2_analysis.json"), "w"), indent=1)
