# Stage 15 RESEARCH_DECISION [v2] — plan (run 4)
- Input {analysis}: results/v2/14_analysis.md (full) + exploratory addendum: results/v2/12_diag_analysis.json
  (finger-relative dev head, touchbed/relframe.py; one of three seeds available at decision time).
- Fresh opus subagent, prompt of stage_prompts/research_decision.md with the REFINE augmentation verbatim.
- Constraints given as context only: RSS 2027 extended abstract 2026-12-04 AoE (owner decides on submission), full
  paper 2027-04-16; RESTRICTS loops.max_refine_cycles = 3; CPU-only; v1 → v2 was already one PIVOT.
- Output results/v2/15_decision.md; loop marker in PROGRESS.md; version bump to v3.
