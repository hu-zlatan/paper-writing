# p2 Stage 14 — RESULT_ANALYSIS [v4], run 47 (2026-11-10)

Template `pipeline/references/stage_prompts/result_analysis.md` verbatim (system + user); placeholders filled by
`docs/prompts/build_stage14_v4.py` → `docs/prompts/stage14_v4_{system,user}.txt`:
- `{preamble}`: iteration v4 after the third (last) REFINE loop (v3 gate 6.8); C1–C5 confirmatory (Holm, amendment 11,
  written before any v4 code / run); S1–S7 secondary; v1–v3 verdicts not re-decided.
- `{data_context}`: `results/v4/v4_analysis.json` unaltered (the only v4 read-out; produced by `code/analysis_v4.py`,
  committed before any v4 replay) + `results/v3/a7_integrated.json` for the v3 break-even being replaced by S6.
- `{context}`: `docs/11_amendment_v4.md` (rules + predictions stated before the run), hardware, completeness
  (`--check`: 4,800 replay instances per pool, 0 duplicates), caveats.
Pass 1: fresh opus subagent → `results/14_analysis_v4_pass1.md`. Pass 2: fresh opus subagent with the template's
area-chair prompt verbatim → `results/14_analysis_v4_pass2.md`. Merge → `results/14_analysis_v4.md`; main session
checks key numbers against the JSON. Red lines: no number outside the files; registered decisions taken as the code
printed them (C4 / C5 "inferiority" = CI** below 0, not superiority).
