"""Build a stage-19-template prompt (pipeline/references/stage_prompts/paper_revision.md, verbatim) for the paper-level
items of the stage-20 [v6] gate (run 51, while the owner decision is pending). Reviews slot = gate paper-level items."""
import json
import os
import re

R = os.path.abspath(os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "..", ".."))
rd = lambda p: open(os.path.join(R, p)).read()
tpl = rd("pipeline/references/stage_prompts/paper_revision.md")
system = re.search(r"\*\*System:\*\*\n```\n(.*?)\n```", tpl, re.S).group(1)
user_t = re.search(r"\*\*User:\*\*\n```\n(.*?)\n```\n", tpl, re.S).group(1)
u16 = rd("paper/mypaper/prompts/stage16_v6_user.txt")
block = u16[u16.index("=== HARD TOPIC CONSTRAINT ==="):u16.index("=== END CONSTRAINT ===") + len("=== END CONSTRAINT ===")] + "\n"
g = json.loads(rd("paper/mypaper/20_quality_gate.json"))
sel = lambda xs, tag: "\n".join("- " + x for x in xs if x.startswith(tag))
reviews = ("=== Stage-20 quality gate [v6] (paper/mypaper/20_quality_gate.json), score "
           f"{g['score_1_to_10']} / 10 ===\nVerdict: {g['verdict']}\n\nPaper-level weaknesses:\n"
           + sel(g["weaknesses"], "[paper-level]") + "\n\nPaper-level required actions:\n"
           + sel(g["required_actions"], "[paper-level]")
           + "\n\nEvidence-level required actions (need new experiments; NOT to be addressed in text except as limitations / "
           "future work, which the draft already lists; do not invent results for them):\n"
           + sel(g["required_actions"], "[evidence-level]") + """

=== BINDING INSTRUCTIONS FROM THE PIPELINE (main session; override anything above that conflicts) ===
- Address: (1) tighten the abstract and C1 to one clear sentence of result plus one of qualification; move the
  bootstrap-seed and 100,000-resample detail to Section 5.1 and Appendix B (move, do not delete); (2) state in the
  abstract that the student is not shown to be the best non-oracle policy in four of five cells (use the draft's own
  Section 5.1 wording/numbers); (3) remove repeated latency, E12 and Holm-count caveats across Sections 4, 5.1, 6, 7, 8:
  keep each caveat once (Limitations, or its home section) and replace repeats with a short cross-reference. Limitations
  must not be shortened or softened (keep every item). The three citations are already resolved (\\cite{zaheer2017deep},
  \\cite{efron1979bootstrap}, \\cite{holm1979simple}); keep them. Figure rendering is out of scope; keep the FIGURE 1
  PROMPT block and the leading HTML comment line, changing the comment to say 'revised run 51 (gate paper-level items)'.
- Do NOT write anything results/v6/15_decision.md section 4.5 forbids; this stays a pre-registered measurement paper with
  one narrow H6b claim. The internal-only pre-registration stays disclosed as it is.
- Numbers are locked: introduce no number that is not already in the draft; rounding in the abstract is allowed only to
  the precision a value already has elsewhere in the draft. Do not change any table value. Write p < 1e-4, never p = 0.
- Abstract 150-250 words. The template's never-shorten rule applies per section except where text is moved to
  Section 5.1 / Appendix B as instructed; the page-length cut is done in stage 22, not here.
""")
user = user_t.replace("{topic_constraint}", block).replace("{draft}", rd("paper/mypaper/sections/draft_v6.md")).replace("{reviews}", reviews)
d = os.path.dirname(os.path.abspath(__file__))
open(os.path.join(d, "gatefix_v6_system.txt"), "w").write(system + "\n")
open(os.path.join(d, "gatefix_v6_user.txt"), "w").write(user)
print(len(user.split()), "words")
