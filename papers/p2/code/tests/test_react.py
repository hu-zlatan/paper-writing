"""Addendum 10a: the controller hook is a no-op by default (replays identical to the v1 crc replays), and the
reactive controller only ever raises the force, at most MAX_STEPS times."""
import json
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from certgrip.data import make_instance  # noqa: E402
from certgrip.io import ROOT  # noqa: E402
from certgrip.sim import Sim, preload_force  # noqa: E402
from main import SLIP  # noqa: E402
import react_run as R  # noqa: E402


def _rows():
    p = os.path.join(ROOT, "v1/crc/F1_200.jsonl")
    return [json.loads(l) for l in open(p)][1:3]


def test_default_replays_identical_to_v1():
    for r in _rows():
        k = r["key"]
        sim = Sim(make_instance(*k), preload_force(), delta_t=SLIP["delta_t"], rot_t_deg=SLIP["rot_t_deg"], protocol="rd")
        for arm in ("CSF-1", "full_rd@0.2#0"):
            for F, s in list(zip(r["F"][arm], r["slip"][arm]))[::4]:
                assert bool(sim.run(F)["slip"]) == s


def test_controller_monotone_and_capped():
    k = _rows()[0]["key"]
    inst = make_instance(*k)
    sim = Sim(inst, preload_force(), delta_t=SLIP["delta_t"], rot_t_deg=SLIP["rot_t_deg"], protocol="rd")
    ctl = R.React(inst, 20.0, 0.0)          # r_safe 0 -> triggers whenever allowed; 20 N holds (no early break)
    o = sim.run(20.0, controller=ctl)
    assert o["n_steps"] == R.MAX_STEPS
    assert abs(o["F_end"] - 20.0 * R.FACTOR ** R.MAX_STEPS) < 1e-9
