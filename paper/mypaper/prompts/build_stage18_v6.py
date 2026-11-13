"""Build the stage-18 [v6] prompt from the verbatim template (pipeline/references/stage_prompts/peer_review.md)."""
import glob
import os
import re
import subprocess
R = os.path.abspath(os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "..", ".."))
rd = lambda p: open(os.path.join(R, p)).read()
tpl = rd("pipeline/references/stage_prompts/peer_review.md")
system = re.search(r"\*\*System:\*\*\n```\n(.*?)\n```", tpl, re.S).group(1)
user_t = re.search(r"\*\*User:\*\*\n```\n(.*?)\n```\n", tpl, re.S).group(1)
u16 = rd("paper/mypaper/prompts/stage16_v6_user.txt")
topic = re.search(r"The paper MUST be about: (.*?)\n", u16).group(1)
draft = rd("paper/mypaper/sections/draft_v6.md")
logs = sorted(glob.glob(os.path.join(R, "results/v6/test5/*.jsonl")), key=os.path.getsize)[-1]
log_head = "\n".join(l[:400] for l in open(logs).read().splitlines()[:200])
grep = subprocess.run("grep -rn 'scipy.stats\\|crossed_bootstrap_diff\\|def holm\\|holm(\\|wls\\|weighted' code/*_v6.py code/touchbed/stats.py",
                      shell=True, cwd=R, capture_output=True, text=True).stdout
nv6 = sum(len(f) for _, _, f in os.walk(os.path.join(R, "results/v6")))
ev = ("EXPERIMENT EVIDENCE\n\n(a1) results/v6/14_v6_analysis.json (full; v6 frozen read-out):\n" + rd("results/v6/14_v6_analysis.json")
      + "\n\n(a2) results/v6/15_derived_v6.json (full; post-hoc arithmetic, no CI):\n" + rd("results/v6/15_derived_v6.json")
      + "\n\n(a3) results/v5/results_v5.json (full; v5 rows: validation, RL sweep, latency E6, E7):\n" + rd("results/v5/results_v5.json")
      + f"\n\n(b) First 200 lines of the longest v6 test5 run log ({os.path.relpath(logs, R)}), lines cut at 400 chars:\n" + log_head
      + "\n\n(c) Statistical tests actually present in code/ (grep over the v6 analysis script and code/touchbed/stats.py):\n" + grep
      + "\n\n(d) Pre-registration and amendments of record: docs/07c_amendment_v6_0.md (with addendum v6.1) and, for v5 rows, "
      "docs/07c_amendment_v5_0.md and docs/07c_amendment_v5_1.md (open them)."
      + f" Condition x seed combinations: see 'episodes_per_method', 'n_episodes', 'n_seeds' in (a1). Run outputs: "
      f"{nv6} files under results/v6/. The reviewer may open any file in code/, docs/, results/v5/ and results/v6/ "
      "of the repository at /home/claude/paper-writing to verify claims.\n")
user = user_t.replace("{topic}", topic).replace("{draft}", draft).replace("{experiment_evidence}", ev)
d = os.path.dirname(os.path.abspath(__file__))
open(os.path.join(d, "stage18_v6_system.txt"), "w").write(system + "\n")
open(os.path.join(d, "stage18_v6_user.txt"), "w").write(user)
print(len(user.split()), "words; log", os.path.relpath(logs, R), "; grep lines", grep.count("\n"))
