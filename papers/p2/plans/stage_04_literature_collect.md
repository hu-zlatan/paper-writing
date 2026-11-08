# p2 Stage 4 · LITERATURE_COLLECT — plan (run 37, 2026-11-08)

- Route: real APIs only (OpenAlex → arXiv → Semantic Scholar) via `.github/workflows/literature.yml` with
  `docs_dir: papers/p2/docs`; shared stdlib collector `code/literature/collect.py` (unchanged; same normalisation,
  dedupe and cite_key rules as paper 1).
- Output: `papers/p2/docs/03_candidates.jsonl` (target ≥ 30 with id, title, source, url, year, abstract,
  collected_at) + `03_collect_log.json` (per-query hits / errors).
- Check: count, field completeness, every record has a DOI / arXiv ID / OpenAlex ID; the 9 stage-1 seed IDs present
  (if not, add them through the API in a supplement, never by hand).
- Template `stage_prompts/literature_collect.md` is NOT used: it is only for when API access is unavailable.
