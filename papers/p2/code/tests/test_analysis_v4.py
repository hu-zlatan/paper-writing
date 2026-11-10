"""analysis_v4 on synthetic data: matched-slip interpolation, Holm, a full run_pool pass (no real v4 result read)."""
import os
import sys

import numpy as np

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
import analysis_v4 as M  # noqa: E402


def synth(seed=0):
    rng = np.random.default_rng(seed)
    objs = [(f, o) for f in ("F1", "F2") for o in range(40)]
    keys = [("f4", f, o, d, None) for f, o in objs for d in ("D1", "D2")]
    N, J = len(keys), 81
    lam = np.linspace(-1.6, 1.6, J)
    fstar = np.exp(rng.normal(0, 0.5, N))
    D = {"L": {}, "F": {}, "strata": np.array([k[3] for k in keys]), "obj": [(k[1], k[2]) for k in keys],
         "split": ["cal" if k[2] < 20 else "test" for k in keys], "avoid": np.ones(N, bool),
         "mu": np.exp(rng.uniform(np.log(0.3), 0, N)), "keys": keys, "ref": {"mid": fstar}}
    for arm, sd in (("A", 0.2), ("B", 0.6)):
        g = fstar * np.exp(rng.normal(0, sd, N))
        F = g[:, None] * np.exp(lam)[None, :]
        D["F"][arm], D["L"][arm] = F, F < fstar[:, None]
    D["by_obj"] = {}
    for i, o in enumerate(D["obj"]):
        D["by_obj"].setdefault(o, []).append(i)
    return D


def test_run_pool_and_holm():
    D = synth()
    r, _ = M.run_pool(D, {"x": ("A", "B", "match"), "y": ("A", "B", "crc")}, 50)
    assert r["rows"]["x"]["point"] > 0 and r["rows"]["y"]["point"] > 0      # the sharper base force wins
    assert r["rows"]["x"]["valid_draws"] > 0
    adj = M.holm(np.array([0.01, 0.04, 0.03]))
    assert np.allclose(adj, [0.03, 0.06, 0.06])
