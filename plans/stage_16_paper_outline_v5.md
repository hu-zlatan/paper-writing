# Stage 16 PAPER_OUTLINE [v5] — plan (run 41, 2026-11-09)

- Pre-step (stage-15 §4.1 task 1, report-only): `code/tools_posthoc_v5.py` → `results/v5/15_posthoc_derived.json`
  (student means from diffs, margins vs the best test5 heuristic, latency ratios vs job-2 student medians, H5b span
  translation), collected into `results_v5.json`. Task 2 (OWNER_TODO correction) was done in run 40.
- Template `pipeline/references/stage_prompts/paper_outline.md` verbatim, fresh-context subagent (strongest model);
  prompt files `paper/mypaper/prompts/stage16_v5_system.txt`, `stage16_v5_user.txt` (built by
  `paper/mypaper/prompts/build_stage16_v5.py`).
- {preamble}: RSS 2027 Stage 1 extended abstract (≤ 5 content pages + 1 reference page), measurement paper per
  `results/v5/15_decision.md` §4.2–4.4; 5-page word targets (≈ 3,000–3,500 words body), a stated deviation from the
  9-page floors; evidence keys from `results/v5/results_v5.json` (+ v3 / v4 results as prior cells), cite_keys from
  `docs/05_knowledge_cards.json`.
- {topic_constraint}: block verbatim, topic updated to the five-cell v5 study.
- {feedback}: v4 stage-18 merged review + v4 stage-20 gate JSON (the failing gate that led to v5).
- {analysis}: `results/v5/14_analysis.md`; {decision}: `results/v5/15_decision.md`; plus `15_posthoc_derived.json`.
- Snapshot of the v4 outline: `paper/mypaper/v4/00_outline_v4.md`. Output: `paper/mypaper/sections/00_outline.md`.
- Self-check against `hard_constraints.md` (numbers traceable, no disallowed claim from 15_decision §4.4, Figure 1 plan,
  ablation/row map with JSON keys).
