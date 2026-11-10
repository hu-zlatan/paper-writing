"""Builds the stage-14 [v4] RESULT_ANALYSIS prompt for p2 from the verbatim template
(pipeline/references/stage_prompts/result_analysis.md). usage: python docs/prompts/build_stage14_v3.py"""
import glob
import os

H = os.path.dirname(os.path.abspath(__file__)); P2 = os.path.join(H, "..", "..")
pre = ("This is p2 (CertGrip: conformal slip-rate guarantees for tactile grip-force selection, simulated in MuJoCo), "
       "iteration v4 after the third and last REFINE loop (stage-20 gates v1 6.5, v2 5.5, v3 6.8 / 10). The five "
       "decisions C1-C5 are CONFIRMATORY (Holm at 5 %, amendment 11, written and committed before any v4 code or run, "
       "with the predictions stated there); S1-S7 are secondary / descriptive. v1-v3 verdicts are not re-decided. "
       "results/v3/a7_integrated.json (the v3 break-even that S6 measures directly) is included unaltered for "
       "comparison. Every number you write must appear in the files below.")
files = ["results/v4/v4_analysis.json", "results/v3/a7_integrated.json"]
data = "\n\n".join(f"### {f}\n```json\n{open(os.path.join(P2, f)).read()}\n```" for f in files)
ctx = [f"### docs/11_amendment_v4.md\n" + open(os.path.join(P2, "docs/11_amendment_v4.md")).read(),
       "Hardware: sandbox (2 cores) for labels / grids / read-out, GitHub Actions 2-core runners for the W replays "
       "(80 jobs); MuJoCo 4.0.0, numpy 2.5.3. Completeness before the read-out (analysis_v4.py --check): f4 4,800 "
       "instances with replays, c4 4,800 (cal + test; the 800 selection instances only set grid centres and CSF-fam "
       "mu-bar: F1 0.379, F2 0.496, F3 0.677, F4 0.852), noprobe 4,800; 0 duplicates. The read-out code was committed "
       "before any v4 replay and run once; no parameter was changed after seeing results. Caveats: CI** are "
       "object-cluster bootstrap percentiles within family (2,000 draws, seed 2027), so p = 0.0 means no draw crossed "
       "the null (resolution 1 / 2,000); the code labels a C4 / C5 row 'inferiority' when it is not superior and the "
       "CI** lies below 0 (the registered rule only defines superiority for C4 / C5). sigma is the simulated "
       "probe-noise level (no hardware). No model was re-trained (v1 seed-0 fits and the v3 OLS shrinkage frozen)."]
user = (f"{pre}\n\n\n{data}\n\n\nAnalyze run metrics and produce markdown report with statistical interpretation.\n\n"
        "Use the ACTUAL quantitative values provided above — do NOT invent numbers.\n\n"
        "Required sections: Metrics Summary (with real values), Comparative Findings, Statistical Checks, Limitations, "
        "Conclusion.\n\nRun context:\n\n" + "\n\n".join(ctx))
open(os.path.join(H, "stage14_v4_user.txt"), "w").write(user)
open(os.path.join(H, "stage14_v4_system.txt"), "w").write("You are a quantitative ML analyst. Always cite exact numbers from the provided data.")
print(len(user))
