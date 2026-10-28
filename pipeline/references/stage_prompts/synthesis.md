# Stage 7 — SYNTHESIS

## Purpose
Cluster the knowledge cards into thematic groups, surface research gaps, and prioritize opportunities.

## Mode
- LLM: strongest model (this is a reasoning-heavy stage).
- json_mode: false.

## Prompt template

**System:**
```
You are a synthesis specialist for literature reviews.
```

**User:**
```
Produce merged synthesis output (topic clusters + research gaps).

Output markdown with sections: Cluster Overview, Cluster 1..N, Gap 1..N, Prioritized Opportunities.

Topic: {topic}

Cards context:

{cards_context}
```

## Placeholders

- `{topic}` — research topic.
- `{cards_context}` — full contents of `docs/05_knowledge_cards.json`. If too long, batch by 30 cards and merge the cluster lists.

## Hard rules

- Each cluster must reference at least 3 `cite_key`s from the cards.
- Each gap must be **falsifiable** — phrased so that an experiment could either confirm or refute that the gap exists. "More research is needed on X" is not a gap; "no prior work has measured X under condition Y" is.
- The Prioritized Opportunities section should rank gaps by (a) feasibility within the project's compute/time budget, (b) novelty likelihood, (c) match with the SMART goal from stage 1.

## Output

`docs/06_synthesis.md`.
