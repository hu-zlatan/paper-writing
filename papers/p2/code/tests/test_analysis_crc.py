import numpy as np

from analysis_crc import TARGET, analyse, lam_index


def _synth(sd_t, sd_c, n_obj=(60, 80), seed=0):
    rng = np.random.default_rng(seed)
    keys = [(f, o, d) for f in ("F1", "F2") for o in range(sum(n_obj)) for d in ("D1", "D2", "D3", "D4")]
    N = len(keys)
    fstar = np.exp(rng.normal(2.0, 0.5, N))
    D = {"L": {}, "F": {}, "strata": np.array([k[2] for k in keys]), "obj": [(k[0], k[1]) for k in keys],
         "split": ["cal" if k[1] < n_obj[0] else "test" for k in keys], "avoid": np.ones(N, bool)}
    for arm, sd in ((TARGET, sd_t), ("CSF-1", sd_c), ("CSF-muhat@0.2", sd_c)):
        e = rng.normal(0, sd, N)
        q = np.quantile(-e, 0.9)
        grid = q + np.linspace(-0.4, 0.4, 20)
        F = fstar[:, None] * np.exp(e[:, None] + grid[None, :])
        D["F"][arm], D["L"][arm] = F, F < fstar[:, None]
    D["ref"] = {"mid": fstar, "lo": fstar * 0.996, "hi": fstar * 1.004}
    D["fhi"] = D["ref"]["hi"]
    return D


def test_lam_index_edges():
    assert lam_index(np.zeros((50, 20), bool)) == (0, False)
    assert lam_index(np.ones((50, 20), bool)) == (19, True)
    L = np.zeros((99, 20), bool); L[:, :5] = True; L[:15, 10] = True    # non-monotone flicker is monotonised
    assert lam_index(L)[0] == 11
    L[:15, 10] = False; L[0, 10] = True
    assert lam_index(L)[0] == 5


def test_superiority_and_validity():
    r = analyse(_synth(0.1, 0.5), draws=200)
    assert r["contrasts"]["H2a"]["decision"] == "superiority"
    assert r["arms"][TARGET]["slip_phys"] <= 0.16
    assert r["arms"][TARGET]["RE_mid"] < r["arms"]["CSF-1"]["RE_mid"]


def test_equal_arms_not_superior():
    r = analyse(_synth(0.3, 0.3, seed=1), draws=200)
    assert r["contrasts"]["H2b"]["decision"] != "superiority"
    assert abs(r["contrasts"]["H2b"]["D"]["mid"]) < 0.3
