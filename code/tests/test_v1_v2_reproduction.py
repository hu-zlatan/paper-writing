"""G0 (vi): with kappa = 0 and tau = 3, the v2 runner reproduces the v1 runner bit for bit given the same action
sequence and RNG streams (environment, likelihood, evaluation PF and estimate are shared code)."""
import numpy as np

from touchbed.evaluate import make_states, run_episode
from touchbed.evaluate_v2 import run_episode_v2
from touchbed.likelihood import ObsModel
from touchbed.travel import PHI, PSI

SEQ = [5, 77, 140]


class FixedV1:
    def __init__(self, rng):
        self.t = 0

    def act(self, pf):
        a = SEQ[self.t]; self.t += 1
        return float(PHI[a]), float(PSI[a])


class FixedV2:
    def __init__(self, rng):
        self.t = 0

    def act(self, pf, ts):
        a = SEQ[self.t]; self.t += 1
        return a


def test_kappa0_tau3_reproduces_v1():
    lib, prior, states = make_states("S", "pilot", 3)
    om = ObsModel()
    for i, s0 in enumerate(states):
        key = ("repro", i)
        r1, _ = run_episode(FixedV1, lib, prior, om, s0, 3, key, n_eval=1500, needs_belief=False)
        r2 = run_episode_v2(FixedV2, lib, prior, om, s0, 0.0, 0.0, 3.0, key, n_eval=1500, needs_belief=False)
        assert r2["n_probes"] == 3
        for m in ("success", "identity_ok", "trans_err_mm", "rot_err_deg"):
            assert r1[m] == r2[m], (m, r1[m], r2[m])
