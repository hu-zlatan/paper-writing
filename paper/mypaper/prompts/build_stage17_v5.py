"""Build the stage-17 [v5] prompt from the verbatim template (pipeline/references/stage_prompts/paper_draft.md)."""
import os
import re
R = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "..", "..")
rd = lambda p: open(os.path.join(R, p)).read()
tpl = rd("pipeline/references/stage_prompts/paper_draft.md")
system = re.search(r"\*\*System:\*\*\n````\n(.*?)\n````", tpl, re.S).group(1)
user_t = re.search(r"\*\*User:\*\*\n```\n(.*?)\n```\n", tpl, re.S).group(1)
# topic block identical to stage 16 v5
u16 = rd("paper/mypaper/prompts/stage16_v5_user.txt")
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
    "Results >= 500, Discussion >= 300, Limitations >= 200, Conclusion >= 150. Paper type: a pre-registered five-cell "
    "MEASUREMENT / CHARACTERISATION paper with NO method claim (results/v5/15_decision.md sections 4.3-4.4 are pasted "
    "inside the outline's section 0 and are binding: follow every binding sentence, label (DEC / GATE / REP / EXPL / PH / "
    "PRIOR) and never-write item in the outline; every value from 15_posthoc_derived.json is labelled post hoc, no CI; "
    "the E5 evaluator-resolution caveat sits next to every test5 success contrast). The outline's [NEED: ...] items: "
    "use a value only if it appears verbatim in the pasted JSON; otherwise write the sentence without the number or "
    "leave the marker [NEED: ...] in place - never invent it. 16_report_rows.json now holds the rl_success training "
    "episode counts (print them next to every rl_success number) and the student last-checkpoint sensitivity rows "
    "(held-out label regret R_bar, kept vs last epoch). The outline's [CITE-MISSING: ...] items stay as markers. "
    "The v4 final draft is appended at the very end of this message as a wording source only: reuse its still-valid "
    "technical descriptions (task, belief, G*, evaluator, learners, statistics), but wherever it conflicts with the "
    "outline or the v5 numbers, the outline and the JSON win; v4 numbers may appear only as PRIOR cells as the outline "
    "says. Draft the Figure 1 prompt first, as a fenced block headed 'FIGURE 1 PROMPT' before the Title.")
metrics = ("EXPERIMENT METRICS (use ONLY these numbers; round to 4 sig figs; three files pasted in full. Refer to keys "
           "as v5:<key>, v4:<key> and v3:<key>):\n\n=== v5: results/v5/results_v5.json ===\n" + rd("results/v5/results_v5.json")
           + "\n\n=== v4: results/v4/results_v4.json ===\n" + rd("results/v4/results_v4.json")
           + "\n\n=== v3: results/v3/results_v3.json ===\n" + rd("results/v3/results_v3.json") + "\n\n")
outline = rd("paper/mypaper/sections/00_outline.md") + \
    "\n\n=== WORDING SOURCE ONLY: v4 final draft (paper/mypaper/v4/draft_v4_final.md) ===\n" + rd("paper/mypaper/v4/draft_v4_final.md")
user = (user_t.replace("{preamble}", preamble).replace("{topic_constraint}", block)
        .replace("{exp_metrics_instruction}", metrics).replace("{citation_instruction}", cites)
        .replace("{outline}", outline))
d = os.path.dirname(os.path.abspath(__file__))
open(os.path.join(d, "stage17_v5_system.txt"), "w").write(system + "\n")
open(os.path.join(d, "stage17_v5_user.txt"), "w").write(user)
print(len(system.split()), len(user.split()), "words;", cites.count("\n- "), "cite keys")
