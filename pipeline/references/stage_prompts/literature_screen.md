# Stage 5 — LITERATURE_SCREEN  [GATE]

## Purpose
Strict relevance + quality screening. Reject off-topic papers aggressively, even if they're individually high-quality.

## Mode
- LLM: mid-tier or strongest.
- **json_mode: true.**
- This is a **GATE** — pause for human review or use `--auto-approve`.

## Prompt template

**System:**
```
You are a strict domain-aware reviewer. Reject off-topic papers aggressively.
```

**User:**
```
Perform merged relevance+quality screening and return shortlist.

Return JSON: {shortlist: [...]} each with title, cite_key (if present), relevance_score (0-1), quality_score (0-1), keep_reason.

Preserve all original fields (paper_id, doi, arxiv_id, cite_key, etc.) from the input.

Topic: {topic}

Domains: {domains}

Threshold: {quality_threshold}

IMPORTANT: Only keep papers genuinely relevant to the topic above. Reject papers about unrelated domains even if they
are high quality.

Candidates JSONL:

{candidates_text}
```

## Placeholders

- `{topic}` — research topic.
- `{domains}` — comma-separated list of in-scope domains.
- `{quality_threshold}` — e.g. `0.6` (combined relevance × quality min).
- `{candidates_text}` — the entire JSONL contents from stage 4.

## Hard rules for output

- Every output entry **must preserve** the original `cite_key`, `doi`, `arxiv_id`, `paper_id` fields exactly. If the LLM strips or renames these, reject the output and re-prompt.
- Aim for **≥30 entries** in the shortlist. If fewer, loop back to stage 3 (broader queries) — do not proceed with a thin shortlist.
- Year filter: drop anything older than the project's cutoff (typically 2018 for ML; configurable in `RESTRICTS.yaml`).

## Gate

Before continuing to stage 6, present the shortlist to the user (count + 5-line summary). They can:
- **Approve** → continue.
- **Reject specific entries** → remove and continue (but check count is still ≥30).
- **Reject the whole shortlist** → loop back to stage 3 with feedback on what's missing.

## Output

`docs/04_shortlist.jsonl`.
