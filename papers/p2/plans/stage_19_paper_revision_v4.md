# p2 Stage 19 PAPER_REVISION [v4] — plan (run 48, 2026-11-12)
- Template `paper_revision.md` verbatim via `build_stage19_v4.py` (draft_v4 + merged record 18_peer_review_v4.md + both
  runs + binding notes). Fresh opus subagent writes the revised `paper/mypaper/draft_v4.md`; snapshot before →
  `v4/draft_v4_stage18in.md`, after → `v4/draft_v4_stage19pass1.md`.
- Length: the template rule (never shorten) applies; Intro / Related / Setup raised to RESTRICTS floors; page fit is decided in stage 22 on the real PDF.
- Self-check after: `code/tools_number_audit.py` on the draft (0 unmatched decimals target), every changed value checked
  against `results/v4/v4_analysis.json`; then stage 18 pass 2 (two fresh subagents), 19 pass 2, 20.
