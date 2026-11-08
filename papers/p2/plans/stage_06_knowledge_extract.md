# p2 Stage 6 · KNOWLEDGE_EXTRACT — plan (run 37, 2026-11-08)

- Template `stage_prompts/knowledge_extract.md` verbatim (mid-tier model: a fresh Sonnet subagent, abstracts only).
- Output `docs/05_knowledge_cards.json` via `code/literature/build_cards_v1.py` (titles / cite_keys / citations built in
  code; content fields hand-written from each abstract; "not stated in abstract" and "(inferred)" markers).
- Checks: every shortlist cite_key has exactly one card; every number in findings / data / metrics appears in that
  record's abstract or title (automatic check by the orchestrating session).

## Outputs
- 52 cards; 0 numbers absent from the source abstracts; 2 thin records (Vovk 2005 book without abstract; Lindemann
  2025 abstract is an introduction only).
