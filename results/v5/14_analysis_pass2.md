# Stage 14 Analysis (v5, pass 2): area-chair audit of pass 1

Scope: each claim in `14_analysis_pass1.md` was checked against the JSON block and run context in `results/v5/prompts/stage14_pass1_user.txt`, and nothing else. JSON paths are written as in pass 1, with the file-name key first. Values marked *(derived)* are hand arithmetic on cited values and have no CI. Severity: **S** = changes a verdict or headline, **M** = material overstatement or missing caveat, **m** = minor.

All tables in pass 1 (sections 1.1–1.4, 2.1–2.4) were checked cell by cell and match the JSON. The problems are in the prose built on top of the tables.

---

## S: changes a verdict or headline

**S1. The primary-question headline calls the gap "small".**
- Claim (section 5, bullet 1): "the student's success gap to G* is small (point estimates 0.2–2.5 pp on test5 and 3.2–6.0 pp on validation) but not shown to be within 4 pp."
- Evidence:
  - In two cells the validation point estimate already lies beyond the pre-registered margin delta = 0.04: `12_d5_analysis.json.S4.succ.delta_hat` = -0.0548 and `12_d5_analysis.json.A16-2.succ.delta_hat` = -0.0596.
  - All 25 per-seed validation differences are negative (`12_d5_analysis.json.<cell>.succ.per_seed.*`, range -0.068 to -0.01).
  - The test5 lower bounds reach -0.08333 (`14_test5_analysis.json.S4.student_minus_gstar.success.ci95[0]`).
  - Nothing in the data supports the word "small" relative to the 4 pp margin the study set for itself.
- Supported rewrite: "The student is below G* in every cell on both splits (validation 3.2–6.0 pp, with S4 and A16-2 beyond the 4 pp margin; test5 0.2–2.5 pp, CIs down to -8.3 pp), and the pre-registered gate failed in all cells, so matching G* is not supported."

**S2. Pass 1 invents a pooled "true gap of roughly 1–5 pp" and tells the paper to report it.**
- Claim (section 4, item 2): "Read together, validation (500 episodes) and test (300 episodes) suggest a true success gap of roughly 1–5 pp, and that range is what the paper should report."
- Evidence:
  - No pooled estimate or interval exists in the data.
  - The validation point estimates are 0.0324–0.0596 (`12_d5_analysis.json.<cell>.succ.delta_hat`), so two cells lie above 5 pp.
  - The test5 point estimates are 0.002–0.02533 (`14_test5_analysis.json.<cell>.student_minus_gstar.success.diff`), so A16-2 lies below 1 pp.
  - The test5 CIs run from -0.08333 to +0.06067.
  - The two splits also use different G* sources in S2 and S12 (`12_d5_analysis.json.S2.gstar_source` = v4, `...S12.gstar_source` = v3).
- Supported rewrite: "Validation point gaps are 3.2–6.0 pp and test5 point gaps are 0.2–2.5 pp (test5 95% CIs from -8.3 to +6.1 pp); no pooled estimate was computed, so the paper should report both splits separately with their intervals."

**S3. The conclusion says there is "No dependence on travel cost."**
- Claim (section 5, bullet 4): "**No dependence on travel cost.** H5b slope = -0.01571/rad, ci95 [-0.1041, 0.07277]."
- Evidence:
  - The pre-registered verdict is only "no trend detected over 5 cells" (`14_test5_analysis.json.H5b.verdict`).
  - Over the observed G* travel span of 0.1112–0.8213 rad (`...H5b.gstar_mean_travel_rad`), the CI still allows a change in Δsucc of about -7.4 to +5.2 pp *(derived: ci95_per_rad × 0.7101 rad)*.
  - The regressor is G* mean travel, not kappa, and the regression mixes two shape sets, since A16-2 is one of the 5 points (`...H5b.cells`).
  - With 5 points, failing to detect a trend is not evidence that there is none.
- Supported rewrite: "H5b detects no trend of Δsucc on G* travel over 5 cells (slope -0.0157/rad, ci95 [-0.104, 0.073]), but a change of up to about 7 pp across the observed travel range cannot be excluded."

---

## M: material overstatement or missing caveat

