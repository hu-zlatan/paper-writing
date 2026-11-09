# Stage 17 PAPER_DRAFT [v5] — plan (run 41, 2026-11-09)

## Goal
Markdown master draft of the v5 five-cell measurement paper from `paper/mypaper/sections/00_outline.md`; every number
traceable to `results/v5/results_v5.json` (or v4 / v3 results for PRIOR cells).

## Preconditions (stage 16 v5 open items)
- [x] rl_success episode counts + last-checkpoint sensitivity rows → `results/v5/16_report_rows.json` (in results_v5.json).
- [x] m8 erratum ruled on (outline §0.3; PROGRESS run 41).
- [x] Citations: same 60 cards as the v3/v4 stage-17 prompts; outline's 3 [CITE-MISSING] stay as markers.

## Length decision (same as v3 / v4)
Master draft meets the RESTRICTS floors (≥ 4,000 words); the 5-page Stage 1 abstract is condensed in stage 22 using the
outline's word targets (3,430 body).

## Execution
- Fresh-context opus subagent; template `paper_draft.md` verbatim (system + user, extracted by
  `paper/mypaper/prompts/build_stage17_v5.py` → `stage17_v5_{system,user}.txt`). Placeholders: preamble (venue,
  length, measurement framing, NEED / CITE-MISSING handling, v4 final draft appended as wording source),
  topic block (= stage 16 v5), metrics (v5 / v4 / v3 JSONs in full), citations (60 keys), outline.
- Output: `paper/mypaper/sections/draft_v5.md`; Figure 1 prompt → `paper/mypaper/figures/figure1_prompt.txt`.

## Checks (main session)
- [ ] Number audit (`code/tools_number_audit.py`) against the JSONs.
- [ ] Every \cite key exists in the cards.
- [ ] Word counts vs RESTRICTS floors.
- [ ] Outline never-write list (15_decision §4.4) respected.
