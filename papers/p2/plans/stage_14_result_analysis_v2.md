# p2 Stage 14 — RESULT_ANALYSIS [v2], run 44 (2026-11-10)

Template `pipeline/references/stage_prompts/result_analysis.md` verbatim (system + user); placeholders filled by
`docs/prompts/build_stage14_v2.py` → `docs/prompts/stage14_v2_{system,user}.txt`:
- `{preamble}`: iteration v2 after the REFINE loop; v2 rows are secondary (09 amendment); compare with the v1
  primary read-out (`results/v1/crc_analysis.json`, `results/v1/h3_analysis.json`, included unaltered).
- `{data_context}`: every v2 analysis JSON unaltered (`a_analysis*.json`, `b_analysis*.json`, `b3_analysis.json`);
  raw grids and the freeze hash file omitted.
- `{context}`: `docs/09_amendment_v2.md`, the B3 plan, hardware, anomalies (0 flagged logs; B3 pilot timing).
Pass 1: fresh opus subagent → `results/14_analysis_v2_pass1.md`. Pass 2: fresh opus subagent with the template's
area-chair prompt verbatim → `results/14_analysis_v2_pass2.md`. Merge → `results/14_analysis_v2.md`; main session
checks every number against the JSON. Red lines: no number outside the JSON files; v1 verdicts not re-decided.
