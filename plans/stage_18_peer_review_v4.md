# Stage 18 PEER_REVIEW [v4] — plan (run 10, 2026-11-01)

## Goal
Evidence audit of `paper/mypaper/sections/draft_v4.md` with ≥ 2 reviewer perspectives; CRITICAL FABRICATION check.

## Execution (same protocol as v3)
- Template `pipeline/references/stage_prompts/peer_review.md` verbatim (system + user). Placeholders: {topic} (v4
  two-regime topic string from stage 16), {draft} (draft_v4.md), {experiment_evidence} ((a) results_v4.json and
  results_v3.json in full; (b) first 200 lines of the longest v4 run log, cut at 400 chars; (c) grep of statistical
  tests in code/; (d) run-file counts). Prompt files `paper/mypaper/prompts/stage18_v4_*.txt`.
- Two fresh opus subagents ("different temperature seeds"); run 2 asked to review as a demanding RSS/CoRL pair. Both
  may open code/, results/v3/, results/v4/ for spot-checks.
- Output: `paper/mypaper/18_review_v4_run1.md`, `18_review_v4_run2.md`; merged record + triage in
  `paper/mypaper/18_peer_review.md` (v3 record snapshotted to `paper/mypaper/v3/18_peer_review_v3.md`).

## Decision rule
CRITICAL FABRICATION in either run → stop, LOOP MARKER, option (a)/(b) per template. Otherwise → stage 19 with triage.