**M1. Pass 1 says test5 "contradicts" the D5 verdict in its point estimates.**
- Claim (section 2.1): "This contradicts the pre-registered D5 verdict (m = 0) only in its point estimates."
- Evidence:
  - D5 does not compare a point estimate with -delta. It compares delta_hat with an SE-dependent threshold. For all five cells, threshold = -0.04 + 1.163·se (e.g. S2: -0.04 + 1.163×0.02189 = -0.01454; `12_d5_analysis.json.<cell>.succ.{se,threshold}`) *(derived)*.
  - Approximate test5 SEs come from CI half-width / 1.96: S2 ≈ 0.026, S4 ≈ 0.030, S8 ≈ 0.025, S12 ≈ 0.025, A16-2 ≈ 0.032.
  - With those SEs, the same rule gives thresholds of about -0.010, -0.006, -0.011, -0.012 and -0.003. Then S2 (-0.0247), S4 (-0.0253), S8 (-0.0127) and S12 (-0.0153) would still fail, and only A16-2 (-0.002) would pass *(derived, approximate)*.
  - The val-vs-test comparison in S2 and S12 also changes the G* source (v4 and v3 files on validation), so it is not a like-for-like comparison.
- Supported rewrite: "Test5 point gaps are smaller than the validation gaps in every cell, but applying the D5 rule to test5 would still fail in about 4 of 5 cells, so test5 does not contradict the D5 verdict."

**M2. Pass 1 undercounts the cells where H* is not the best test5 heuristic, so the student−H* margins look better than they are.**
- Claims:
  - Section 4, item 6: "In 3/5 cells, a different heuristic (b_cov) does better on test5."
  - Section 2.2 lists only S4, S12 and A16-2.
  - Section 5: "beats the pilot-chosen heuristic H* in 4/5 cells after Holm correction (+6.1 to +16.8 pp)".
- Evidence:
  - S8 is also inverted. H* = b_cov (`14_test5_analysis.json.S8.H_star`), but on test5 b_fan = 0.3833 > b_cov = 0.3733 (`...S8.means.b_fan.success`, `...S8.means.b_cov.success`).
  - So the count is 4/5 cells, not 3/5. The better heuristic is b_cov in three cells and b_fan in S8.
  - Against the best test5 heuristic, the student's margins are S4 +0.0513, S8 +0.0607, S12 +0.0347 and A16-2 +0.1447 *(derived; no CI, not pre-registered)*.
- Supported rewrite: "The student beats the pilot-chosen H* in 4/5 cells after Holm (+6.1 to +16.8 pp). In 4/5 cells, though, H* is not the best heuristic on test5, and against the best test5 heuristic the post-hoc margin falls to +3.5 to +14.5 pp, with no CI."

**M3. Pass 1 overstates the shortfall that is "consistent with the data in every cell".**
- Claim (section 2.1): "A student shortfall of 6–8 pp is therefore consistent with the data in every cell."
- Evidence: the lower bounds are -0.076 (S2), -0.08333 (S4), -0.06133 (S8), -0.06333 (S12) and -0.06267 (A16-2) (`14_test5_analysis.json.<cell>.student_minus_gstar.success.ci95[0]`). An 8 pp shortfall lies outside four of the five CIs.
- Supported rewrite: "A shortfall of up to 6.1 pp (the tightest lower bound, S8) is consistent with the data in every cell, and up to 8.3 pp in S4."

**M4. The latency ratio rests on a single student seed whose timing is not representative.**
- Claims:
  - Section 5: "The student decides in about 0.33–0.50 ms. Full G* is 2523× to 9933× slower per decision."
  - Section 4, item 8.
- Evidence:
  - All ratios use the job-1 seed-701 student timing (`14_e6_analysis.json.<cell>.job1.ratio_full_gstar_over_student.median`).
  - Within the same cell, the job-2 student medians differ from seed 701 by up to about 24%:
    - A16-2: 0.000326 s for seed 701 vs 0.000404–0.000407 s (`...A16-2.job1.student.median`, `...A16-2.job2.70x.median`).
    - S12: 0.000358 s vs 0.000423–0.000437 s.
    - S4: 0.000494 s vs 0.000415–0.000419 s.
  - Dividing the job-1 G* median by the job-2 student medians gives roughly S12 ≈ 2,080–2,150×, A16-2 ≈ 6,640–6,690× and S4 ≈ 8,060–8,120× *(derived, ratio of medians, not paired)*.
  - Across all seeds, the student medians span 0.326–0.513 ms.
  - Most of the spread across cells comes from G* time (0.910–4.880 s, `...job1.g2000_512_64.median`).
- Supported rewrite: "With seed-701 timings, full G* is 2,523–9,933× slower per decision (median paired ratio, CI rule met only in A16-2). Other seeds' student medians (0.36–0.51 ms) differ by up to about 24% within a cell, so each per-cell ratio is uncertain at about that level."

