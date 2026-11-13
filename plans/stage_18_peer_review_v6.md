# Stage 18 PEER_REVIEW [v6] — plan (run 50, 2026-11-13)

## Goal
Evidence audit of `paper/mypaper/sections/draft_v6.md` with ≥ 2 reviewer perspectives; CRITICAL FABRICATION check.

## Execution (same protocol as v3 – v5)
- Template `peer_review.md` verbatim (builder `paper/mypaper/prompts/build_stage18_v6.py` → `stage18_v6_*.txt`):
  {topic} = stage-16 v6 topic; {draft} = draft_v6.md; {experiment_evidence} = (a) v6 read-out, v6 derived and v5 results JSONs in full,
  (b) first 200 lines of the longest v6 test5 log, (c) grep of statistical tests in the v6 script + stats.py,
  (d) amendments of record + file counts.
- Two fresh opus subagents; run 2 reviews as a demanding RSS / CoRL pair. Both may open code/, docs/, results/.
- Output: `paper/mypaper/18_review_v6_run1.md`, `18_review_v6_run2.md`; merged record + triage in
  `paper/mypaper/18_peer_review.md` (v5 record already at `paper/mypaper/v5/18_peer_review.md`).

## Decision rule
CRITICAL FABRICATION in either run → stop, LOOP MARKER, per template. Otherwise → stage 19 with the triage.
