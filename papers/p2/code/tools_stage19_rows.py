"""Report-only rows requested by the stage-18 review (p2 v1), computed from existing raw files; no new simulation,
no change to any registered analysis. Output: results/v1/19_report_rows.json.
(1) onset detector quality on the main id pool (sigma = 0, i.e. the raw detector, before the added sigma*eps):
    log(m g / (2 F_onset)) vs log mu: Pearson r, mean (bias) and SD of the difference; found rate; slip displacement
    at onset (mm). (2) logged compute: sum of 'seconds:' lines in results/v1/logs/*.log by job prefix, and the sum of
    per-row 'seconds' in label / mono files. (3) per-disturbance-stratum test physical slip of the main arms on the
    08c CRC route (same lam-hat as analysis_crc.evaluate). (4) H1-M violations split by pool."""
import glob
import json
import math
import os
import re
import sys

import numpy as np

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
from certgrip.io import load_rows  # noqa: E402
import analysis_crc as A  # noqa: E402

RES = os.path.join(HERE, "..", "results", "v1")
G9 = 9.81
out = {"note": "report-only rows for stage 19 (code/tools_stage19_rows.py); computed from existing raw files"}

# (1) detector
rows = [r for r in load_rows("v1/labels/id_F*.jsonl") if r["pool"] == "id" and r.get("shift") is None]
fo = [r for r in rows if r["rec"]["onset"]["found"]]
x = np.array([math.log(r["inst"]["mass"] * G9 / (2 * r["rec"]["onset"]["F_onset"])) for r in fo])
y = np.array([math.log(r["inst"]["mu"]) for r in fo])
dsp = np.array([r["rec"]["onset"]["disp_at_onset_mm"] for r in fo])
out["detector_id_sigma0"] = {"n_rows": len(rows), "found_rate": len(fo) / len(rows),
                             "pearson_r_logmu": float(np.corrcoef(x, y)[0, 1]),
                             "bias_mean_diff": float(np.mean(x - y)), "sd_diff": float(np.std(x - y, ddof=1)),
                             "disp_at_onset_mm": {"median": float(np.median(dsp)), "p95": float(np.percentile(dsp, 95)),
                                                  "max": float(dsp.max()), "n_ge_2mm": int((dsp >= 2.0).sum())}}

# (2) compute
by = {}
for f in glob.glob(os.path.join(RES, "logs", "*.log")):
    pre = re.sub(r"_(F\d|seed\d|s0\.\d.*|\d+)?\.log$", "", os.path.basename(f))
    pre = re.sub(r"_(F\d|\d+)$", "", pre)
    s = sum(float(m) for m in re.findall(r"^seconds: ([\d.]+)", open(f).read(), re.M))
    by[pre] = by.get(pre, 0.0) + s
row_s = {}
for sub in ("labels", "mono"):
    t = 0.0
    for f in glob.glob(os.path.join(RES, sub, "*.jsonl")):
        for line in open(f):
            if '"seconds"' in line:
                r = json.loads(line)
                if "header" not in r:
                    t += float(r.get("seconds", 0.0))
    row_s[sub] = t
out["compute_logged_cpu_hours"] = {"logs_by_prefix": {k: v / 3600 for k, v in sorted(by.items()) if v > 0},
                                   "rows_sum": {k: v / 3600 for k, v in row_s.items()}}
out["compute_logged_cpu_hours"]["total"] = (sum(by.values()) + sum(row_s.values())) / 3600

# (3) per-stratum test slip, 08c CRC route
G, keys, idx, rep, missing, dup = A.load_real()
D = A.build(G, keys, rep)
split = np.array(D["split"])
cal, test = np.where(split == "cal")[0], np.where(split == "test")[0]
m = A.evaluate(D, cal, test)
st = D["strata"]
ps = {}
for a in ("full_rd@0.2#0", "CSF-1", "CSF-muhat@0.2", "P_onset@0.2#0"):
    if a not in m:
        continue
    ps[a] = {"overall_slip_phys": m[a]["slip_phys"], "lam_idx": m[a]["lam_idx"]}
    for s in ("D1", "D2", "D3", "D4"):
        sel = test[st[test] == s]
        ps[a][s] = {"n": int(len(sel)), "slip_phys": float(D["L"][a][sel, m[a]["lam_idx"][s]].mean())}
out["per_stratum_test_slip_crc08c"] = ps

# (4) H1-M violations by pool
h = json.load(open(os.path.join(RES, "h1m_analysis.json")))
v = h["violations"]
idv = [z for z in v if z["pool"] == "id" and z["shift"] is None]   # the 800-instance id gate set
out["h1m_violations_split"] = {"id_count": len(idv), "id_max_rel_above_F_hi": max(z["rel_above_F_hi"] for z in idv),
                               "shift_count": len(v) - len(idv),
                               "shift_max_rel_above_F_hi": max(z["rel_above_F_hi"] for z in v if z not in idv),
                               "shift_pools": h["shift_pools"]}
json.dump(out, open(os.path.join(RES, "19_report_rows.json"), "w"), indent=1)
print(json.dumps(out, indent=1)[:3000])
