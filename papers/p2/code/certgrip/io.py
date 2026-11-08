"""Load label JSONL rows (header / EARLY_STOP lines dropped; duplicates from resumed shards keep the last copy)."""
from __future__ import annotations

import glob
import json
import os

ROOT = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "..", "results")


def key(r: dict) -> tuple:
    return (r["pool"], r["family"], r["obj"], r["dist"], r.get("shift"))


def load_rows(pattern: str, root: str = ROOT) -> list:
    rows = {}
    for f in sorted(glob.glob(os.path.join(root, pattern))):
        for line in open(f):
            if not line.strip():
                continue
            r = json.loads(line)
            if "header" in r or "EARLY_STOP_AT_80_PCT_BUDGET" in r:
                continue
            rows[key(r)] = r
    return [rows[k] for k in sorted(rows, key=lambda k: tuple("" if v is None else str(v).zfill(4) for v in k))]
