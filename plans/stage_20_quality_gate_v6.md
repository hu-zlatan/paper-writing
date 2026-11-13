# Stage 20 QUALITY_GATE [v6] — plan (run 50, 2026-11-13)

- Template `quality_gate.md` verbatim (threshold 7.5, `RESTRICTS.yaml`); prompt files
  `paper/mypaper/prompts/stage20_v6_{system,user}.txt` ({revised} = `sections/draft_v6.md` after stage 19 pass 2).
- Fresh opus subagent, paper only (no repository access beyond the prompt files) → `paper/mypaper/20_quality_gate.json`
  (v5 gate already at `paper/mypaper/v5/20_quality_gate.json`).
- Decision per the template table. Auto-approval (AUTOPILOT §1) only if score ≥ 7.5; a below-threshold score is not
  evidence for approval. Refine cap 5 / 5 used: an evidence-level FAIL cannot loop to stage 13 → owner decision
  (Stage 2 / CoRL 2027 / RA-L / workshop), per the 11-10 directive's fallback.
