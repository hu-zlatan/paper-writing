# p2 Stage 17 PAPER_DRAFT [v1] — plan (run 43, 2026-11-09)

- Template `paper_draft.md` verbatim (system + user extracted by `paper/mypaper/prompts/build_stage17.py` →
  `stage17_{system,user}.txt`); fresh opus subagent.
- {preamble}: RSS 2027 master draft (Stage 1 condensed at stage 22); binding floors from RESTRICTS (≥ 4,000 words);
  binding re-scoped story; method details only from the frozen design docs (07, 08a–08h); [NEED: …] marker rule.
- {exp_metrics_instruction}: `results/v1/results_v1.json` pasted in full. {citation_instruction}: the 52 cards.
- {outline}: `paper/mypaper/sections/00_outline.md`.
- Outputs: `paper/mypaper/draft_v1.md`, `paper/mypaper/figures/figure1_prompt.txt`.
- Checks: `code/tools_number_audit.py` (0 unmatched or each explained), cite keys ⊂ cards, section word floors,
  red lines of hard_constraints.md (no claim beyond 15_decision).
