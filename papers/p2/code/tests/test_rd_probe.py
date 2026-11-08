"""Amendment 08a tests: ramp-down probe determinism, touch-only onset, bracket consistency, CSF-mu-hat, feature sets."""
import math
import os
import sys

import numpy as np

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from certgrip.baselines import MU_HAT_CLIP, f_nom, f_nom_muhat, mu_hat  # noqa: E402
from certgrip.data import make_instance  # noqa: E402
from certgrip.features import record  # noqa: E402
from certgrip.featsets import matrix  # noqa: E402
from certgrip.sim import Sim, preload_force  # noqa: E402

F0 = preload_force()


def _rec(inst, F=60.0):
    s = Sim(inst, F0, protocol="rd")
    return s, s.run(F, record=True)


def test_probe_deterministic_and_force_independent():
    inst = make_instance("pilot", "F1", 3, "D4")
    s, r1 = _rec(inst, 60.0)
    o1 = r1["features"]["onset"]
    o2 = s.run(5.0, record=True)["features"]["onset"]       # the probe precedes the force ramp
    assert o1["F_onset"] == o2["F_onset"] and o1["eps"] == o2["eps"] and o1["found"]


def test_onset_tracks_coulomb_force():
    """Onset force within a factor e^0.6 below the Coulomb holding force on pilot objects 0-4 (D4)."""
    for fam in ("F1", "F2"):
        for o in range(5):
            inst = make_instance("pilot", fam, o, "D4")
            on = _rec(inst)[1]["features"]["onset"]
            r = math.log(inst.mass * 9.81 / (2 * inst.mu)) - math.log(on["F_onset"])
            assert -0.2 < r < 0.6, (fam, o, r)


def test_no_probe_drop_at_high_force_and_bracket():
    """No contact loss from the probe at F_max; slip is monotone across a coarse bracket (F 2 -> 60)."""
    inst = make_instance("pilot", "F2", 2, "D1")
    s = Sim(inst, F0, protocol="rd")
    out = [s.run(F)["slip"] for F in (0.5, 2.0, 8.0, 30.0, 100.0)]
    assert not out[-1]
    k = out.index(False)
    assert not any(out[k:])


def test_squeeze_protocol_unchanged():
    inst = make_instance("pilot", "F1", 0, "D4")
    r = Sim(inst, F0).run(30.0, record=True)
    assert "onset" not in r["features"]


def test_mu_hat_and_csf():
    assert MU_HAT_CLIP[0] <= mu_hat(0.5, 1e-6) <= MU_HAT_CLIP[1]
    m, mu = 0.4, 0.5
    Fon = m * 9.81 / (2 * mu)
    assert abs(mu_hat(m, Fon) - mu) < 1e-12
    assert abs(f_nom_muhat(m, "D4", 0.5, 0.0, Fon) - Fon) < 1e-12
    assert f_nom_muhat(m, "D1", 5.0, 0.0, Fon) > f_nom_muhat(m, "D3", 1.0, 0.0, Fon)
    assert f_nom(m, "D4", 0.5, 0.0) > 0


def test_featsets_sigma():
    inst = make_instance("pilot", "F3", 1, "D2")
    s, r = _rec(inst)
    row = {"inst": dict(inst.__dict__), "dist": "D2", "preload_slip": r["preload_slip"], "rec": record(r["features"])}
    X0, X2 = matrix([row], "full_rd", sigma=0.0), matrix([row], "full_rd", sigma=0.2)
    Xf = matrix([row], "full")
    assert X0.shape[1] == Xf.shape[1] + 2
    assert np.allclose(X0[:, :-2], Xf) and abs((X2 - X0)[0, -2] - 0.2 * row["rec"]["onset"]["eps"]) < 1e-9
    assert matrix([row], "P_onset").shape[1] == matrix([row], "P").shape[1] + 2
