"""Build the p2 stage-17 [v2] prompt from the verbatim template (pipeline/references/stage_prompts/paper_draft.md):
as build_stage17.py, with outline = sections/00_outline_v2.md, metrics = results_v1.json + results_v2.json, the 55
cards, and a v2 note in the preamble."""
import os
import runpy

d = os.path.dirname(os.path.abspath(__file__))
P2 = os.path.join(d, "..", "..", "..")
rd = lambda p: open(os.path.join(P2, p)).read()
g = runpy.run_path(os.path.join(d, "build_stage17.py"))          # rewrites the v1 prompt files (cards now 55)
preamble = g["preamble"].replace("results/15_decision.md", "results/15_decision_v2.md").replace(
    "results/14_analysis.md", "results/14_analysis_v2.md (statements of record 1-6) and results/14_analysis.md") + (
    " This is iteration v2 after a REFINE loop: the v2 rows (docs/09_amendment_v2.md: risk-efficiency frontier, "
    "Learn-then-Test certificate, extra contrasts, CSF-proxy friction-prior baseline / H5, probe + fixed margin, online "
    "tracking with physical feedback) are SECONDARY and must be labelled so; the v1 primary verdicts are unchanged. "
    "Write a complete new draft following the v2 outline. The v1 final draft (paper/mypaper/draft_v1.md, reviewed twice "
    "with no fabrication found) is pasted at the end for method / protocol wording that has already been audited; reuse "
    "its facts, not its framing where the v2 outline differs. Metadata-only cards (p2c53-p2c55) may be cited only for "
    "the content named in their title.")
metrics = ("EXPERIMENT METRICS (use ONLY these numbers; round to 4 sig figs; each block the unchanged content of a file "
           "in results/v1/ or results/v2/):\n\n=== results/v1/results_v1.json ===\n" + rd("results/v1/results_v1.json")
           + "\n\n=== results/v2/results_v2.json ===\n" + rd("results/v2/results_v2.json") + "\n\n")
user = (g["user_t"].replace("{preamble}", preamble).replace("{topic_constraint}", g["block"])
        .replace("{exp_metrics_instruction}", metrics).replace("{citation_instruction}", g["cites"])
        .replace("{outline}", rd("paper/mypaper/sections/00_outline_v2.md")))
user += "\n\n=== Reference: v1 final draft (paper/mypaper/draft_v1.md) ===\n\n" + rd("paper/mypaper/draft_v1.md")
open(os.path.join(d, "stage17_v2_system.txt"), "w").write(g["system"] + "\n")
open(os.path.join(d, "stage17_v2_user.txt"), "w").write(user)
print(len(user.split()), "words;", g["cites"].count("\n- "), "cite keys")
