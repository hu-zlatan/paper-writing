# Stage 21 — KNOWLEDGE_ARCHIVE

## Purpose
Reproducibility-focused retrospective. This is the artifact you (or future contributors) will read in six months when asked "what did we actually do?".

## Mode
- LLM: strongest or mid-tier (this is summarization-heavy).
- json_mode: false.

## Prompt template

**System:**
```
You produce reproducibility-focused research retrospectives.
```

**User:**
```
{preamble}


Write retrospective archive markdown with lessons, reproducibility notes, and future work.

Decision:

{decision}


Analysis:

{analysis}


Revised paper:

{revised}
```

## Placeholders

- `{preamble}` — short framing, e.g. "Project: <name>. Final version: v<N>. Total elapsed: <hours>."
- `{decision}` — `results/15_decision.md` (most recent).
- `{analysis}` — `results/14_analysis.md` (most recent).
- `{revised}` — final revised paper markdown.

## Recommended sections in the output

- Executive summary (3 sentences).
- What worked.
- What didn't (and why).
- Loop log — a table of every REFINE/PIVOT with the reason.
- Reproducibility notes:
  - Final hyperparameters per condition.
  - Random seeds used.
  - Hardware spec.
  - Total wall-clock time.
  - Pinned package versions (from `code/requirements.txt`).
  - Where each artifact lives (results.json path, figures/, sections/).
- Lessons for future projects.
- Open questions / future work.

## Output

`docs/21_retrospective.md`.
