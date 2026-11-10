# p2 Stage 18 PEER_REVIEW [v2] — pass 2 plan (run 45, 2026-11-10)

- Why: stage 19 pass 1 grew the file by +33 % (> 30 %) → second review pass before stage 20 (same rule as v1).
- Template `peer_review.md` verbatim via `paper/mypaper/prompts/build_stage18_v2.py _v2_pass2` (same evidence block
  as pass 1, revised `draft_v2.md`) → `stage18_v2_pass2_{system,user}.txt`.
- Two fresh opus subagents (run 2 as an RSS pair), no access to earlier review / gate / stage-14 / 15 files.
  Outputs `paper/mypaper/18_review_v2_pass2_run{1,2}.md`; merged record `paper/mypaper/18_peer_review_v2_pass2.md`.
- CRITICAL FABRICATION → stop and loop; else must-fix list → stage 19 pass 2.
