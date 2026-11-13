# Stage 17 PAPER_DRAFT [v6] — plan (run 50, 2026-11-13)

## Goal
Markdown master draft of the v6 measurement paper (narrow H6b frontier claim) from `paper/mypaper/sections/00_outline.md`;
every number traceable to `results/v6/14_v6_analysis.json`, `results/v6/15_derived_v6.json` (post hoc) or
`results/v5/results_v5.json`.

## Length decision (same as v3–v5)
Master draft meets the RESTRICTS floors (≥ 4,000 words); the 5-page Stage 1 abstract is condensed in stage 22 using the
outline's word targets (≈ 3,350 body).

## Execution
- Fresh-context opus subagent; template `paper_draft.md` verbatim (system + user extracted by
  `paper/mypaper/prompts/build_stage17_v6.py` → `stage17_v6_{system,user}.txt`). Placeholders: preamble (venue, length,
  measurement framing + §4.5 never-write list, NEED / CITE-MISSING handling, v5 final draft appended as wording source),
  topic block (= stage 16 v6), metrics (v6 read-out, v6 derived, v5 JSON in full), citations (60 keys), outline.
- Output: `paper/mypaper/sections/draft_v6.md`; Figure 1 prompt inside the draft (fenced block).

## Checks (main session)
- Number audit (`code/tools_number_audit.py`, design doc = amendment v6.0 only) → 0 unmatched.
- Every \cite key exists in `docs/05_knowledge_cards.json`.
- Word counts vs RESTRICTS floors.
- No `15_decision.md` §4.5 disallowed claim (grep for match / equivalent / dominate / within a few / negligible / p = 0).
