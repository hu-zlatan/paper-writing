"""Build a follow-up manifest: jobs whose eval3/g2v3/bias3 output is missing, or early-stopped (resume at next_index)."""
import json, os, re, sys
src, dst, purpose = sys.argv[1], sys.argv[2], sys.argv[3]
root = "/home/claude/paper-writing/code"
m = json.load(open(src)); jobs = []
for j in m["jobs"]:
    cmd = j["cmd"]; out = re.search(r"--out (\S+)", cmd).group(1)
    f = os.path.join(root, out + ".jsonl")
    start = int(re.search(r"--start (\d+)", cmd).group(1)); count = int(re.search(r"--count (\d+)", cmd).group(1))
    if not os.path.exists(f):
        jobs.append(j); continue
    rows = [json.loads(l) for l in open(f) if l.strip()]
    stop = [r for r in rows if r.get("EARLY_STOP_AT_80_PCT_BUDGET")]
    done = [r for r in rows if "episode" in r or "index" in r]
    if stop:
        ni = stop[0]["next_index"]; rem = start + count - ni
        c2 = re.sub(r"--start \d+", f"--start {ni}", cmd); c2 = re.sub(r"--count \d+", f"--count {rem}", c2)
        c2 = c2.replace(f"--out {out}", f"--out {out}_r{ni}")
        jobs.append({"id": j["id"] + f"_r{ni}", "cmd": c2})
    elif len(done) < count:
        ni = max(r.get("episode", r.get("index", -1)) for r in done) + 1 if done else start
        rem = start + count - ni
        c2 = re.sub(r"--start \d+", f"--start {ni}", cmd); c2 = re.sub(r"--count \d+", f"--count {rem}", c2)
        c2 = c2.replace(f"--out {out}", f"--out {out}_r{ni}")
        jobs.append({"id": j["id"] + f"_r{ni}", "cmd": c2})
json.dump({"purpose": purpose, "jobs": jobs}, open(dst, "w"), indent=1)
print(len(jobs), "jobs")
