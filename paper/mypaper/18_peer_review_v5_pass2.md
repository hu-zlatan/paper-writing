# Stage 18 PEER_REVIEW [v5] — pass 2 merged record (run 41, 2026-11-09)

Second pass on the stage-19 pass-1 draft (`v5/draft_v5_stage19pass1.md`); two fresh opus subagents, same template and
evidence (prompt `prompts/stage18_v5_pass2_user.txt`); full reviews `18_review_v5_pass2_run1.md`, `..._run2.md`.

| run | reviewer | score | verdict |
|---|---|---|---|
| 1 | A (methodology–evidence) | 4 / 10 | borderline, leaning reject |
| 1 | B (significance / novelty) | 3 / 10 | reject |
| 2 | A (significance, RSS / CoRL) | 3 / 10 | reject |
| 2 | B (methodology–evidence) | 4 / 10 | borderline, leaning reject |

**CRITICAL_FABRICATION: no** (both runs; 45 + 40 spot-checks; test5 / validation rows recounted from raw logs, weight
hashes checked). → stage 19 pass 2.

## Must-fix (pass 2)
P1. **Reduced-planner accuracy is not "unevaluated"** (both runs; verified: addendum v5.1f, `docs/07c_amendment_v5_1.md`
    l.115–116, names the v4 E5 S12 rows as the accuracy side of the frontier; `results/v4/results_v4.json` >
    `14_e5_analysis.json`). Report those S12 rows (g125_512_16 / g500_512_4 vs G\* on S12 test3, 300 episodes, values
    from that block) as the registered PRIOR accuracy side, at their logged latencies; say that for S2 / S4 / S8 /
    A16-2 no reduced-G\* accuracy exists (none was registered). Fix deviation (b), §5.2, §6, Limitation 7.
P2. **RL sweep "validation stream (92,160 episodes)"** is the training-episode count at the last validation; the
    validation stream is 500 episodes (`code/analysis_rl_sweep_v5.py`; `val_episodes: 500` in `results/v5/rl/*.json`).
P3. **"Design constants not in a citable field"** (Limitation 11, §4 Implementation) is stale: RL episodes per seed and
    label / DAgger budgets are in `16_report_rows.json`. Reword.
P4. **Inversion check is one-directional** in code (`analysis_test5_v5.py` l.110–112: RL higher on g_T AND student
    higher on success, both CIs excluding 0). Fix the "opposite directions" wording.
P5. **Latency "seed spread ≈ 24 %"** is between seed 701 (job 1) and the job-2 seeds on different runners; within job 2,
    seeds 702–705 differ by ≤ 3 %. Reword (both runs).
P6. **Disclosures:** A16's first 8 shapes are v3's set A (same seed stream, `shapes.py`); S2 / S12 round-0 labels re-use
    v4 / v3 labels (amendment v5.0 E1 allows it; `experiments/v5_d5_r0_S2_S12_rerun.json`); g_T estimator sizes J 16,
    L 4,095 (amendment v5.1 / `gt3`); "about 4 of 5" → "4 of 5 (approximate, post hoc), A16-2 the exception".
P7. **New report-only row (pipeline computed, script committed):** `code/tools_lat_agreement_v5.py` →
    `results/v5/19_lat_agreement.json`: agreement of each method's recorded action with full G\* on the E6 job-1 states.
    Student / g125_512_16 / g500_512_4: S2 0.182 / 0.099 / 0.072; S4 0.299 / 0.175 / 0.116; S8 0.462 / 0.235 / 0.212;
    S12 0.513 / 0.312 / 0.243; A16-2 0.326 / 0.146 / 0.092. **Caveat that must accompany it:** G\* samples outcomes
    (M = 64), so its agreement with itself on a re-run is below 1 and was not measured; agreement is not accuracy.
P8. S2 validation gap under the v5 recipe (−3.3 pp, 5 seeds) vs v4's −2.8 pp (3 seeds, other recipe): may be stated as a
    PRIOR comparison without a test, using the JSON values.

## Not actioned
- Moving report-only items to an appendix / length: stage 22 condensation (RSS Stage 1 has no supplementary).
- New experiments (reduced G\* on test5, RL re-tuning, G\* re-runs): refine cap 4 / 4 used; decision §4.1.

## Decision
No CRITICAL FABRICATION → stage 19 pass 2 (targeted edits P1–P8), then stage 20.
