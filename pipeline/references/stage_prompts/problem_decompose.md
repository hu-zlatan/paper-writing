# Stage 2 — PROBLEM_DECOMPOSE

## Purpose
Decompose the research problem into ≥4 prioritized sub-questions.

## Mode
- LLM: strongest model.
- json_mode: false.

## Prompt template

**System:**
```
You are a senior research strategist.
```

**User:**
```
Decompose this research problem into at least 4 prioritized sub-questions.

Topic: {topic}

Output markdown with sections: Source, Sub-questions, Priority Ranking, Risks.

Goal context:

{goal_text}
```

## Placeholders

- `{topic}` — same as stage 1.
- `{goal_text}` — full markdown contents of `docs/00_topic_init.md`.

## Output

`docs/01_problem_tree.md`. Verify ≥4 sub-questions and that the Risks section is non-trivial (each risk should have a one-sentence mitigation note).
