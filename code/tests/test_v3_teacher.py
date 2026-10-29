"""Amendment v3.0 C7: GStar.score_vector() is the teacher label; argmax must equal GStar.act on the same RNG state."""
import numpy as np

from touchbed.evaluate_v2 import make_states_v2
from touchbed.likelihood import ObsModel, sample_obs
from touchbed.pf import ParticleFilter
from touchbed.policies_v2 import GStar
from touchbed.travel import A, PHI, PSI, TravelState


def _belief(seed, n=400, probes=1):
    lib, prior, eps = make_states_v2("S", "pilot", seed + 1)
    (k0, x0, y0, t0), phi0 = eps[seed]
    om = ObsModel()
    pf = ParticleFilter(lib, om, prior, n, np.random.default_rng(seed))
    rng = np.random.default_rng(100 + seed)
    for a in rng.choice(A, size=probes, replace=False):
        obs = tuple(v[0] for v in sample_obs(om, lib, rng, np.array([k0]), x0, y0, t0, float(PHI[a]), float(PSI[a])))
        pf.update(float(PHI[a]), float(PSI[a]), obs)
    return pf, TravelState(phi0, 12.0, 8.0)


def test_score_vector_matches_act():
    for seed in range(3):
        pf, ts = _belief(seed)
        a_act = GStar(np.random.default_rng(7), M=8).act(pf, ts)
        s, mask, a_sv = GStar(np.random.default_rng(7), M=8).score_vector(pf, ts)
        assert a_sv == a_act
        assert s.dtype == np.float32 and s.shape == (A,) and mask.shape == (A,)
        assert np.all(s[~mask] == 0) and np.all(s >= 0)
        assert np.array_equal(mask, ts.feasible())          # full candidate set: all feasible actions scored
        if s.max() > 0:
            assert s[a_sv] == s.max()


def test_score_vector_respects_subset():
    pf, ts = _belief(0)
    sub = np.arange(0, A, 4)
    s, mask, a = GStar(np.random.default_rng(3), M=4, subset=sub).score_vector(pf, ts)
    assert set(np.flatnonzero(mask)) <= set(sub) and a in sub


def test_numpy_lse_matches_scipy_in_ball_eig(monkeypatch):
    """Run-5 speed-up of ball_eig (plain-numpy log-sum-exp) is numerically equivalent to the scipy version."""
    from scipy.special import logsumexp

    from touchbed import ball
    pf, ts = _belief(1, n=300, probes=2)
    feas = np.flatnonzero(ts.feasible())
    args = (pf, PHI[feas], PSI[feas], 16)
    e_new = ball.ball_eig(*args, np.random.default_rng(4))
    monkeypatch.setattr(ball, "_lse", lambda a, axis: logsumexp(a, axis=axis))
    e_old = ball.ball_eig(*args, np.random.default_rng(4))
    assert np.allclose(e_new, e_old, rtol=0, atol=1e-10)
    assert int(np.argmax(e_new)) == int(np.argmax(e_old))
