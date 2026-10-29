"""Gate D4 (docs/07c_amendment_v4_0.md): S2 (S, kappa 2, tau 4.7), budget-matched students (seeds 601-603, final DAgger
round r2), val3 0-499 paired with G*, sub-8 grid read-out. D3 form with delta = 0.04 (no G5' S2 cell) and the BI floor
-0.15 nats only (no eps_c for S2):
(i)  Delta_succ >= max(-0.02, -delta + 1.645 * SE_s * sqrt(500/1000))
(ii) Delta_BI   >= -0.15
(iii) every seed's point Delta_succ > -delta
SE = SD of the crossed bootstrap (as analysis_d3_v3.boot_sd). Writes results/v4/12_d4_analysis.json."""
import glob
import json
import math
import os

import numpy as np

base = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "results", "v4")
SEEDS, N_EP, DELTA = (601, 602, 603), 500, 0.04


def load(pat):
    d = {}
    for f in glob.glob(os.path.join(base, "d4_val", pat)):
        for line in open(f):
            r = json.loads(line)
            if "episode" in r and "header" not in r:
                d[r["episode"]] = r
    return d


def boot_sd(A, B, n_boot=10000, seed=0):
    rng = np.random.default_rng(seed)
    n = A.shape[0]
    st = np.empty(n_boot)
    for b in range(n_boot):
        ei = rng.integers(0, n, n)
        sa = rng.integers(0, A.shape[1], A.shape[1])
        st[b] = np.mean(A[ei][:, sa].mean(1) - B[ei])
    return float(st.std(ddof=1))


def main():
    g = load("S_k2_gstar_*.jsonl")
    st = {s: load(f"S_k2_student_s{s}_r2_*.jsonl") for s in SEEDS}
    eps = [e for e in range(N_EP) if e in g and all(e in st[s] for s in SEEDS)]
    out = {"cell": "S2", "n_episodes": len(eps), "complete": len(eps) == N_EP, "delta": DELTA}
    if eps:
        for metric, key in (("succ", "success"), ("bi", "ball_info")):
            A = np.array([[float(st[s][e][key]) for s in SEEDS] for e in eps])
            B = np.array([float(g[e][key]) for e in eps])
            d = float(np.mean(A.mean(1) - B))
            se = boot_sd(A, B)
            thr = max(-0.02, -DELTA + 1.645 * se * math.sqrt(500 / 1000)) if metric == "succ" else -0.15
            out[metric] = {"delta_hat": d, "se": se, "threshold": thr, "passes": bool(d >= thr),
                           "student_mean": float(A.mean()), "gstar_mean": float(B.mean()),
                           "per_seed": {str(s): float(np.mean(A[:, i] - B)) for i, s in enumerate(SEEDS)}}
        out["seeds_ok"] = {s: v > -DELTA for s, v in out["succ"]["per_seed"].items()}
        out["passes"] = bool(out["succ"]["passes"] and out["bi"]["passes"] and all(out["seeds_ok"].values()))
    os.makedirs(base, exist_ok=True)
    json.dump(out, open(os.path.join(base, "12_d4_analysis.json"), "w"), indent=1)
    print(json.dumps(out, indent=1))


if __name__ == "__main__":
    main()
