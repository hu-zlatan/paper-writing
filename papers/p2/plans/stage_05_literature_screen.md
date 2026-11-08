# p2 Stage 5 · LITERATURE_SCREEN [GATE] — plan (run 37, 2026-11-08)

- Template `stage_prompts/literature_screen.md` verbatim (system "You are a strict domain-aware reviewer. Reject
  off-topic papers aggressively."); topic from RESTRICTS; domains: tactile sensing, robotic grasping, conformal
  prediction / UQ, robot learning; threshold relevance ≥ 0.6 & quality ≥ 0.5 (same rule as paper 1).
- Tools: `code/literature/screen_p2.py prefilter` (year/ID/abstract filter + keyword ordering only) → reviewer
  decisions in `code/literature/screen_decisions_v1.py` (titles copied by code) → `screen_p2.py merge` (original fields
  verbatim; KeyError on any unknown cite_key).
- Gate: auto-approve (AUTOPILOT §1) if ≥ 30 entries, all with verifiable IDs; else loop to stage 3.

## Outputs
- 872 → 824 after filter → 52 shortlisted (`docs/04_shortlist.jsonl`), every entry with DOI / arXiv / OpenAlex ID,
  2 seminal pre-2018 exceptions (Vovk 2005, Lei 2017). Gate auto-approved.
