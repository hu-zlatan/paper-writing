import math

import numpy as np

from touchbed.relframe import RelDeepSets, abs_index_of_rel, rel_ctx, rel_features, rel_index_of_abs
from touchbed.train_v2 import TrainConfigV2, TrainerV2, masked_log_softmax
from touchbed.travel import A, PHI, TravelState


def test_permutations_are_inverse():
    s = np.array([0, 5, 31])
    r, a = rel_index_of_abs(s), abs_index_of_rel(s)
    for b in range(3):
        assert np.array_equal(r[b][a[b]], np.arange(A))
        assert np.array_equal(PHI[a[b][0]], PHI[s[b] * 8])   # relative action 0 = current angle


def test_rel_deepsets_gradient():
    rng = np.random.default_rng(0)
    B, T = 2, 3
    net = RelDeepSets(rng, A, hidden=8, out_scale=1.0)
    raw = rng.standard_normal((B, T, 6)); raw[..., 2] = rng.integers(0, 2, (B, T))
    phit = rng.uniform(0, 2 * math.pi, (B, T)); valid = np.ones((B, T), bool)
    Fr, M = rel_features(raw, phit, valid)
    ctx, s = rel_ctx(phit, np.full((B, T), 3.0), 5.0)
    W = rng.standard_normal((B, T, A))
    f = lambda: float(np.sum(net.forward(Fr, M, ctx, s)[0] * W))
    out, cache = net.forward(Fr, M, ctx, s)
    g = net.backward(cache, W)
    for P, G in zip(net.params(), g):
        idx = tuple(rng.integers(0, n) for n in P.shape)
        old = P[idx]; P[idx] = old + 1e-6; fp = f(); P[idx] = old - 1e-6; fm = f(); P[idx] = old
        assert abs((fp - fm) / 2e-6 - G[idx]) < 1e-4 * max(1, abs(G[idx]))


def test_rel_policy_is_rotation_equivariant_at_first_step():
    """With no history, rotating phi0 by k grid steps rotates the logits (absolute (cos, sin) phi_t context zeroed)."""
    tr = TrainerV2(TrainConfigV2(setname="S", kappa=6.0, tau=5.0, L=15, J=2, batch=4, hidden=16, extra={"frame": "rel"}))
    out = []
    for k in (0, 3):
        phit = np.array([[k * 2 * math.pi / 32]]); raw = np.zeros((1, 1, 6))
        Fr, M = rel_features(raw, phit, np.zeros((1, 1), bool))
        ctx, s = rel_ctx(phit, np.array([[5.0]]), 5.0); ctx[..., 3:] = 0
        out.append(tr.pi.forward(Fr, M, ctx, s)[0][0, 0])
    assert np.allclose(np.roll(out[0], 3 * 8), out[1])


def test_rel_training_step_runs():
    tr = TrainerV2(TrainConfigV2(setname="S", kappa=6.0, tau=5.0, L=15, J=2, batch=8, hidden=16, extra={"frame": "rel"}))
    ro = tr.rollout(tr.rng)
    st = tr.update(ro)
    assert np.isfinite(st["v_loss"]) and np.isfinite(ro["g_T"]).all()
