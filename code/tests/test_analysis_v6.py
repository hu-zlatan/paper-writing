"""Synthetic checks of the v6 read-out (amendment v6.0): TOST direction, completeness gating, Holm wiring."""
import json
import os

import numpy as np


def _write(d, tag, m, eps, success, extra=None):
    os.makedirs(d, exist_ok=True)
    with open(os.path.join(d, f"{tag}_{m}_000.jsonl"), "w") as f:
        f.write(json.dumps({"header": True}) + "\n")
        for e in eps:
            r = {"episode": e, "success": int(success(e)), "ball_info": float(success(e)), "travel_rad": 0.1,
                 "n_probes": 4, "actions": [e % 7, 1]}
            r.update(extra or {})
            f.write(json.dumps(r) + "\n")


def test_tost_direction(monkeypatch, tmp_path):
    monkeypatch.setenv("V5_RESULTS", str(tmp_path / "v5")); monkeypatch.setenv("V6_RESULTS", str(tmp_path / "v6"))
    import importlib, analysis_v6
    importlib.reload(analysis_v6)
    analysis_v6.N_BOOT = 400
    rng = np.random.default_rng(1)
    B = (rng.random((2000, 2)) < 0.5).astype(float)
    same = analysis_v6.tost(B[:, :1].repeat(5, 1), B)
    far = analysis_v6.tost(B[:, :1].repeat(5, 1) + 0.2, B)
    assert same["p_tost"] < 0.05 and same["ci90"][0] > -0.04 and same["ci90"][1] < 0.04
    assert far["p_tost"] > 0.5


def test_incomplete_window_is_not_analysed(monkeypatch, tmp_path):
    monkeypatch.setenv("V5_RESULTS", str(tmp_path / "v5")); monkeypatch.setenv("V6_RESULTS", str(tmp_path / "v6"))
    import importlib, analysis_v6
    importlib.reload(analysis_v6)
    _write(str(tmp_path / "v5" / "test5"), "S_k2", "gstar", range(300), lambda e: e % 2)
    r, a = analysis_v6.window_result("S2", "0-499", range(500), {"cells": {"S2": {"H_star": "b_cov"}}})
    assert r["complete"] is False and a is None and r["episodes_per_method"]["gstar"] == 300
