"""§1.7 heuristics: reservation rule, determinism, and the specific choices of B-spread / B-fan."""
import math

import numpy as np

from touchbed.evaluate_v2 import make_states_v2
from touchbed.heuristics import PSI_DEG, BCov, BFan, BSpread, allowed_mask
from touchbed.likelihood import ObsModel, sample_obs
from touchbed.pf import ParticleFilter
from touchbed.travel import PHI, PSI, TravelState, wrap


def _rollout(cls, kappa, tau, n_star, seed=0, pf=None):
    ts = TravelState(0.4, kappa, tau)
    pol = cls(np.random.default_rng(seed), n_star)
    acts = []
    while not ts.done():
        a = pol.act(pf, ts)
        assert ts.feasible()[a]
        ts.step(a)
        acts.append(a)
    return acts, ts


def test_reservation_rule_guarantees_n_star_probes():
    for cls in (BSpread, BFan):
        for kappa, tau in ((0.0, 4.0), (12.0, 9.0), (12.0, 14.0)):
            acts, ts = _rollout(cls, kappa, tau, n_star=4)
            assert ts.n_probes >= 4, (cls.name, kappa, tau, ts.n_probes)


def test_allowed_mask_definition():
    ts = TravelState(0.0, 12.0, 6.0)
    m = allowed_mask(ts, 4)               # reserve 3 strokes for the remaining probes
    assert np.array_equal(m, ts.costs() <= 3.0 + 1e-12)


def test_determinism_and_choices():
    a1, _ = _rollout(BSpread, 12.0, 14.0, 4)
    a2, _ = _rollout(BSpread, 12.0, 14.0, 4)
    assert a1 == a2 and all(PSI_DEG[a] == 5 for a in a1)
    f1, _ = _rollout(BFan, 0.0, 4.0, 4)
    assert [int(PSI_DEG[a]) for a in f1] == [5, -5, 15, -15]
    assert len({round(float(PHI[a]), 9) for a in f1}) == 1          # no travel at kappa = 0 either: stays put
    # spread at kappa = 0: first probe (near) antipodal to phi0 = 0.4, second at ~90 degrees from both
    s0, _ = _rollout(BSpread, 0.0, 4.0, 4)
    assert abs(abs(float(wrap(PHI[s0[0]] - 0.4))) - math.pi) < 0.2
    assert abs(abs(float(wrap(PHI[s0[1]] - PHI[s0[0]]))) - math.pi / 2) < 0.2


def test_bcov_runs_on_a_belief():
    lib, prior, eps = make_states_v2("S", "pilot", 1)
    (k0, x0, y0, t0), _ = eps[0]
    om = ObsModel()
    pf = ParticleFilter(lib, om, prior, 300, np.random.default_rng(0))
    ts = TravelState(0.4, 12.0, 9.0)
    pol = BCov(np.random.default_rng(1), 4)
    rng = np.random.default_rng(2)
    while not ts.done():
        a = pol.act(pf, ts)
        ts.step(a)
        obs = tuple(v[0] for v in sample_obs(om, lib, rng, np.array([k0]), x0, y0, t0, float(PHI[a]), float(PSI[a])))
        pf.update(float(PHI[a]), float(PSI[a]), obs)
    assert ts.n_probes >= 4
