"""Builds the stage-14 [v3] RESULT_ANALYSIS prompt for p2 from the verbatim template
(pipeline/references/stage_prompts/result_analysis.md). usage: python docs/prompts/build_stage14_v3.py"""
import glob
import os

H = os.path.dirname(os.path.abspath(__file__)); P2 = os.path.join(H, "..", "..")
pre = ("This is p2 (CertGrip: conformal slip-rate guarantees for tactile grip-force selection, simulated in MuJoCo), "
       "iteration v3 after a second REFINE loop (stage-20 gates v1 6.5, v2 5.5 / 10). Every v3 row is SECONDARY "
       "(amendment 10 + addendum 10a, written before any v3 code or run); the v1 primary and v2 verdicts are not "
       "re-decided. Compare v3 against the v1 primary "
       "read-outs results/v1/crc_analysis.json (H2a / H2b, CRC route) and results/v1/h3_analysis.json (H3, label-rule "
       "feedback), included unaltered. Every number you write must appear in the files below.")
files = ["results/v1/crc_analysis.json", "results/v1/h3_analysis.json"] + \
    [f"results/v3/{n}" for n in ("a3_holm.json", "a_analysis.json", "a_analysis_08e.json", "b1_analysis.json",
                                 "b1_analysis_edge.json", "b1_analysis_edge_samegrid.json", "b2_analysis.json",
                                 "b3_analysis.json")]
data = "\n\n".join(f"### {f}\n```json\n{open(os.path.join(P2, f)).read()}\n```" for f in files)
ctx = [f"### docs/10_amendment_v3.md\n" + open(os.path.join(P2, "docs/10_amendment_v3.md")).read(),
       "Hardware: sandbox / GitHub Actions CPUs (2 cores); MuJoCo 4.0.0, numpy 2.5.3. Part A (A1-A7) and A3 are "
       "re-analyses of the existing v1 replays in the sandbox (minutes); B1 shrunk plug-in 4,800 instances of new "
       "replays (protocol rd), plus the edge-rule 08e-recipe grid for sigma 0.2 (b1_analysis_edge.json mixes "
       "CertGrip-full on its 08c grid; b1_analysis_edge_samegrid.json uses CertGrip-full / CSF-1 on their 08e-recipe "
       "replays, the same-grid row); B2 reactive controllers 4,800 id cal + test instances (F5 has no id cal / test "
       "objects); B3 100 new streams + 20 reused v2 streams, 20 orderings x 3 shifts. Anomalies / caveats: B3 95 % "
       "intervals are over orderings only (fixed object pools), so they do not cover object-sampling uncertainty; a "
       "3-object B2 timing pilot printed 12 cal-instance outcomes before the full run and no parameter was changed "
       "afterwards (all fixed in addendum 10a); A1 is descriptive; A3 p-values are vs 0 as registered, which is not "
       "the own threshold for H2-T, H4c and the oracle share (flagged in the file), resolution 1 / 2,000, v2 rows not "
       "re-drawn. The B1 registered prediction (sigma 0.4 advantage shrinks with CI including 0) was stated before "
       "running."]
user = (f"{pre}\n\n\n{data}\n\n\nAnalyze run metrics and produce markdown report with statistical interpretation.\n\n"
        "Use the ACTUAL quantitative values provided above — do NOT invent numbers.\n\n"
        "Required sections: Metrics Summary (with real values), Comparative Findings, Statistical Checks, Limitations, "
        "Conclusion.\n\nRun context:\n\n" + "\n\n".join(ctx))
open(os.path.join(H, "stage14_v3_user.txt"), "w").write(user)
open(os.path.join(H, "stage14_v3_system.txt"), "w").write("You are a quantitative ML analyst. Always cite exact numbers from the provided data.")
print(len(user))
