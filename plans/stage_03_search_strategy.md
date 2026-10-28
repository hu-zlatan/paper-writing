# Stage 3 · SEARCH_STRATEGY · v1

## Goal
Produce a comprehensive, machine-executable literature search plan (≥3 strategies, ≥8 short queries) and a sources manifest.

## Tasks
- [ ] Fill `stage_prompts/search_strategy.md` with `{topic}` and `{problem_tree}` (docs/01_problem_tree.md); run verbatim (json_mode).
- [ ] Save `docs/02_search_plan.yaml` (valid YAML, parsed by PyYAML) and `docs/02_sources.json`.
- [ ] Cover: core topic, related methods (BED / active perception / RL), benchmarks & simulators, theoretical foundations (submodularity, EIG bounds), applications (dexterous manipulation).
- [ ] Update PROGRESS.md, commit, push.

## Inputs
- docs/01_problem_tree.md

## Expected outputs
- docs/02_search_plan.yaml, docs/02_sources.json

## Hard-constraint checks
- [ ] ≥3 strategies, each 3–5 queries of 3–6 words; ≥8 queries total (checked by script).
- [ ] Sources are real public APIs with real URLs (OpenAlex, Semantic Scholar, arXiv).

## Notes / risks
Execution happens in stage 4 through a GitHub Actions workflow because the sandbox shell cannot reach the bibliographic APIs.

---

## Output Summary  (filled in AFTER the stage runs)
- 5 strategies, 22 queries (all 3–6 words, verified by a PyYAML check) + 4 seminal queries collected without the year filter. Sources: OpenAlex (primary), arXiv (recent preprints), Semantic Scholar (cross-check), WebSearch (spot checks).
- **Decision:** PROCEED → stage 4 (executed through GitHub Actions).
