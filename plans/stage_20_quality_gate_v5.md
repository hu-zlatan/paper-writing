# Stage 20 QUALITY_GATE [v5] — plan (run 41, 2026-11-09)

- Template `quality_gate.md` verbatim (threshold 7.5 from RESTRICTS), prompts `paper/mypaper/prompts/stage20_v5_*.txt`,
  {revised} = `paper/mypaper/sections/draft_v5.md` (stage-19 pass 2). Fresh opus subagent, paper only (as v3 / v4).
- Output `paper/mypaper/20_quality_gate.json` (v4 gate kept at `paper/mypaper/v4/20_quality_gate.json`).
- Decision: per template table. Refine cap 4 / 4 is used, so an evidence-level failure cannot loop to stage 13 →
  stop and escalate to the owner (15_decision §4.5 d). A paper-level failure → stage 19 with the required actions.
  Gate is auto-approved only if it passes (AUTOPILOT §1); the reason is logged.
