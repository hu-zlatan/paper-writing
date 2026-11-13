"""Build the stage-17 [v6] prompt from the verbatim template (pipeline/references/stage_prompts/paper_draft.md)."""
import os
import re
R = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "..", "..")
rd = lambda p: open(os.path.join(R, p)).read()
tpl = rd("pipeline/references/stage_prompts/paper_draft.md")
system = re.search(r"\*\*System:\*\*\n````\n(.*?)\n````", tpl, re.S).group(1)
user_t = re.search(r"\*\*User:\*\*\n```\n(.*?)\n```\n", tpl, re.S).group(1)
# topic block identical to stage 16 v5
u16 = rd("paper/mypaper/prompts/stage16_v6_user.txt")
block = u16[u16.index("=== HARD TOPIC CONSTRAINT ==="):u16.index("=== END CONSTRAINT ===") + len("=== END CONSTRAINT ===")] + "\n"
# citation list: same 60 cards as the v3/v4 stage-17 prompts
u17v4 = rd("paper/mypaper/prompts/stage17_v4_user.txt")
cites = u17v4[u17v4.index("CITATIONS: Use the cite_keys provided."):u17v4.index("\n\nOutline:")] + "\n\n"
preamble = (
    "Target: RSS 2027 (Robotics: Science and Systems). This master draft serves the Stage 1 extended abstract "
    "(<= 5 content pages + 1 page of references, due 2026-12-04 AoE; condensed from this draft in stage 22 using the "
    "outline's per-section word targets) and later the Stage 2 full paper (<= 8 pages). Binding length floors for this "
    "repo (RESTRICTS.yaml; they replace the 9-page floors quoted below): total main body >= 4,000 words (aim "
    "4,300-5,000); Abstract >= 150, Introduction >= 700, Related Work >= 500, Method >= 800, Experiments >= 600, "
    "Results >= 500, Discussion >= 300, Limitations >= 200, Conclusion >= 150. Paper type: a pre-registered "
    "MEASUREMENT paper with ONE narrow positive claim (the H6b accuracy-latency frontier, Holm-qualified per reduced "
    "planner and cell) and NO parity, method-superiority or effective-component claim. results/v6/15_decision.md "
    "sections 4.3-4.5 (allowed and disallowed claims) are binding and summarised in the outline: follow every binding "
    "sentence and never write a disallowed claim. Every value from results/v6/15_derived_v6.json is labelled post hoc, no "
    "CI; the E12 evaluator-grid caveat sits next to every student - G* success number; 0-499 is the primary window and "
    "300-499 the fresh check, reported side by side; write p < 1e-4 instead of p = 0. The outline's [NEED: ...] items: "
    "use a value only if it appears verbatim in the pasted JSON; otherwise write the sentence without the number or leave "
    "the marker [NEED: ...] in place - never invent it. The outline's [CITE-MISSING: ...] items stay as markers. The v5 "
    "final draft is appended at the very end of this message as a wording source only: reuse its still-valid technical "
    "descriptions (task, belief, G*, evaluator, learners, statistics, method constants with their provenance), but "
    "wherever it conflicts with the outline or the v6 numbers, the outline and the JSON win; v5 test5 0-299 contrasts are "
    "superseded by the v6 0-499 / 300-499 rows. Draft the Figure 1 prompt first, as a fenced block headed "
    "'FIGURE 1 PROMPT' before the Title (data panels must name the JSON keys they plot).")
metrics = ("EXPERIMENT METRICS (use ONLY these numbers; round to 4 sig figs; three files pasted in full. Refer to keys "
           "as A:<key> (v6 read-out), D:<key> (v6 post-hoc arithmetic, no CI) and v5:<key>):\n\n"
           "=== A: results/v6/14_v6_analysis.json ===\n" + rd("results/v6/14_v6_analysis.json")
           + "\n\n=== D: results/v6/15_derived_v6.json ===\n" + rd("results/v6/15_derived_v6.json")
           + "\n\n=== v5: results/v5/results_v5.json ===\n" + rd("results/v5/results_v5.json") + "\n\n")
outline = rd("paper/mypaper/sections/00_outline.md") + \
    "\n\n=== WORDING SOURCE ONLY: v5 final draft (paper/mypaper/v5/draft_v5_final.md) ===\n" + rd("paper/mypaper/v5/draft_v5_final.md")
user = (user_t.replace("{preamble}", preamble).replace("{topic_constraint}", block)
        .replace("{exp_metrics_instruction}", metrics).replace("{citation_instruction}", cites)
        .replace("{outline}", outline))
d = os.path.dirname(os.path.abspath(__file__))
open(os.path.join(d, "stage17_v6_system.txt"), "w").write(system + "\n")
open(os.path.join(d, "stage17_v6_user.txt"), "w").write(user)
print(len(system.split()), len(user.split()), "words;", cites.count("\n- "), "cite keys")
