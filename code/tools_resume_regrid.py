"""Follow-up manifest for regrid3 jobs (E12): re-run only the episodes a job did not finish.

A regrid3 job lists its episodes with `--episodes a b c d`. When the time guard stops it, the output ends with
{"EARLY_STOP_AT_80_PCT_BUDGET": true, "remaining": [[method, episode], ...]}. The follow-up job is the same command
with `--episodes` set to the remaining episodes and `--out <out>_r<first remaining>`. A job with no output is re-run
unchanged. Usage: python tools_resume_regrid.py <src manifest> <dst manifest> "<purpose>"
"""
import json, os, re, sys

src, dst, purpose = sys.argv[1], sys.argv[2], sys.argv[3]
root = os.path.join(os.path.dirname(os.path.abspath(__file__)))
m = json.load(open(src)); jobs = []
for j in m["jobs"]:
    cmd = j["cmd"]; out = re.search(r"--out (\S+)", cmd).group(1)
    eps = [int(e) for e in re.search(r"--episodes ([\d ]+?)(?= --|$)", cmd).group(1).split()]
    f = os.path.join(root, out + ".jsonl")
    if not os.path.exists(f):
        jobs.append(j); continue
    rows = [json.loads(l) for l in open(f) if l.strip()]
    stop = [r for r in rows if r.get("EARLY_STOP_AT_80_PCT_BUDGET")]
    done = {r["episode"] for r in rows if "episode" in r}
    if stop:
        rem = sorted({int(e) for _, e in stop[0]["remaining"]})
    else:
        rem = [e for e in eps if e not in done]
    if not rem:
        continue
    c2 = re.sub(r"--episodes [\d ]+?(?= --|$)", "--episodes " + " ".join(map(str, rem)), cmd)
    c2 = c2.replace(f"--out {out}", f"--out {out}_r{rem[0]}")
    jobs.append({"id": j["id"] + f"_r{rem[0]}", "cmd": c2})
json.dump({"purpose": purpose, "jobs": jobs}, open(dst, "w"), indent=1)
print(len(jobs), "jobs")
