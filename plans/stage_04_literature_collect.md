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
- Actions run 40654783282 (2026-10-28, ~47 min): 800 raw records → 681 unique candidates. OpenAlex answered all 26 queries; arXiv returned HTTP 429 for all queries and Semantic Scholar for 20/26 (shared runner IPs are rate-limited). arXiv preprints are still covered through OpenAlex's arXiv index (many candidates carry arXiv DOIs 10.48550/arXiv.*).
- Fix pushed after the first run: 40-min query budget + skip a source after 3 consecutive failures, so partial results are always written; the workflow now re-collects only when docs/02_search_plan.yaml changes (keeps cite_keys stable).
- Known gaps to add by targeted lookup (stage 6/23): Golovin & Krause adaptive submodularity (JAIR 2011, seminal); ICRA 2013 version of Javdani et al.
- **Decision:** PROCEED → stage 5 (681 ≥ 30).
