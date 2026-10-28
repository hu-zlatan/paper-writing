# Stage 3 — SEARCH_STRATEGY

## Purpose
Design a comprehensive literature retrieval strategy. A real top-tier paper cites 30–60 references — the strategy must produce enough diverse queries to find them.

## Mode
- LLM: mid-tier or strongest.
- **json_mode: true.**

## Prompt template

**System:**
```
You design literature retrieval strategies and source verification plans. You aim for COMPREHENSIVE coverage — a good research paper needs 30-60 references.
```

**User:**
```
Create a merged search strategy package.

Return a JSON object with keys: search_plan_yaml, sources.

search_plan_yaml must be valid YAML text with search_strategies containing at least 3 strategies,
each with 3-5 diverse keyword queries (short, 3-6 words each). Generate at least 8 total queries.
Cover: core topic, related methods, benchmarks/datasets, theoretical foundations, applications.

sources must include id, name, type, url, status, query, verified_at.

Topic: {topic}

Problem tree:

{problem_tree}
```

## Placeholders

- `{topic}` — research topic.
- `{problem_tree}` — full markdown contents of `docs/01_problem_tree.md`.

## Output

Parse the returned JSON. Save:
- `docs/02_search_plan.yaml` (the `search_plan_yaml` value).
- `docs/02_sources.json` (the `sources` array).

Verify ≥3 strategies and ≥8 total queries before moving on.
