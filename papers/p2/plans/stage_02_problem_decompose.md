# p2 Stage 2 · PROBLEM_DECOMPOSE — plan (run 37, 2026-11-08)

- Inputs: `docs/00_topic_init.md` (goal_text, verbatim), topic string from `RESTRICTS.yaml`.
- Template: `pipeline/references/stage_prompts/problem_decompose.md`, used verbatim
  (system "You are a senior research strategist."; user "Decompose this research problem into at least 4 prioritized
  sub-questions. Topic: {topic} Output markdown with sections: Source, Sub-questions, Priority Ranking, Risks. Goal
  context: {goal_text}").
- Output: `docs/01_problem_tree.md` (≥ 4 sub-questions; every risk with a one-sentence mitigation).
- Checks (hard_constraints): no results claimed (none exist); literature only as already listed in stage 1 docs.
- Next: stage 3 SEARCH_STRATEGY (re-verify the RSS CFP first, as recorded in stage 1).

## Outputs
- `docs/01_problem_tree.md`: 6 sub-questions (SQ1 F\* measurability, SQ2 split-conformal validity, SQ3 efficiency vs a
  calibrated safety factor, SQ4 tactile value, SQ5 online validity under shift, SQ6 group-conditional coverage);
  priority SQ1 > SQ2 > SQ3 > SQ5 > SQ4 > SQ6; 8 risks each with a mitigation.
