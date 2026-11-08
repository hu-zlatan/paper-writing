"""UT1 (split / pool disjointness), instance determinism, shift pairing, label bracket sanity (tiny)."""
import dataclasses
import json
import math
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from certgrip.data import DISTS, FAMILIES, SALT, make_instance, sample_object, split_of  # noqa: E402


def test_splits_disjoint_and_sized():
    s = [split_of("id", i) for i in range(500)]
    assert s.count("train") == 150 and s.count("select") == 50 and s.count("cal") == 125 and s.count("test") == 175
    from certgrip.data import N_OBJ, h3_role
    r = [h3_role("id", i) for i in range(500)]
    assert r.count("oracle") == 44 and r.count("stream") == 131 and r.count("none") == 325
    t = [split_of("s2", i) for i in range(N_OBJ["s2"])]
    assert t.count("oracle") == 175 and t.count("stream") == 375
    assert len(set(SALT.values())) == len(SALT)


def test_deterministic_and_object_shared():
    a = make_instance("id", "F2", 7, "D3")
    b = make_instance("id", "F2", 7, "D3")
    assert a == b
    c = make_instance("id", "F2", 7, "D1")
    assert (a.size, a.mass, a.mu, a.com) == (c.size, c.mass, c.mu, c.com)   # same object across disturbances
    assert a.grasp_dz != c.grasp_dz


def test_pools_differ():
    assert sample_object("id", "F1", 0) != sample_object("pilot", "F1", 0)


def test_shift_pairing_changes_one_factor():
    for fam in FAMILIES:
        for d in DISTS:
            base = make_instance("id", fam, 400, d)
            s1 = make_instance("id", fam, 400, d, "S1")
            s3 = make_instance("id", fam, 400, d, "S3")
            assert math.isclose(s1.mu, 0.6 * base.mu) and dataclasses.replace(s1, mu=base.mu) == base
            assert math.isclose(s3.amp, 1.5 * base.amp) and dataclasses.replace(s3, amp=base.amp) == base


def test_label_cli_bracket(tmp_path):
    import main
    out = str(tmp_path / "lab")
    main.main(["label", "--pool", "pilot", "--family", "F1", "--start", "0", "--count", "1", "--dists", "D4",
               "--halvings", "4", "--out", out])
    rows = [json.loads(l) for l in open(out + ".jsonl")]
    assert rows[0]["header"] and len(rows) == 2
    r = rows[1]
    if not r["unavoidable"]:
        assert r["F_lo"] < r["F_mid"] < r["F_hi"] <= 100.0 and r["n_replays"] == 5
    assert len(r["rec"]["touch_probe"]) == 10 and len(r["rec"]["touch_preload"]) == 14
