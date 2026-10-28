import numpy as np

from touchbed.stats import crossed_bootstrap_diff, holm, seed_robustness


def test_bootstrap_detects_shift_and_null():
    rng = np.random.default_rng(0)
    base = rng.random(2000)
    A = (base[:, None] + 0.05 + 0.01 * rng.standard_normal((2000, 6)) > 0.5).astype(float)
    B = (base > 0.5).astype(float)
    r = crossed_bootstrap_diff(A, B, n_boot=2000)
    assert r["lower"] > 0 and r["p_greater"] < 0.01
    r0 = crossed_bootstrap_diff(B, B, n_boot=500)
    assert r0["diff"] == 0.0


def test_holm():
    assert holm([0.01, 0.04, 0.03, 0.2]) == [True, False, False, False]
    assert holm([0.001, 0.01, 0.02]) == [True, True, True]


def test_seed_robustness():
    A = np.array([[1, 0, 1], [1, 1, 1]], float)
    B = np.array([0.5, 0.5])
    assert seed_robustness(A, B) == (2, 3)
