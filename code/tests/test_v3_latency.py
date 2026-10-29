"""v3.0 C11: timed decisions reproduce the untimed policies; component timers sum to L_dec."""
import time

import numpy as np

from touchbed.distill import Student
from touchbed.evaluate_v2 import make_states_v2
from touchbed.latency3 import CONFIGS, parse, run_latency3, subset_for, timed_greedy, timed_student
from touchbed.likelihood import ObsModel, sample_obs
from touchbed.pf import ParticleFilter
from touchbed.policies_v2 import GStar
from touchbed.travel import A, PHI, PSI, TravelState
from touchbed.v3 import History


def test_grid_is_27_configs():
    assert len(CONFIGS) == 27 and len(set(CONFIGS)) == 27
    assert parse("g125_32_4") == (125, 32, 4)


def test_timed_greedy_equals_gstar_and_timers_sum():
    lib, prior, eps = make_states_v2("S", "pilot", 1)
    (k0, x0, y0, t0), phi0 = eps[0]
    om = ObsModel()
    rng = np.random.default_rng(0)
    a0 = 3
    obs = tuple(v[0] for v in sample_obs(om, lib, rng, np.array([k0]), x0, y0, t0, float(PHI[a0]), float(PSI[a0])))
    last = (float(PHI[a0]), float(PSI[a0]), obs)
    ts = TravelState(phi0, 12.0, 8.0)
    pf1 = ParticleFilter(lib, om, prior, 300, np.random.default_rng(5))
    pf2 = ParticleFilter(lib, om, prior, 300, np.random.default_rng(5))
    sub = np.arange(0, A, 2)
    pf1.update(*last)
    a_ref = GStar(np.random.default_rng(1), M=8, subset=sub).act(pf1, ts)
    t_start = time.perf_counter()
    a, tm = timed_greedy(pf2, ts, np.random.default_rng(1), 8, sub, last)
    total = time.perf_counter() - t_start
    assert a == a_ref
    assert abs(sum(tm.values()) - total) <= 0.05 * total + 2e-4


def test_timed_student_equals_act():
    st = Student(np.random.default_rng(0), hidden=32, tau=8.0)
    h = History()
    ts = TravelState(0.7, 12.0, 8.0)
    a, z, tm = timed_student(st, h.hist, ts)
    assert a == st.act(h, ts) and set(tm) == {"t_feat", "t_fwd", "t_mask"}


def test_run_latency3_smoke():
    st = Student(np.random.default_rng(0), hidden=16, tau=6.0)
    recs, finals = run_latency3("S", 12.0, 6.0, st, [0], warmup=0, max_decisions=2,
                                configs=["g125_32_4", "g125_%d_4" % A if A == 512 else "g125_128_4"], pruned=True)
    assert len(recs) == 2 and len(finals) == 1
    for r in recs:
        for m, tm in r["timers"].items():
            assert tm["L_dec"] > 0
