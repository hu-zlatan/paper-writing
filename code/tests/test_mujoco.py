import math

import numpy as np

from touchbed.geometry import Library, cast
from touchbed.mujoco_eval import MujocoProbe
from touchbed.shapes import get_set


def test_small_finger_matches_ray_model():
    shapes = get_set("S")
    lib = Library(shapes)
    mp = MujocoProbe(shapes, r_finger=0.3)
    rng = np.random.default_rng(0)
    agree, errs, nerr = 0, [], []
    for i in range(40):
        k = int(rng.integers(lib.K)); x, y = rng.uniform(-15, 15, 2); th = rng.uniform(-math.pi, math.pi)
        phi, psi = rng.uniform(-math.pi, math.pi), rng.uniform(-0.6, 0.6)
        mp.set_object(k, x, y, th)
        h1, x1, y1, n1 = mp.probe(phi, psi)
        h2, x2, y2, n2 = cast(lib, k, x, y, th, phi, psi)
        agree += int(h1 == bool(h2))
        if h1 and h2:
            errs.append(math.hypot(x1 - x2, y1 - y2))
            nerr.append(abs((n1 - n2 + math.pi) % (2 * math.pi) - math.pi))
    assert agree >= 38
    assert np.median(errs) < 0.6 and np.median(nerr) < math.radians(3)
