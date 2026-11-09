"""COMP selection (08b §3, 08c §3): read only the id selection split (objects 150-199 per family, label rule).

Candidates: CSF-1 (one q-hat per disturbance stratum), Mondrian-CSF (one q-hat per family x disturbance cell, privileged
family ID), CertGrip-P (seed-0 fit `a010_P_seed0`). Objects with even index calibrate and odd index evaluate, then the
roles swap; the criterion is the mean label-rule RE at alpha 0.10 over both halves (RE = mean (F - F*_mid) / F*_mid on
avoidable evaluation instances, F = min(F_max, g exp(q-hat))). The smallest wins. Unavoidable instances have no F* and
are excluded (counted per candidate as label slips, reported only). No cal / test row is read: rows are filtered to
split == "select" before any score is computed.
Writes results/v1/comp_selection.json.  usage (from papers/p2/code): python comp_selection.py
"""
import hashlib
import json
import os

import numpy as np

from certgrip.baselines import f_nom
from certgrip.conformal import qhat
from certgrip.io import ROOT, key, load_rows

ALPHA, F_MAX = 0.10, 100.0


def label_re(logp, fhi, fmid, strata, cal, ev):
    F = np.full(len(logp), np.nan)
    for st in np.unique(strata):
        idx = strata == st
        q = qhat(np.log(fhi[cal & idx]) - logp[cal & idx], ALPHA)
        F[idx] = np.minimum(np.exp(logp[idx] + q), F_MAX)
    return float(np.mean((F[ev] - fmid[ev]) / fmid[ev])), float(np.mean(F[ev] < fhi[ev]))


def select(rows, logp_P):
    """rows: id-pool unshifted selection rows (any order); logp_P: CertGrip-P log predictions aligned with rows."""
    av = np.array([not r["unavoidable"] for r in rows])
    rows_a = [r for r, a in zip(rows, av) if a]
    fhi = np.array([r["F_hi"] for r in rows_a])
    fmid = np.array([r["F_mid"] for r in rows_a])
    dist = np.array([r["dist"] for r in rows_a])
    cell = np.array([f"{r['family']}_{r['dist']}" for r in rows_a])
    even = np.array([r["obj"] % 2 == 0 for r in rows_a])
    csf = np.log([f_nom(r["inst"]["mass"], r["dist"], r["inst"]["amp"], r["inst"]["freq"]) for r in rows_a])
    cands = {"CSF-1": (csf, dist), "Mondrian-CSF": (csf, cell), "CertGrip-P": (np.asarray(logp_P)[av], dist)}
    out = {}
    for name, (lp, st) in cands.items():
        halves = [label_re(lp, fhi, fmid, st, even, ~even), label_re(lp, fhi, fmid, st, ~even, even)]
        out[name] = {"RE_even_cal": halves[0][0], "RE_odd_cal": halves[1][0],
                     "RE_mean": float(np.mean([h[0] for h in halves])),
                     "label_slip_avoidable_mean": float(np.mean([h[1] for h in halves]))}
    winner = min(out, key=lambda k: out[k]["RE_mean"])
    return out, winner, int((~av).sum()), len(rows)


def main():
    allrows = load_rows("v1/labels/*.jsonl")
    pred = json.load(open(os.path.join(ROOT, "v1/preds/a010_P_seed0.json")))
    ks = hashlib.sha256(json.dumps([list(key(r)) for r in allrows]).encode()).hexdigest()
    assert ks == pred["keys_sha256"], "prediction rows do not match the label rows"
    sel = [(r, p) for r, p in zip(allrows, pred["log_pred"])
           if r["pool"] == "id" and r["shift"] is None and r["split"] == "select"]
    rows, lp = [r for r, _ in sel], [p for _, p in sel]
    res, winner, n_unav, n = select(rows, lp)
    out = {"purpose": "p2 COMP selection (08b §3, 08c §3): selection split only, label rule, alpha 0.10, "
                      "even/odd object halves, mean RE over both halves; smallest wins",
           "n_instances": n, "n_unavoidable_excluded": n_unav, "objects": sorted({(r["family"], r["obj"]) for r in rows})[:1]
           and f"{len({(r['family'], r['obj']) for r in rows})} objects (150-199 per family)",
           "candidates": res, "COMP": winner, "pred_file": "v1/preds/a010_P_seed0.json", "keys_sha256": ks}
    json.dump(out, open(os.path.join(ROOT, "v1/comp_selection.json"), "w"), indent=1)
    for k, v in res.items():
        print(f"{k}: RE_mean {v['RE_mean']:.4f}")
    print(f"COMP: {winner}")


if __name__ == "__main__":
    main()
