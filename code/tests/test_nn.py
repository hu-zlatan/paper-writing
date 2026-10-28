import numpy as np

from touchbed.nn import DeepSetsNet, FEAT_DIM


def _loss(net, F, bl, st, Wout):
    out, cache = net.forward(F, bl, st)
    return float(np.sum(out * Wout)), cache


def check(encoder):
    rng = np.random.default_rng(0)
    net = DeepSetsNet(rng, out_dim=3, hidden=16, out_scale=1.0, encoder=encoder, t_max=5)
    B, T = 3, 5
    F = rng.standard_normal((B, T, FEAT_DIM))
    bl = rng.integers(1, 10, (B, T)).astype(float)
    st = np.tile(np.arange(T), (B, 1)).astype(float)
    Wout = rng.standard_normal((B, T, 3))
    L, cache = _loss(net, F, bl, st, Wout)
    grads = net.backward(cache, Wout)
    for p, g in zip(net.params(), grads):
        for _ in range(6):
            idx = tuple(rng.integers(0, s) for s in p.shape)
            old = p[idx]
            p[idx] = old + 1e-6
            Lp, _ = _loss(net, F, bl, st, Wout)
            p[idx] = old - 1e-6
            Lm, _ = _loss(net, F, bl, st, Wout)
            p[idx] = old
            num = (Lp - Lm) / 2e-6
            assert abs(num - g[idx]) < 1e-5 * max(1.0, abs(num)), (encoder, p.shape, num, g[idx])


def test_grad_deepsets():
    check("deepsets")


def test_grad_concat():
    check("concat")


def test_prefix_excludes_current_touch():
    rng = np.random.default_rng(1)
    net = DeepSetsNet(rng, out_dim=2, hidden=8, out_scale=1.0)
    F = rng.standard_normal((1, 4, FEAT_DIM))
    bl = np.ones((1, 4)); st = np.zeros((1, 4))
    out1, _ = net.forward(F, bl, st)
    F2 = F.copy(); F2[0, 2] += 5.0  # changing touch 2 must not affect decisions at steps 0..2
    out2, _ = net.forward(F2, bl, st)
    assert np.allclose(out1[0, :3], out2[0, :3]) and not np.allclose(out1[0, 3], out2[0, 3])
