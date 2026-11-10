"""Synthetic checks for analysis_v3_a (amendment 10 part A); no real replay is read."""
import os
import sys

import numpy as np

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
import analysis_v3_a as V  # noqa: E402


def test_lam_emp_smallest_ok():
    # 10 instances, 5 grid points; slips decrease with j
    L = np.zeros((10, 5), bool)
    L[:3, 0] = True; L[:1, 1] = True
    j, flag = V.lam_emp(L, alpha=0.10)
    assert (j, flag) == (1, False)   # j=0 slip 0.3 > 0.1, j=1 slip 0.1 <= 0.1


def test_lam_emp_monotonised_and_fallback():
    L = np.ones((4, 3), bool)
    assert V.lam_emp(L) == (2, True)
    L = np.zeros((10, 3), bool); L[:5, 2] = True   # a slip at the top propagates down after monotonising
    assert V.lam_emp(L) == (2, True)


def test_chosen_per_stratum():
    N, J = 8, 4
    L = np.zeros((N, J), bool)
    L[0:2, 0] = True                     # stratum 0 cal: needs j>=1
    D = {"L": {"a": L}, "strata": np.array([0, 0, 0, 0, 1, 1, 1, 1])}
    cal = np.array([0, 1, 4, 5]); test = np.array([2, 3, 6, 7])
    j = V.chosen(D, "a", cal, test, "emp")
    assert list(j) == [1, 1, 0, 0]
