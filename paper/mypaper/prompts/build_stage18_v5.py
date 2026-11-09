"""Build the stage-18 [v5] prompt from the verbatim template (pipeline/references/stage_prompts/peer_review.md)."""
import glob
import os
import re
import subprocess
R = os.path.abspath(os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "..", ".."))
rd = lambda p: open(os.path.join(R, p)).read()
tpl = rd("pipeline/references/stage_prompts/peer_review.md")
system = re.search(r"\*\*System:\*\*\n```\n(.*?)\n```", tpl, re.S).group(1)
user_t = re.search(r"\*\*User:\*\*\n```\n(.*?)\n```\n", tpl, re.S).group(1)
u16 = rd("paper/mypaper/prompts/stage16_v5_user.txt")
topic = re.search(r"The paper MUST be about: (.*?)\n", u16).group(1)
draft = rd("paper/mypaper/sections/draft_v5.md")
logs = sorted(glob.glob(os.path.join(R, "results/v5/test5/*.jsonl")), key=os.path.getsize)[-1]
log_head = "\n".join(l[:400] for l in open(logs).read().splitlines()[:200])
grep = subprocess.run("grep -rn 'scipy.stats\\|crossed_bootstrap_diff\\|def holm\\|holm(\\|wls\\|weighted' code/*_v5.py code/touchbed/stats.py",
                      shell=True, cwd=R, capture_output=True, text=True).stdout
nv5 = sum(len(f) for _, _, f in os.walk(os.path.join(R, "results/v5")))
ev = ("EXPERIMENT EVIDENCE\n\n(a1) results/v5/results_v5.json (full):\n" + rd("results/v5/results_v5.json")
      + "\n\n(a2) results/v4/results_v4.json (full; prior S2 cell):\n" + rd("results/v4/results_v4.json")
      + "\n\n(a3) results/v3/results_v3.json (full; prior S12 cell):\n" + rd("results/v3/results_v3.json")
      + f"\n\n(b) First 200 lines of the longest v5 test5 run log ({os.path.relpath(logs, R)}), lines cut at 400 chars:\n" + log_head
      + "\n\n(c) Statistical tests actually present in code/ (grep over the v5 analysis scripts and code/touchbed/stats.py):\n" + grep
      + "\n\n(d) Pre-registration and amendments of record: docs/07c_amendment_v5_0.md and docs/07c_amendment_v5_1.md (open them)."
      + f" Condition x seed combinations: see 'episodes_per_method', 'n_episodes', 'n_seeds' and per-seed keys in (a1). Run outputs: "
      f"{nv5} files under results/v5/. The reviewer may open any file in code/, docs/, results/v3/, results/v4/ and results/v5/ "
      "of the repository at /home/claude/paper-writing to verify claims.\n")
user = user_t.replace("{topic}", topic).replace("{draft}", draft).replace("{experiment_evidence}", ev)
d = os.path.dirname(os.path.abspath(__file__))
open(os.path.join(d, "stage18_v5_system.txt"), "w").write(system + "\n")
open(os.path.join(d, "stage18_v5_user.txt"), "w").write(user)
print(len(user.split()), "words; log", os.path.relpath(logs, R), "; grep lines", grep.count("\n"))
