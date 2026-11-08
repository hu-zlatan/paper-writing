# p2 Stage 3 · SEARCH_STRATEGY — plan (run 37, 2026-11-08)

- Inputs: topic (`RESTRICTS.yaml`), `docs/01_problem_tree.md`. Template `stage_prompts/search_strategy.md` verbatim
  (json_mode: search_plan_yaml + sources).
- Pre-step from stage 1: re-verify the RSS 2027 CFP.
- Outputs: `docs/02_search_plan.yaml` (≥ 3 strategies, ≥ 8 queries of 3–6 words), `docs/02_sources.json`.
- Collection route (stage 4): `.github/workflows/literature.yml` gains a `docs_dir` dispatch input (default `docs`,
  paper 1 unchanged) so `code/literature/collect.py` (shared, unchanged) writes `papers/p2/docs/03_candidates.jsonl`.

## Outputs
- 5 strategies, 22 queries + 4 seminal queries; 4 sources.
- RSS CFP re-check: the fetch of roboticsconference.org/information/cfp/ failed this run (fetch permission timed out;
  no content); WebSearch returned no newer page. Last successful verification stays 2026-11-06 (paper 1). Retry in stage 4/5.
