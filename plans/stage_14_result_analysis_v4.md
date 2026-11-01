# Stage 14 RESULT_ANALYSIS [v4] — plan (run 9, 2026-11-01)

**Inputs.** `results/v4/results_v4.json` (collected unchanged by `code/tools_results_v4.py`: `12_d4_analysis.json`,
`14_s2_analysis.json`, `14_e5_analysis.json`, S2 student training summaries), rules in `docs/07c_amendment_v4_0.md`
(D4, H2-S2, E5 reading), the v3 baseline `results/v3/14_analysis.md` / `results_v3.json` for comparison.

**Procedure** (`pipeline/references/stage_prompts/result_analysis.md`, template verbatim):
1. Pass 1 — fresh subagent (strongest model) with the template's system/user prompts; {data_context} = the unaltered
   content of `results_v4.json`; {preamble} = v4 is the third (last) refine loop, adds cell S2 + E5, compare with v3;
   {context} = run facts (runtimes, which parts ran in the sandbox vs runners, RL re-run not bitwise reproducible, the
   npz re-dispatch, early-stop follow-ups, exploratory status, budget).
2. Pass 2 — fresh subagent, the template's adversarial area-chair prompt on pass 1.
3. Merge → `results/v4/14_analysis.md` (pass-1 body, pass-2 supported rewrites applied, merge log).

**Precondition.** D4 complete (val3 0–499, 3 seeds) and the S2 test3 sub-8 rows complete for G*, students, RL,
B-fan; random may still be partial (stated in {context}; its block is then marked incomplete).

## Done (run 9)
Pass 1 → `results/v4/14_analysis_pass1.md`, pass 2 → `14_analysis_pass2.md` (3 S / 3 M / 9 m items, no verdict
wrong), merged `14_analysis.md`. Random anchor still partial at merge time (stated).
