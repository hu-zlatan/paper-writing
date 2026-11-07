"""Synthetic check of code/analysis_test5_v5.py (no real test5 data is read)."""
import json
import os

import numpy as np


def _write(root, tag, m, rng, p, travel, gT):
    os.makedirs(os.path.join(root, "test5"), exist_ok=True)
    os.makedirs(os.path.join(root, "test5_gt"), exist_ok=True)
    with open(os.path.join(root, "test5", f"{tag}_{m}_000.jsonl"), "w") as f:
        f.write(json.dumps({"header": True}) + "\n")
        for e in range(300):
            f.write(json.dumps({"episode": e, "success": bool(rng.random() < p), "ball_info": float(rng.normal(5, 1)),
                                "travel_rad": float(travel), "n_probes": 4, "method": m}) + "\n")
    with open(os.path.join(root, "test5_gt", f"{tag}_{m}_000.jsonl"), "w") as f:
        for e in range(300):
            f.write(json.dumps({"episode": e, "g_T": float(rng.normal(gT, 0.3)), "method": m}) + "\n")


def test_synthetic_trend_and_rules(tmp_path, monkeypatch):
    root = str(tmp_path)
    monkeypatch.setenv("V5_RESULTS", root)
    import importlib
    import analysis_test5_v5 as A
    A = importlib.reload(A)
    monkeypatch.setattr(A, "N_BOOT", 300)
    rng = np.random.default_rng(1)
    gaps = {"S2": 0.25, "S4": 0.15, "S8": 0.08, "S12": 0.02, "A16-2": 0.25}   # gap grows with travel
    trav = {"S2": 1.0, "S4": 0.6, "S8": 0.3, "S12": 0.1, "A16-2": 1.0}
    for c, tag in A.CELLS.items():
        for m in A.methods(c):
            p = 0.6 if m == "gstar" else 0.6 - gaps[c] if m.startswith("student") else 0.1
            _write(root, tag, m, rng, p, trav[c] if m == "gstar" else 0.1, 6.0 if m.startswith("rl") else 5.5)
    json.dump({"cells": {c: {"H_star": "b_fan"} for c in A.CELLS}}, open(os.path.join(root, "12_base_hstar.json"), "w"))
    json.dump({"H5a_validation": {"cells_complete": list(A.CELLS), "cells_pass": []}}, open(os.path.join(root, "12_d5_analysis.json"), "w"))
    A.main()
    r = json.load(open(os.path.join(root, "14_test5_analysis.json")))
    assert all(r[c]["complete"] and r[c]["gt_complete"] for c in A.CELLS)
    assert r["H5b"]["verdict"] == "gap shrinks with travel"   # student - G* becomes more negative as travel grows
    assert r["S2"]["student_minus_gstar"]["success"]["holm_reject_5cells"]
    assert r["S2"]["H2_v5"]["claim_student_higher_on_rl_objective"] is False
    assert r["S2"]["H2_v5"]["inversion"] is True and "check_rlsucc" in r["S2"]["H2_v5"]
    assert "check_rlsucc" not in r["S4"]["H2_v5"]


def test_incomplete_cell_reports_nothing(tmp_path, monkeypatch):
    root = str(tmp_path)
    monkeypatch.setenv("V5_RESULTS", root)
    import importlib
    import analysis_test5_v5 as A
    A = importlib.reload(A)
    out, arr = A.cell_result("S4", {"cells": {}})
    assert out["complete"] is False and arr is None and "means" not in out
