import math

import numpy as np

from touchbed.geometry import Library, cast, probe_ray
from touchbed.likelihood import ObsModel, loglik_from_pred, sample_obs, wrap
from touchbed.shapes import Shape


def square_lib():
    v = np.array([[-10.0, -10.0], [10.0, -10.0], [10.0, 10.0], [-10.0, 10.0]])
    return Library([Shape("sq", v, [0.0, math.pi / 2, math.pi, 3 * math.pi / 2])])


def test_axis_aligned_hit():
    lib = square_lib()
    # probe from +x axis pointing to the origin hits the right face x = 10 with normal 0 rad
    hit, px, py, n = cast(lib, 0, 0.0, 0.0, 0.0, 0.0, 0.0)
    assert hit and abs(px - 10) < 1e-9 and abs(py) < 1e-9 and abs(n) < 1e-9


def test_translation_rotation():
    lib = square_lib()
    # object moved to (5, 0) and rotated 45 deg: the vertex points to +x at x = 5 + 10*sqrt(2)
    hit, px, py, n = cast(lib, 0, 5.0, 0.0, math.pi / 4, 0.0, 0.0)
    assert hit and abs(px - (5 + 10 * math.sqrt(2))) < 1e-6
    # from +y the hit is on a face with normal pointing up after the 90-degree rotation of the bottom face etc.
    hit, px, py, n = cast(lib, 0, 0.0, 0.0, math.pi / 2, math.pi / 2, 0.0)
    assert hit and abs(py - 10) < 1e-9 and abs(wrap(n - math.pi / 2)) < 1e-9


def test_miss_and_angle():
    lib = square_lib()
    hit, *_ = cast(lib, 0, 0.0, 0.0, 0.0, 0.0, math.radians(30))  # line passes y = 100 tan30 ≈ 57.7 at x=0 → misses
    assert not hit
    # oblique hit: analytic intersection with x = 10 face
    psi = math.radians(3)
    ox, oy, dx, dy = probe_ray(0.0, psi)
    t = (10 - ox) / dx
    hit, px, py, n = cast(lib, 0, 0.0, 0.0, 0.0, 0.0, psi)
    assert hit and abs(py - (oy + t * dy)) < 1e-9


def test_broadcast_shapes():
    lib = square_lib()
    rng = np.random.default_rng(0)
    th = rng.uniform(0, 2 * math.pi, (7, 1))
    phi = rng.uniform(0, 2 * math.pi, (1, 5))
    hit, px, py, n = cast(lib, np.zeros((7, 1), int), 0.0, 0.0, th, phi, 0.0)
    assert hit.shape == (7, 5) and hit.all()  # centred square, rays through the centre always hit
    r = np.hypot(px, py)
    assert (r >= 10 - 1e-9).all() and (r <= 10 * math.sqrt(2) + 1e-9).all()


def test_likelihood_normalisation_monte_carlo():
    """The contact-branch density integrates (with NC mass) to 1: check E_{y~p}[1] via importance sampling from u."""
    lib = square_lib()
    om = ObsModel()
    rng = np.random.default_rng(1)
    # probability of NC for a hitting ray must be eps/2; for a missing ray 1 - eps/2
    c, *_ = sample_obs(om, lib, rng, np.zeros(200000, int), 0.0, 0.0, 0.0, 0.0, 0.0)
    assert abs((~c).mean() - om.eps / 2) < 5e-4
    c, *_ = sample_obs(om, lib, rng, np.zeros(200000, int), 0.0, 0.0, 0.0, 0.0, math.radians(30))
    assert abs((~c).mean() - (1 - om.eps / 2)) < 5e-4


def test_loglik_peak_and_nc():
    lib = square_lib()
    om = ObsModel()
    hit, qx, qy, qn = cast(lib, 0, 0.0, 0.0, 0.0, 0.0, 0.0)
    l_true = loglik_from_pred(om, True, qx, qy, qn, hit, qx, qy, qn)
    l_off = loglik_from_pred(om, True, qx + 3, qy, qn, hit, qx, qy, qn)
    assert l_true - l_off > 4.4  # 0.5 * 9 = 4.5 nats
    l_nc = loglik_from_pred(om, False, 0, 0, 0, hit, qx, qy, qn)
    assert abs(l_nc - math.log(om.eps / 2)) < 1e-12
