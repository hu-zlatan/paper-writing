import numpy as np
import sys, os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))
from analysis_v2_a import cp_upper, lam_ltt, matched_re


def test_cp_upper_monotone():
    assert cp_upper(0, 100) < cp_upper(5, 100) < cp_upper(10, 100) <= 1.0
    assert abs(cp_upper(0, 100) - (1 - 0.1 ** (1 / 100))) < 1e-9


def test_ltt_scans_from_top():
    n, J = 500, 5
    L = np.zeros((n, J), bool)
    L[:250, :2] = True          # risk 0.5 at j 0-1, 0 above
    j, f = lam_ltt(L)
    assert j == 2 and not f
    j, f = lam_ltt(np.ones((n, J), bool))
    assert j == J - 1 and f


def test_matched_re_interpolates():
    fr = [(0.2, 0.1), (0.12, 0.2), (0.08, 0.4), (0.05, 0.6)]
    assert abs(matched_re(fr) - 0.3) < 1e-12
    assert matched_re([(0.05, 1.0), (0.04, 2.0)]) is None
