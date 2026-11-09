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
reviews = (rd("paper/mypaper/18_peer_review.md")
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
open(os.path.join(d, "stage19_system.txt"), "w").write(system + "\n")
open(os.path.join(d, "stage19_user.txt"), "w").write(user)
print(len(user.split()), "words")
