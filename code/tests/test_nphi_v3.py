"""Amendment v3.0 C1: TOUCHBED_NPHI flag. The constant is read at import, so the module is reloaded under each value
and restored afterwards (other modules keep their import-time bindings; only travel's own objects are inspected)."""
import importlib
import os

import numpy as np
import pytest

from touchbed import travel


def _load(monkeypatch, nphi):
    if nphi is None:
        monkeypatch.delenv("TOUCHBED_NPHI", raising=False)
    else:
        monkeypatch.setenv("TOUCHBED_NPHI", str(nphi))
    return importlib.reload(travel)


@pytest.fixture(autouse=True)
def _restore():
    old = os.environ.get("TOUCHBED_NPHI")
    yield
    if old is None:
        os.environ.pop("TOUCHBED_NPHI", None)
    else:
        os.environ["TOUCHBED_NPHI"] = old
    importlib.reload(travel)


def test_default_is_v2_grid_bit_identical(monkeypatch):
    t = _load(monkeypatch, None)
    assert t.N_PHI == 32 and t.A == 256
    phi = np.repeat(np.arange(32) * (2 * np.pi / 32), 8)
    psi = np.tile(np.deg2rad(np.arange(-35, 36, 10, dtype=float)), 32)
    assert np.array_equal(t.PHI, phi) and np.array_equal(t.PSI, psi)
    assert t.rung_subset(16, 8).tolist() == [i * 8 + j for i in range(0, 32, 2) for j in range(8)]
    c = t.cost(0.3, 12.0)
    t32 = _load(monkeypatch, 32)
    assert np.array_equal(t32.PHI, phi) and np.array_equal(t32.cost(0.3, 12.0), c)


def test_v3_grid_512_and_nested_subsets(monkeypatch):
    t = _load(monkeypatch, 64)
    assert t.N_PHI == 64 and t.A == 512
    assert np.allclose(np.diff(np.unique(t.PHI)), 2 * np.pi / 64)
    c128, c32 = set(t.rung_subset(32, 4).tolist()), set(t.rung_subset(16, 2).tolist())
    assert len(c128) == 128 and len(c32) == 32 and c32 <= c128 <= set(range(512))
    assert len(t.rung_subset(16, 8)) == 128          # H3 completion candidate count unchanged (v3.0 C12)
    cost = t.cost(0.3, 12.0)
    assert cost.shape == (512,) and cost.min() >= 1.0 and cost.max() <= 13.0 + 1e-9
    ts = t.TravelState(0.3, 12.0, 6.0)
    assert ts.feasible().shape == (512,)


def test_invalid_flag_rejected(monkeypatch):
    monkeypatch.setenv("TOUCHBED_NPHI", "48")
    with pytest.raises(ValueError):
        importlib.reload(travel)
