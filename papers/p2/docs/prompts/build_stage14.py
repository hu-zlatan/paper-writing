"""Builds the stage-14 RESULT_ANALYSIS user prompt for p2 from the verbatim template
(pipeline/references/stage_prompts/result_analysis.md): {preamble}, {data_context} = every analysis JSON in
results/v1 (unaltered; crc_grids*.json and 13_freeze.json omitted as raw inputs / hashes; UT3 per-cell list omitted,
its summary kept), {context} = the pre-registration and addenda 08a-08h.  usage: python docs/prompts/build_stage14.py
"""
import glob
import json
import os

H = os.path.dirname(os.path.abspath(__file__)); P2 = os.path.join(H, "..", "..")
pre = ("This is p2 (CertGrip: conformal slip-rate guarantees for tactile grip-force selection, simulated in MuJoCo), "
       "iteration v1, after all pre-registered primary and secondary analyses were run. Files are the analysis outputs "
       "of the repository code; every number you write must appear in them. Note which results are primary (H1, H2a, "
       "H2b, H3 in 08b §4) and which are secondary / diagnostics / post hoc sensitivity (08e).")
skip = {"crc_grids.json", "crc_grids_v2.json", "13_freeze.json"}
parts = []
for f in sorted(glob.glob(os.path.join(P2, "results/v1/*.json"))):
    n = os.path.basename(f)
    if n in skip:
        continue
    d = json.load(open(f))
    if n == "sec08f_ut3.json":
        d = {k: v for k, v in d.items() if k != "cells"}
        txt = json.dumps(d, indent=1)
    else:
        txt = open(f).read()
    parts.append(f"### results/v1/{n}\n```json\n{txt}\n```")
data = "\n\n".join(parts)
ctx = []
for f in ("08a_pilot_amendment.md", "08b_preregistration.md", "08c_analysis_plan.md", "08d_h3_stream_plan.md",
          "08e_crc_grid_sensitivity.md", "08f_secondaries_batch.md", "08g_secondaries_batch2.md", "08h_secondaries_batch3.md"):
    ctx.append(f"### docs/{f}\n" + open(os.path.join(P2, "docs", f)).read())
ctx.append("Hardware: sandbox / GitHub Actions CPUs (2 cores); MuJoCo 4.0.0, numpy 2.5.3, scikit-learn 1.9.1. Anomalies "
           "noticed during runs: none numerical (0 / 194 logs with NaN / Inf / RuntimeWarning); the 08c lambda-grid "
           "defect (08e); H1-M gate failed (8 / 800 non-monotone).")
user = (f"{pre}\n\n\n{data}\n\n\nAnalyze run metrics and produce markdown report with statistical interpretation.\n\n"
        "Use the ACTUAL quantitative values provided above — do NOT invent numbers.\n\n"
        "Required sections: Metrics Summary (with real values), Comparative Findings, Statistical Checks, Limitations, "
        "Conclusion.\n\nRun context:\n\n" + "\n\n".join(ctx))
open(os.path.join(H, "stage14_user.txt"), "w").write(user)
open(os.path.join(H, "stage14_system.txt"), "w").write("You are a quantitative ML analyst. Always cite exact numbers from the provided data.")
print(len(user))
