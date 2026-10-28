import math

import numpy as np

from touchbed.ball import ball_eig, in_ball, neighbours
from touchbed.geometry import Library, cast
from touchbed.likelihood import ObsModel
from touchbed.pf import ParticleFilter, Prior
from touchbed.shapes import Shape
from touchbed.travel import A, PHI, PSI, TravelState, cost, rung_subset


def test_action_set_and_cost():
    assert A == 256 and len(set(zip(PHI.round(6), PSI.round(6)))) == 256
    c = cost(0.0, 6.0)
    assert abs(c.min() - 1.0) < 1e-12 and abs(c.max() - 7.0) < 1e-9
    ts = TravelState(0.0, 6.0, 4.0)
    a = int(np.argmax(np.where(ts.feasible(), PHI, -1)))
    assert ts.feasible()[a]
    ts.step(0)
    assert abs(ts.tau_rem - 3.0) < 1e-12 and ts.n_probes == 1
    assert set(rung_subset(16, 8)) < set(range(256)) and len(rung_subset(8, 4)) == 32


def test_ball_eig_two_separated_hypotheses():
    """Two particles far apart (different balls), equal weight; an action that hits one and misses the other identifies
    the ball: EIG_B ≈ log 2."""
    v = np.array([[-10.0, -10.0], [10.0, -10.0], [10.0, 10.0], [-10.0, 10.0]])
    lib = Library([Shape("sq", v, [0.0])])
    pf = ParticleFilter(lib, ObsModel(), Prior(1), 2, np.random.default_rng(0))
    k = np.array([0, 0]); x = np.zeros(2); y = np.array([0.0, 40.0]); th = np.zeros(2); w = np.array([0.5, 0.5])
    nb = neighbours(lib, k, x, y, th)
    assert nb.sum() == 2
    e = ball_eig(pf, np.array([0.0]), np.array([0.0]), 20000, np.random.default_rng(1), particles=(k, x, y, th, w), nb=nb)
    assert abs(e[0] - math.log(2)) < 0.02
    # two particles inside the same ball: no ball information can be gained
    y2 = np.array([0.0, 2.0])
    nb2 = neighbours(lib, k, x, y2, th)
    e2 = ball_eig(pf, np.array([math.pi / 2]), np.array([0.0]), 4000, np.random.default_rng(2), particles=(k, x, y2, th, w), nb=nb2)
    assert abs(e2[0]) < 1e-9
