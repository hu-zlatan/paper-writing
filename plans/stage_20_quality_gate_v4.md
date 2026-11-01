# Stage 20 QUALITY_GATE [v4] — plan (run 10)

- Template `pipeline/references/stage_prompts/quality_gate.md` verbatim (json mode), threshold 7.5 (RESTRICTS), {revised} = `paper/mypaper/sections/draft_v4.md` after stage-19 pass 2. Fresh opus subagent; prompts `paper/mypaper/prompts/stage20_v4_*`.
- Output `paper/mypaper/20_quality_gate.json` (v3 gate kept in `paper/mypaper/v3/20_quality_gate.json`).
- Decision: pass (score ≥ 7.5, no actions) → auto-approve per owner directive, record evidence. Fail: refine cycles are exhausted (3 of 3), so no loop to 13; paper-level actions may loop to 19 once; otherwise escalate to the owner (OWNER_TODO) as stage 15 v4 pre-committed.
