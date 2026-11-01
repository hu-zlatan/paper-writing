# Stage 19 PAPER_REVISION [v4] — plan (run 10, 2026-11-01)

- Snapshot: `paper/mypaper/v4/draft_v4_stage17.md`.
- Template `pipeline/references/stage_prompts/paper_revision.md` verbatim, fresh opus subagent; {topic_constraint}
  (v4 block), {draft} (draft_v4.md), {reviews} = `18_peer_review.md` + both full reviews + a binding instruction/data
  block (M1–M9 fixes; `14_travel_split.json`; PENDING markers for the S2 Cal′ verify, the val3 pipeline check and the
  random anchor). Prompts `paper/mypaper/prompts/stage19_v4_*.txt`.
- Checks: per-section word counts (never shorter than the stage-17 draft per section; limitations not softened), number
  audit, cite keys, PENDING list. If > 30 % words added or major restructuring → second stage-18 pass.
- After the diagnostics finish: fill PENDING markers from JSON (code-produced), re-audit.
