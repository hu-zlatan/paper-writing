# Stage 4 · LITERATURE_COLLECT · v1

## Goal
Collect ≥30 (target ≥150 raw) real candidate papers with verifiable IDs from OpenAlex + arXiv (+ Semantic Scholar when not rate-limited) → `docs/03_candidates.jsonl`.

## Tasks
- [ ] Write `code/literature/collect.py` (stdlib only): runs every query in `docs/02_search_plan.yaml`, normalizes records to the stage-4 schema (id, title, source, url, year, abstract, authors, doi, arxiv_id, openalex_id, cite_key, citation_count, venue, query, collected_at), deduplicates by DOI / arXiv ID / normalized title, generates immutable cite_keys.
- [ ] Workflow `.github/workflows/literature.yml` runs it on GitHub Actions (sandbox shell cannot reach the APIs) and commits the JSONL back. If pushing a workflow is rejected → `ci/workflows/` + OWNER_TODO (charter fallback).
- [ ] Inspect output: count, year distribution, per-query hit counts; loop back to stage 3 if < 30.
- [ ] Update PROGRESS.md, commit, push.

## Inputs
- docs/02_search_plan.yaml

## Expected outputs
- docs/03_candidates.jsonl, docs/03_collect_log.json (per-query counts, errors)

## Hard-constraint checks
- [ ] Every record has a real source ID (OpenAlex W-id / DOI / arXiv id); no LLM-fallback rows.
- [ ] cite_key generated once here: `<firstauthorlastname><year><firstsignificantword>`, made unique with a/b suffixes.

## Notes / risks
- Semantic Scholar unauthenticated rate limits (429) → retry with backoff, otherwise skip and log.
- OpenAlex abstracts come as inverted indexes → reconstruct.
