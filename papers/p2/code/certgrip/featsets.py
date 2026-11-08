"""Feature sets of the fairness table (07_hypotheses §1.3), built from label JSONL rows.

base (every method): disturbance one-hot, commanded acceleration (D1/D2; 0 for D3/D4), log mass.
P  = base + proprio (aperture at contact; the measured preload force equals the constant F0, so it carries no
     information in simulation and is omitted).
S  = P + static touch at the preload (both pads' 7 statistics) + preload-slip flag.
full (CertGrip) = S + probe-squeeze features (per pad: normal / tangential sums and centroid at each probe frame
     minus the preload frame, and the aperture change during the probe).
No feature uses the external D3/D4 amplitude, mu, CoM offset or family ID (privileged; oracle ceiling only).
"""
from __future__ import annotations

import math

import numpy as np

from .baselines import commanded_acc

DISTS = ("D1", "D2", "D3", "D4")


def _nan0(v):
    return [0.0 if (x is None or (isinstance(x, float) and math.isnan(x))) else float(x) for x in v]


def row_features(r: dict, fset: str, no_mass: bool = False) -> list:
    i = r["inst"]
    x = [float(r["dist"] == d) for d in DISTS] + [commanded_acc(r["dist"], i["amp"], i["freq"])]
    if not no_mass:
        x.append(math.log(i["mass"]))
    if fset == "base":
        return x
    rec = r["rec"]
    x.append(rec["aperture"])
    if fset == "P":
        return x
    x += _nan0(rec["touch_preload"]) + [float(r["preload_slip"])]
    if fset == "S":
        return x
    pre = np.array(_nan0(rec["touch_preload"])).reshape(2, 7)
    for fr in rec["touch_probe"]:
        d = np.array(_nan0(fr)).reshape(2, 7) - pre
        x += d[:, :5].ravel().tolist()
    x.append(rec["aperture_probe"] - rec["aperture"])
    if fset == "full":
        return x
    raise ValueError(fset)


def privileged(r: dict) -> list:
    """Oracle-ceiling inputs: mu, every amplitude, CoM offset, geometry, mass, disturbance one-hot, family one-hot."""
    i = r["inst"]
    size = list(i["size"]) + [0.0] * (3 - len(i["size"]))
    return ([float(r["dist"] == d) for d in DISTS] + [float(i["family"] == f) for f in ("F1", "F2", "F3", "F4", "F5")]
            + [math.log(i["mu"]), math.log(i["mass"]), i["amp"], i["freq"], i["com"], i["grasp_dz"]] + size)


def matrix(rows, fset: str, no_mass: bool = False) -> np.ndarray:
    if fset == "oracle":
        return np.array([privileged(r) for r in rows])
    return np.array([row_features(r, fset, no_mass) for r in rows])
