"""Build the p2 stage-18 prompt from the verbatim template (pipeline/references/stage_prompts/peer_review.md).
Usage: python build_stage18.py [draft path relative to papers/p2] [output suffix]"""
import glob
import os
import re
import subprocess
import sys
P2 = os.path.abspath(os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "..", ".."))
ROOT = os.path.abspath(os.path.join(P2, "..", ".."))
rd = lambda p, b=P2: open(os.path.join(b, p)).read()
tpl = rd("pipeline/references/stage_prompts/peer_review.md", ROOT)
system = re.search(r"\*\*System:\*\*\n```\n(.*?)\n```", tpl, re.S).group(1)
user_t = re.search(r"\*\*User:\*\*\n```\n(.*?)\n```\n", tpl, re.S).group(1)
u16 = rd("paper/mypaper/prompts/stage16_user.txt")
topic = re.search(r"The paper MUST be about: (.*?)\n", u16).group(1)
draft_p = sys.argv[1] if len(sys.argv) > 1 else "paper/mypaper/draft_v1.md"
suffix = sys.argv[2] if len(sys.argv) > 2 else ""
draft = rd(draft_p)
logs = sorted(glob.glob(os.path.join(P2, "results/v1/logs/*.log")), key=os.path.getsize)[-1]
log_head = "\n".join(l[:400] for l in open(logs).read().splitlines()[:200])
grep = subprocess.run("grep -rn 'scipy.stats\\|def .*boot\\|bootstrap(\\|clopper\\|beta.ppf\\|tost\\|holm' code/*.py code/certgrip/*.py",
                      shell=True, cwd=P2, capture_output=True, text=True).stdout
nres = sum(len(f) for _, _, f in os.walk(os.path.join(P2, "results/v1")))
ev = ("EXPERIMENT EVIDENCE\n\n(a) results/v1/results_v1.json (full; every block is an unchanged analysis file of results/v1/):\n"
      + rd("results/v1/results_v1.json")
      + f"\n\n(b) First 200 lines of the longest run log ({os.path.relpath(logs, P2)}), lines cut at 400 chars:\n" + log_head
      + "\n\n(c) Statistical procedures actually present in code/ (grep):\n" + grep
      + "\n\n(d) Pre-registration and amendments of record: docs/07_hypotheses.md, docs/08_experiment_plan.yaml, "
      "docs/08a_pilot_amendment.md ... docs/08h_secondaries_batch3.md (open them). Condition x seed combinations: see the "
      "per-arm keys (arm names carry feature set, sigma and seed, e.g. full_rd@0.2#0) and n / n_objects fields in (a). "
      f"Run outputs: {nres} files under results/v1/ (labels/, preds/, crc/, h3/, mono/, h1v/, logs/). The reviewer may open "
      "any file in code/, docs/ and results/ under /home/claude/paper-writing/papers/p2 to verify claims.\n")
user = user_t.replace("{topic}", topic).replace("{draft}", draft).replace("{experiment_evidence}", ev)
d = os.path.dirname(os.path.abspath(__file__))
open(os.path.join(d, f"stage18{suffix}_system.txt"), "w").write(system + "\n")
open(os.path.join(d, f"stage18{suffix}_user.txt"), "w").write(user)
print(len(user.split()), "words; log", os.path.relpath(logs, P2), "; grep lines", grep.count("\n"))
