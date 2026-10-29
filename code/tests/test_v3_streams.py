"""Amendment v3.0 C5 / v3.1 D1: v3 split salts and kappa-keyed training streams."""
import pytest

from touchbed.evaluate import SPLIT_SALT
from touchbed.evaluate_v2 import make_states_v2
from touchbed.v3 import V3_SALTS, dagger_index, state_v3


def test_salts_registered_and_v2_unchanged():
    assert {"pilot": 11, "val": 23, "test": 37, "g2": 53}.items() <= SPLIT_SALT.items()
    assert all(SPLIT_SALT[k] == v for k, v in V3_SALTS.items())
    assert len(set(SPLIT_SALT.values())) == len(SPLIT_SALT)


def test_eval_split_paired_across_kappa_and_disjoint_from_v2():
    a, b = state_v3("S", "test3", 5), state_v3("S", "test3", 5, kappa=12.0)
    assert a == b
    _, _, v2 = make_states_v2("S", "test", 6)
    assert state_v3("S", "test3", 5) != v2[5]


def test_training_split_needs_kappa_and_differs_by_kappa():
    with pytest.raises(ValueError):
        state_v3("S", "label3", 0)
    assert state_v3("S", "label3", 0, kappa=0.0) != state_v3("S", "label3", 0, kappa=12.0)


def test_dagger_indices_disjoint():
    seen = set()
    for r in (1, 2):
        for seed in list(range(501, 506)) + [521, 522, 523, 531, 532, 533]:
            for j in range(800):
                i = dagger_index(r, seed, j)
                assert i not in seen
                seen.add(i)
    with pytest.raises(ValueError):
        dagger_index(3, 501, 0)
