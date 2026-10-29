"""Amendment v3.0 C7: soft-label CE gradient check, target and regret definitions, end-to-end labelling + training."""
import numpy as np

from touchbed.distill import (DistillConfig, Student, episode_arrays, loss_and_grad, mean_regret, regret, soft_target,
                              stack, train_round)
from touchbed.likelihood import ObsModel
from touchbed.nn import Adam
from touchbed.policies_v2 import GStar
from touchbed.travel import A
from touchbed.v3 import History, ep_key_v3, run_episode_v3, states_v3


def test_soft_label_gradient_matches_finite_differences():
    rng = np.random.default_rng(0)
    B, T = 2, 3
    logits = rng.normal(size=(B, T, A))
    s = np.abs(rng.normal(size=(B, T, A)))
    mask = rng.random((B, T, A)) < 0.6
    valid = np.array([[True, True, False], [True, False, False]])
    at = np.argmax(np.where(mask, s, -1), -1)
    for beta, lam in ((4.0, 0.5), (16.0, 0.0)):
        _, g = loss_and_grad(logits, s, mask, at, valid, beta, lam)
        for _ in range(20):
            b, t, a = rng.integers(B), rng.integers(T), rng.integers(A)
            e = np.zeros_like(logits); e[b, t, a] = 1e-5
            fd = (loss_and_grad(logits + e, s, mask, at, valid, beta, lam)[0]
                  - loss_and_grad(logits - e, s, mask, at, valid, beta, lam)[0]) / 2e-5
            assert abs(fd - g[b, t, a]) < 1e-6


def test_soft_target_tie_rule_and_support():
    s = np.zeros((1, A)); mask = np.zeros((1, A), dtype=bool); mask[0, :4] = True
    s[0, :4] = 0.3                      # sigma_s = 0 -> uniform over the argmax set
    q = soft_target(s, mask, 4.0)
    assert np.allclose(q[0, :4], 0.25) and q[0, 4:].sum() == 0
    s[0, 0] = 1.0
    q = soft_target(s, mask, 4.0)
    assert q[0, 0] > q[0, 1] and abs(q.sum() - 1) < 1e-12 and q[0, 4:].sum() == 0


def test_regret_floor_ties_and_exclusion():
    mask = np.zeros((3, A), dtype=bool); mask[:, :5] = True
    s = np.zeros((3, A))
    s[0, :5] = [1.0, 0.5, 0.4, 0.3, 0.2]       # median 0.4 -> den 0.6
    s[1, :5] = [1.0, 0.99, 0.99, 0.99, 0.0]    # median 0.99 -> floored den 0.05 (tie decision)
    r, ex, tie = regret(s, mask, np.array([1, 1, 0]))
    assert abs(r[0] - 0.5 / 0.6) < 1e-12 and abs(r[1] - 0.01 / 0.05) < 1e-9
    assert ex.tolist() == [False, False, True] and tie.tolist() == [False, True, False]
    assert regret(s, mask, np.array([0, 0, 0]))[0][0] == 0.0


def test_label_and_train_end_to_end_small():
    om = ObsModel()
    lib, prior, eps = states_v3("S", "label3", range(6), kappa=12.0)
    T = 4
    packed = []
    for i, (s0, phi0) in enumerate(eps):
        teacher = GStar(np.random.default_rng(i), M=4)
        r = run_episode_v3(None, lib, prior, om, s0, phi0, 12.0, 6.0, ep_key_v3("S", "label3", 12.0, 6.0, i),
                           n_dec=200, teacher=teacher, evaluate=False)
        assert len(r["labels"]) == r["n_probes"] and all(r["executed_teacher"])
        assert [lab["a_teacher"] for lab in r["labels"]] == r["actions"]
        packed.append(episode_arrays(r["history"], r["labels"], T))
    D = stack(packed)
    cfg = DistillConfig(lr=3e-3, batch=16, max_epochs=40, stop_patience=40, tau=6.0, budget_minutes=5)
    st = Student(np.random.default_rng(1), hidden=32, tau=6.0)
    before = mean_regret(st, D)["R_bar"]
    log = []
    train_round(st, Adam(st.net.params(), lr=cfg.lr), D, np.arange(6), D, np.arange(6), cfg, np.random.default_rng(2), log)
    after = mean_regret(st, D)["R_bar"]
    assert after < before                      # fits its own training labels
    # the student acts from a touch history only
    from touchbed.travel import TravelState
    a = st.act(History(), TravelState(0.3, 12.0, 6.0))
    assert 0 <= a < A
    # DAgger episode: student acts, teacher labels every visited decision, beta = 0.5 mixing; grid read-out
    s0, phi0 = eps[0]
    r = run_episode_v3(st, lib, prior, om, s0, phi0, 12.0, 6.0, ep_key_v3("S", "dagger3", 12.0, 6.0, 100_001),
                       needs_belief=False, n_dec=200, teacher=GStar(np.random.default_rng(9), M=4), beta=0.5,
                       mix_rng=np.random.default_rng(10), evaluate=True)
    assert len(r["labels"]) == r["n_probes"]
    for lab, a_ex, used in zip(r["labels"], r["actions"], r["executed_teacher"]):
        assert a_ex == (lab["a_teacher"] if used else lab["a_policy"])
    assert {"success", "ball_info"} <= set(r)
