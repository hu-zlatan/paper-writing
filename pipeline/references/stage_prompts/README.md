# Stage Prompts — Index

Each file in this directory contains the exact `system:` + `user:` prompt block to send to an LLM for that stage, along with usage notes (model tier, temperature, JSON mode, max_tokens).

**Read the file for the stage you are running. Do not paraphrase the prompt — the templates are tuned.**

| Stage | File | LLM mode | Group |
|---|---|---|---|
| 1 | `topic_init.md` | text | A |
| 2 | `problem_decompose.md` | text | A |
| 3 | `search_strategy.md` | json_mode | B |
| 4 | `literature_collect.md` | json_mode (fallback only — prefer real APIs) | B |
| 5 | `literature_screen.md` | json_mode | B |
| 6 | `knowledge_extract.md` | json_mode | B |
| 7 | `synthesis.md` | text | C |
| 8 | `hypothesis_gen.md` | text (run 2–3× for debate) | C |
| 8.5 | `theoretical_bounds.md` | text | C |
| 9 | `experiment_design.md` | text (YAML output) | D |
| 10 | `code_generation.md` | text (max_tokens 8192) | D |
| 11 | `resource_planning.md` | json_mode | D |
| 13 | `iterative_refine.md` | text (max_tokens 8192) — covers `iterative_improve` + `iterative_repair` + `code_repair` | E |
| 14 | `result_analysis.md` | text (fresh context) | F |
| 15 | `research_decision.md` | text | F |
| 16 | `paper_outline.md` | text (max_tokens 8192) | G |
| 17 | `paper_draft.md` | text (max_tokens 32768) | G |
| 18 | `peer_review.md` | text (max_tokens 8192) | G |
| 19 | `paper_revision.md` | text (max_tokens 32768) | G |
| 20 | `quality_gate.md` | json_mode | H |
| 21 | `knowledge_archive.md` | text | H |
| 22 | `export_publish.md` | text (max_tokens 16384) | H |
| 23 | `citation_verify.md` | text (manual + scripted) | H |
| 24 | `third_party_review.md` | text (fresh context, harshest reviewer persona) | I |
| 25 | `rebuttal.md` | text | I |

## Placeholder convention

The templates use `{placeholder}` for variables you must fill in. Common ones:

- `{topic}` — the research topic string from stage 1.
- `{topic_constraint}` — the block from `references/topic_constraint_block.md`.
- `{preamble}` — any project-specific preamble (e.g. "this is iteration v3 of a paper on X").
- `{outline}` / `{draft}` / `{revised}` — markdown bodies passed between stages.
- `{exp_plan}` — the YAML from stage 9.
- `{results.json content}` / `{run_summaries}` — execution evidence.
- `{quality_threshold}` — typically 7.5 for top-tier conferences.

When you encounter a placeholder, fill it before sending the prompt. Do not send placeholders verbatim — the LLM will produce nonsense.
