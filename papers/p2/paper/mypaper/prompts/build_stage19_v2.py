"""Build the p2 stage-19 [v2] prompt from the verbatim template (pipeline/references/stage_prompts/paper_revision.md)
on paper/mypaper/draft_v2.md with the v2 reviews (18_peer_review_v2.md + both full runs)."""
import os
import re
import sys

PASS2 = "--pass2" in sys.argv  # second pass: pass-2 merged record + its two runs, binding items P1-P9
P2 = os.path.abspath(os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "..", ".."))
ROOT = os.path.abspath(os.path.join(P2, "..", ".."))
rd = lambda p, b=P2: open(os.path.join(b, p)).read()
tpl = rd("pipeline/references/stage_prompts/paper_revision.md", ROOT)
system = re.search(r"\*\*System:\*\*\n```\n(.*?)\n```", tpl, re.S).group(1)
user_t = re.search(r"\*\*User:\*\*\n```\n(.*?)\n```\n", tpl, re.S).group(1)
u16 = rd("paper/mypaper/prompts/stage16_user.txt")
block = u16[u16.index("=== HARD TOPIC CONSTRAINT ==="):u16.index("=== END CONSTRAINT ===") + len("=== END CONSTRAINT ===")] + "\n"
if PASS2:
    reviews = (rd("paper/mypaper/18_peer_review_v2_pass2.md")
               + "\n\n=== Full review pass 2 run 1 (paper/mypaper/18_review_v2_pass2_run1.md) ===\n"
               + rd("paper/mypaper/18_review_v2_pass2_run1.md")
               + "\n\n=== Full review pass 2 run 2 (paper/mypaper/18_review_v2_pass2_run2.md) ===\n"
               + rd("paper/mypaper/18_review_v2_pass2_run2.md")
               + "\n\n=== BINDING for this revision (main session) ===\n"
               "- Address must-fix items P1-P9 of the merged record with targeted edits; do not rewrite sections that "
               "the record does not touch. E1-E8 need new experiments or analyses and are NOT to be simulated in text: "
               "only as limitations / future work. No citations outside docs/05_knowledge_cards.json.\n"
               "- New numbers only from results/v1/results_v1.json or results/v2/results_v2.json (open them under "
               "/home/claude/paper-writing/papers/p2) or constants quoted from the design docs (docs/07*, 08a-08h, 09). "
               "Reviewer-computed numbers that are in neither must not be printed.\n"
               "- Keep the FIGURE 1 PROMPT block first and the appendix structure.\n"
               "- Length floors (RESTRICTS): total >= 4,000 words; Abstract >= 150 (<= 250), Introduction >= 700, Related "
               "Work >= 500, Method >= 800, Experiments >= 600, Results >= 500, Discussion >= 300, Limitations >= 200, "
               "Conclusion >= 150. Limitations not shortened or softened.\n")
else:
    reviews = (rd("paper/mypaper/18_peer_review_v2.md")
               + "\n\n=== Full review run 1 (paper/mypaper/18_review_v2_run1.md) ===\n" + rd("paper/mypaper/18_review_v2_run1.md")
               + "\n\n=== Full review run 2 (paper/mypaper/18_review_v2_run2.md) ===\n" + rd("paper/mypaper/18_review_v2_run2.md")
               + "\n\n=== BINDING for this revision (main session) ===\n"
               "- Address must-fix items 1-10 of the merged record. E1-E4 need new experiments or data and are NOT to be "
               "simulated in text: only as limitations / future work. No citations outside docs/05_knowledge_cards.json.\n"
               "- New numbers only from results/v1/results_v1.json or results/v2/results_v2.json (open them under "
               "/home/claude/paper-writing/papers/p2) or constants quoted from the design docs (docs/07*, 08a-08h, 09). "
               "Reviewer-computed numbers that are in neither must not be printed.\n"
               "- Keep the FIGURE 1 PROMPT block first; redraw panel (b) on one grid.\n"
               "- Length floors (RESTRICTS): total >= 4,000 words; Abstract >= 150 (<= 250), Introduction >= 700, Related "
               "Work >= 500, Method >= 800, Experiments >= 600, Results >= 500, Discussion >= 300, Limitations >= 200, "
               "Conclusion >= 150. Material moved to the appendix counts for no floor; Limitations not shortened or softened.\n")
user = (user_t.replace("{topic_constraint}", block).replace("{draft}", rd("paper/mypaper/draft_v2.md"))
        .replace("{reviews}", reviews))
d = os.path.dirname(os.path.abspath(__file__))
sfx = "_v2_pass2" if PASS2 else "_v2"
open(os.path.join(d, f"stage19{sfx}_system.txt"), "w").write(system + "\n")
open(os.path.join(d, f"stage19{sfx}_user.txt"), "w").write(user)
print(len(user.split()), "words")
