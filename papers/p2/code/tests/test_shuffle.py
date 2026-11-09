"""08f §2: the H4c shuffle permutes only non-P columns, within (pool, shift, split, dist) groups, deterministically."""
import os
import sys

import numpy as np

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from certgrip.featsets import matrix, row_features  # noqa: E402
from certgrip.io import load_rows  # noqa: E402


def _rows():
    rows = [r for r in load_rows("v1/labels/id_F1.jsonl") if r["split"] in ("train", "cal")]
    return rows[:200]


def test_shuffle_properties():
    rows = _rows()
    X = matrix(rows, "full_rd")
    Y = matrix(rows, "full_rd_shuf")
    Z = matrix(rows, "full_rd_shuf")
    n_p = len(row_features(rows[0], "P"))
    assert np.array_equal(Y, Z)
    assert np.array_equal(X[:, :n_p], Y[:, :n_p])
    assert not np.array_equal(X[:, n_p:], Y[:, n_p:])
    for key in {(r["split"], r["dist"]) for r in rows}:
        idx = [i for i, r in enumerate(rows) if (r["split"], r["dist"]) == key]
        a = sorted(map(tuple, X[idx, n_p:])); b = sorted(map(tuple, Y[idx, n_p:]))
        assert a == b
