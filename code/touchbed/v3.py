"""v3 episode streams (amendment v3.0 C5, v3.1 D1).

Evaluation splits (cal3, pilot3, val3, test3, g2v3, bank3) use the v2 key without kappa, so episode i is the same
initial state in every cell of a set (paired across kappa). Training splits (label3, dagger3) put kappa in the key, so
S0 and S12 training states are disjoint. Every v3 job runs with TOUCHBED_NPHI=64 and records `action_set` below.
"""
from __future__ import annotations

import math

from .evaluate import SPLIT_SALT, stream
from .geometry import Library
from .pf import Prior
from .shapes import get_set
from .travel import A, N_PHI, N_PSI

V3_SALTS = {"cal3": 61, "pilot3": 67, "val3": 71, "test3": 79, "label3": 83, "dagger3": 89, "g2v3": 97, "bank3": 101}
TRAIN_SPLITS = ("label3", "dagger3")
for _k, _v in V3_SALTS.items():           # register without touching the v1/v2 entries
    assert SPLIT_SALT.get(_k, _v) == _v
    SPLIT_SALT[_k] = _v
assert len(set(SPLIT_SALT.values())) == len(SPLIT_SALT)

ACTION_SET = f"{N_PHI}x{N_PSI}"


def require_v3_actions():
    if A != 512:
        raise RuntimeError("v3 runs need TOUCHBED_NPHI=64 (amendment v3.0 C1); got action set " + ACTION_SET)


def dagger_index(round_: int, seed: int, j: int) -> int:
    """Amendment v3.1 D1: index = 100,000·r + 1,000·(seed − 500) + j, r ∈ {1, 2}, j ∈ [0, 800)."""
    if round_ not in (1, 2) or not 0 <= j < 800 or not 501 <= seed <= 599:
        raise ValueError((round_, seed, j))
    return 100_000 * round_ + 1_000 * (seed - 500) + j


def state_v3(setname: str, split: str, i: int, kappa: float | None = None, prior=None):
    """Initial state s0 = (k, x, y, theta) and finger start angle phi0 of episode i."""
    if split not in V3_SALTS:
        raise ValueError(split)
    if prior is None:
        prior = Prior(Library(get_set(setname)).K)
    if split in TRAIN_SPLITS:
        if kappa is None:
            raise ValueError("training splits are kappa-keyed (amendment v3.1 D1)")
        rng = stream("state", setname, split, V3_SALTS[split], float(kappa), i)
        phi_rng = stream("phi0", setname, split, float(kappa), i)
    else:
        rng = stream("state", setname, split, V3_SALTS[split], i)
        phi_rng = stream("phi0", setname, split, i)
    k, x, y, th = prior.sample(rng, 1)
    return (int(k[0]), float(x[0]), float(y[0]), float(th[0])), float(phi_rng.uniform(0, 2 * math.pi))


def states_v3(setname: str, split: str, indices, kappa: float | None = None):
    lib = Library(get_set(setname))
    prior = Prior(lib.K)
    return lib, prior, [state_v3(setname, split, int(i), kappa, prior) for i in indices]


def ep_key_v3(setname: str, split: str, kappa: float, tau: float, i: int):
    """Key of the observation / policy / decision-PF streams of one episode (v2 convention, v3 split names)."""
    return (setname, split, float(kappa), float(tau), int(i))
