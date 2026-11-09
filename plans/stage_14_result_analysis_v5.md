# Stage 14 RESULT_ANALYSIS [v5] — plan (written run 40, 2026-11-09, before any test5 outcome is read)

**Precondition.** `python code/analysis_test5_v5.py --check` shows every cell complete (300 test5 episodes for every
method) and g_T complete; then `python code/analysis_test5_v5.py` (frozen read-out, written in run 35) →
`results/v5/14_test5_analysis.json`; `python code/tools_results_v5.py` → `results/v5/results_v5.json`.

**Inputs.** `results_v5.json` (D5 validation read-out, freeze record, test5 H5a / H5b / H2-v5 / H* / Holm, E5 sub-16
check, E6 latency, E7, RL sweep selection, calibration); rules `docs/07c_amendment_v5_0.md` + addenda v5.1a–h; the v4
analysis `results/v4/14_analysis.md` for comparison.

**Procedure** (`pipeline/references/stage_prompts/result_analysis.md`, template verbatim):
1. Pass 1 — fresh subagent (strongest model), the template's system / user prompts; {data_context} = unaltered
   `results_v5.json`; {preamble} = v5 is the fourth (owner-authorised, last) refine loop: 5 cells, 5 seeds, fresh
   test5, four heuristics, sub-16 check, latency; compare with v4; {context} = run facts (test5 reduced to 300 by
   addendum v5.1e before any test5 data; random baseline split into small time-guarded jobs; g_T partly on runners
   (v5.1h) with a 2-file determinism check; E6 median-CI rule failing for full G\* in 4 cells; budget overrun logged).
2. Pass 2 — fresh subagent, the template's adversarial area-chair prompt on pass 1.
3. Merge → `results/v5/14_analysis.md` (pass-1 body, supported pass-2 rewrites, merge log). Then stage 15.
Red lines: numbers only from the JSON files; no re-analysis outside the frozen script without labelling it
exploratory; E5 flip rate (6.5–8 %) must be stated next to every test5 success contrast.
