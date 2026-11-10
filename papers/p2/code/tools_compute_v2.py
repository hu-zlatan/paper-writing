"""Sum the logged wall-clock seconds of the p2 v2 simulation jobs (single-process jobs, so ~CPU seconds):
B1 / B2 CRC replays (results/v1/logs/p2_crc09*.log, Actions; 09 and 09e grids) and the B3 streams
(results/v2/logs/b3_*.log, sandbox). Writes results/v2/compute_v2.json."""
import glob
import json
import os
import re

R = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "results")


def secs(pattern):
    out = {}
    for f in sorted(glob.glob(os.path.join(R, pattern))):
        m = re.findall(r"^seconds: ([\d.]+)", open(f).read(), re.M)
        if m:
            out[os.path.basename(f)] = float(m[-1])
    return out


groups = {"B1_B2_crc09_replays_actions": secs("v1/logs/p2_crc09_*.log"),
          "B1_edge_crc09e_replays_actions": secs("v1/logs/p2_crc09e_*.log"),
          "B3_streams_sandbox": secs("v2/logs/b3_*.log")}
out = {"note": "logged 'seconds:' of each job (wall clock of one single-threaded process); CPU model not recorded "
               "(platform.processor() is empty on these hosts)",
       "groups": {k: {"n_jobs": len(v), "seconds_total": round(sum(v.values()), 1),
                      "cpu_hours": round(sum(v.values()) / 3600, 3), "per_job": v} for k, v in groups.items()}}
out["total_cpu_hours"] = round(sum(g["cpu_hours"] for g in out["groups"].values()), 3)
json.dump(out, open(os.path.join(R, "v2/compute_v2.json"), "w"), indent=1)
print({k: (g["n_jobs"], g["cpu_hours"]) for k, g in out["groups"].items()}, out["total_cpu_hours"])
