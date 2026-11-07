"""v5 E5 evaluator check (amendment v5.0 E5): G* and student seed 701 on test5 S2 and S12, episodes 0-199, re-read at
sub 16 with regrid3 (histories rebuilt from the recorded actions). Shards of 15 episodes (~45-70 s per episode at sub 16
measured on a val3 record in the sandbox, run 35), 25-min budget; regrid3 writes EARLY_STOP with the remaining episodes.
usage: python tools_v5_e5.py      writes experiments/v5_e5_sub16.json; refuses unless every source episode 0-199 exists
(counts only, no outcome is read)."""
import glob
import json
import os

ROOT = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..")
ROWS = [("S2", "S_k2"), ("S12", "S_k12")]
METHODS = ["gstar", "student_s701"]
N, SHARD = 200, 15


def main():
    jobs = []
    for c, tag in ROWS:
        for m in METHODS:
            files = sorted(glob.glob(os.path.join(ROOT, "results/v5/test5", f"{tag}_{m}_*.jsonl")))
            have = set()
            for f in files:
                for line in open(f):
                    r = json.loads(line)
                    if "episode" in r and "header" not in r:
                        have.add(r["episode"])
            miss = [e for e in range(N) if e not in have]
            assert not miss, f"{c} {m}: {len(miss)} of episodes 0-{N - 1} missing"
            src = " ".join(os.path.relpath(f, os.path.join(ROOT, "code")) for f in files)
            for st in range(0, N, SHARD):
                eps = " ".join(str(e) for e in range(st, min(N, st + SHARD)))
                jobs.append({"id": f"v5_e5_{c}_{m}_{st:03d}", "cmd": f"python main.py regrid3 --src {src} --episodes {eps} "
                             f"--sub 16 --budget-minutes 25 --out ../results/v5/e5/{tag}_{m}_sub16_{st:03d}"})
    json.dump({"purpose": "v5 E5: sub-16 re-read of test5 0-199, G* and student 701, S2/S12 (code/tools_v5_e5.py)", "jobs": jobs},
              open(os.path.join(ROOT, "experiments", "v5_e5_sub16.json"), "w"), indent=1)
    print(len(jobs))


if __name__ == "__main__":
    main()
