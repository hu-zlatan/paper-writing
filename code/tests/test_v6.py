"""Amendment v6.0 E10: --run-salt is opt-in; the default reproduces the recorded v5 test5 G* actions exactly."""
import argparse
import json
import os

from touchbed import cli3

HERE = os.path.dirname(os.path.abspath(__file__))


def _parse(extra):
    p = argparse.ArgumentParser(); sub = p.add_subparsers(dest="cmd"); cli3.register(sub)
    return p.parse_args(["eval3", "--method", "g125_512_16", "--out", "o"] + extra)


def test_run_salt_defaults_to_none():
    assert _parse([]).run_salt is None
    assert _parse(["--run-salt", "r1"]).run_salt == "r1"


def _run(tmp_path, salt):
    out = str(tmp_path / f"e_{salt}")
    extra = ["--set", "S", "--kappa", "2", "--tau", "4.7", "--n-star", "4", "--split", "test5", "--start", "0",
             "--count", "1", "--no-grid"] + (["--run-salt", salt] if salt else [])
    p = argparse.ArgumentParser(); sub = p.add_subparsers(dest="cmd"); cli3.register(sub)
    a = p.parse_args(["eval3", "--method", "gstar", "--out", out] + extra)
    cli3.cmd_eval3(a)
    return [json.loads(l) for l in open(out + ".jsonl")][1]["actions"]


def test_default_reproduces_v5_and_salt_is_independent(tmp_path):
    rec = os.path.join(HERE, "..", "..", "results", "v5", "test5", "S_k2_gstar_000.jsonl")
    v5 = [json.loads(l) for l in open(rec)][1]
    assert v5["episode"] == 0
    assert _run(tmp_path, None) == v5["actions"]
    a1, a2 = _run(tmp_path, "r1"), _run(tmp_path, "r1")
    assert a1 == a2                                   # a salted re-run is itself deterministic
