import numpy as np

from comp_selection import select


def _rows(rng, n_obj=40):
    rows = []
    for fam in ("F1", "F2"):
        for obj in range(150, 150 + n_obj):
            for d in ("D1", "D2", "D3", "D4"):
                m, mu = rng.uniform(0.2, 1.0), rng.uniform(0.3, 1.0)
                fstar = m * 9.81 / (2 * mu) * rng.lognormal(0, 0.05)
                rows.append({"family": fam, "obj": obj, "dist": d, "unavoidable": False, "F_hi": fstar * 1.007,
                             "F_mid": fstar, "inst": {"mass": m, "mu": mu, "amp": 0.0, "freq": 1.0}})
    return rows


def test_informed_predictor_wins():
    rng = np.random.default_rng(0)
    rows = _rows(rng)
    lp = np.log([r["F_hi"] for r in rows]) + rng.normal(0, 0.02, len(rows))   # near-oracle "CertGrip-P"
    res, winner, n_unav, n = select(rows, lp)
    assert winner == "CertGrip-P" and n_unav == 0 and n == len(rows)
    assert res["CertGrip-P"]["RE_mean"] < res["CSF-1"]["RE_mean"]
