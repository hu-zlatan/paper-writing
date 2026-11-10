# p2 Stage 16 PAPER_OUTLINE [v3] — plan (run 46, 2026-11-10)
- Pre-step: `code/tools_results_v3.py` → `results/v3/results_v3.json`; `tools_number_audit.py` now also reads it.
- Template `paper_outline.md` verbatim; prompt built by `paper/mypaper/prompts/build_stage16_v3.py`: preamble / topic
  block as v1 + v3 note; {feedback} = v2 stage-20 gate + v2 stage-18 pass-2 record + the v2 outline to revise;
  {analysis} = `results/14_analysis_v3.md` (binding) + v3 pass 1 / pass 2 + v2 merged analysis; {decision} =
  `results/15_decision_v3.md`. Note for the subagent: A7 integrated force / break-even now exist in
  `a7_integrated.json` (pass 1 said they did not).
- Fresh opus subagent → `paper/mypaper/sections/00_outline_v3.md`. Self-check: number audit, v3 rows labelled
  secondary, statements of record 1–7 respected, Figure 1 plan present.
