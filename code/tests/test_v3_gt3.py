import numpy as np

from touchbed.evaluate import stream
from touchbed.gt3 import contrast_draws, g_T
from touchbed.train_v2 import TrainConfigV2, TrainerV2


def test_gT_matches_trainer_reward():
    """g_T recomputed from the trainer's own states, actions and observations equals the rollout's g_T."""
    tr = TrainerV2(TrainConfigV2(setname="S", kappa=12.0, tau=4.9, batch=3, L=255, extra={"frame": "rel"}))
    rec = {}
    orig = tr._states

    def wrapped(rng, B):
        out = orig(rng, B)
        rec["s"] = out
        return out
    tr._states = wrapped
    ro = tr.rollout(stream("gt3_test"), B=3, greedy=True)
    _, J, (kS, xS, yS, tS) = rec["s"]
    for b in range(3):
        hist = [(ro["RAW"][b, t, 0], ro["RAW"][b, t, 1], tuple(ro["RAW"][b, t, 2:6]))
                for t in range(ro["RAW"].shape[1]) if ro["alive"][b, t]]
        g = g_T(tr.lib, tr.om, hist, (kS[b], xS[b], yS[b], tS[b]), J=J)
        assert abs(g - ro["g_T"][b]) < 1e-9


def test_draws_are_method_free_and_fixed():
    tr = TrainerV2(TrainConfigV2(setname="S", kappa=12.0, tau=4.9))
    s0 = (0, 1.0, -2.0, 0.3)
    key = ("S", "test3", 12.0, 4.9, 7)
    a = contrast_draws(tr.lib, tr.prior, s0, key, J=16, L=63)
    b = contrast_draws(tr.lib, tr.prior, s0, key, J=16, L=63)
    assert all(np.array_equal(u, v) for u, v in zip(a, b)) and len(a[0]) == 79 and np.all(a[0][:16] == 0)
