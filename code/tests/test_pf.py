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


def test_contact_proposal_density_integrates_to_one():
    """Monte Carlo check: E_{s~q}[1/q(s)] over the box... instead check E_{s~prior}[q(s)/p(s)] ≈ 1 restricted to the box
    is not exact (q leaks outside); so check self-normalisation by sampling from q and comparing histogram mass."""
    lib = Library(get_set("A"))
    pf = ParticleFilter(lib, ObsModel(), Prior(lib.K), 10, np.random.default_rng(0))
    C = np.array([[30.0, 5.0, 0.2], [-20.0, 25.0, 2.0]])
    rng = np.random.default_rng(1)
    # importance estimate of the integral of q over R^2 x S^1 x {k}: E_{s~g}[q(s)/g(s)] with g uniform on a big box
    n = 200000
    half = 120.0
    k = rng.integers(0, lib.K, n); x = rng.uniform(-half, half, n); y = rng.uniform(-half, half, n)
    th = rng.uniform(-np.pi, np.pi, n)
    lg = -math.log(lib.K) - 2 * math.log(2 * half) - math.log(2 * np.pi)
    pf.q_beta = 1e-12  # contact component only
    est = np.mean(np.exp(pf._q_logpdf(C, k, x, y, th) - lg))
    assert abs(est - 1.0) < 0.08


def test_rejuvenate_zero_is_noop_and_keeps_posterior_support():
    lib, pf, s0 = run(n=2000, T=4, seed=3)
    before = (pf.k.copy(), pf.x.copy(), pf.th.copy(), pf.logw.copy())
    pf.rejuvenate(0)
    assert all(np.array_equal(a, b) for a, b in zip(before, (pf.k, pf.x, pf.th, pf.logw)))
    pf.rejuvenate(5)
    assert np.allclose(pf.logw, -math.log(pf.n))            # forced resample leaves uniform weights
    assert np.allclose(pf.loglik_hist, pf._hist_loglik(pf.k, pf.x, pf.y, pf.th))  # cached likelihoods stay exact
    assert pf.mh_steps == 3                                   # path kernel restored
