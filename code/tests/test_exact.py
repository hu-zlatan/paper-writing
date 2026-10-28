"""Exact checks of the EIG estimator on a discrete problem (two known states, one action)."""
import math

import numpy as np

from touchbed.geometry import Library, cast
from touchbed.likelihood import ObsModel
from touchbed.pf import ParticleFilter, Prior
from touchbed.policies import eig_candidates
from touchbed.shapes import Shape


def test_eig_two_hypotheses_hit_vs_miss():
    """Two equally likely states; the action hits one and misses the other -> outcomes almost perfectly separate the
    hypotheses (up to eps), so EIG ≈ log 2 (slightly less because of eps)."""
    v = np.array([[-10.0, -10.0], [10.0, -10.0], [10.0, 10.0], [-10.0, 10.0]])
    lib = Library([Shape("sq", v, [0.0])])
    om = ObsModel()
    pf = ParticleFilter(lib, om, Prior(1), 2, np.random.default_rng(0))
    k = np.array([0, 0]); x = np.array([0.0, 0.0]); y = np.array([0.0, 40.0]); th = np.zeros(2)
    w = np.array([0.5, 0.5])
    phi, psi = np.array([0.0]), np.array([0.0])  # ray along -x through y=0: hits state 0, misses state 1 (at y=40)
    hit, *_ = cast(lib, k, x, y, th, 0.0, 0.0)
    assert hit[0] and not hit[1]
    eig = eig_candidates(pf, phi, psi, 20000, np.random.default_rng(1), particles=(k, x, y, th, w))[0]
    assert abs(eig - math.log(2)) < 0.02
    # an action that misses both is uninformative
    eig0 = eig_candidates(pf, np.array([math.pi / 2]), np.array([0.6]), 4000, np.random.default_rng(2),
                          particles=(k, x, np.array([0.0, 0.0]), th, w))[0]
    assert abs(eig0) < 0.02
