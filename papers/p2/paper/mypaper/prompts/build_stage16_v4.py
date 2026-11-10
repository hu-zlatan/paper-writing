"""Build the p2 stage-16 [v4] prompt from the verbatim template (pipeline/references/stage_prompts/paper_outline.md):
same preamble / topic block as v1 (build_stage16.py), {feedback} = the v2 stage-20 gate + the v2 outline to revise,
{analysis} = results/14_analysis_v3.md + its pass 1 tables, then the v2 merged analysis, {decision} = results/15_decision_v3.md."""
import os
import runpy

d = os.path.dirname(os.path.abspath(__file__))
P2 = os.path.join(d, "..", "..", "..")
rd = lambda p: open(os.path.join(P2, p)).read()
g = runpy.run_path(os.path.join(d, "build_stage16.py"))          # rewrites the v1 prompt files identically
preamble = g["preamble"].replace("results/15_decision.md", "results/15_decision_v4.md") + (
    "\n\nThis is iteration v4 after the third and last REFINE loop (stage-20 gates v1 6.5, v2 5.5, v3 6.8 / 10). v4 "
    "(docs/11_amendment_v4.md, registered before any v4 code or run) adds the paper's CONFIRMATORY evidence: C1-C5 "
    "with Holm on fresh objects (pool f4) and on a friction-correlated pool (c4) with a deployable family prior "
    "(CSF-fam), plus secondary rows S1 sigma band, S2 shrunk plug-in, S3 friction-width sweep, S4 per-family, S5 "
    "CRC-route versions, S6 measured no-probe grasp and break-even, S7 200 re-splits. Evidence links for v4 rows must "
    "name keys of results/v4/v4_analysis.json; v1-v3 rows keep their links (results_v1/v2/v3.json). The statements of "
    "record in results/14_analysis_v4.md are binding (including its qualifiers: C2 equivalence only on the matched "
    "route and only at sigma 0.2; the width sweep is descriptive and does not establish a noise-vs-width mechanism; "
    "the guarantee is marginal, not per stratum / family; C4 / C5 'inferiority' is the read-out label for CI below 0). "
    "S6 replaces the v3 arithmetic break-even. v1 primary and v2 / v3 verdicts are unchanged. Revise the v3 outline "
    "given below; per results/15_decision_v4.md the paper is reframed around the confirmatory C1-C5 table and the "
    "conditions under which the probe saving holds or disappears. Target: RSS 2027 Stage 1 extended abstract "
    "(<= 5 pages body + 1 page references), simulation only.")
feedback = ("Prior feedback (v3 stage-20 quality gate, paper/mypaper/20_quality_gate_v3.json; stage-18 v3 pass-2 record "
            "paper/mypaper/18_peer_review_v3_pass2.md):\n\n" + rd("paper/mypaper/20_quality_gate_v3.json") +
            "\n\n" + rd("paper/mypaper/18_peer_review_v3_pass2.md") +
            "\n\nv3 outline to revise (paper/mypaper/sections/00_outline_v3.md):\n\n" + rd("paper/mypaper/sections/00_outline_v3.md") + "\n\n")
analysis = (rd("results/14_analysis_v4.md") + "\n\n=== v4 pass-1 analysis (tables; superseded by the merged record and the "
            "pass-2 audit where they differ) ===\n\n" + rd("results/14_analysis_v4_pass1.md") +
            "\n\n=== v4 pass-2 audit (binding) ===\n\n" + rd("results/14_analysis_v4_pass2.md") +
            "\n\n=== v3 merged analysis (results/14_analysis_v3.md) ===\n\n" + rd("results/14_analysis_v3.md"))
decision = rd("results/15_decision_v4.md")
user = f"""{preamble}


Create a detailed paper outline in markdown.

Include per-section goals and evidence links.

{g['block']}{feedback}Analysis:

{analysis}


Decision:

{decision}
"""
open(os.path.join(d, "stage16_v4_system.txt"), "w").write("You are an academic writing planner.\n")
open(os.path.join(d, "stage16_v4_user.txt"), "w").write(user)
print(len(user.split()), "words")
