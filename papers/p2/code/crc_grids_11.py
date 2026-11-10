"""Amendment 11 (p2 v4) wide pre-specified grids W and base log-forces, read by
`main.py crc --grids ../v4/crc_grids_11_<name>.json --pool <pool> [--rep-protocol noprobe]`.
W: per arm and disturbance stratum, centre q_sel = the label-rule conformal quantile at alpha 0.10 of
log F*_hi - log g on the avoidable SELECTION rows of that stratum (f4 arms: id-pool selection rows of results/v1/labels;
c4 arms: c4 selection rows), grid = q_sel + linspace(-1.6, 1.6, 81). No cal / test label is read.
Arms. f4: full_rd@{0.1,0.2,0.4}#0 (frozen v1 fits, results/v4/preds via predict_v4.py; id selection from v1/preds),
CSF-muhat@{0.1,0.2,0.4}, CSF-shrunk@0.2 (frozen v3 OLS a, b from results/v3/crc_grids_10.json), CSF-1.
c4: full_rd@0.2#0, CSF-muhat@0.2, CSF-1, CSF-fam (CSF-1 formula with mu-bar = geometric-mean true mu of the family's c4
selection objects). np (protocol noprobe, f4 instances): CSF-1 with the f4 CSF-1 grid.
Writes results/v4/crc_grids_11_{f4,c4,np}.json.  usage (from papers/p2/code): python crc_grids_11.py"""
import hashlib
import json
import math
import os

import numpy as np

from certgrip.baselines import G, commanded_acc, f_nom, f_nom_muhat
from certgrip.conformal import qhat
from certgrip.featsets import onset_log_force
from certgrip.io import ROOT, key, load_rows
from crc_grids_10 import f_shrunk

ALPHA, N_GRID, HALF, F_MAX = 0.10, 81, 1.6, 100.0
DISTS = ("D1", "D2", "D3", "D4")


def ks_of(rows):
    return hashlib.sha256(json.dumps([list(key(r)) for r in rows]).encode()).hexdigest()


def pred_map(path):
    p = json.load(open(os.path.join(ROOT, path)))
    if "keys" in p:
        return {tuple(k): v for k, v in zip(p["keys"], p["log_pred"])}
    return p


def base_log(r, kind, arg, preds):
    i = r["inst"]
    if kind == "pred":
        return preds[arg][key(r)]
    if kind == "csf1":
        return math.log(f_nom(i["mass"], r["dist"], i["amp"], i["freq"]))
    if kind == "muhat":
        return math.log(f_nom_muhat(i["mass"], r["dist"], i["amp"], i["freq"], math.exp(onset_log_force(r, arg))))
    if kind == "shrunk":
        return math.log(f_shrunk(r, 0.2, arg["a"], arg["b"]))
    if kind == "fam":
        return math.log(i["mass"] * (G + commanded_acc(r["dist"], i["amp"], i["freq"])) / (2 * arg[r["family"]]))
    raise ValueError(kind)


def build(name, arms, sel_rows, ct_rows, preds):
    out = {"purpose": f"p2 amendment 11 wide grids W ({name})", "alpha": ALPHA, "n_grid": N_GRID, "half_width": HALF,
           "F_max": F_MAX, "keys_sha256": ks_of(ct_rows), "instances": [list(key(r)) for r in ct_rows], "arms": {}}
    sel = [r for r in sel_rows if not r["unavoidable"]]
    for arm, (kind, arg) in arms.items():
        qs, grids = {}, {}
        for d in DISTS:
            rs = [r for r in sel if r["dist"] == d]
            sc = np.array([math.log(r["F_hi"]) - base_log(r, kind, arg, preds) for r in rs])
            qs[d] = float(qhat(sc, ALPHA))
            grids[d] = [round(float(x), 6) for x in qs[d] + np.linspace(-HALF, HALF, N_GRID)]
        out["arms"][arm] = {"kind": kind, "source": arg if not isinstance(arg, float) else arg, "q_sel": qs,
                            "grids": grids, "log_g": [round(base_log(r, kind, arg, preds), 6) for r in ct_rows]}
        print(name, arm, {d: round(q, 3) for d, q in qs.items()})
    json.dump(out, open(os.path.join(ROOT, "v4", f"crc_grids_11_{name}.json"), "w"))
    print(name, "instances", len(ct_rows))


def main():
    v1 = load_rows("v1/labels/*.jsonl")
    v1_ks = ks_of(v1)
    id_sel = [r for r in v1 if r["pool"] == "id" and r["shift"] is None and r["split"] == "select"]
    v4 = load_rows("v4/labels/*.jsonl")
    f4 = [r for r in v4 if r["pool"] == "f4" and r["split"] in ("cal", "test")]
    c4 = [r for r in v4 if r["pool"] == "c4"]
    c4_sel, c4_ct = [r for r in c4 if r["split"] == "select"], [r for r in c4 if r["split"] in ("cal", "test")]
    assert len(f4) == 4800 and len(c4_ct) == 4800 and len(c4_sel) == 800, (len(f4), len(c4_ct), len(c4_sel))
    preds = {}
    for s in (0.1, 0.2, 0.4):
        p1 = json.load(open(os.path.join(ROOT, "v1/preds", f"a010_full_rd_s{s}_seed0.json")))
        assert p1["keys_sha256"] == v1_ks
        m = {key(r): v for r, v in zip(v1, p1["log_pred"])}
        m.update(pred_map(f"v4/preds/full_rd_s{s}_seed0.json"))
        preds[f"full_rd@{s}#0"] = m
    ols = json.load(open(os.path.join(ROOT, "v3/crc_grids_10.json")))["arms"]["CSF-shrunk@0.2"]["ols"]
    arms_f4 = {f"full_rd@{s}#0": ("pred", f"full_rd@{s}#0") for s in (0.1, 0.2, 0.4)}
    arms_f4.update({f"CSF-muhat@{s}": ("muhat", s) for s in (0.1, 0.2, 0.4)})
    arms_f4["CSF-shrunk@0.2"] = ("shrunk", {"a": ols["a"], "b": ols["b"]})
    arms_f4["CSF-1"] = ("csf1", None)
    build("f4", arms_f4, id_sel, f4, preds)
    build("np", {"CSF-1": ("csf1", None)}, id_sel, f4, preds)
    mubar = {}
    for fam in ("F1", "F2", "F3", "F4"):
        mus = {r["obj"]: r["inst"]["mu"] for r in c4_sel if r["family"] == fam}
        mubar[fam] = float(math.exp(np.mean(np.log(list(mus.values())))))
    print("CSF-fam mu-bar", mubar)
    arms_c4 = {"full_rd@0.2#0": ("pred", "full_rd@0.2#0"), "CSF-muhat@0.2": ("muhat", 0.2), "CSF-1": ("csf1", None),
               "CSF-fam": ("fam", mubar)}
    build("c4", arms_c4, c4_sel, c4_ct, preds)


if __name__ == "__main__":
    main()
