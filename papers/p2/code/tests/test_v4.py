"""Amendment 11: new pools f4 / c4 leave the id pool unchanged; c4 friction lies in its family band; splits have the
registered sizes; protocol noprobe runs (rd default replays are checked by test_react.py)."""
import glob
import json
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from certgrip.data import FAMILIES, MU_BAND, N_OBJ, make_instance, sample_object, split_of  # noqa: E402
from certgrip.io import ROOT  # noqa: E402
from certgrip.sim import Sim, preload_force  # noqa: E402
from main import SLIP  # noqa: E402


def test_id_pool_unchanged():
    f = sorted(glob.glob(os.path.join(ROOT, "v1/labels/id_F1*.jsonl")))[0]
    rows = [json.loads(l) for l in open(f)][1:6]
    for r in rows:
        if "inst" not in r:
            continue
        k = r["key"] if "key" in r else None
        o = sample_object("id", r["inst"]["family"], r["obj"]) if "obj" in r else sample_object(*(k[:1] + k[1:3]))
        assert abs(o["mu"] - r["inst"]["mu"]) < 1e-12 and abs(o["mass"] - r["inst"]["mass"]) < 1e-12


def test_c4_band_and_splits():
    for fam in FAMILIES:
        lo, hi = MU_BAND[fam]
        for obj in range(0, N_OBJ["c4"], 7):
            assert lo <= sample_object("c4", fam, obj)["mu"] <= hi
    assert [split_of("f4", o) for o in range(300)].count("cal") == 125
    assert [split_of("f4", o) for o in range(300)].count("test") == 175
    c = [split_of("c4", o) for o in range(350)]
    assert (c.count("select"), c.count("cal"), c.count("test")) == (50, 125, 175)
    assert sample_object("f4", "F1", 0)["mu"] != sample_object("id", "F1", 0)["mu"]


def test_noprobe_runs():
    inst = make_instance("f4", "F2", 3, "D1")
    sim = Sim(inst, preload_force(), delta_t=SLIP["delta_t"], rot_t_deg=SLIP["rot_t_deg"], protocol="noprobe")
    assert not sim.run(60.0)["slip"]
    assert sim.run(0.05)["slip"]


def test_crc_default_unchanged(tmp_path):
    """main.py crc with the default pool / protocol reproduces a stored v1 08c replay line exactly."""
    import main as M
    ref = [json.loads(l) for l in open(os.path.join(ROOT, "v1/crc/F1_200.jsonl"))][1]
    obj = ref["key"][2]
    out = str(tmp_path / "x")
    M.main(["crc", "--family", "F1", "--start", str(obj), "--count", "1", "--out", out])
    got = [json.loads(l) for l in open(out + ".jsonl")][1]
    assert got["key"] == ref["key"] and got["slip"] == ref["slip"] and got["F"] == ref["F"]
