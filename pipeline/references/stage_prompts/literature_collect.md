# Stage 4 — LITERATURE_COLLECT

## Purpose
Gather ≥30 candidate papers from real bibliographic sources.

## Strong preference: real APIs over LLM

The LLM is the **worst** source for real bibliographic data — it hallucinates titles, authors, DOIs, and years. **Always prefer the real APIs.** Use the LLM template at the bottom of this file only as a last resort when no API access is available.

### Recommended API order

1. **OpenAlex** (best metadata, free, no auth).
   ```
   GET https://api.openalex.org/works?search=<query>&per_page=25&filter=publication_year:>=2018
   ```
   Returns `id` (OpenAlex ID), `title`, `abstract_inverted_index`, `publication_year`, `authorships`, `doi`, `cited_by_count`, `concepts`.

2. **Semantic Scholar** (good for AI/ML, has TLDRs, free with API key).
   ```
   GET https://api.semanticscholar.org/graph/v1/paper/search
       ?query=<query>&limit=25
       &fields=title,abstract,year,authors,externalIds,citationCount,tldr
   ```

3. **arXiv** (for very-recent preprints).
   ```
   GET http://export.arxiv.org/api/query
       ?search_query=all:<query>&max_results=25&sortBy=relevance
   ```

For each paper retrieved, build a record with these fields (the literature_screen stage requires them):

```json
{
  "id": "<source>:<source_id>",
  "title": "...",
  "source": "openalex|semanticscholar|arxiv",
  "url": "https://...",
  "year": 2023,
  "abstract": "...",
  "authors": ["...", "..."],
  "doi": "10.xxxx/...",
  "arxiv_id": "2301.xxxxx",
  "cite_key": "lastname2023shortword",   // generate now; will be reused all the way to the .bib file
  "citation_count": 142,
  "collected_at": "<ISO timestamp>"
}
```

**Generate `cite_key` here, once.** Format: `<first_author_lastname><year><first_significant_word_of_title_lowercase>`. From this point on, the `cite_key` is treated as immutable through stages 5, 6, 17, 22, 23.

## LLM-fallback prompt (only if APIs unreachable)

**System:**
```
You are a literature mining assistant.
```

**User:**
```
Generate candidate papers from the search plan.

Return JSON: {candidates: [...]} with >=30 rows.

Each candidate must include id, title, source, url, year, abstract, collected_at.

Topic: {topic}

Search plan:

{plan_text}
```

⚠️ The LLM-generated entries will need manual verification at stage 5 — many will be hallucinated. Mark each LLM-sourced row with `"source": "llm_fallback"` and audit it.

## Output

`docs/03_candidates.jsonl` — one JSON object per line, ≥30 rows.

If after running the search plan you have <30 candidates, loop back to stage 3 and broaden the queries before continuing. Don't proceed with thin literature.
