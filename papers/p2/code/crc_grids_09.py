"""Amendment 09 (p2 v2) part B grids, read by `main.py crc --grids ../v2/crc_grids_09.json` (the replay command is
unchanged). Selection split only; no label of a cal / test row is read.
B1 CSF-proxy@sp (sp in 0.2 / 0.4 / 0.8): CSF-1 formula with mu_bar replaced by mu_tilde = clip(mu exp(sp eps_p), 0.1,
   3.0); eps_p ~ N(0, 1) per instance from default_rng([909, family, obj, dist]) (independent of the onset eps).
   Grid: the 08c recipe (pooled label-rule quantile at alpha 0.10 on the avoidable selection rows, +-0.4, 20 points).
B2 margin@0.2: base = the CSF-mu-hat sigma 0.2 force; 'grid' = log(1 + m), m in {0, 0.25, 0.5, 1.0} (no calibration).
Writes results/v2/crc_grids_09.json.  usage (from papers/p2/code): python crc_grids_09.py"""
import hashlib
import json
import math
import os

import numpy as np

from certgrip.baselines import G, MU_HAT_CLIP, commanded_acc, f_nom_muhat
from certgrip.conformal import qhat
from certgrip.featsets import onset_log_force
from certgrip.io import ROOT, key, load_rows

ALPHA, N_GRID, HALF = 0.10, 20, 0.4
SIGMA_P = (0.2, 0.4, 0.8)
MARGINS = (0.0, 0.25, 0.5, 1.0)
FAM, DIST = {"F1": 1, "F2": 2, "F3": 3, "F4": 4, "F5": 5}, {"D1": 1, "D2": 2, "D3": 3, "D4": 4}


def eps_p(r):
    return float(np.random.default_rng([909, FAM[r["family"]], int(r["obj"]), DIST[r["dist"]]]).standard_normal())


def f_proxy(r, sp):
    mu_t = min(max(r["inst"]["mu"] * math.exp(sp * eps_p(r)), MU_HAT_CLIP[0]), MU_HAT_CLIP[1])
    i = r["inst"]
    return i["mass"] * (G + commanded_acc(r["dist"], i["amp"], i["freq"])) / (2 * mu_t)


def main_edge():
    """Amendment 09 B1 edge rule: CSF-proxy@0.2 put lambda-hat on grid index 0 in D1 / D2 (results/v2/b_analysis.json),
    so that arm is re-gridded with the 08e recipe (per-stratum q_sel on the selection split, +-0.8, 41 points).
    Writes results/v2/crc_grids_09e.json."""
    rows = load_rows("v1/labels/*.jsonl")
    ks = hashlib.sha256(json.dumps([list(key(r)) for r in rows]).encode()).hexdigest()
    unshift_id = [r["pool"] == "id" and r["shift"] is None for r in rows]
    sel = np.array([u and r["split"] == "select" and not r["unavoidable"] for u, r in zip(unshift_id, rows)])
    ct = [i for i, (u, r) in enumerate(zip(unshift_id, rows)) if u and r["split"] in ("cal", "test")]
    dist = np.array([r["dist"] for r in rows])
    log_fhi = np.log([r["F_hi"] if r["F_hi"] else 1.0 for r in rows])
    lg = np.log([f_proxy(r, 0.2) for r in rows])
    grids, qs = {}, {}
    for d in ("D1", "D2", "D3", "D4"):
        m = sel & (dist == d)
        qs[d] = qhat(log_fhi[m] - lg[m], ALPHA)
        grids[d] = [round(float(x), 6) for x in qs[d] + np.linspace(-0.8, 0.8, 41)]
    out = {"purpose": "p2 amendment 09 B1 edge rule: CSF-proxy@0.2 on 08e-recipe grids", "alpha": ALPHA,
           "n_grid": 41, "half_width": 0.8, "F_max": 100.0, "keys_sha256": ks,
           "instances": [list(key(rows[i])) for i in ct],
           "arms": {"CSF-proxy@0.2": {"kind": "proxy", "source": 0.2, "q_sel": qs, "grids": grids,
                                      "log_g": [round(float(lg[i]), 6) for i in ct]}}}
    json.dump(out, open(os.path.join(ROOT, "v2/crc_grids_09e.json"), "w"))
    print(qs)


def main():
    rows = load_rows("v1/labels/*.jsonl")
    ks = hashlib.sha256(json.dumps([list(key(r)) for r in rows]).encode()).hexdigest()
    unshift_id = [r["pool"] == "id" and r["shift"] is None for r in rows]
    sel = np.array([u and r["split"] == "select" and not r["unavoidable"] for u, r in zip(unshift_id, rows)])
    ct = [i for i, (u, r) in enumerate(zip(unshift_id, rows)) if u and r["split"] in ("cal", "test")]
    log_fhi_sel = np.log([r["F_hi"] for r, s in zip(rows, sel) if s])
    out = {"purpose": "p2 amendment 09 B1 / B2 grids (selection split only)", "alpha": ALPHA, "F_max": 100.0,
           "keys_sha256": ks, "instances": [list(key(rows[i])) for i in ct], "arms": {}}
    for sp in SIGMA_P:
        lg = np.log([f_proxy(r, sp) for r in rows])
        q = qhat(log_fhi_sel - lg[sel], ALPHA)
        out["arms"][f"CSF-proxy@{sp}"] = {"kind": "proxy", "source": sp, "q_sel": q,
                                          "grid": [round(float(x), 6) for x in q + np.linspace(-HALF, HALF, N_GRID)],
                                          "log_g": [round(float(lg[i]), 6) for i in ct]}
        print(f"CSF-proxy@{sp}: q_sel {q:.4f}")
    lg = np.log([f_nom_muhat(r["inst"]["mass"], r["dist"], r["inst"]["amp"], r["inst"]["freq"],
                             math.exp(onset_log_force(r, 0.2))) for r in rows])
    out["arms"]["margin@0.2"] = {"kind": "margin", "source": list(MARGINS), "q_sel": None,
                                 "grid": [round(math.log(1 + m), 6) for m in MARGINS],
                                 "log_g": [round(float(lg[i]), 6) for i in ct]}
    os.makedirs(os.path.join(ROOT, "v2"), exist_ok=True)
    json.dump(out, open(os.path.join(ROOT, "v2/crc_grids_09.json"), "w"))
    print(f"instances: {len(ct)}")


if __name__ == "__main__":
    import sys
    main_edge() if "--edge" in sys.argv else main()
