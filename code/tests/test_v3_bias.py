"""G2' bias check (touchbed/bias3.py): the full-G* reference is deterministic given its keys and finite."""
import math

from touchbed.bias3 import bias_reference


def test_bias_reference_deterministic():
    a = bias_reference("A", 12.0, 3.3, 3, 0, n_roll=2)
    b = bias_reference("A", 12.0, 3.3, 3, 0, n_roll=2)
    assert a == b
    assert math.isfinite(a["v_ref"]) and a["n_roll"] == 2
