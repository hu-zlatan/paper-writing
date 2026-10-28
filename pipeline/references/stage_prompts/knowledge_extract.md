# Stage 6 — KNOWLEDGE_EXTRACT

## Purpose
Convert the shortlist into structured knowledge cards — high-signal evidence digests of each kept paper.

## Mode
- LLM: mid-tier (this is a structured extraction task, not creative).
- **json_mode: true.**

## Prompt template

**System:**
```
You extract high-signal evidence cards from papers.
```

**User:**
```
Extract structured knowledge cards from shortlist.

Return JSON: {cards:[{card_id, title, cite_key, problem, method, data, metrics, findings, limitations, citation}]}.

IMPORTANT: If the input contains cite_key fields, preserve them exactly in the output.

Shortlist:

{shortlist}
```

## Placeholders

- `{shortlist}` — entire contents of `docs/04_shortlist.jsonl`.

## Hard rules

- **`cite_key` MUST be preserved verbatim** from the shortlist. The synthesis (stage 7) and paper draft (stage 17) reference these keys; mutating them breaks the chain.
- `findings` should be **quantitative** when the paper reports numbers — pull the actual metrics, not vague summaries.
- `limitations` is the most useful field for the gap analysis in stage 7 — push the LLM to extract real, specific limitations from each paper, not generic ones.

## Output

`docs/05_knowledge_cards.json`.

Sanity-check: every card's `cite_key` must appear in `docs/04_shortlist.jsonl`. If any are different, the LLM hallucinated — re-run with a smaller batch.