**M5. "G* is a single deterministic arm" is not supported by the data.**
- Claim (section 4, item 4): "**G* is a single deterministic arm.** `n_seeds` = [5, 1], so the CIs carry no G* seed variance."
- Evidence:
  - The data show only that G* was run once per cell (`14_test5_analysis.json.<cell>.student_minus_gstar.success.n_seeds` = [5, 1]). Nothing in the data says G* is deterministic.
  - E7 reports a non-zero selection bias in the G* value estimates (`12_e7_analysis.json.cells.S2.C1_512.selection_bias_nats` = 0.02179 [0.00427, 0.04013]). That points to noisy Monte-Carlo estimation, which can make G* vary from run to run.
- Supported rewrite: "G* was run once per cell (n_seeds = [5, 1]), so any run-to-run variability of G* (E7 shows noisy, upward-biased value estimates in S2) is missing from the student−G* CIs, and those CIs may be too narrow."

**M6. E7 is used to call the deployed G* sub-optimal.**
- Claims:
  - Section 2.6: "G* is a greedy planner with measurable headroom, not an optimal ceiling."
  - Section 4, item 4: "The student is being compared with a sub-optimal greedy reference."
- Evidence:
  - E7 compares a 32-candidate setting with a 512-candidate setting on 32 beliefs in 2 cells (`12_e7_analysis.json.cells.<cell>.paired_indep_gap_512_minus_32`, n = 32).
  - The JSON does not link either setting to the G* configuration used on test5 (`g2000_512_64` in E6).
  - The gaps are one-decision values in nats (0.0484 in S2, 0.0183 in S12). They are not converted into success.
  - In S12 the selection bias is null in both settings (`...S12.C1_32/C1_512.selection_bias_nats` CIs include 0).
- Supported rewrite: "In S2 and S12, a 512-candidate G* setting gives a larger independent-estimate gap than a 32-candidate setting (+0.048 and +0.018 nats per belief, n = 32). Whether the deployed G* has headroom in success terms was not measured."

**M7. The A16-2 H2-v5 "true" verdict is reported without the RL-collapse caveat.**
- Claim (section 5, bullet 3): "H2-v5 (higher on RL's own objective) holds only in A16-2 (LB 0.5964)".
- Evidence:
  - In A16-2, 4/5 RL seeds use 2.0 probes against a budget of n* = 3 (`14_test5_analysis.json.A16-2.means.rl_s712..rl_s715.n_probes` = 2.0; `12_cal_analysis.json.n_star.A16.n_star` = 3).
  - RL success there (0.1833–0.29) is below the b_fan heuristic (0.32).
  - G* also beats RL on g_T by +0.854 [0.567, 1.144] (`...A16-2.H2_v5.gstar_minus_rl_gT`).
  - The verdict is mechanically correct, but it measures how badly RL transferred, not a property of the student.
- Supported rewrite: "H2-v5 is met only in A16-2 (LB 0.596 > 0.10), where cfg-6 RL collapses to 2 of 3 probes in 4/5 seeds and G* also beats RL by 0.85 nats, so the result reflects RL failing to transfer rather than a student advantage."

**M8. E5 is described as evaluator noise "comparable to the effect".**
- Claim (section 4, item 5): "**Evaluator noise is comparable to the effect.** ... moves the student − G* contrast by up to 0.03, which exceeds the S8/S12/A16-2 test5 point gaps."
- Evidence:
  - E5 covers one student seed, 200 episodes and 2 cells (`14_e5_analysis.json.<cell>.n_episodes`).
  - The two contrast changes have opposite signs: +0.02 in S2 and -0.03 in S12 (`...contrast_change_student_minus_gstar`).
  - Gains and losses largely offset: G* in S2 has 8 gains and 8 losses.
  - The effect on the 5-seed, 300-episode test5 contrast was never measured, so comparing it with the S8/S12/A16-2 gaps compares different estimands.
- Supported rewrite: "Re-reading at sub-16 flips 6.5–8% of single-seed outcomes and shifts the seed-701 student−G* contrast by +0.02 (S2) and -0.03 (S12) on 200 episodes; its effect on the 5-seed test5 contrast was not measured."

---

## m: minor

**m1. CI width range.**
- Claim (section 4, item 1): "the student − G* success CIs are about 10–12 pp wide".
- Evidence: the widths are 9.6 pp (S12), 9.87 (S8), 10.27 (S2), 11.6 (S4) and 12.33 (A16-2) *(derived from `...student_minus_gstar.success.ci95`)*.
- Supported rewrite: "The student−G* success CIs are 9.6–12.3 pp wide."

**m2. The "~7,000–10,000×" framing for S4.**
- Claim (section 4, item 8): "the '~7,000–10,000×' framing holds only for S2, A16-2 and S4."
- Evidence: the S4 median is 6,990, which is below 7,000, and its ci95 is [4,747, 7,270] with half_width_ok = false (`14_e6_analysis.json.S4.job1.ratio_full_gstar_over_student`).
- Supported rewrite: "Only S2 (9,933×) and A16-2 (8,301×) fall in the 7,000–10,000× band; S4 is at 6,990× with a CI down to 4,747×."

