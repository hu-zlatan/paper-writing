# Stage 18 PEER_REVIEW [v5] — plan (run 41, 2026-11-09)

## Goal
Evidence audit of `paper/mypaper/sections/draft_v5.md` with ≥ 2 reviewer perspectives; CRITICAL FABRICATION check.

## Execution (same protocol as v3 / v4)
- Template `peer_review.md` verbatim (builder `paper/mypaper/prompts/build_stage18_v5.py` → `stage18_v5_*.txt`):
  {topic} = stage-16 v5 topic; {draft} = draft_v5.md; {experiment_evidence} = (a) v5 / v4 / v3 results JSONs in full,
  (b) first 200 lines of the longest v5 test5 log, (c) grep of statistical tests in the v5 scripts + stats.py,
  (d) amendments of record + file counts.
- Two fresh opus subagents; run 2 reviews as a demanding RSS / CoRL pair. Both may open code/, docs/, results/.
- Output: `paper/mypaper/18_review_v5_run1.md`, `18_review_v5_run2.md`; merged record + triage in
  `paper/mypaper/18_peer_review.md` (v4 record already at `paper/mypaper/v4/18_peer_review.md`).

## Decision rule
CRITICAL FABRICATION in either run → stop, LOOP MARKER, per template. Otherwise → stage 19 with the triage.
