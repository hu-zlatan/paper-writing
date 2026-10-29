# Stage 14 RESULT_ANALYSIS [v3] — plan (run 7, 2026-10-29)

**Inputs.** `results/v3/results_v3.json` (every v3 analysis JSON, collected unchanged by `code/tools_results_v3.py`),
pre-registered rules in `docs/07_hypotheses_v3.md` (§3.3 H2, §3.4 H3, §4 D3, §5 outcome map),
`docs/07c_amendment_v3_0.md` status notes, `docs/07c_amendment_v3_1.md`, `plans/stage_12_experiment_run_v3_main_row4.md`.

**Procedure** (`pipeline/references/stage_prompts/result_analysis.md`, template verbatim):
1. Pass 1 — fresh-context subagent (strongest model), system "You are a quantitative ML analyst. Always cite exact
   numbers from the provided data." and the user template with {preamble}, {data_context} = the content of
   `results/v3/results_v3.json` (read from the file, unaltered), {context}.
2. Pass 2 — second fresh subagent with the template's adversarial area-chair prompt on pass 1's report.
3. Merge into `results/v3/14_analysis.md` (pass 1 body, pass 2's supported rewrites applied, a short merge log).

**Known partial inputs at the time of the analysis (stated in {context}):** G5′ sub-8 heuristic rows (S12 154–187 of
200; A12/S0 mostly missing; re-reads running) and D3-B validation (295 of 300). Both are report-only.

**Preamble.** "This is iteration v3 (the last loop before escalation). The pre-registered learnability gate D3 failed
twice (first attempt and the one remedy), so the outcome map's row 4 applies (characterisation paper). Compare with v2
where useful (results/v2/14_analysis.md)."
