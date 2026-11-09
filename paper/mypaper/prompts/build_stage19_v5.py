"""Build the stage-19 [v5] prompt from the verbatim template (pipeline/references/stage_prompts/paper_revision.md)."""
import os
import re
R = os.path.abspath(os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "..", ".."))
rd = lambda p: open(os.path.join(R, p)).read()
tpl = rd("pipeline/references/stage_prompts/paper_revision.md")
system = re.search(r"\*\*System:\*\*\n```\n(.*?)\n```", tpl, re.S).group(1)
user_t = re.search(r"\*\*User:\*\*\n```\n(.*?)\n```\n", tpl, re.S).group(1)
u16 = rd("paper/mypaper/prompts/stage16_v5_user.txt")
block = u16[u16.index("=== HARD TOPIC CONSTRAINT ==="):u16.index("=== END CONSTRAINT ===") + len("=== END CONSTRAINT ===")] + "\n"
binding = """

=== BINDING INSTRUCTIONS FROM THE PIPELINE (main session; override anything in the reviews that conflicts) ===
- Fix every item 1-7 and S1-S6 of the merged record above, in the way its 'action' column says. Do NOT claim anything
  the outline's never-write list (results/v5/15_decision.md section 4.4) forbids; this stays a measurement paper.
- Numbers stay locked: every number must come from results/v5/results_v5.json (or v4 / v3 results for PRIOR cells),
  or from the frozen amendments docs/07c_amendment_v5_0.md / v5_1.md, or from code constants named in the reviews
  (latency bootstrap B = 2,000 in code/analysis_e6_v5.py; RL sweep seed 719 in amendment v5.0 E3). Open those files to
  copy values; never compute new statistics. Reviewer-computed numbers that are not in a repository file (e.g. run 2's
  exact D5-on-test5 recomputation for A16-2) must NOT be cited as numbers.
- E7 (item 1): copy values from results/v5/12_e7_analysis.json (cells > S2 / S12 > C1_32 / C1_512 > indep_gap_nats,
  selection_bias_nats, G_indep; paired_indep_gap_512_minus_32). It is report-only look-ahead headroom over greedy in
  nats on 32 beliefs per cell, plus the screen's selection bias; it says nothing about G*'s own value-estimate noise;
  success-terms headroom was not measured.
- DAgger R-bar (S4): values from results/v5/16_report_rows.json > student_checkpoint_sensitivity > <cell> > <seed> >
  r0 / r2 > R_bar_kept. You may state per-cell ranges only by copying the min and max of listed values; mark the
  qualifier "report-only".
- Keep the three [CITE-MISSING: ...] markers as they are (fixed in stage 23).
- Never shorten a section or soften Limitations. Keep the leading HTML comment line and the FIGURE 1 PROMPT block
  (fix it only where item 1 or 2 makes it wrong). Change the leading comment to say 'revised in stage 19 [v5] pass 1'.
"""
reviews = (rd("paper/mypaper/18_peer_review.md") + "\n\n=== FULL REVIEW, RUN 1 ===\n" + rd("paper/mypaper/18_review_v5_run1.md")
           + "\n\n=== FULL REVIEW, RUN 2 ===\n" + rd("paper/mypaper/18_review_v5_run2.md") + binding)
user = user_t.replace("{topic_constraint}", block).replace("{draft}", rd("paper/mypaper/sections/draft_v5.md")).replace("{reviews}", reviews)
d = os.path.dirname(os.path.abspath(__file__))
open(os.path.join(d, "stage19_v5_system.txt"), "w").write(system + "\n")
open(os.path.join(d, "stage19_v5_user.txt"), "w").write(user)
print(len(user.split()), "words")
