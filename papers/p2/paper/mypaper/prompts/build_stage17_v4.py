"""Build the p2 stage-17 [v4] prompt from the verbatim template (pipeline/references/stage_prompts/paper_draft.md):
as build_stage17.py, with outline = sections/00_outline_v4.md, metrics = results_v1/v2/v3 JSON, the cards, a v3 note in
the preamble and the v2 final draft appended as audited wording."""
import os
import runpy

d = os.path.dirname(os.path.abspath(__file__))
P2 = os.path.join(d, "..", "..", "..")
rd = lambda p: open(os.path.join(P2, p)).read()
g = runpy.run_path(os.path.join(d, "build_stage17.py"))          # rewrites the v1 prompt files (cards now 55)
preamble = g["preamble"].replace("results/15_decision.md", "results/15_decision_v4.md").replace(
    "results/14_analysis.md", "results/14_analysis_v4.md (statements of record 1-9, binding, with their qualifiers), results/14_analysis_v3.md, "
    "results/14_analysis_v2.md and results/14_analysis.md") + (
    " This is iteration v4 after the third and last REFINE loop: v4 rows (docs/11_amendment_v4.md, registered before "
    "any v4 run) C1-C5 are the paper's CONFIRMATORY evidence (Holm at 5 %, fresh pool f4, correlated pool c4 with the "
    "family prior CSF-fam); S1-S7 are secondary / descriptive; v1-v3 rows keep their status (v1 primary verdicts "
    "unchanged; v2 / v3 rows secondary) and are supporting evidence. Write a complete new draft following the v4 "
    "outline, within the RSS 2027 Stage 1 budget (<= 5 pages body; the outline's word budget). The v3 final draft "
    "(paper/mypaper/draft_v3.md, reviewed twice with no fabrication found) is pasted at the end for method / protocol "
    "wording that has already been audited; reuse its facts, not its framing where the v4 outline differs. Check every "
    "v4 key the outline names against results/v4/v4_analysis.json below. Metadata-only cards may be cited only for "
    "the content named in their title.")
metrics = ("EXPERIMENT METRICS (use ONLY these numbers; round to 4 sig figs; each block the unchanged content of a file "
           "in results/v1/, results/v2/, results/v3/ or results/v4/):\n\n=== results/v1/results_v1.json ===\n" + rd("results/v1/results_v1.json")
           + "\n\n=== results/v2/results_v2.json ===\n" + rd("results/v2/results_v2.json")
           + "\n\n=== results/v3/results_v3.json ===\n" + rd("results/v3/results_v3.json")
           + "\n\n=== results/v4/v4_analysis.json ===\n" + rd("results/v4/v4_analysis.json") + "\n\n")
user = (g["user_t"].replace("{preamble}", preamble).replace("{topic_constraint}", g["block"])
        .replace("{exp_metrics_instruction}", metrics).replace("{citation_instruction}", g["cites"])
        .replace("{outline}", rd("paper/mypaper/sections/00_outline_v4.md")))
user += "\n\n=== Reference: v3 final draft (paper/mypaper/draft_v3.md) ===\n\n" + rd("paper/mypaper/draft_v3.md")
open(os.path.join(d, "stage17_v4_system.txt"), "w").write(g["system"] + "\n")
open(os.path.join(d, "stage17_v4_user.txt"), "w").write(user)
print(len(user.split()), "words;", g["cites"].count("\n- "), "cite keys")
