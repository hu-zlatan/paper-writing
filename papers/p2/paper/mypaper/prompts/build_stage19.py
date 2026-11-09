"""Build the p2 stage-19 prompt from the verbatim template (pipeline/references/stage_prompts/paper_revision.md)."""
import os
import re
P2 = os.path.abspath(os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "..", ".."))
ROOT = os.path.abspath(os.path.join(P2, "..", ".."))
rd = lambda p, b=P2: open(os.path.join(b, p)).read()
tpl = rd("pipeline/references/stage_prompts/paper_revision.md", ROOT)
system = re.search(r"\*\*System:\*\*\n```\n(.*?)\n```", tpl, re.S).group(1)
user_t = re.search(r"\*\*User:\*\*\n```\n(.*?)\n```\n", tpl, re.S).group(1)
u16 = rd("paper/mypaper/prompts/stage16_user.txt")
block = u16[u16.index("=== HARD TOPIC CONSTRAINT ==="):u16.index("=== END CONSTRAINT ===") + len("=== END CONSTRAINT ===")] + "\n"
import sys
PASS2 = "--pass2" in sys.argv
reviews = (rd("paper/mypaper/18_peer_review_pass2.md")
           + "\n\n=== Full review pass 2 run 1 ===\n" + rd("paper/mypaper/18_review_pass2_run1.md")
           + "\n\n=== Full review pass 2 run 2 ===\n" + rd("paper/mypaper/18_review_pass2_run2.md")
           + "\n\n=== BINDING for this revision (main session) ===\n"
           "- Address must-fix items P1-P9 of the pass-2 merged record. E1-E5 only as limitations / future work; no "
           "citations outside docs/05_knowledge_cards.json.\n"
           "- New numbers only from results/v1/results_v1.json (block 19_report_rows.json holds the new report-only rows: "
           "detector_error_structure, static_touch_check). Reviewer-computed numbers not in that file must not be printed.\n"
           "- Abstract <= 250 words (the only section allowed to get shorter, by the reviewers' explicit request); every "
           "other section no shorter than now; Limitations not shortened or softened; keep the FIGURE 1 PROMPT block first.\n"
           ) if PASS2 else (rd("paper/mypaper/18_peer_review.md")
           + "\n\n=== Full review run 1 (paper/mypaper/18_review_run1.md) ===\n" + rd("paper/mypaper/18_review_run1.md")
           + "\n\n=== Full review run 2 (paper/mypaper/18_review_run2.md) ===\n" + rd("paper/mypaper/18_review_run2.md")
           + "\n\n=== BINDING for this revision (main session) ===\n"
           "- Address must-fix items 1-10 of the merged record. Evidence-level items E1-E5 need new experiments or new "
           "literature and are NOT to be simulated in text: mention them only as limitations / future work; do not add "
           "citations outside docs/05_knowledge_cards.json (E5 stays a gap).\n"
           "- New numbers may come only from results/v1/results_v1.json, which now includes block 19_report_rows.json "
           "(report-only rows computed by code/tools_stage19_rows.py from existing raw files; label them report-only). "
           "Reviewer-computed numbers that are not in that file must not be printed.\n"
           "- Keep the FIGURE 1 PROMPT block first and update it where the reviews require (CSF-mu-hat grid-floor caveat).\n"
           "- Length floors of this repo (RESTRICTS): total >= 4,000 words; Abstract >= 150, Introduction >= 700, "
           "Related Work >= 500, Method >= 800, Experiments >= 600, Results >= 500, Discussion >= 300, Limitations >= "
           "200, Conclusion >= 150; no section shorter than in the draft; Limitations must not be shortened or softened.\n")
user = (user_t.replace("{topic_constraint}", block).replace("{draft}", rd("paper/mypaper/draft_v1.md"))
        .replace("{reviews}", reviews))
d = os.path.dirname(os.path.abspath(__file__))
sfx = "_pass2" if PASS2 else ""
open(os.path.join(d, f"stage19{sfx}_system.txt"), "w").write(system + "\n")
open(os.path.join(d, f"stage19{sfx}_user.txt"), "w").write(user)
print(len(user.split()), "words")
