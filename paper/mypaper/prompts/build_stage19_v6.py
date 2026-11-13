"""Build the stage-19 [v6] prompt from the verbatim template (pipeline/references/stage_prompts/paper_revision.md)."""
import os
import re
import sys
PASS2 = "--pass2" in sys.argv
SUF, RS, OUT = ("_v6_pass2", "_pass2", "stage19_v6_pass2_user.txt") if PASS2 else ("", "", "stage19_v6_user.txt")
R = os.path.abspath(os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "..", ".."))
rd = lambda p: open(os.path.join(R, p)).read()
tpl = rd("pipeline/references/stage_prompts/paper_revision.md")
system = re.search(r"\*\*System:\*\*\n```\n(.*?)\n```", tpl, re.S).group(1)
user_t = re.search(r"\*\*User:\*\*\n```\n(.*?)\n```\n", tpl, re.S).group(1)
u16 = rd("paper/mypaper/prompts/stage16_v6_user.txt")
block = u16[u16.index("=== HARD TOPIC CONSTRAINT ==="):u16.index("=== END CONSTRAINT ===") + len("=== END CONSTRAINT ===")] + "\n"
binding = """

=== BINDING INSTRUCTIONS FROM THE PIPELINE (main session; override anything in the reviews that conflicts) ===
- Fix every item of the triage in the merged record above (items 1-7 of "Triage for stage 19"; pass 2: the pass-2
  record's items), in the way it says. The "Evidence-level requests" cannot be run (refine cap used): do NOT promise
  them as done; add them to Limitations / future work only. Do NOT write anything results/v6/15_decision.md section 4.5
  forbids; this stays a pre-registered measurement paper with one narrow H6b claim.
- Numbers stay locked: every number must come from results/v6/14_v6_analysis.json, results/v6/15_derived_v6.json
  (post hoc, no CI), results/v6/18_posthoc_v6.json (post hoc, report-only; label it so), results/v5/results_v5.json, or
  the frozen amendment docs/07c_amendment_v6_0.md. Open those files to copy values; never compute new statistics.
  Reviewer-computed numbers that are not in one of these files must NOT be cited as numbers.
- Item 2 (DAgger): the warm start is a fact of the code (each round initialised from the previous round's weights,
  code/tools_v5_manifests.py --init); kept-checkpoint epochs from results/v6/18_posthoc_v6.json > P3_checkpoint_epochs
  (copied from results_v5.json > 16_report_rows.json > student_checkpoint_sensitivity) - copy, do not summarise with
  statistics that are not in the file other than min / max / listing values.
- Item 3 (E12): ci95 from results/v6/18_posthoc_v6.json > P1_e12_shift_ci95 > <cell>.
- Item 1 (H6b): seed sensitivity from results/v6/18_posthoc_v6.json > P2_h6b_bootstrap_seed_sensitivity > <window> >
  <seed> > n_rejected (seed 0 is the registered one).
- Item 6: the project-history narrative ("previous round" etc.) moves to a short appendix "Study history"; do not delete
  facts. The abstract and the page-length cut are done in stage 22 (condensation), not here; the template's
  never-shorten rule applies to this stage.
- Keep the three [CITE-MISSING: ...] markers as they are (fixed in stage 23). Never soften Limitations. Keep the leading
  HTML comment line and the FIGURE 1 PROMPT block (fix it only where a triage item makes it wrong). Change the leading
  comment to say 'revised in stage 19 [v6] pass 1' (pass 2: '... pass 2'). Write p < 1e-4, never p = 0.
"""
reviews = (rd(f"paper/mypaper/18_peer_review{SUF}.md") + "\n\n=== FULL REVIEW, RUN 1 ===\n" + rd(f"paper/mypaper/18_review_v6{RS}_run1.md")
           + "\n\n=== FULL REVIEW, RUN 2 ===\n" + rd(f"paper/mypaper/18_review_v6{RS}_run2.md") + binding)
user = user_t.replace("{topic_constraint}", block).replace("{draft}", rd("paper/mypaper/sections/draft_v6.md")).replace("{reviews}", reviews)
d = os.path.dirname(os.path.abspath(__file__))
open(os.path.join(d, "stage19_v6_system.txt"), "w").write(system + "\n")
open(os.path.join(d, OUT), "w").write(user)
print(len(user.split()), "words")
