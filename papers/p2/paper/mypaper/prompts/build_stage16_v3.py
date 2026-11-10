"""Build the p2 stage-16 [v3] prompt from the verbatim template (pipeline/references/stage_prompts/paper_outline.md):
same preamble / topic block as v1 (build_stage16.py), {feedback} = the v2 stage-20 gate + the v2 outline to revise,
{analysis} = results/14_analysis_v3.md + its pass 1 tables, then the v2 merged analysis, {decision} = results/15_decision_v3.md."""
import os
import runpy

d = os.path.dirname(os.path.abspath(__file__))
P2 = os.path.join(d, "..", "..", "..")
rd = lambda p: open(os.path.join(P2, p)).read()
g = runpy.run_path(os.path.join(d, "build_stage16.py"))          # rewrites the v1 prompt files identically
preamble = g["preamble"].replace("results/15_decision.md", "results/15_decision_v3.md") + (
    "\n\nThis is iteration v3 after a second REFINE loop (v2 gate 5.5 / 10). v2 rows keep their v2 status and link to "
    "results/v2/results_v2.json; v3 rows (amendment 10: A1 re-splits, A2 slip tables, A3 Holm, A4 losing sub-pool on "
    "CRC, A5 empirical margin, A6 direct learned vs plug-in, A7 force in newtons + integrated force, B1 shrunk plug-in, "
    "B2 reactive controllers, B3 online study 3 shifts x 20 orderings) are SECONDARY and their evidence links must "
    "name blocks / keys of results/v3/results_v3.json (blocks a3_holm.json, a7_integrated.json, a_analysis.json, "
    "a_analysis_08e.json, b1_analysis.json, b1_analysis_edge.json, b1_analysis_edge_samegrid.json, b2_analysis.json, "
    "b3_analysis.json). The statements of record in results/14_analysis_v3.md are binding. v1 primary verdicts are "
    "unchanged. A7 integrated force and break-even T were computed by code after stage 14 (code/analysis_v3_d.py -> "
    "a7_integrated.json: shared phases 27.4258 N*s, probe-specific phases 14.3458 N*s, break-even 13.22 s / 25.28 s); "
    "use those, not the pass-1 hand reconstruction. Revise the v2 outline given below rather than starting over.")
feedback = ("Prior feedback (v2 stage-20 quality gate, paper/mypaper/20_quality_gate_v2.json; stage-18 records "
            "paper/mypaper/18_peer_review_v2.md and 18_peer_review_v2_pass2.md):\n\n" + rd("paper/mypaper/20_quality_gate_v2.json") +
            "\n\n" + rd("paper/mypaper/18_peer_review_v2_pass2.md") +
            "\n\nv2 outline to revise (paper/mypaper/sections/00_outline_v2.md):\n\n" + rd("paper/mypaper/sections/00_outline_v2.md") + "\n\n")
analysis = (rd("results/14_analysis_v3.md") + "\n\n=== v3 pass-1 analysis (tables; superseded by the merged record and the "
            "pass-2 audit where they differ) ===\n\n" + rd("results/14_analysis_v3_pass1.md") +
            "\n\n=== v3 pass-2 audit (binding) ===\n\n" + rd("results/14_analysis_v3_pass2.md") +
            "\n\n=== v2 merged analysis (results/14_analysis_v2.md) ===\n\n" + rd("results/14_analysis_v2.md"))
decision = rd("results/15_decision_v3.md")
user = f"""{preamble}


Create a detailed paper outline in markdown.

Include per-section goals and evidence links.

{g['block']}{feedback}Analysis:

{analysis}


Decision:

{decision}
"""
open(os.path.join(d, "stage16_v3_system.txt"), "w").write("You are an academic writing planner.\n")
open(os.path.join(d, "stage16_v3_user.txt"), "w").write(user)
print(len(user.split()), "words")
