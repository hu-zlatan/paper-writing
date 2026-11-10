"""Instance generation, object splits and shift pools (07_hypotheses §1.2; 08_experiment_plan datasets).

Every instance is a pure function of (pool, family, object index, disturbance, shift): the object's own parameters
(geometry, mass, mu, CoM offset) come from a generator seeded by (salt, family, object), and the per-instance draws
(grasp offset, disturbance amplitude/frequency) from one seeded by (salt, family, object, disturbance). So the four
instances of one object share the object, and the paired shift pools S1 / S1m / S3 change exactly one factor.
Pools have disjoint salts; splits are disjoint object-index ranges (UT1).
"""
from __future__ import annotations

import dataclasses

import numpy as np

from .sim import Instance

FAMILIES = ("F1", "F2", "F3", "F4")
DISTS = ("D1", "D2", "D3", "D4")
SALT = {"id": 1001, "s2": 2002, "pilot": 3003,      # pool -> salt (disjoint objects across pools)
        "f4": 4004, "c4": 5005}                      # amendment 11: fresh pool f4, friction-correlated pool c4
N_OBJ = {"id": 500, "s2": 550, "pilot": 225, "f4": 300, "c4": 350}   # pilot 0-24 first pilot / detector tuning; 25-124 attempt 1 (discarded);
#                                               125-224 re-pilot under the frozen 08a protocol
MU_BAND = {"F1": (0.30, 0.45), "F2": (0.40, 0.60), "F3": (0.55, 0.80), "F4": (0.70, 1.00)}   # c4 (amendment 11)
SHIFTS = {None: {}, "S1": {"mu": 0.6}, "S1m": {"mu": 0.9}, "S3": {"amp": 1.5}}


def split_of(pool: str, obj: int) -> str:
    """Object-level split (frozen in docs/08b_preregistration.md §5; the pilot power rule moved 50 train objects per
    family to test). id pool: 0-149 train, 150-199 selection (held out of train), 200-324 cal, 325-499 test.
    s2 pool (shift family F5): 0-174 oracle calibration, 175-549 stream. pilot: all pilot."""
    if pool == "id":
        return "train" if obj < 150 else "select" if obj < 200 else "cal" if obj < 325 else "test"
    if pool == "s2":
        return "oracle" if obj < 175 else "stream"
    if pool == "f4":      # amendment 11: 0-124 cal, 125-299 test
        return "cal" if obj < 125 else "test"
    if pool == "c4":      # amendment 11: 0-49 selection, 50-174 cal, 175-349 test
        return "select" if obj < 50 else "cal" if obj < 175 else "test"
    return "pilot"


def h3_role(pool: str, obj: int) -> str:
    """H3 stream roles (08b §5). Paired shifts S1 / S1m / S3 re-simulate the id test objects: 325-368 per family
    (176 objects) are the oracle-recalibration objects (their unshifted instances also feed the 500 pre-shift steps),
    369-499 (524 objects) the shifted stream. S2: split_of('s2', obj)."""
    if pool == "s2":
        return split_of(pool, obj)
    if pool == "id" and obj >= 325:
        return "oracle" if obj < 369 else "stream"
    return "none"


def _fam_index(family: str) -> int:
    return ("F1", "F2", "F3", "F4", "F5").index(family)


def sample_object(pool: str, family: str, obj: int) -> dict:
    rng = np.random.default_rng([SALT[pool], _fam_index(family), obj])
    lo, hi = MU_BAND[family] if pool == "c4" else (0.3, 1.0)       # one draw either way (draw order unchanged)
    mu = float(np.exp(rng.uniform(np.log(lo), np.log(hi))))
    mass = float(np.exp(rng.uniform(np.log(0.05), np.log(1.0))))
    if family in ("F1", "F4"):
        size = (rng.uniform(0.015, 0.035), rng.uniform(0.015, 0.035), rng.uniform(0.02, 0.05))
    elif family == "F2":
        size = (rng.uniform(0.015, 0.035), rng.uniform(0.02, 0.05))
    elif family == "F3":
        size = (rng.uniform(0.015, 0.03), rng.uniform(0.01, 0.04))
    elif family == "F5":   # thin plates (box <= 5 mm thick); disks are a later option (same primitive class)
        size = (rng.uniform(0.002, 0.005), rng.uniform(0.02, 0.04), rng.uniform(0.02, 0.05))
    else:
        raise ValueError(family)
    zext = size[-1]
    com = float(rng.uniform(-1, 1) * (0.6 if family == "F4" else 0.4) * zext)
    return {"family": family, "size": tuple(float(s) for s in size), "mass": mass, "mu": mu, "com": com}


def make_instance(pool: str, family: str, obj: int, dist: str, shift: str | None = None) -> Instance:
    o = sample_object(pool, family, obj)
    rng = np.random.default_rng([SALT[pool], _fam_index(family), obj, 10 + DISTS.index(dist)])
    grasp_dz = float(rng.uniform(-0.3, 0.3) * o["size"][-1])
    freq = 0.0
    if dist == "D1":
        amp = rng.uniform(1, 10)
    elif dist == "D2":
        amp, freq = rng.uniform(0.005, 0.02), rng.uniform(2, 5)
    elif dist == "D3":
        amp = rng.uniform(0.5, 2.0)
    else:
        amp = rng.uniform(0.2, 1.0)
    inst = Instance(family, o["size"], o["mass"], o["mu"], o["com"], grasp_dz, dist, float(amp), float(freq))
    f = SHIFTS[shift]
    if "mu" in f:
        inst = dataclasses.replace(inst, mu=inst.mu * f["mu"])
    if "amp" in f:
        inst = dataclasses.replace(inst, amp=inst.amp * f["amp"])
    return inst
