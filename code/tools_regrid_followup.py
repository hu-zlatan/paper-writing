"""Follow-up manifest for regrid3 jobs: re-issue the episodes of each job that its output file does not contain
(early stop at 80 % budget). Usage: python tools_regrid_followup.py <src manifest> <dst manifest> <purpose> [chunk]."""
import json
import os
import re
import sys

here = os.path.dirname(os.path.abspath(__file__))
src, dst, purpose = sys.argv[1:4]
chunk = int(sys.argv[4]) if len(sys.argv) > 4 else 10 ** 9
jobs = []
for j in json.load(open(src))["jobs"]:
    cmd = j["cmd"]
    out = re.search(r"--out (\S+)", cmd).group(1)
    want = [int(x) for x in re.search(r"--episodes ([\d ]+?) --", cmd).group(1).split()]
    f = os.path.join(here, out + ".jsonl")
    have = set()
    if os.path.exists(f):
        have = {json.loads(l)["episode"] for l in open(f) if '"episode"' in l and "header" not in l}
    miss = [e for e in want if e not in have]
    for k in range(0, len(miss), chunk):
        part = miss[k:k + chunk]
        c2 = re.sub(r"--episodes [\d ]+? --", "--episodes " + " ".join(map(str, part)) + " --", cmd)
        c2 = c2.replace(f"--out {out}", f"--out {out}_r{part[0]}")
        jobs.append({"id": j["id"] + f"_r{part[0]}", "cmd": c2})
json.dump({"purpose": purpose, "jobs": jobs}, open(dst, "w"), indent=1)
print(len(jobs), "jobs,", sum(len(re.search(r"--episodes ([\d ]+?) --", x["cmd"]).group(1).split()) for x in jobs), "episodes")
