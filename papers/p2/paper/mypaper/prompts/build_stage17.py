"""Build the p2 stage-17 prompt from the verbatim template (pipeline/references/stage_prompts/paper_draft.md)."""
import json
import os
import re
P2 = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "..", "..")
ROOT = os.path.join(P2, "..", "..")
rd = lambda p, base=P2: open(os.path.join(base, p)).read()
tpl = rd("pipeline/references/stage_prompts/paper_draft.md", ROOT)
system = re.search(r"\*\*System:\*\*\n````\n(.*?)\n````", tpl, re.S).group(1)
user_t = re.search(r"\*\*User:\*\*\n```\n(.*?)\n```\n", tpl, re.S).group(1)
u16 = rd("paper/mypaper/prompts/stage16_user.txt")
block = u16[u16.index("=== HARD TOPIC CONSTRAINT ==="):u16.index("=== END CONSTRAINT ===") + len("=== END CONSTRAINT ===")] + "\n"
cards = json.load(open(os.path.join(P2, "docs/05_knowledge_cards.json")))
cards = cards.get("cards", cards) if isinstance(cards, dict) else cards
cites = ("CITATIONS: Use the cite_keys provided. Format as \\cite{cite_key}. Available cite_keys and one-line summaries:\n"
         + "\n".join(f"- {c['cite_key']}: {c['title']} — {str(c.get('findings',''))[:160]}" for c in cards) + "\n\n")
preamble = (
    "Target: RSS 2027 (Robotics: Science and Systems). This master draft serves the Stage 1 extended abstract "
    "(<= 5 content pages + 1 page of references, due 2026-12-04 AoE; condensed from this draft in stage 22 using the "
    "outline's per-section word targets) and later the Stage 2 full paper (<= 8 pages). Binding length floors for this "
    "paper (papers/p2/RESTRICTS.yaml total_words_floor 4,000; they replace the 9-page floors quoted below): total main "
    "body >= 4,000 words (aim 4,300-5,000); Abstract >= 150, Introduction >= 700, Related Work >= 500, Method >= 800, "
    "Experiments >= 600, Results >= 500, Discussion >= 300, Limitations >= 200, Conclusion >= 150. The re-scoped story "
    "of results/15_decision.md and the binding audit rewrites of results/14_analysis.md (both summarised inside the "
    "outline) are binding: the claim is the friction-onset probe plus conformal risk control; the learned tactile model "
    "adds no demonstrated gain (H2b not confirmed); H1-M failed; H3 inconclusive; the H2-R scope limit appears in the "
    "abstract; H2-M is descriptive only; post hoc analyses (08e grid sensitivity, any secondary added after freezing) are "
    "labelled as such. Method and protocol details (constants, protocol steps, label rule, splits, families, "
    "disturbances, learners) must be taken from the design documents docs/07_hypotheses.md, docs/08a_pilot_amendment.md, "
    "docs/08b_preregistration.md, docs/08c_analysis_plan.md, docs/08d_h3_stream_plan.md, docs/08e_crc_grid_sensitivity.md, "
    "docs/08f-08h (all under papers/p2/), quoted as written there. If a needed value is in none of these, write the "
    "sentence without it or leave a marker [NEED: ...]; never invent it. Draft the Figure 1 prompt first, as a fenced "
    "block headed 'FIGURE 1 PROMPT' before the Title.")
metrics = ("EXPERIMENT METRICS (use ONLY these numbers; round to 4 sig figs; the evidence index pasted in full, each "
           "block the unchanged content of a file in results/v1/):\n\n=== results/v1/results_v1.json ===\n"
           + rd("results/v1/results_v1.json") + "\n\n")
outline = rd("paper/mypaper/sections/00_outline.md")
user = (user_t.replace("{preamble}", preamble).replace("{topic_constraint}", block)
        .replace("{exp_metrics_instruction}", metrics).replace("{citation_instruction}", cites)
        .replace("{outline}", outline))
d = os.path.dirname(os.path.abspath(__file__))
open(os.path.join(d, "stage17_system.txt"), "w").write(system + "\n")
open(os.path.join(d, "stage17_user.txt"), "w").write(user)
print(len(system.split()), len(user.split()), "words;", cites.count("\n- "), "cite keys")
