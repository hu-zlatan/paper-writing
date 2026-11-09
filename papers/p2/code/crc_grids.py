"""08c §2/§4: lambda-grids for the CRC route, fixed from the selection split only, plus each arm's base log-force for
every id calibration / test instance (the replay jobs read this file; no label of a cal / test row is read here).

Arms (08c §4, COMP = CSF-1 from results/v1/comp_selection.json): CertGrip-full [full_rd] seed 0 at sigma 0 / 0.1 / 0.2 /
0.4 and seeds 1-4 at sigma 0.2 (per-seed D, 08c §3 secondary); CSF-1; CSF-mu-hat at sigma 0 / 0.1 / 0.2 / 0.4;
onset-only [P_onset] seed 0 at sigma 0.2.
Grid: Lambda = q_sel + linspace(-0.4, 0.4, 20), q_sel = label-rule conformal quantile at alpha 0.10 of the arm's scores
(log F*_hi - log g) on the avoidable selection rows, pooled over strata. Decision at lambda: F = min(F_max, g e^lambda).
Writes results/v1/crc_grids.json.  usage (from papers/p2/code): python crc_grids.py
"""
import hashlib
import json
import math
import os

import numpy as np

from certgrip.baselines import f_nom, f_nom_muhat
from certgrip.conformal import qhat
from certgrip.featsets import onset_log_force
from certgrip.io import ROOT, key, load_rows

ALPHA, N_GRID, HALF = 0.10, 20, 0.4
SIGMAS = (0.0, 0.1, 0.2, 0.4)


def arms():
    a = {f"full_rd@{s}#0": ("pred", f"a010_full_rd_s{s}_seed0") for s in SIGMAS}
    a.update({f"full_rd@0.2#{k}": ("pred", f"a010_full_rd_s0.2_seed{k}") for k in (1, 2, 3, 4)})
    a["CSF-1"] = ("csf1", None)
    a.update({f"CSF-muhat@{s}": ("muhat", s) for s in SIGMAS})
    a["P_onset@0.2#0"] = ("pred", "a010_P_onset_s0.2_seed0")
    return a


def base_logs(rows, kind, arg, ks):
    if kind == "pred":
        p = json.load(open(os.path.join(ROOT, "v1/preds", arg + ".json")))
        assert p["keys_sha256"] == ks, arg
        return np.asarray(p["log_pred"], dtype=float)
    if kind == "csf1":
        return np.log([f_nom(r["inst"]["mass"], r["dist"], r["inst"]["amp"], r["inst"]["freq"]) for r in rows])
    return np.log([f_nom_muhat(r["inst"]["mass"], r["dist"], r["inst"]["amp"], r["inst"]["freq"],
                               math.exp(onset_log_force(r, arg))) for r in rows])


def main_v2():
    """Addendum 08e: per-stratum grids q_sel[stratum] + linspace(-0.8, 0.8, 41), q_sel per stratum on the selection
    split; 10 arms (CertGrip seed 0 at the four sigma, CSF-1, CSF-mu-hat at the four sigma, onset-only)."""
    rows = load_rows("v1/labels/*.jsonl")
    ks = hashlib.sha256(json.dumps([list(key(r)) for r in rows]).encode()).hexdigest()
    unshift_id = [r["pool"] == "id" and r["shift"] is None for r in rows]
    sel = np.array([u and r["split"] == "select" and not r["unavoidable"] for u, r in zip(unshift_id, rows)])
    ct = [i for i, (u, r) in enumerate(zip(unshift_id, rows)) if u and r["split"] in ("cal", "test")]
    dist = np.array([r["dist"] for r in rows])
    log_fhi = np.log([r["F_hi"] if r["F_hi"] else 1.0 for r in rows])
    out = {"purpose": "p2 08e CRC per-stratum lambda-grids (selection split only), sensitivity check of the 08c grid",
           "alpha": ALPHA, "n_grid": 41, "half_width": 0.8, "F_max": 100.0, "keys_sha256": ks,
           "instances": [list(key(rows[i])) for i in ct], "arms": {}}
    keep = [f"full_rd@{s}#0" for s in SIGMAS] + ["CSF-1"] + [f"CSF-muhat@{s}" for s in SIGMAS] + ["P_onset@0.2#0"]
    for name, (kind, arg) in arms().items():
        if name not in keep:
            continue
        lg = base_logs(rows, kind, arg, ks)
        grids, qs = {}, {}
        for d in ("D1", "D2", "D3", "D4"):
            m = sel & (dist == d)
            qs[d] = qhat(log_fhi[m] - lg[m], ALPHA)
            grids[d] = [round(float(x), 6) for x in qs[d] + np.linspace(-0.8, 0.8, 41)]
        out["arms"][name] = {"kind": kind, "source": arg, "q_sel": qs, "grids": grids,
                             "log_g": [round(float(lg[i]), 6) for i in ct]}
        print(name, {d: round(q, 3) for d, q in qs.items()})
    json.dump(out, open(os.path.join(ROOT, "v1/crc_grids_v2.json"), "w"))


def main():
    comp = json.load(open(os.path.join(ROOT, "v1/comp_selection.json")))["COMP"]
    assert comp == "CSF-1", "arm list below assumes COMP = CSF-1"
    rows = load_rows("v1/labels/*.jsonl")
    ks = hashlib.sha256(json.dumps([list(key(r)) for r in rows]).encode()).hexdigest()
    unshift_id = [r["pool"] == "id" and r["shift"] is None for r in rows]
    sel = np.array([u and r["split"] == "select" and not r["unavoidable"] for u, r in zip(unshift_id, rows)])
    ct = [i for i, (u, r) in enumerate(zip(unshift_id, rows)) if u and r["split"] in ("cal", "test")]
    log_fhi_sel = np.log([r["F_hi"] for r, s in zip(rows, sel) if s])
    out = {"purpose": "p2 08c CRC lambda-grids (selection split only) and base log-forces for id cal/test instances",
           "alpha": ALPHA, "n_grid": N_GRID, "half_width": HALF, "F_max": 100.0, "COMP": comp, "keys_sha256": ks,
           "n_select_avoidable": int(sel.sum()), "instances": [list(key(rows[i])) for i in ct], "arms": {}}
    for name, (kind, arg) in arms().items():
        lg = base_logs(rows, kind, arg, ks)
        q = qhat(log_fhi_sel - lg[sel], ALPHA)
        out["arms"][name] = {"kind": kind, "source": arg, "q_sel": q,
                             "grid": [round(float(x), 6) for x in q + np.linspace(-HALF, HALF, N_GRID)],
                             "log_g": [round(float(lg[i]), 6) for i in ct]}
        print(f"{name}: q_sel {q:.4f}")
    json.dump(out, open(os.path.join(ROOT, "v1/crc_grids.json"), "w"))
    print(f"instances: {len(ct)}")


if __name__ == "__main__":
    import sys
    main_v2() if "--v2" in sys.argv else main()
