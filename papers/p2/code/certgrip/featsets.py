"""Feature sets of the fairness table (07_hypotheses §1.3), built from label JSONL rows.

base (every method): disturbance one-hot, commanded acceleration (D1/D2; 0 for D3/D4), log mass.
P  = base + proprio (aperture at contact; the measured preload force equals the constant F0, so it carries no
     information in simulation and is omitted).
S  = P + static touch at the preload (both pads' 7 statistics) + preload-slip flag.
full (CertGrip) = S + probe-squeeze features (per pad: normal / tangential sums and centroid at each probe frame
     minus the preload frame, and the aperture change during the probe).
Amendment 08a (protocol "rd" labels only): onset features = [log F_onset + sigma * eps, found flag], where F_onset is
the commanded force at the touch-detected incipient slip (censored at the floor) and eps the instance's stored N(0,1)
draw; sigma in {0, 0.1, 0.2, 0.4}, primary 0.2.
full_rd (CertGrip-full under 08a) = full + onset;  P_onset (onset-only, H4e) = P + onset;  S_onset = S + onset.
No feature uses the external D3/D4 amplitude, mu, CoM offset or family ID (privileged; oracle ceiling only).
"""
from __future__ import annotations

import math

import numpy as np

from .baselines import commanded_acc

DISTS = ("D1", "D2", "D3", "D4")


def _nan0(v):
    return [0.0 if (x is None or (isinstance(x, float) and math.isnan(x))) else float(x) for x in v]


SIGMA_PRIMARY = 0.2


def onset_log_force(r: dict, sigma: float) -> float:
    o = r["rec"]["onset"]
    return math.log(o["F_onset"]) + sigma * o["eps"]


def onset_feats(r: dict, sigma: float) -> list:
    return [onset_log_force(r, sigma), float(r["rec"]["onset"]["found"])]


def row_features(r: dict, fset: str, no_mass: bool = False, sigma: float = SIGMA_PRIMARY) -> list:
    if fset in ("full_rd", "P_onset", "S_onset"):
        return row_features(r, {"full_rd": "full", "P_onset": "P", "S_onset": "S"}[fset], no_mass) + onset_feats(r, sigma)
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


def _group_seed(name: str) -> int:
    import hashlib
    return int(hashlib.sha256(name.encode()).hexdigest()[:8], 16)


def shuffled(rows, no_mass: bool = False, sigma: float = SIGMA_PRIMARY) -> np.ndarray:
    """Addendum 08f §2 (H4c): full_rd features whose non-P columns (static touch, preload-slip flag, squeeze probe,
    onset) are permuted across rows within each (pool, shift, split, dist) group; P columns stay with their row.
    The permutation of a group depends only on the group name and the sorted object keys in it (deterministic)."""
    X = np.array([row_features(r, "full_rd", no_mass, sigma) for r in rows])
    n_p = len(row_features(rows[0], "P", no_mass, sigma))
    groups = {}
    for i, r in enumerate(rows):
        groups.setdefault((r["pool"], str(r.get("shift")), r["split"], r["dist"]), []).append(i)
    for g, idx in groups.items():
        idx = sorted(idx, key=lambda i: (rows[i]["family"], rows[i]["obj"]))
        perm = np.random.default_rng(_group_seed("|".join(g))).permutation(len(idx))
        src = np.array(idx)[perm]
        X[np.array(idx), n_p:] = X[src, n_p:]
    return X


def matrix(rows, fset: str, no_mass: bool = False, sigma: float = SIGMA_PRIMARY) -> np.ndarray:
    if fset == "oracle":
        return np.array([privileged(r) for r in rows])
    if fset == "full_rd_shuf":
        return shuffled(rows, no_mass, sigma)
    return np.array([row_features(r, fset, no_mass, sigma) for r in rows])
