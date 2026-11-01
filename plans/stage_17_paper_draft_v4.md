# Stage 17 PAPER_DRAFT [v4] — plan (run 10, 2026-11-01)

## Goal
Full markdown master draft of the v4 row-4 characterisation paper (S12 + S2 cells, E5) from
`paper/mypaper/sections/00_outline.md`; every number traceable to `results/v4/results_v4.json` or
`results/v3/results_v3.json`.

## Preconditions (stage 16 v4 open items)
- [x] (1) Random anchor sub-8 re-read: follow-up manifest `experiments/v4_e4_rg_random_r1.json` (53 jobs, 66 episodes)
  dispatched this run. The random row enters no contrast; the draft marks its success/BI cell
  `[PENDING:v4:14_s2_analysis.test3_sub8.rows.random]`, filled in stage 19 from the final JSON.
- [x] (2) G2′ κ = 2 used τ = 4.7, n\* = 4, set S (header of `results/v3/g2/S_k2_000.jsonl`: `"kappa": 2.0, "tau": 4.7,
  "n_star": 4`) = the S2 cell definition in `docs/07c_amendment_v4_0.md`. The κ = 2 H3 row may be called "the S2 cell".
- [x] (3) Pass-2 checks: travel coupling (`behaviour.student_vs_gstar_travel_pearson_r`, identical-sequence counts) and
  per-seed g_T are in `14_s2_analysis.json` (commit 4242228) and so in `results_v4.json`. The rest of the outline's
  "do not cite" list (first-action agreement, per-seed travel medians, B-fan sequence identity, g125-vs-v3-B-fan) is
  not in JSON → the draft must not use it.
- [x] Citations: 60 cards, cite-key list identical to the v3 stage-17 prompt; outline reports no [CITE-MISSING].

## Length decision (same as v3, recorded)
Master draft meets the `RESTRICTS.yaml` writing floors (total ≥ 4,000 words; intro 700, related 500, method 800,
experiments 600, results 500, discussion 300, limitations 200, conclusion 150), which target the 8-page Stage 2 paper.
The 5-page RSS Stage 1 extended abstract is condensed in stage 22 as a separate export, so stage 19's never-shorten rule
still holds for the master draft.

## Execution
- Fresh-context opus subagent; template `pipeline/references/stage_prompts/paper_draft.md` verbatim (system + user).
  Placeholders: {preamble} (venue, length decision, row-4 framing, v4 additions, pending marker, v3 final draft
  appended as wording source with the instruction that the outline's binding sentences override it),
  {topic_constraint} (block from `stage16_v4_user.txt`, two-regime topic), {exp_metrics_instruction}
  (`results_v4.json` and `results_v3.json` in full), {citation_instruction} (60 cite_keys, same as v3), {outline}.
- Prompt files: `paper/mypaper/prompts/stage17_v4_{system,user}.txt`. Figure 1 prompt first →
  `paper/mypaper/figures/figure1_prompt.txt` (v3 version kept in git history).
- Output: `paper/mypaper/sections/draft_v4.md`.

## Checks (main session, after the subagent)
- [ ] Number audit (`code/tools_number_audit.py`) against both JSONs + design constants.
- [ ] Every \cite key exists in the cards.
- [ ] Word counts vs RESTRICTS floors.
- [ ] Outline never-write list respected; no claim from the "do not cite" list.

## Done (run 10)
- Draft `paper/mypaper/sections/draft_v4.md` (fresh opus subagent, prompt files above): main body 7,706 words
  (abstract 244; intro 904, related 623, method 1,655, experiments 1,272, results 2,182, discussion 549, limitations 290,
  conclusion 231) — all RESTRICTS floors met; stage 22 condenses to the 5-page Stage 1 abstract.
- Figure 1 prompt → `paper/mypaper/figures/figure1_prompt.txt`.
- Checks: number audit (now also reads `results_v4.json`) against the v3/v4 JSONs + frozen design docs only:
  2 unmatched, both benign — 97.5 (bootstrap quantile) and 0.293 (= (UB − LB)/2 of the H2-S2 one-sided bounds,
  derived as in `results/v4/14_analysis.md` §H2 power). 31 cite keys, all in the cards. No "do not cite" item used
  ("first action" occurrences are the H3 screened-first-action instrument). Random anchor marked [PENDING] (3×).
- Subagent's flagged items: v3-draft design constants (K = 8, ±15 mm prior, σ_p/σ_n, 5 mm/5° success, distillation
  hyper-parameters, L = 4095, J = 16, 1.02 guard) — reused from the v3 text that passed stage 18 audit; G5′ S12 written
  as "pass" (v3 JSON now complete 200/200 on every baseline, so the outline's INC tag is stale). Stage 18 re-audits.
