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


def test_fid_and_massnoise_columns():
    import math
    from certgrip.featsets import noisy_mass, touch_only
    rows = _rows()[:20]
    for r in rows:
        a = row_features(r, "full_rd"); b = row_features(r, "full_rd_fid"); c = row_features(r, "full_rd_mn")
        assert b[:len(a)] == a and sum(b[len(a):]) == 1.0 and b[len(a) + int(r["family"][1]) - 1] == 1.0
        assert len(c) == len(a) and c[:5] == a[:5] and c[6:] == a[6:]
        assert abs(c[5] - math.log(noisy_mass(r))) < 1e-12 and c[5] != a[5]
        assert len(touch_only(r)) == len(row_features(r, "full")) - len(row_features(r, "P"))
    same = [r for r in _rows() if r["obj"] == rows[0]["obj"]]
    assert len({round(noisy_mass(r) / r["inst"]["mass"], 12) for r in same}) == 1
