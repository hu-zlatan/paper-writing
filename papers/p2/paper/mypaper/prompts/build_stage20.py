"""Build the p2 stage-20 prompt from the verbatim template (pipeline/references/stage_prompts/quality_gate.md)."""
import os
import re
import sys

DRAFT = sys.argv[1] if len(sys.argv) > 1 else "paper/mypaper/draft_v1.md"
SUF = sys.argv[2] if len(sys.argv) > 2 else ""
P2 = os.path.abspath(os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "..", ".."))
ROOT = os.path.abspath(os.path.join(P2, "..", ".."))
tpl = open(os.path.join(ROOT, "pipeline/references/stage_prompts/quality_gate.md")).read()
system = re.search(r"\*\*System:\*\*\n```\n(.*?)\n```", tpl, re.S).group(1)
user_t = re.search(r"\*\*User:\*\*\n```\n(.*?)\n```\n", tpl, re.S).group(1)
user = user_t.replace("{quality_threshold}", "7.5").replace(
    "{revised}", open(os.path.join(P2, DRAFT)).read())
d = os.path.dirname(os.path.abspath(__file__))
open(os.path.join(d, f"stage20{SUF}_system.txt"), "w").write(system + "\n")
open(os.path.join(d, f"stage20{SUF}_user.txt"), "w").write(user)
print(len(user.split()), "words")
