"""Amendment 10 (p2 v3) B1 grids, read by `main.py crc --grids ../v3/crc_grids_10.json` (replay command unchanged).
Selection split only; no label of a cal / test row is read.
B1 shrunk plug-in@sigma (sigma in 0.2 / 0.4): log mu_s = a + b log mu_hat, (a, b) = OLS of log mu on log mu_hat over the
   avoidable selection rows; mu_hat = the CSF-mu-hat onset estimate at sigma; mu_s clipped to MU_HAT_CLIP; force =
   CSF-1 formula with mu_s. Grid: the 08c recipe (pooled label-rule quantile at alpha 0.10 on the avoidable selection
   rows, +-0.4, 20 points).
Writes results/v3/crc_grids_10.json.  usage (from papers/p2/code): python crc_grids_10.py"""
import hashlib
import json
import math
import os

import numpy as np

from certgrip.baselines import G, MU_HAT_CLIP, commanded_acc, mu_hat
from certgrip.conformal import qhat
from certgrip.featsets import onset_log_force
from certgrip.io import ROOT, key, load_rows

ALPHA, N_GRID, HALF = 0.10, 20, 0.4
SIGMAS = (0.2, 0.4)


def log_muhat(r, s):
    return math.log(mu_hat(r["inst"]["mass"], math.exp(onset_log_force(r, s))))


def f_shrunk(r, s, a, b):
    mu_s = min(max(math.exp(a + b * log_muhat(r, s)), MU_HAT_CLIP[0]), MU_HAT_CLIP[1])
    i = r["inst"]
    return i["mass"] * (G + commanded_acc(r["dist"], i["amp"], i["freq"])) / (2 * mu_s)


def main():
    rows = load_rows("v1/labels/*.jsonl")
    ks = hashlib.sha256(json.dumps([list(key(r)) for r in rows]).encode()).hexdigest()
    unshift_id = [r["pool"] == "id" and r["shift"] is None for r in rows]
    sel = np.array([u and r["split"] == "select" and not r["unavoidable"] for u, r in zip(unshift_id, rows)])
    ct = [i for i, (u, r) in enumerate(zip(unshift_id, rows)) if u and r["split"] in ("cal", "test")]
    log_fhi_sel = np.log([r["F_hi"] for r, s in zip(rows, sel) if s])
    out = {"purpose": "p2 amendment 10 B1 shrunk plug-in grids (selection split only)", "alpha": ALPHA,
           "F_max": 100.0, "keys_sha256": ks, "instances": [list(key(rows[i])) for i in ct], "arms": {}}
    for s in SIGMAS:
        x = np.array([log_muhat(r, s) for r, m in zip(rows, sel) if m])
        y = np.log([r["inst"]["mu"] for r, m in zip(rows, sel) if m])
        b, a = np.polyfit(x, y, 1)
        lg = np.log([f_shrunk(r, s, a, b) for r in rows])
        q = qhat(log_fhi_sel - lg[sel], ALPHA)
        out["arms"][f"CSF-shrunk@{s}"] = {"kind": "shrunk", "source": s, "ols": {"a": float(a), "b": float(b),
                                                                                  "n_sel": int(sel.sum())},
                                          "q_sel": q,
                                          "grid": [round(float(v), 6) for v in q + np.linspace(-HALF, HALF, N_GRID)],
                                          "log_g": [round(float(lg[i]), 6) for i in ct]}
        print(f"CSF-shrunk@{s}: a {a:.4f} b {b:.4f} q_sel {q:.4f}")
    os.makedirs(os.path.join(ROOT, "v3"), exist_ok=True)
    json.dump(out, open(os.path.join(ROOT, "v3/crc_grids_10.json"), "w"))
    print(f"instances: {len(ct)}")


def main_edge(s=0.2):
    """Amendment 10 B1 edge rule: CSF-shrunk@0.2 put lambda-hat on grid index 0 in D1 / D2 (results/v3/b1_analysis.json),
    so that arm is re-gridded with the 08e recipe (per-stratum q_sel on the selection split, +-0.8, 41 points), same
    (a, b) as in crc_grids_10.json. Writes results/v3/crc_grids_10e.json."""
    rows = load_rows("v1/labels/*.jsonl")
    ks = hashlib.sha256(json.dumps([list(key(r)) for r in rows]).encode()).hexdigest()
    G10 = json.load(open(os.path.join(ROOT, "v3/crc_grids_10.json")))
    ols = G10["arms"][f"CSF-shrunk@{s}"]["ols"]
    unshift_id = [r["pool"] == "id" and r["shift"] is None for r in rows]
    sel = np.array([u and r["split"] == "select" and not r["unavoidable"] for u, r in zip(unshift_id, rows)])
    ct = [i for i, (u, r) in enumerate(zip(unshift_id, rows)) if u and r["split"] in ("cal", "test")]
    dist = np.array([r["dist"] for r in rows])
    log_fhi = np.log([r["F_hi"] if r["F_hi"] else 1.0 for r in rows])
    lg = np.log([f_shrunk(r, s, ols["a"], ols["b"]) for r in rows])
    grids, qs = {}, {}
    for d in ("D1", "D2", "D3", "D4"):
        m = sel & (dist == d)
        qs[d] = qhat(log_fhi[m] - lg[m], ALPHA)
        grids[d] = [round(float(x), 6) for x in qs[d] + np.linspace(-0.8, 0.8, 41)]
    out = {"purpose": f"p2 amendment 10 B1 edge rule: CSF-shrunk@{s} on 08e-recipe grids", "alpha": ALPHA,
           "n_grid": 41, "half_width": 0.8, "F_max": 100.0, "keys_sha256": ks,
           "instances": [list(key(rows[i])) for i in ct],
           "arms": {f"CSF-shrunk@{s}": {"kind": "shrunk", "source": s, "ols": ols, "q_sel": qs, "grids": grids,
                                        "log_g": [round(float(lg[i]), 6) for i in ct]}}}
    json.dump(out, open(os.path.join(ROOT, "v3/crc_grids_10e.json"), "w"))
    print(qs)


if __name__ == "__main__":
    import sys
    main_edge() if "--edge" in sys.argv else main()
