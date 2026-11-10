"""Build the p2 stage-16 [v2] prompt from the verbatim template (pipeline/references/stage_prompts/paper_outline.md):
same preamble / topic block as v1 (build_stage16.py), {feedback} = the v1 stage-20 gate + the v1 outline to revise,
{analysis} = results/14_analysis_v2.md followed by the v1 merged analysis, {decision} = results/15_decision_v2.md."""
import os
import runpy

d = os.path.dirname(os.path.abspath(__file__))
P2 = os.path.join(d, "..", "..", "..")
rd = lambda p: open(os.path.join(P2, p)).read()
g = runpy.run_path(os.path.join(d, "build_stage16.py"))          # rewrites the v1 prompt files identically
preamble = g["preamble"].replace("results/15_decision.md", "results/15_decision_v2.md") + (
    "\n\nThis is iteration v2 after a REFINE loop. v2 rows (amendment 09: risk-efficiency frontier A1, Learn-then-Test "
    "certificate A2, extra contrasts A3, CSF-proxy friction-prior baseline B1 / H5, probe + fixed margin B2, online "
    "tracking with physical feedback B3) are SECONDARY and their evidence links must name blocks / keys of "
    "results/v2/results_v2.json (blocks a_analysis.json, a_analysis_08e.json, b_analysis.json, b_analysis_edge.json, "
    "b3_analysis.json). v1 primary verdicts are unchanged. Revise the v1 outline given below rather than starting over.")
feedback = ("Prior feedback (v1 stage-20 quality gate, paper/mypaper/20_quality_gate.json; peer reviews in "
            "paper/mypaper/18_peer_review*.md):\n\n" + rd("paper/mypaper/20_quality_gate.json") +
            "\n\nv1 outline to revise (paper/mypaper/sections/00_outline.md):\n\n" + rd("paper/mypaper/sections/00_outline.md") + "\n\n")
analysis = rd("results/14_analysis_v2.md") + "\n\n=== v1 merged analysis (results/14_analysis.md) ===\n\n" + rd("results/14_analysis.md")
decision = rd("results/15_decision_v2.md")
user = f"""{preamble}


Create a detailed paper outline in markdown.

Include per-section goals and evidence links.

{g['block']}{feedback}Analysis:

{analysis}


Decision:

{decision}
"""
open(os.path.join(d, "stage16_v2_system.txt"), "w").write("You are an academic writing planner.\n")
open(os.path.join(d, "stage16_v2_user.txt"), "w").write(user)
print(len(user.split()), "words")