**m3. Bootstrap resolution.**
- Claim (section 3, item 1): "The number of resamples is not in the data".
- Evidence: every reported p-value is a multiple of 0.0002 (e.g. `14_test5_analysis.json.S12.student_minus_rl.ball_info.p_two_sided` = 0.0002 and `...S8.student_minus_hstar.success.p_two_sided` = 0.0098). That is consistent with about 5,000 resamples *(inferred)*.
- Supported rewrite: "The resample count is not stated, but every p-value is a multiple of 0.0002, so 'p = 0.0' should be read as p < 0.0002."

**m4. Freeze timing.**
- Claim (section 3, item 8): "weights were frozen before test5 (`13_freeze.json.cells.<cell>.sha256` ...)".
- Evidence: `13_freeze.json` holds only the hashes and the rule text. The timing comes from the run context ("frozen per cell ... before that cell's test5 jobs"), not from the JSON.
- Supported rewrite: "13_freeze.json records 15 (S2, S12) or 10 (S4, S8, A16-2) weight hashes per cell; that they were recorded before test5 is stated in the run context."

**m5. E5 changes "similar in size" to the gaps.**
- Claim (section 3, item 6): "Both changes are similar in size to the test5 point gaps themselves (0.02467 and 0.01533)."
- Evidence: in S12 the change of -0.03 (`14_e5_analysis.json.S12.contrast_change_student_minus_gstar`) is about twice the S12 gap of 0.01533.
- Supported rewrite: "The E5 contrast change is about 0.8× the test5 gap in S2 and about 2× in S12."

**m6. RL "under-tuned outside S2".**
- Claim (section 4, item 7): "**RL is under-tuned outside S2.**"
- Evidence:
  - Direct evidence of failure exists only in A16-2 (2.0 probes in 4/5 seeds).
  - In S4, S8 and S12, RL uses about 3 probes and its success (0.3367–0.4567) is in line with the heuristics.
  - No per-cell tuning was run, so "under-tuned" is an untested hypothesis.
- Supported rewrite: "One RL configuration chosen on S2 was reused everywhere; it visibly fails in A16-2, and whether it is under-tuned in S4, S8 or S12 was not tested."

**m7. Missing multiplicity caveat on the student-vs-RL claim in the conclusion.**
- Claim (section 5): "beats cfg-6 RL on success with a CI excluding 0 in S2, S12 and A16-2".
- Evidence: the student−RL contrasts carry no Holm field (`14_test5_analysis.json.<cell>.student_minus_rl.success`), and pass 1's own section 3, item 2 says they are uncorrected.
- Supported rewrite: "Without multiplicity correction, the student beats cfg-6 RL on success with CIs excluding 0 in S2, S12 and A16-2 (A16-2 confounded by RL collapse)."

**m8. Comparison with v4.**
- Claim (section 5, bullet 2): "This suggests v4's -10.2 pp test3 result was not reproduced."
- Evidence:
  - The v5 S2 validation uses v4 G* files (`12_d5_analysis.json.S2.gstar_source`), so the "validation" side is not independent of v4.
  - The v4 numbers come only from the run context, with no CI.
  - -10.2 pp lies outside the v5 S2 test5 CI [-7.6, +2.67] pp, but v4's own uncertainty is unknown.
- Supported rewrite: "v4's test3 gap (-10.2 pp, run context only) lies outside the v5 S2 test5 ci95 [-7.6, +2.7] pp, but without v4's interval the two cannot be formally compared."

---

## Are any pre-registered verdicts in pass 1 wrong?

No. Each pre-registered verdict in pass 1 matches the JSON flags:
- **D5:** fails in 5/5 cells (`12_d5_analysis.json.H5a_validation.cells_pass` = []), so m = 0.
- **H5a:** no Holm rejection for student−G* in any cell.
- **Student−H* (Holm):** rejected in 4/5 cells; S2 is not.
- **H5b:** no trend, because the CI contains 0.
- **H2-v5:** met only in A16-2, with LB 0.5964 > 0.10.
- **Inversion:** false in every cell, including both RLsucc checks.

The errors are in the interpretation layered on top of these verdicts:
- A "small gap" headline, when two validation cells exceed delta (S1).
- An invented pooled 1–5 pp range (S2).
- "No dependence on travel cost" drawn from a null with only 5 points (S3).
- The claim that test5 contradicts D5, when the D5 rule would still fail on test5 in about 4/5 cells (M1).
- An undercount of the cells where H* is not the best test5 heuristic (M2).

These change how the paper reads, but none of them overturns a pre-registered decision.
