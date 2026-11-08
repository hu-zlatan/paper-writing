"""Split the eval3 jobs of a follow-up manifest into chunks of --chunk episodes (one job each) and set a larger
time guard, so slow methods (random: ~700 s / episode under sub 8) finish in one wave instead of 2 episodes per
25-min job. Only --start/--count/--out/--budget-minutes change; the evaluated method, inputs and episodes are the same.
Usage: python tools_split_manifest.py <src> <dst> <purpose> [--chunk 3] [--budget 60] [--only random]"""
import json, re, sys
src, dst, purpose = sys.argv[1], sys.argv[2], sys.argv[3]
opt = lambda k, d: type(d)(sys.argv[sys.argv.index(k) + 1]) if k in sys.argv else d
chunk, budget, only = opt("--chunk", 3), opt("--budget", 60.0), opt("--only", "random")
jobs = []
for j in json.load(open(src))["jobs"]:
    cmd = j["cmd"]
    if f"--method {only}" not in cmd:
        jobs.append(j); continue
    start = int(re.search(r"--start (\d+)", cmd).group(1)); count = int(re.search(r"--count (\d+)", cmd).group(1))
    out = re.search(r"--out (\S+)", cmd).group(1)
    for s in range(start, start + count, chunk):
        c = min(chunk, start + count - s)
        c2 = re.sub(r"--start \d+", f"--start {s}", cmd); c2 = re.sub(r"--count \d+", f"--count {c}", c2)
        c2 = re.sub(r"--budget-minutes \S+", f"--budget-minutes {budget:g}", c2)
        c2 = c2.replace(f"--out {out}", f"--out {out}_c{s}")
        jobs.append({"id": j["id"] + f"_c{s}", "cmd": c2})
json.dump({"purpose": purpose, "jobs": jobs}, open(dst, "w"), indent=1)
print(len(jobs), "jobs")
