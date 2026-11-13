"""Build a stage-19-template prompt (pipeline/references/stage_prompts/paper_revision.md, verbatim) for the paper-level
items of the stage-20 [v4] gate (run 51, while the owner decision is pending). Reviews slot = gate paper-level items."""
import json
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
g = json.loads(rd("paper/mypaper/20_quality_gate_v4.json"))
pl = lambda xs: "\n".join("- " + x for x in xs if x.startswith("[paper-level]"))
ev = lambda xs: "\n".join("- " + x for x in xs if x.startswith("[evidence-level]"))
reviews = ("=== Stage-20 quality gate [v4] (paper/mypaper/20_quality_gate_v4.json), score "
           f"{g['score_1_to_10']} / 10 ===\nVerdict: {g['verdict']}\n\nPaper-level weaknesses (address all):\n"
           + pl(g["weaknesses"]) + "\n\nPaper-level required actions (address all):\n" + pl(g["required_actions"])
           + "\n\nEvidence-level items (need new experiments; NOT to be addressed in text except as limitations / future "
           "work, which the draft already lists; do not invent results for them):\n" + ev(g["required_actions"])
           + "\n\n=== BINDING for this revision (main session) ===\n"
           "- Numbers are locked: do not introduce any number that is not already in the draft. You may round a number "
           "already in the draft to 2-3 significant figures in the prose (abstract, introduction, discussion); keep full "
           "precision in tables. Do not change any table value.\n"
           "- 'Cut repeated caveats' must not shorten or soften the Limitations section: consolidate each caveat into "
           "Limitations (keep every limitation item) and replace repeats elsewhere with a short cross-reference. Move, "
           "do not delete: Section 5.4 (earlier-round attribution / competitors) and the mid-friction sub-pool row go to "
           "a new Appendix (keep their text and numbers there, with a one-sentence pointer in Section 5).\n"
           "- Abstract and Introduction: state one crisp conditional answer to the title question first (when the probe "
           "pays off, and its modest absolute size), using only numbers already in the draft.\n"
           "- Present relative excess, absolute excess and force-time together as one cost picture, and say plainly that "
           "the probe-vs-learner attribution is unresolved across metrics.\n"
           "- Keep the FIGURE 1 PROMPT and FIGURE 2 PROMPT blocks and every status code (CONF/PRE/SEC/DESC/PH). No new "
           "citations (only cite keys already in the draft).\n"
           "- Length: RSS 2027 Stage 1 extended abstract; RESTRICTS floors: Abstract 150-250, Introduction >= 700, Related "
           "Work >= 500, Method >= 800, Experiments/Setup >= 600, Results >= 500, total >= 4,000 words. Page fit is "
           "handled at stage 22 on the real PDF, not here.\n")
user = (user_t.replace("{topic_constraint}", block).replace("{draft}", rd("paper/mypaper/draft_v4.md"))
        .replace("{reviews}", reviews))
d = os.path.dirname(os.path.abspath(__file__))
open(os.path.join(d, "gatefix_v4_system.txt"), "w").write(system + "\n")
open(os.path.join(d, "gatefix_v4_user.txt"), "w").write(user)
print(len(user.split()), "words")
