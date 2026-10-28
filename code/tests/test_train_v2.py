import numpy as np

from touchbed.nn import FEAT_DIM
from touchbed.train_v2 import CTX_DIM, CategoricalDeepSets, TrainConfigV2, TrainerV2, masked_log_softmax


def test_categorical_net_gradcheck():
    rng = np.random.default_rng(0)
    net = CategoricalDeepSets(rng, 7, hidden=8, out_scale=1.0)
    F = rng.standard_normal((2, 4, FEAT_DIM)); C = rng.standard_normal((2, 4, CTX_DIM)); W = rng.standard_normal((2, 4, 7))
    out, cache = net.forward(F, C)
    grads = net.backward(cache, W)
    for p, g in zip(net.params(), grads):
        idx = tuple(rng.integers(0, s) for s in p.shape)
        old = p[idx]
        p[idx] = old + 1e-6; Lp = np.sum(net.forward(F, C)[0] * W)
        p[idx] = old - 1e-6; Lm = np.sum(net.forward(F, C)[0] * W)
        p[idx] = old
        assert abs((Lp - Lm) / 2e-6 - g[idx]) < 1e-5 * max(1, abs(g[idx]))


def test_masked_softmax_logp_and_entropy_gradients():
    rng = np.random.default_rng(1)
    z = rng.standard_normal(6); mask = np.array([1, 1, 0, 1, 0, 1], bool); a = 3
    def logp(z): return masked_log_softmax(z, mask)[a]
    def ent(z):
        l = masked_log_softmax(z, mask); p = np.where(mask, np.exp(l), 0); return -np.sum(np.where(mask, p * l, 0))
    lsm = masked_log_softmax(z, mask); p = np.where(mask, np.exp(lsm), 0)
    g_lp = (np.eye(6)[a] - p)
    H = ent(z); g_H = -p * (np.where(mask, lsm, 0) + H)
    for i in range(6):
        e = np.zeros(6); e[i] = 1e-6
        assert abs((logp(z + e) - logp(z - e)) / 2e-6 - (g_lp[i] if mask[i] else 0.0)) < 1e-6
        assert abs((ent(z + e) - ent(z - e)) / 2e-6 - g_H[i]) < 1e-6


def test_rollout_shapes_and_budget():
    tr = TrainerV2(TrainConfigV2(setname="S", kappa=6.0, tau=8.0, L=63, J=4, batch=8))
    ro = tr.rollout(tr.rng)
    assert ro["F"].shape[1] == 8 and (ro["n_probes"] >= 1).all()
    spent = (ro["COST"] * ro["alive"]).sum(1)
    assert (spent <= 8.0 + 1e-9).all() and (8.0 - spent < 7.0 + 1e-9).all()
