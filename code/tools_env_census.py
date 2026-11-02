"""Count the software environments recorded in the header line of every result shard.

Usage (from the repo root):  python code/tools_env_census.py [out_json]
Reads results/**/*.jsonl, takes the first line when it is a header with an "env" block, and groups shards by
(version directory, python, numpy, thread variables). Bookkeeping only: no result is changed.
"""
import collections
import glob
import json
import os
import sys


def main(out_path="results/v4/env_census.json"):
    groups = collections.Counter()
    no_env = collections.Counter()
    for path in sorted(glob.glob("results/**/*.jsonl", recursive=True)):
        top = path.split(os.sep)[1]
        try:
            with open(path) as fh:
                head = json.loads(fh.readline())
        except (ValueError, OSError):
            no_env[top] += 1
            continue
        env = head.get("env") if isinstance(head, dict) else None
        if not env:
            no_env[top] += 1
            continue
        threads = env.get("threads") or {}
        key = (top, env.get("python"), env.get("numpy"),
               threads.get("OMP_NUM_THREADS"), threads.get("OPENBLAS_NUM_THREADS"), threads.get("MKL_NUM_THREADS"))
        groups[key] += 1
    rows = [dict(dir=k[0], python=k[1], numpy=k[2], OMP_NUM_THREADS=k[3], OPENBLAS_NUM_THREADS=k[4],
                 MKL_NUM_THREADS=k[5], shards=v) for k, v in sorted(groups.items(), key=lambda kv: (kv[0][0], -kv[1]))]
    out = {"source": "header line of results/**/*.jsonl", "groups": rows,
           "shards_without_env_header": dict(sorted(no_env.items()))}
    with open(out_path, "w") as fh:
        json.dump(out, fh, indent=1)
        fh.write("\n")
    for r in rows:
        print(r)
    print("without env header:", dict(no_env))


if __name__ == "__main__":
    main(*sys.argv[1:])
