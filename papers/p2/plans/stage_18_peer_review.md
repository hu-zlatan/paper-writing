# p2 Stage 18 PEER_REVIEW [v1] — plan (run 43, 2026-11-09)

- Template `peer_review.md` verbatim (`paper/mypaper/prompts/build_stage18.py` → `stage18_{system,user}.txt`):
  topic from the stage-16 constraint block; draft `paper/mypaper/draft_v1.md`; evidence = results_v1.json in full,
  first 200 lines of the longest run log, grep of statistical procedures in code/, pointers to the design docs.
- Two independent fresh opus subagents (template recommends two runs for diverse A / B perspectives); run 2 framed as
  an RSS reviewer pair. Each may open repo files to verify; each spot-checks numbers against raw files.
- Outputs `paper/mypaper/18_review_run{1,2}.md`, merged record `paper/mypaper/18_peer_review.md`.
- CRITICAL FABRICATION → stop and loop per template; else must-fix list → stage 19.
