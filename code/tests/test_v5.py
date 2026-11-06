"""Amendment v5.0: test5 split, v5 DAgger index range, best-checkpoint distillation."""
import numpy as np
import pytest

from touchbed.evaluate import SPLIT_SALT
from touchbed.v3 import V3_SALTS, dagger_index, state_v3


def test_test5_registered_and_fresh():
    assert V3_SALTS["test5"] == SPLIT_SALT["test5"] == 107
    assert len(set(SPLIT_SALT.values())) == len(SPLIT_SALT)
    a = [state_v3("S", "test5", i) for i in range(20)]
    for other in ("test3", "val3", "pilot3", "cal3"):
        assert not set(a) & {state_v3("S", other, i) for i in range(20)}
    assert state_v3("S", "test5", 3) == state_v3("S", "test5", 3, kappa=4.0)   # paired across kappa


def test_v5_dagger_indices_disjoint_from_v3_v4():
    old = {dagger_index(r, s, j) for r in (1, 2) for s in (501, 599, 601, 699) for j in (0, 799)}
    new = {dagger_index(r, s, j) for r in (1, 2) for s in range(701, 706) for j in range(800)}
    assert len(new) == 2 * 5 * 800 and not old & new
    assert min(new) >= 2_000_000
    with pytest.raises(ValueError):
        dagger_index(1, 700, 0)


def test_best_checkpoint_tracks_lowest_val_regret():
    from tests.test_v3_distill import ObsModel, states_v3, GStar, run_episode_v3, ep_key_v3, episode_arrays, stack
    from touchbed.distill import DistillConfig, Student, mean_regret, train_round
    from touchbed.nn import Adam
    om = ObsModel()
    lib, prior, eps = states_v3("S", "label3", range(4), kappa=12.0)
    packed = []
    for i, (s0, phi0) in enumerate(eps):
        r = run_episode_v3(None, lib, prior, om, s0, phi0, 12.0, 6.0, ep_key_v3("S", "label3", 12.0, 6.0, i),
                           n_dec=200, teacher=GStar(np.random.default_rng(i), M=4), evaluate=False)
        packed.append(episode_arrays(r["history"], r["labels"], 4))
    D = stack(packed)
    cfg = DistillConfig(lr=3e-3, batch=16, max_epochs=15, stop_patience=10 ** 9, tau=6.0, budget_minutes=5)
    st = Student(np.random.default_rng(1), hidden=32, tau=6.0)
    log, best = [], {}
    train_round(st, Adam(st.net.params(), lr=cfg.lr), D, np.arange(2), D, np.arange(2, 4), cfg,
                np.random.default_rng(2), log, best_out=best)
    vals = [e["val_R_bar"] for e in log]
    assert len(log) == 15 and best["R_bar"] == min(vals) and best["epoch"] == int(np.argmin(vals))
    st.set_state(best["state"])
    assert abs(mean_regret(st, D, np.arange(2, 4))["R_bar"] - best["R_bar"]) < 1e-12


def test_episode_arrays_belief_width_follows_library():
    """v5 run 31: A16 (K = 16) labels carry 96-wide belief features; S (K = 8) stays 48 wide."""
    import numpy as np
    from touchbed.distill import episode_arrays, A
    for width in (48, 96):
        lab = {"phi_t": 0.0, "tau_rem": 1.0, "s": np.zeros(A), "mask": np.ones(A, bool), "a_teacher": 0,
               "belief": np.ones(width, np.float32)}
        out = episode_arrays([(0.0, 0.0, (0, 0, 0, 0))], [lab], 3)
        assert out["BF"].shape == (3, width) and out["BF"][0].sum() == width
