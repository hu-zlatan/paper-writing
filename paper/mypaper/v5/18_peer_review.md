# Stage 18 PEER_REVIEW [v5] — merged record (run 41, 2026-11-09)

Two independent runs of the stage-18 template (fresh opus subagents; full reviews in `18_review_v5_run1.md`,
`18_review_v5_run2.md`; prompts `prompts/stage18_v5_*.txt`). Four reviewer perspectives. The v4 record is at
`v4/18_peer_review.md`.

| run | reviewer | score | verdict |
|---|---|---|---|
| 1 | A (methodology–evidence) | 4 / 10 | borderline, leaning reject |
| 1 | B (novelty / significance) | 3 / 10 | reject (NeurIPS / ICML framing) |
| 2 | A (significance, RSS / CoRL) | 4 / 10 | borderline, leaning reject |
| 2 | B (methodology–evidence) | 5 / 10 | borderline |

**CRITICAL_FABRICATION: no** (both runs; 40 + 38 spot-checks). Trial / episode counts, seeds, tests, hyperparameters
and weight hashes match; run 1 recomputed S4 and A16-2 test5 contrasts and run 2 the G\* test5 means and E5 sub-8
values from raw episode files, all exact. → no rollback; stage 19 with the fixes below.

## Factual / wording mismatches (must fix in stage 19)
1. **E7 mis-described** (run 2, verified by the main session in `code/analysis_e7_v5.py` docstring and
   `results/v5/12_e7_analysis.json`). E7 measures a one-step *look-ahead* screen's value over greedy (H3 headroom) and
   that screen's max-selection bias — not noise or bias of G\*'s own value estimates. Rewrite the E7 note, §5.1 / C5,
   §6 (G\* run once) and Limitation 2: drop "E7 shows noisy, upward-biased value estimates [of G\*]"; report the
   independent-estimate gap at C1 = 512 (S2 +0.0658 nats [0.0297, 0.1084]; S12 from the JSON) as report-only
   look-ahead headroom in nats, with the decision's limit that success-terms headroom was not measured.
2. **H5b weights** (both runs): only the rule (inverse bootstrap variance, addendum v5.1f) was fixed before test5; the
   values come from test5. Fix §4 / §5.4.
3. **"D5 rule on test5 would fail in about 4 of 5 cells"** (both runs): approximate and post hoc (`14_analysis.md`
   M1, SE ≈ half-width / 1.96, clause (i) only). Label it post hoc / approximate and name the exception (A16-2, the
   worst validation cell). Run 2's exact recomputation (A16-2 passes all three clauses) is a reviewer computation not
   in any results file → not cited as a number; at most "the exception is A16-2".
4. **Inversion rule wording** (run 2): both g_T and success CIs must exclude 0 (amendment v5.0 H2-v5); fix paraphrase.
5. **Deviations to state** (both runs): the pre-registered E6 latency–accuracy frontier was not produced (reduced G\*
   was timed only); E5 per-contrast flip rates only for 2 cells / seed 701; the reduction-order history (E7 was run in
   v5.1d before the v5.1e sizing, so step 1 was unavailable and test5 went 500 → 300).
6. **Disclosure gaps:** latency bootstrap B = 2,000 (`code/analysis_e6_v5.py`) vs 10,000 elsewhere; RL sweep single
   seed 719; 9 / 10 `rl_success` runs stopped by the wall-clock time guard (say so, not only "before the cap");
   describe A16 (16 irregular asymmetric polygons, `code/touchbed/shapes.py`) and note it changes K, family and n\* at
   once; §3.2 introduces the reduced G\* configurations twice; D5's effective margin at the observed SE (≈ −1.5 pp)
   vs the nominal δ.
7. **[CITE-MISSING] ×3** (DeepSets, Holm 1979, Efron): stage 23 / a targeted literature lookup; until then the
   sentences stay with markers or the method is named without a citation.

## Substantive points and triage
| # | point | action |
|---|---|---|
| S1 | test5 CIs ±5–6 pp vs δ = 4 pp: the main comparison cannot decide; only validation is resolved | **Report** — already the decision's framing; make it the first sentence of §5.1. No new runs (cap used). |
| S2 | Reduced G\* (22–194 ms) never evaluated on test5 — the obvious cheap baseline | **Limitation + deviation** (E6 frontier dropped); cannot run (refine cap 4 / 4; decision §4.1 forbids new runs). |
| S3 | Latency speed-up has no task-time model | **Discussion**: state that per-decision latency is reported without a physical time model. |
| S4 | DAgger barely moves held-out R̄ (r0 → r2 −0.0069 to +0.0052); student ≈ BC | **Report** from `16_report_rows.json` (report-only), as a qualifier on "DAgger". |
| S5 | G\* single run per cell; RL tuned once on S2 with one seed; B-spread below Random in 4 / 5 cells | **Limitations** (already partly); add the sweep seed and the B-spread remark. |
| S6 | Incremental novelty; planar, model-matched likelihood; 3–4 probes | **Positioning**: measurement paper; keep in Limitations. |
| S7 | Over-length (≈ 8,500 words with tables) for RSS width | Master draft keeps floors; condense in stage 22 to the outline's 3,430-word body. |

## Decision
No CRITICAL FABRICATION → **PROCEED to stage 19** (revision with items 1–7 and S1–S6). Mean score 4.0 / 10.
