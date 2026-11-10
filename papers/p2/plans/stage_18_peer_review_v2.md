# p2 Stage 18 PEER_REVIEW [v2] — plan (run 44, 2026-11-10)

- Template `peer_review.md` verbatim via `paper/mypaper/prompts/build_stage18_v2.py` (v1 builder on draft_v2 +
  results_v2.json in the evidence block) → `stage18_v2_{system,user}.txt`.
- Two independent fresh opus subagents (run 2 framed as an RSS reviewer pair), each free to open repo files and
  recompute numbers from raw replays. Outputs `paper/mypaper/18_review_v2_run{1,2}.md`; merged record
  `paper/mypaper/18_peer_review_v2.md`. CRITICAL FABRICATION → stop and loop; else must-fix list → stage 19.
