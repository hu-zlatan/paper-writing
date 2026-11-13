# Stage 15 RESEARCH_DECISION [v6] — plan (run 50, 2026-11-13)

- Template `pipeline/references/stage_prompts/research_decision.md` with its REFINE augmentation, verbatim
  (`results/v6/prompts/stage15_{system,user}.txt`); {analysis} = merged `results/v6/14_analysis.md`.
- Fresh opus subagent; it may read the template's hard rules, `RESTRICTS.yaml` (loops), `results/v5/15_decision.md`,
  `AUTOPILOT.md` §1 (owner directives) and `OWNER_TODO.md`. Output `results/v6/15_decision.md`.
- Constraint known in advance: `max_refine_cycles` 5 / 5 used (v6 is the 5th); REFINE / PIVOT can only go to the owner.
  Owner's v6 directive: target RSS 2027 Stage 1 (12-04 AoE); if stage 20 is not passed by 12-01, switch to Stage 2 /
  CoRL 2027.
- Then stage 16 [v6] if PROCEED.
