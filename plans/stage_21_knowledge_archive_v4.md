# Stage 21 KNOWLEDGE_ARCHIVE [v4] — plan (run 11, 2026-11-01)

Context: stage 20 v4 FAILED (5.0 < 7.5) and was escalated to the owner (OWNER_TODO, run 10). No owner answer yet
(no open issues, AUTOPILOT §1 unchanged, RESTRICTS max_refine_cycles still 3). Default per OWNER_TODO: low-risk work
only. Stage 21 is a retrospective that changes no claim, no number and no paper text, so it is allowed.

Steps
1. Fill the template `pipeline/references/stage_prompts/knowledge_archive.md` verbatim:
   {preamble} = project / final version v4 / elapsed calendar time / gate status (not DONE) + loop log facts copied
   from PROGRESS.md LOOP MARKERs; {decision} = `results/v4/15_decision.md`; {analysis} = `results/v4/14_analysis.md`;
   {revised} = `paper/mypaper/sections/draft_v4.md`. Saved in `docs/prompts/stage21_v4_{system,user}.txt`.
2. Run it in a fresh subagent (summarisation; the template allows strongest or mid-tier). Reproducibility facts
   (seeds, hyper-parameters, package pins, artefact paths) may only be copied from the named repo files with paths;
   nothing invented.
3. Verify: every number in `docs/21_retrospective.md` must appear in the inputs or in a cited repo file; paths exist.
4. Mark that the paper is NOT done (gate failed, owner decision pending). Update PROGRESS, commit, push.

Red lines checked (hard_constraints.md): no new numbers, no altered results, no citation changes, no paper edits.
