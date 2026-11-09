# p2 Stage 16 PAPER_OUTLINE [v1] — plan (run 43, 2026-11-09)

- Pre-step: `code/tools_results_v1.py` collects every v1 analysis JSON unchanged into `results/v1/results_v1.json`
  (the evidence index the template calls results.json; grid dumps and the freeze are referenced, not inlined).
- Template `pipeline/references/stage_prompts/paper_outline.md` verbatim; fresh-context subagent (strongest model).
  Prompt files built by `paper/mypaper/prompts/build_stage16.py` → `stage16_{system,user}.txt`.
- {preamble}: RSS 2027 Stage 1 extended abstract (≤ 5 content pages + 1 page refs); re-scoped story of
  `results/15_decision.md` is binding (claim = friction-onset probe + conformal calibration; learned model adds no
  demonstrated gain; H1-M failed; H3 inconclusive; H2-R scope limit in abstract-level claims). Word targets scaled to
  5 pages (≈ 3,000–3,500 words), a stated deviation from the 9-page floors; master draft may be longer, condensed at 22.
  Evidence links must name `results/v1/results_v1.json` blocks / keys; cite_keys from `docs/05_knowledge_cards.json`
  (list of the 52 keys + titles appended to the preamble).
- {topic_constraint}: block verbatim with the re-scoped topic. {feedback}: empty (first pass).
- {analysis}: `results/14_analysis.md`; {decision}: `results/15_decision.md`.
- Output: `paper/mypaper/sections/00_outline.md`. Self-check vs `hard_constraints.md`: every number traceable,
  no claim disallowed by 15_decision, Figure 1 plan present, ablation-row map with JSON keys.
