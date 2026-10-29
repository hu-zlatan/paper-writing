"""Build regrid3 (sub 8) manifests for recorded eval3 outputs (E' failed -> sub = 8 for every v3 number, amendment
v3.0 C2). Usage: python tools_regrid_manifest.py <out manifest> <purpose> <src glob> [<src glob> ...]
Each glob must select the eval3 files of ONE (set, kappa, method) group (original shard files and their _r follow-ups).
Jobs are chunked so that the projected sub-8 time (3.6 x the recorded sub-4 eval3 wall time, E' pilot ratio) is about
15 minutes per job; episodes already re-read in results/v3/<dest> are skipped."""
import glob
import json
import os
import sys

RATIO, TARGET_S = 3.6, 900.0
here = os.path.dirname(os.path.abspath(__file__))


def main():
    dst, purpose, globs = sys.argv[1], sys.argv[2], sys.argv[3:]
    jobs = []
    for g in globs:
        files = sorted(glob.glob(os.path.join(here, g)))
        recs = {}
        for f in files:
            for line in open(f):
                r = json.loads(line)
                if "episode" in r:
                    recs[r["episode"]] = (os.path.relpath(f, here), r["wall_s"])
        if not recs:
            continue
        name = os.path.basename(files[0]).rsplit("_", 1)[0]          # e.g. S_k12_gstar
        folder = os.path.basename(os.path.dirname(files[0]))           # g5 or cal
        dest = f"../results/v3/{folder}_sub8/{name}"
        done = set()
        for f in glob.glob(os.path.join(here, dest + "_*.jsonl")):
            for line in open(f):
                r = json.loads(line)
                if "episode" in r:
                    done.add(r["episode"])
        eps = sorted(e for e in recs if e not in done)
        chunk, acc = [], 0.0
        chunks = []
        for e in eps:
            chunk.append(e)
            acc += RATIO * recs[e][1]
            if acc >= TARGET_S:
                chunks.append(chunk); chunk, acc = [], 0.0
        if chunk:
            chunks.append(chunk)
        for c in chunks:
            srcs = sorted({recs[e][0] for e in c})
            jid = f"v3_sub8_{name}_{c[0]:03d}"
            jobs.append({"id": jid, "cmd": f"python main.py regrid3 --src {' '.join(srcs)} --episodes {' '.join(map(str, c))} "
                                          f"--sub 8 --budget-minutes 25 --out {dest}_{c[0]:03d}"})
    json.dump({"purpose": purpose, "jobs": jobs}, open(dst, "w"), indent=1)
    print(len(jobs), "jobs")


if __name__ == "__main__":
    main()
