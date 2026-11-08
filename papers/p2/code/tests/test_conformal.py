"""UT2 (quantile indexing), UT4 (OQT identity and bound), UT7 (physics config identity), UT9 (tangential-only
slip metric), plus feature-set shapes. Synthetic data only; nothing here is a paper result."""
import math
import os
import sys

import numpy as np

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from certgrip.conformal import OQT, calibrate, decide, qhat  # noqa: E402
from certgrip.data import FAMILIES, DISTS, make_instance  # noqa: E402
from certgrip.sim import Sim, build_xml, preload_force, tangential_disp  # noqa: E402


def test_ut2_quantile_indexing_exact():
    rng = np.random.default_rng(0)
    for n in (19, 50, 149):
        for alpha in (0.05, 0.1, 0.2):
            s = rng.permutation(n + 1).astype(float)          # distinct scores
            miss = 0
            for j in range(n + 1):                             # leave-one-out: test point j
                rest = np.delete(s, j)
                miss += s[j] > qhat(rest, alpha)
            rate = miss / (n + 1)
            assert alpha - 1 / (n + 1) - 1e-12 <= rate <= alpha + 1e-12, (n, alpha, rate)


def test_qhat_infinite_when_n_small():
    assert qhat([1.0, 2.0], 0.1) == math.inf


def test_mondrian_and_decide():
    q = calibrate([0, 1, 2, 3], [0, 0, 0, 0], ["a", "a", "b", "b"], 0.5)
    assert set(q) == {"a", "b"}
    F, capped = decide(np.log([1.0, 50.0]), math.log(3.0), 100.0)
    assert np.allclose(F, [3.0, 100.0]) and list(capped) == [False, True]


def test_ut4_identity_and_bound():
    rng = np.random.default_rng(1)
    o = OQT(q1=0.2, eta=0.05, alpha=0.1, f_max=100.0)
    for t in range(3000):
        lp = rng.normal(1.0, 1.0) + (0.5 if t > 1000 else 0.0)
        F, capped = o.force(lp)
        fstar = math.exp(lp + rng.normal(0.3 + (0.5 if t > 1000 else 0.0), 0.2))
        o.update(F < fstar, capped)
    assert abs(o.identity_residual()) < 1e-8
    assert o.rate_bound() < 0.1


def test_ut7_physics_identical_across_families_and_shifts():
    import mujoco
    ref = None
    for fam in FAMILIES + ("F5",):
        pool = "s2" if fam == "F5" else "id"
        for d in DISTS:
            for sh in (None, "S1", "S3"):
                m = mujoco.MjModel.from_xml_string(build_xml(make_instance(pool, fam, 3, d, sh)))
                key = (m.opt.timestep, m.opt.cone, m.opt.integrator, m.opt.impratio,
                       tuple(sorted(set(m.geom_condim.tolist()))),
                       tuple(np.unique(m.geom_solref.round(9), axis=0).ravel().tolist()),
                       tuple(np.unique(m.geom_solimp.round(9), axis=0).ravel().tolist()))
                ref = ref or key
                assert key == ref, (fam, d, sh)


def test_ut9_tangential_only():
    assert tangential_disp([0.003, 0.0, 0.0]) == 0.0           # 3 mm pure normal -> no slip
    assert tangential_disp([0.0, 0.003, 0.0]) > 0.002          # 3 mm tangential -> slip
    assert tangential_disp([0.0, 0.0, 0.003]) > 0.002


def test_featsets_shapes():
    import main
    from certgrip.featsets import matrix
    import json
    import tempfile
    with tempfile.TemporaryDirectory() as d:
        main.main(["label", "--pool", "pilot", "--family", "F2", "--count", "1", "--halvings", "2", "--out", d + "/x"])
        rows = [json.loads(l) for l in open(d + "/x.jsonl")][1:]
    dims = [matrix(rows, f).shape[1] for f in ("base", "P", "S", "full", "oracle")]
    assert dims[0] < dims[1] < dims[2] < dims[3]
    assert not np.isnan(matrix(rows, "full")).any()
