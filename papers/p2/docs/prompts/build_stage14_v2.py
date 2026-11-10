"""Builds the stage-14 [v2] RESULT_ANALYSIS prompt for p2 from the verbatim template
(pipeline/references/stage_prompts/result_analysis.md). usage: python docs/prompts/build_stage14_v2.py"""
import glob
import os

H = os.path.dirname(os.path.abspath(__file__)); P2 = os.path.join(H, "..", "..")
pre = ("This is p2 (CertGrip: conformal slip-rate guarantees for tactile grip-force selection, simulated in MuJoCo), "
       "iteration v2 after a REFINE loop (stage-20 gate 6.5 / 10). Every v2 row is SECONDARY (amendment 09, written "
       "before any v2 code or run); the v1 primary verdicts are not re-decided. Compare v2 against the v1 primary "
       "read-outs results/v1/crc_analysis.json (H2a / H2b, CRC route) and results/v1/h3_analysis.json (H3, label-rule "
       "feedback), included unaltered. Every number you write must appear in the files below.")
files = ["results/v1/crc_analysis.json", "results/v1/h3_analysis.json"] + \
    [f"results/v2/{n}" for n in ("a_analysis.json", "a_analysis_08e.json", "b_analysis.json", "b_analysis_edge.json",
                                 "b3_analysis.json")]
data = "\n\n".join(f"### {f}\n```json\n{open(os.path.join(P2, f)).read()}\n```" for f in files)
ctx = [f"### docs/09_amendment_v2.md\n" + open(os.path.join(P2, "docs/09_amendment_v2.md")).read(),
       f"### plans/stage_13_v2_b3_online_physical.md\n" + open(os.path.join(P2, "plans/stage_13_v2_b3_online_physical.md")).read(),
       "Hardware: sandbox / GitHub Actions CPUs (2 cores); MuJoCo 4.0.0, numpy 2.5.3. Wall-clock: B1 / B2 replays 12 "
       "Actions jobs of about 525 s plus 12 edge-rule jobs; B3 20 streams of about 25 s each in the sandbox (pilot 200 "
       "replays in 2.5 s). Anomalies: 0 logs with NaN / Inf / RuntimeWarning; CSF-muhat at grid index 0 on the 08c "
       "grids (08e rows are the fair ones); CSF-proxy@0.2 hit grid index 0 -> edge rule (b_analysis_edge.json). "
       "B3 has 5 orderings per shift and no registered interval or test."]
user = (f"{pre}\n\n\n{data}\n\n\nAnalyze run metrics and produce markdown report with statistical interpretation.\n\n"
        "Use the ACTUAL quantitative values provided above — do NOT invent numbers.\n\n"
        "Required sections: Metrics Summary (with real values), Comparative Findings, Statistical Checks, Limitations, "
        "Conclusion.\n\nRun context:\n\n" + "\n\n".join(ctx))
open(os.path.join(H, "stage14_v2_user.txt"), "w").write(user)
open(os.path.join(H, "stage14_v2_system.txt"), "w").write("You are a quantitative ML analyst. Always cite exact numbers from the provided data.")
print(len(user))
