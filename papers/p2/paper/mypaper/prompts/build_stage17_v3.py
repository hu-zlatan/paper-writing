"""Build the p2 stage-17 [v3] prompt from the verbatim template (pipeline/references/stage_prompts/paper_draft.md):
as build_stage17.py, with outline = sections/00_outline_v3.md, metrics = results_v1/v2/v3 JSON, the cards, a v3 note in
the preamble and the v2 final draft appended as audited wording."""
import os
import runpy

d = os.path.dirname(os.path.abspath(__file__))
P2 = os.path.join(d, "..", "..", "..")
rd = lambda p: open(os.path.join(P2, p)).read()
g = runpy.run_path(os.path.join(d, "build_stage17.py"))          # rewrites the v1 prompt files (cards now 55)
preamble = g["preamble"].replace("results/15_decision.md", "results/15_decision_v3.md").replace(
    "results/14_analysis.md", "results/14_analysis_v3.md (statements of record 1-7, binding), results/14_analysis_v2.md "
    "and results/14_analysis.md") + (
    " This is iteration v3 after a second REFINE loop: v3 rows (docs/10_amendment_v3.md: re-splits, slip tables, Holm, "
    "losing sub-pool on CRC, empirical margin, direct learned vs plug-in, force in newtons + integrated force, shrunk "
    "plug-in, reactive controllers, online study 3 shifts x 20 orderings) and v2 rows are SECONDARY and must be labelled "
    "so; the v1 primary verdicts are unchanged. Write a complete new draft following the v3 outline. The v2 final draft "
    "(paper/mypaper/draft_v2.md, reviewed twice with no fabrication found) is pasted at the end for method / protocol "
    "wording that has already been audited; reuse its facts, not its framing where the v3 outline differs. "
    "Metadata-only cards may be cited only for the content named in their title.")
metrics = ("EXPERIMENT METRICS (use ONLY these numbers; round to 4 sig figs; each block the unchanged content of a file "
           "in results/v1/, results/v2/ or results/v3/):\n\n=== results/v1/results_v1.json ===\n" + rd("results/v1/results_v1.json")
           + "\n\n=== results/v2/results_v2.json ===\n" + rd("results/v2/results_v2.json")
           + "\n\n=== results/v3/results_v3.json ===\n" + rd("results/v3/results_v3.json") + "\n\n")
user = (g["user_t"].replace("{preamble}", preamble).replace("{topic_constraint}", g["block"])
        .replace("{exp_metrics_instruction}", metrics).replace("{citation_instruction}", g["cites"])
        .replace("{outline}", rd("paper/mypaper/sections/00_outline_v3.md")))
user += "\n\n=== Reference: v2 final draft (paper/mypaper/draft_v2.md) ===\n\n" + rd("paper/mypaper/draft_v2.md")
open(os.path.join(d, "stage17_v3_system.txt"), "w").write(g["system"] + "\n")
open(os.path.join(d, "stage17_v3_user.txt"), "w").write(user)
print(len(user.split()), "words;", g["cites"].count("\n- "), "cite keys")
