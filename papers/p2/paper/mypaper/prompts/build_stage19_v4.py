"""Build the p2 stage-19 [v4] prompt from the verbatim template (pipeline/references/stage_prompts/paper_revision.md)
on paper/mypaper/draft_v4.md with the v4 reviews (18_peer_review_v4.md + both full runs). --pass2: pass-2 record."""
import os
import re
import sys

PASS2 = "--pass2" in sys.argv
P2 = os.path.abspath(os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "..", ".."))
ROOT = os.path.abspath(os.path.join(P2, "..", ".."))
rd = lambda p, b=P2: open(os.path.join(b, p)).read()
tpl = rd("pipeline/references/stage_prompts/paper_revision.md", ROOT)
system = re.search(r"\*\*System:\*\*\n```\n(.*?)\n```", tpl, re.S).group(1)
user_t = re.search(r"\*\*User:\*\*\n```\n(.*?)\n```\n", tpl, re.S).group(1)
u16 = rd("paper/mypaper/prompts/stage16_user.txt")
block = u16[u16.index("=== HARD TOPIC CONSTRAINT ==="):u16.index("=== END CONSTRAINT ===") + len("=== END CONSTRAINT ===")] + "\n"
sfx = "_v4_pass2" if PASS2 else "_v4"
rec = "18_peer_review_v4_pass2.md" if PASS2 else "18_peer_review_v4.md"
r1 = "18_review_v4_pass2_run1.md" if PASS2 else "18_review_v4_run1.md"
r2 = "18_review_v4_pass2_run2.md" if PASS2 else "18_review_v4_run2.md"
reviews = (rd("paper/mypaper/" + rec)
           + f"\n\n=== Full review run 1 (paper/mypaper/{r1}) ===\n" + rd("paper/mypaper/" + r1)
           + f"\n\n=== Full review run 2 (paper/mypaper/{r2}) ===\n" + rd("paper/mypaper/" + r2)
           + "\n\n=== BINDING for this revision (main session) ===\n"
           "- Address the must-fix items of the merged record with targeted edits; do not rewrite sections the record does "
           "not touch. The 'Deferred' items need new experiments and are NOT to be simulated in text: only as limitations / "
           "future work. No citations outside docs/05_knowledge_cards.json.\n"
           "- New numbers only from results/v4/v4_analysis.json, results/v3/a7_integrated.json, results/v3/results_v3.json, "
           "results/v2/results_v2.json or results/v1/results_v1.json (open them under /home/claude/paper-writing/papers/p2), "
           "or constants read from code/ (e.g. CSF-1's mu) or the design docs (docs/07*, 08a-08h, 09, 10, 11). "
           "Reviewer-computed numbers that are in none of these must not be printed. Check every value you change against "
           "the JSON (e.g. the CSF-fam RE at slip 0.10 vs at its CRC point).\n"
           "- Keep the FIGURE 1 PROMPT block first.\n"
           "- Length: this is the RSS 2027 Stage 1 extended abstract (5 pages body, checked on the real PDF in stage 22). "
           "RESTRICTS floors: Abstract 150-250, Introduction >= 700, Related Work >= 500, Method >= 800, Experiments/Setup "
           ">= 600, Results >= 500, total >= 4,000 words. Bring Introduction, Related Work and Setup up to their floors; "
           "the template's rule applies: no section gets shorter (Limitations must not be shortened or softened). Page fit "
           "is handled at stage 22 on the real PDF, not here.\n")
user = (user_t.replace("{topic_constraint}", block).replace("{draft}", rd("paper/mypaper/draft_v4.md"))
        .replace("{reviews}", reviews))
d = os.path.dirname(os.path.abspath(__file__))
open(os.path.join(d, f"stage19{sfx}_system.txt"), "w").write(system + "\n")
open(os.path.join(d, f"stage19{sfx}_user.txt"), "w").write(user)
print(len(user.split()), "words")
