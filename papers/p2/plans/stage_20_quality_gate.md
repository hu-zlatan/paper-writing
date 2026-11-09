# p2 Stage 20 QUALITY_GATE [v1] — plan (run 43, 2026-11-09)

- Template `quality_gate.md` verbatim (threshold 7.5 from RESTRICTS), prompts `paper/mypaper/prompts/stage20_*.txt`
  (`build_stage20.py`), {revised} = `paper/mypaper/draft_v1.md` after stage-19 pass 2. Fresh opus subagent, paper only.
- Output `paper/mypaper/20_quality_gate.json`.
- Decision per template table. p2 refine cycles used 0 / 3, so an evidence-level failure loops to stage 13 (v2 with a
  frozen amendment written before any new run); a paper-level failure → stage 19. Auto-approved only if it passes
  (AUTOPILOT §1), with the reason logged.
