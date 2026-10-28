import math
import time

import numpy as np

from touchbed.geometry import Library
from touchbed.likelihood import ObsModel, sample_obs
from touchbed.pf import ParticleFilter, Prior, success
from touchbed.shapes import get_set


def run(n=4000, T=10, seed=0, setname="A"):
    lib = Library(get_set(setname))
    om = ObsModel()
    prior = Prior(lib.K)
    rng = np.random.default_rng(seed)
    s0 = tuple(v[0] for v in prior.sample(rng, 1))
    pf = ParticleFilter(lib, om, prior, n, np.random.default_rng(seed + 100))
    for t in range(T):
        phi, psi = rng.uniform(-math.pi, math.pi), rng.uniform(-0.3, 0.3)
        obs = tuple(v[0] for v in sample_obs(om, lib, rng, np.array([s0[0]]), s0[1], s0[2], s0[3], phi, psi))
        pf.update(phi, psi, obs)
    return lib, pf, s0


def test_pf_localizes_with_many_touches():
    oks, igs = [], []
    for seed in range(6):
        lib, pf, s0 = run(n=4000, T=12, seed=seed)
        r = success(lib, pf.estimate(), s0)
        oks.append(r["identity_ok"])
        igs.append(pf.realized_ig_evidence(s0))
    assert sum(oks) >= 5
    assert np.mean(igs) > 3.0


def test_ig_zero_without_data():
    lib = Library(get_set("A"))
    prior = Prior(lib.K)
    pf = ParticleFilter(lib, ObsModel(), prior, 8000, np.random.default_rng(0))
    rng = np.random.default_rng(3)
    vals = [pf.realized_ig_evidence(tuple(v[0] for v in prior.sample(rng, 1))) for _ in range(5)]
    assert max(abs(v) for v in vals) < 1e-12  # no data -> zero information


def test_evidence_ig_positive_after_touches():
    """Three touches give a finite, positive realized information gain (an exact-posterior check on a discrete
    problem is in test_exact.py)."""
    lib, pf, s0 = run(n=6000, T=3, seed=4)
    ig = pf.realized_ig_evidence(s0)
    assert np.isfinite(ig) and ig > 0
