"""Follow-up manifest for E5 (regrid3) shards: re-run the episodes listed in each EARLY_STOP record's
`remaining` (or the whole shard if its output is missing), split into chunks of --chunk episodes so each
job fits its 25-min time guard. Same command otherwise (frozen inputs, sub 16). Usage:
python tools_resume_e5.py <src manifest> <dst manifest> <tag> [--chunk 5]"""
import json, os, re, sys
src, dst, tag = sys.argv[1], sys.argv[2], sys.argv[3]
chunk = int(sys.argv[sys.argv.index("--chunk") + 1]) if "--chunk" in sys.argv else 5
root = os.path.dirname(os.path.abspath(__file__))
jobs = []
for j in json.load(open(src))["jobs"]:
    cmd = j["cmd"]; out = re.search(r"--out (\S+)", cmd).group(1)
    eps = [int(x) for x in re.search(r"--episodes ([\d ]+?) --", cmd).group(1).split()]
    f = os.path.join(root, out + ".jsonl")
    if os.path.exists(f):
        rows = [json.loads(l) for l in open(f) if l.strip()]
        stop = [r for r in rows if r.get("EARLY_STOP_AT_80_PCT_BUDGET")]
        if stop:
            todo = [e for _, e in stop[0]["remaining"]]
        else:
            done = {r["episode"] for r in rows if "episode" in r}
            todo = [e for e in eps if e not in done]
    else:
        todo = eps
    for k in range(0, len(todo), chunk):
        part = todo[k:k + chunk]
        c2 = re.sub(r"--episodes [\d ]+? --", "--episodes " + " ".join(map(str, part)) + " --", cmd)
        c2 = c2.replace(f"--out {out}", f"--out {out}_{tag}e{part[0]:03d}")
        jobs.append({"id": j["id"] + f"_{tag}e{part[0]:03d}", "cmd": c2})
json.dump({"purpose": f"E5 follow-up {tag}: remaining episodes of {os.path.basename(src)}, {chunk} per job", "jobs": jobs},
          open(dst, "w"), indent=1)
print(len(jobs), "jobs", sum(len(re.search(r'--episodes ([\d ]+?) --', x['cmd']).group(1).split()) for x in jobs), "episodes")
