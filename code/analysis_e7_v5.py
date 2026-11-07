"""v5 E7 H3 full screen (amendment v5.1d) on results/v5/e7: g2v3 beliefs 0-31 in S2 (kappa 2) and S12 (kappa 12),
look-ahead screen C1 = 32 (v3/v4 estimator) vs C1 = 512 (all feasible first actions), with an independent re-estimate
(M = 256, own stream) of the selected and the greedy action. Report-only (no decision rule).
Per (cell, C1), ratio-of-means G = (mean V_LA - mean V_G) / mean V_LA as in analysis_g2_v3.py, on the selection
re-estimate (biased upward by the max) and on the independent re-estimate (G_indep); selection bias in nats =
mean gap_abs - mean indep gap_abs. Paired C1 512 - C1 32 difference of the independent gap. Two-sided 95 % belief
bootstrap (B = 10,000, rng 7). No-budget beliefs contribute 0 to every mean. Writes results/v5/12_e7_analysis.json."""
import glob
import json
import os

import numpy as np

ROOT = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..")
N = 32


def load():
    d = {}
    for f in glob.glob(os.path.join(ROOT, "results/v5/e7", "*.jsonl")):
        c1 = int(os.path.basename(f).split("_c")[1].split("_")[0])
        for line in open(f):
            r = json.loads(line)
            if "index" in r:
                d.setdefault((float(r["kappa"]), c1), {})[r["index"]] = r
    return d


def arrays(rs):
    la = np.array([r["v_la"] for r in rs]); g = np.array([r["v_greedy"] for r in rs])
    ila = np.array([r["indep"]["v_la"] if "indep" in r else 0.0 for r in rs])
    ig = np.array([r["indep"]["v_greedy"] if "indep" in r else 0.0 for r in rs])
    return la, g, ila, ig


def stats(la, g, ila, ig, rng):
    def f(j):
        G = (la[j].mean() - g[j].mean()) / la[j].mean()
        Gi = (ila[j].mean() - ig[j].mean()) / ila[j].mean() if ila[j].mean() > 0 else np.nan
        return G, Gi, (la[j] - g[j]).mean() - (ila[j] - ig[j]).mean(), (ila[j] - ig[j]).mean()
    pt = f(np.arange(len(la)))
    bs = np.array([f(rng.integers(0, len(la), len(la))) for _ in range(10000)])
    names = ["G_selected", "G_indep", "selection_bias_nats", "indep_gap_nats"]
    return {n: {"est": float(pt[i]), "ci95": [float(np.nanquantile(bs[:, i], 0.025)), float(np.nanquantile(bs[:, i], 0.975))]}
            for i, n in enumerate(names)}


def main():
    d = load()
    rng = np.random.default_rng(7)
    out = {"design": "amendment v5.1d; g2v3 beliefs 0-31; indep M 256", "cells": {}}
    for k, name in [(2.0, "S2"), (12.0, "S12")]:
        cell = {}
        for c1 in (32, 512):
            rs = d.get((k, c1), {})
            idx = sorted(rs)
            e = {"n_beliefs": len(idx), "complete": idx == list(range(N))}
            if idx:
                rr = [rs[i] for i in idx]
                e.update(stats(*arrays(rr), rng))
                e["mean_candidates"] = float(np.mean([len(r.get("candidates", [])) for r in rr]))
                e["frac_la_differs"] = float(np.mean([r["a_la"] != r["a_greedy"] for r in rr]))
                e["n_no_budget_left"] = int(sum(bool(r.get("no_budget_left")) for r in rr))
            cell[f"C1_{c1}"] = e
        common = sorted(set(d.get((k, 32), {})) & set(d.get((k, 512), {})))
        if common:
            a = arrays([d[(k, 512)][i] for i in common]); b = arrays([d[(k, 32)][i] for i in common])
            diff = (a[2] - a[3]) - (b[2] - b[3])
            bs = [diff[rng.integers(0, len(diff), len(diff))].mean() for _ in range(10000)]
            cell["paired_indep_gap_512_minus_32"] = {"n": len(common), "est": float(diff.mean()),
                                                     "ci95": [float(np.quantile(bs, 0.025)), float(np.quantile(bs, 0.975))]}
        out["cells"][name] = cell
    json.dump(out, open(os.path.join(ROOT, "results/v5/12_e7_analysis.json"), "w"), indent=1)
    print(json.dumps(out, indent=1))


if __name__ == "__main__":
    main()
