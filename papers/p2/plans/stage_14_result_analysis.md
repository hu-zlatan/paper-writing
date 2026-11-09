# p2 Stage 14 — RESULT_ANALYSIS (v1), run 42

**Plan.** Template `pipeline/references/stage_prompts/result_analysis.md` verbatim (system + user), placeholders filled
by `docs/prompts/build_stage14.py` → `docs/prompts/stage14_{system,user}.txt`: `{data_context}` = every analysis JSON in
`results/v1/` unaltered (raw grid inputs, hash file and the UT3 per-cell list omitted), `{context}` = 08a–08h.
- Pass 1: fresh opus subagent (Agent tool, no conversation history, only the prompt files) → `results/14_analysis_pass1.md`.
- Pass 2 (template's adversarial second pass, area-chair prompt verbatim): a second fresh opus subagent reads pass 1 and
  the same data → `results/14_analysis_pass2.md`.
- Merge → `results/14_analysis.md`; the main session checks every number in the merged file against the JSON files.
Red lines: no number that is not in `results/v1/*.json`; primary vs secondary vs post hoc kept separate.
