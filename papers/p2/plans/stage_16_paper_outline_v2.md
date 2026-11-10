# p2 Stage 16 PAPER_OUTLINE [v2] — plan (run 44, 2026-11-10)

- Pre-step: `code/tools_results_v2.py` → `results/v2/results_v2.json` (v2 analysis JSONs unchanged);
  `tools_number_audit.py` now also reads it (v1 audit results unchanged: draft_v1 still 3 design-margin tokens "1.10").
- Template `paper_outline.md` verbatim; prompt built by `paper/mypaper/prompts/build_stage16_v2.py`:
  preamble / topic block as v1 + v2 note; {feedback} = v1 stage-20 gate JSON + the v1 outline to revise;
  {analysis} = `results/14_analysis_v2.md` + v1 merged analysis; {decision} = `results/15_decision_v2.md`.
- Fresh opus subagent → `paper/mypaper/sections/00_outline_v2.md`. Self-check: number audit 0 unmatched (design
  margins excepted), every v2 row labelled secondary, statements of record 1–6 respected, Figure 1 plan present.
