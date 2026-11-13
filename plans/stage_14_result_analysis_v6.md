# Stage 14 RESULT_ANALYSIS [v6] — plan (written run 50, 2026-11-13, before any v6 outcome is read)

**Precondition.** `python code/analysis_v6.py --check` shows test5 0–499, g_T and E12 (100 episodes per method and
cell) complete. Then the frozen read-out `python code/analysis_v6.py` (committed 2026-11-10, before any E8–E12 record)
→ `results/v6/14_v6_analysis.json`, committed unaltered.

**Inputs.** `results/v6/14_v6_analysis.json` (H6a / H6b / H6c with Holm, E12 flip rates, report-only v6 updates of
the v5 rows, G\* run-2 agreement); rules `docs/07c_amendment_v6_0.md` (+ addendum v6.1); the v5 analysis
`results/v5/14_analysis.md` and decision `results/v5/15_decision.md` for comparison.

**Procedure** (`pipeline/references/stage_prompts/result_analysis.md`, template verbatim):
1. Pass 1 — fresh subagent (strongest model), the template's system / user prompts; {data_context} = unaltered
   `14_v6_analysis.json` plus the amendment's rule text; {preamble} = v6 is the fifth (owner-authorised) refine loop;
   compare with v5; {context} = run facts (E8 test5 300–499, E9 reduced G\* on 0–499, E10 second G\* run, E11 round-0
   BC students, E12 sub-16 check in all cells; ≈ 733 CPU-h on free Actions runners; E12 long single episodes split
   into one-episode jobs and one cancelled run (221) — job splitting only, no setting changed).
2. Pass 2 — fresh subagent, the template's adversarial area-chair prompt on pass 1.
3. Merge → `results/v6/14_analysis.md` (pass-1 body, supported pass-2 rewrites, merge log). Prompts saved in
   `results/v6/prompts/`. Then stage 15 [v6].

**Red lines.** Numbers only from the JSON; any extra analysis is labelled exploratory; "equivalent within 4 pp" only
where the Holm-adjusted TOST rejects; the E12 sub-8 → sub-16 flip rate is stated next to every success contrast.
