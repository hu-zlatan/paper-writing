import numpy as np

import h3_streams as H


def _pool(rng, n_obj, fam, pool, shift=0.0, start=0):
    keys, objs = [], []
    for o in range(start, start + n_obj):
        for d in H.STRATA:
            keys.append((pool, fam, o, d, None)); objs.append((fam, o, pool))
    N = len(keys)
    lg = rng.normal(2.0, 0.4, N)
    fstar = np.exp(lg + rng.normal(0, 0.2, N) + shift)
    return {"key": keys, "obj": objs, "st": np.tile(np.arange(4), n_obj),
            "lg": np.stack([lg, lg + rng.normal(0, 0.3, N)], 1), "fhi": fstar * 1.005, "fmid": fstar,
            "avoid": np.ones(N, bool)}


def test_oqt_identity_and_rate():
    rng = np.random.default_rng(0)
    B, T = 4, 4000
    st = rng.integers(0, 4, (B, T)); lg = rng.normal(0, 0.3, (B, T)); fhi = np.exp(lg + rng.normal(0, 0.3, (B, T)))
    q0 = np.zeros((B, 4)); eta = 0.03
    F, slip, cap = H.run_streams(lg, fhi, st, q0, eta)
    assert not cap.any()
    assert abs(slip[:, 1000:].mean() - H.ALPHA) < 0.02
    # UT4 identity per stratum: final q - q1 = eta * sum(slip - alpha)
    q_final = np.log(F[:, -1]) - lg[:, -1]  # q used at the last step of its stratum
    s_last = st[:, -1]
    for b in range(B):
        m = (st[b] == s_last[b]); m[-1] = False
        assert np.isclose(q_final[b], eta * (slip[b][m] - H.ALPHA).sum(), atol=1e-9)


def test_no_shift_ratio_near_one():
    rng = np.random.default_rng(1)
    pre = _pool(rng, 180, "F1", "id")
    stm = _pool(rng, 524, "F1", "id", start=400)
    pools = {"X": {"pre": pre, "oracle": pre, "stream": stm}}
    cal = _pool(rng, 500, "F1", "id", start=2000)
    qoff, eta = H.offline(cal)
    H.SHIFTS = ("X",)
    point, *_ = H.shift_summary(pools, "X", qoff, eta, n_ord=4)
    r = point["OQT-CertGrip"]["RE_window"] / point["Oracle-CertGrip"]["RE_window"]
    assert 0.85 < r < 1.2
    assert abs(point["OQT-CertGrip"]["slip_label_window"] - H.ALPHA) < 0.04
    bs = H.bootstrap(pools, "X", qoff, eta, draws=6, chunk=3, n_ord=2)
    assert bs["OQT-CertGrip"].shape == (6, 2)


def test_shift_breaks_frozen_not_oqt():
    rng = np.random.default_rng(2)
    pre = _pool(rng, 180, "F1", "id")
    orc = _pool(rng, 180, "F1", "id", shift=0.5)
    stm = _pool(rng, 524, "F1", "id", shift=0.5, start=400)
    cal = _pool(rng, 500, "F1", "id", start=2000)
    qoff, eta = H.offline(cal)
    H.SHIFTS = ("X",)
    point, *_ = H.shift_summary({"X": {"pre": pre, "oracle": orc, "stream": stm}}, "X", qoff, eta, n_ord=4)
    assert point["Frozen-CertGrip"]["slip_label_window"] > 0.4
    assert abs(point["OQT-CertGrip"]["slip_label_window"] - H.ALPHA) < 0.05
    assert abs(point["Oracle-CertGrip"]["slip_label_window"] - H.ALPHA) < 0.05
