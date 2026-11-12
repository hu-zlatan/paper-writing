# p2 Stage 18 PEER_REVIEW [v4] — plan (run 48, 2026-11-12)
- Template `pipeline/references/stage_prompts/peer_review.md` verbatim via `paper/mypaper/prompts/build_stage18_v4.py`
  (v1 builder on `draft_v4.md` + `results/v4/v4_analysis.json` + `results/v3/a7_integrated.json` in the evidence block).
- Two fresh opus subagents, given only the two prompt files and the repo path (no main-session reasoning); run 2 reads
  as an RSS program-committee pair. Both may recompute from raw files; neither edits the repo except its own output.
- Outputs `paper/mypaper/18_review_v4_run1.md`, `18_review_v4_run2.md`; merged record `18_peer_review_v4.md`.
- Red lines: CRITICAL FABRICATION → stop and roll back; code-level findings are fixed in code and re-run before text.
- Then stage 19 [v4] (template `paper_revision.md` verbatim), second 18/19 pass, stage 20.
