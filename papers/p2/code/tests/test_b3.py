"""B3: the scalar per-stratum tracker equals the 08d vectorised OQT when fed label-rule feedback."""
import numpy as np

import b3_online as B
import h3_streams as H


def test_tracker_matches_08d():
    rng = np.random.default_rng(0)
    T = 400
    lg = rng.normal(1.0, 0.5, T); st = rng.integers(0, 4, T); fhi = np.exp(lg + rng.normal(0.1, 0.3, T))
    fhi[::37] = np.inf
    q0, eta = rng.normal(0, 0.2, 4), 0.05
    F, sl, cap, _ = B.tracker(lg, st, q0, eta, lambda t, f: f < fhi[t])
    F2, sl2, cap2 = H.run_streams(lg[None], fhi[None], st[None], q0[None], eta)
    assert np.allclose(F, F2[0]) and (sl == sl2[0]).all() and (cap == cap2[0]).all()
