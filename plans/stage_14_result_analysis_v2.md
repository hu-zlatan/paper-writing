# Stage 14 RESULT_ANALYSIS [v2] — plan (run 4, 2026-10-28)

- Input: the complete v2 pre-run gate record — results/v2/12_{g1,g2,g3,g4,g4_fallback,g4_b5,b8,gridcheck,calib,g5}_analysis.json,
  12_g3_hp_selection.txt, 12_g3_notch_analysis.json, the exploratory diagnostics 12_diag_analysis.json (labelled
  exploratory), docs/07_hypotheses_v2.md (§3 hypotheses, §4 gate rules), docs/07c_amendment_v2_0.md.
- Pass 1: fresh-context opus subagent, prompt of pipeline/references/stage_prompts/result_analysis.md verbatim
  (system: "You are a quantitative ML analyst. Always cite exact numbers from the provided data."), preamble = "v2
  after a PIVOT; no main run, gate record only".
- Pass 2: separate fresh opus subagent with the area-chair adversarial prompt from the same template; merge.
- Output: results/v2/14_analysis.md. Statistical checks may only cite tests implemented in code (bootstrap CIs in
  code/analysis_*.py and touchbed/stats.py).
