# Stage 16 — PAPER_OUTLINE

## Purpose
Detailed paper outline with per-section goals and explicit evidence links to results.

## Mode
- LLM: strongest model.
- json_mode: false.
- **max_tokens: 8192.**

## Prompt template

**System:**
```
You are an academic writing planner.
```

**User:**
```
{preamble}


Create a detailed paper outline in markdown.

Include per-section goals and evidence links.

{topic_constraint}{feedback}Analysis:

{analysis}


Decision:

{decision}
```

## Placeholders

- `{preamble}` — short framing, e.g. "Target conference: NeurIPS 2025. Page limit: 9 main pages + unlimited references + unlimited appendix."
- `{topic_constraint}` — the entire HARD TOPIC CONSTRAINT block from `references/topic_constraint_block.md`. **Do not skip this** — it's the on-topic guardrail.
- `{feedback}` — empty for the first pass; populated on revisions with the prior peer-review feedback.
- `{analysis}` — `results/14_analysis.md`.
- `{decision}` — `results/15_decision.md`.

## Hard rules

- Each section in the outline must list:
  - **Goal** — what the section accomplishes for the reader.
  - **Word target** — pulled from `references/hard_constraints.md` §3 length floors.
  - **Evidence links** — explicit references to specific tables/figures from `results/results.json` or knowledge cards from `docs/05_knowledge_cards.json` (use `cite_key`).
- The outline must explicitly include a **Figure 1 plan** (not just "we'll have a figure 1") — what visual elements, what story it tells, what the caption says.
- The outline must include a list of all ablation rows that will appear in Results, mapped to results.json keys.

## Output

`paper/mypaper/sections/00_outline.md`.

## Loop target

Stage 25 (rebuttal) may PIVOT back here when the rebuttal calls for a paper-structural change. In that case, prefix the user prompt with the rebuttal feedback and the current draft.
