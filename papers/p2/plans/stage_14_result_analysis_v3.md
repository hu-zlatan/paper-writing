# p2 Stage 14 — RESULT_ANALYSIS [v3], run 46 (2026-11-10)

Template `pipeline/references/stage_prompts/result_analysis.md` verbatim (system + user); placeholders filled by
`docs/prompts/build_stage14_v3.py` → `docs/prompts/stage14_v3_{system,user}.txt`:
- `{preamble}`: iteration v3 after the second REFINE loop (v2 gate 5.5); all v3 rows secondary (amendment 10 + 10a,
  written before any v3 code / run); v1 primary verdicts not re-decided; v1 crc / h3 read-outs included unaltered.
- `{data_context}`: every v3 analysis JSON unaltered (a3_holm, a_analysis, a_analysis_08e, b1_analysis(_edge,
  _edge_samegrid), b2_analysis, b3_analysis); raw grids omitted.
- `{context}`: `docs/10_amendment_v3.md`, hardware, anomalies and the caveats recorded in PROGRESS (B3 intervals over
  orderings only; B2 3-object timing pilot; A1 descriptive).
Pass 1: fresh opus subagent → `results/14_analysis_v3_pass1.md`. Pass 2: fresh opus subagent with the template's
area-chair prompt verbatim → `results/14_analysis_v3_pass2.md`. Merge → `results/14_analysis_v3.md`; main session
checks the numbers against the JSON. Red lines: no number outside the JSON files; v1 / v2 verdicts not re-decided.
