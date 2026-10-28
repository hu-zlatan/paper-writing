# Stage 20 — QUALITY_GATE  [GATE]

## Purpose
Final quality threshold check. If the paper scores below threshold, loop back to stage 19 (or stage 13 if the issue is experimental).

## Mode
- LLM: strongest model.
- **json_mode: true.**
- This is a **GATE**.

## Prompt template

**System:**
```
You are a final quality gate evaluator.
```

**User:**
```
Evaluate revised paper quality and return JSON.

Schema: {score_1_to_10:number, verdict:string, strengths:[...], weaknesses:[...], required_actions:[...]}.

Threshold: {quality_threshold}

Paper:

{revised}
```

## Placeholders

- `{quality_threshold}` — typically `7.5` for top-tier conferences.
- `{revised}` — full revised paper markdown from stage 19.

## Decision logic

After parsing the JSON:

| `score_1_to_10` | Action |
|---|---|
| ≥ threshold and 0 `required_actions` | PROCEED to stage 21. |
| ≥ threshold but `required_actions` non-empty | Apply the actions, loop back to stage 19, then re-run stage 20. |
| < threshold, weaknesses are paper-level (writing, framing, missing analysis) | Loop back to stage 19 with the weaknesses appended to the reviews. |
| < threshold, weaknesses are evidence-level (weak baselines, missing ablations, fabrication) | Loop back to **stage 13** — the underlying experiments are insufficient. |
| Three failed cycles at stage 20 | Escalate to the user; the project may need a major PIVOT (back to stage 8). |

## Output

`paper/mypaper/20_quality_gate.json`.
