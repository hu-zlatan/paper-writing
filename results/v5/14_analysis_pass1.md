# Stage 14 Analysis (v5, pass 1)

Scope: this report uses only the JSON block in `results/v5/prompts/stage14_pass1_user.txt`. Every number is cited by its JSON path. Paths are relative to the top-level JSON object, and the file-name key is written first (for example `14_test5_analysis.json.S2...`). Values are rounded to about 4 significant figures. "pp" means percentage points of success rate. A value marked *(derived)* is simple arithmetic on cited values. No bootstrap was run for derived values, so they carry no CI.

Cells: S2, S4, S8, S12 (shape set S, travel cost kappa = 2/4/8/12) and A16-2 (shape set A16, kappa 2). On test5 each method has 300 episodes per cell (`14_test5_analysis.json.<cell>.episodes_per_method.*` = 300; `complete` = true in all five cells).

---

## 1. Metrics Summary

### 1.1 Pre-registered validation gate D5 (val3, 500 episodes, delta = 0.04)

| Cell | student succ | G* succ | delta_hat succ | threshold | succ passes | delta_hat BI | BI passes | cell passes |
|---|---|---|---|---|---|---|---|---|
| S2 | 0.4812 | 0.514 | -0.0328 | -0.01454 | false | -0.06820 | true | false |
| S4 | 0.4492 | 0.504 | -0.0548 | -0.01503 | false | -0.1334 | true | false |
| S8 | 0.4116 | 0.448 | -0.0364 | -0.01639 | false | -0.04650 | true | false |
| S12 | 0.4136 | 0.446 | -0.0324 | -0.01722 | false | -0.06348 | true | false |
| A16-2 | 0.4124 | 0.472 | -0.0596 | -0.01229 | false | -0.06293 | true | false |

Sources: `12_d5_analysis.json.<cell>.succ.{student_mean,gstar_mean,delta_hat,threshold,passes}`, `12_d5_analysis.json.<cell>.bi.{delta_hat,passes}` (BI threshold = -0.15), `12_d5_analysis.json.<cell>.passes`, and `12_d5_analysis.json.<cell>.delta` = 0.04. **No cell passes D5:** `12_d5_analysis.json.H5a_validation.cells_pass` = [] and `14_test5_analysis.json.H5a.validation_cells_within_delta` = [], so the validation count is m = 0 of 5. Every per-seed success difference is negative, from -0.068 (`12_d5_analysis.json.A16-2.succ.per_seed.701`) to -0.01 (`12_d5_analysis.json.S12.succ.per_seed.701`). In A16-2 no seed passes (`12_d5_analysis.json.A16-2.seeds_ok.*` = false for all five).

### 1.2 Test5 mean success (300 episodes per method)

| Cell | G* | student seeds 701–705 (min–max) | RL seeds 711–715 (min–max) | random | b_fan | b_spread | b_cov | H* (pilot-chosen) |
|---|---|---|---|---|---|---|---|---|
| S2 | 0.5333 | 0.4967–0.53 | 0.39–0.48 | 0.1033 | 0.35 | 0.04667 | 0.45 | b_cov |
| S4 | 0.4967 | 0.4333–0.5033 | 0.3833–0.4567 | 0.08333 | 0.3733 | 0.09 | 0.42 | b_fan |
| S8 | 0.4567 | 0.42–0.4567 | 0.3833–0.43 | 0.09667 | 0.3833 | 0.05 | 0.3733 | b_cov |
| S12 | 0.4567 | 0.42–0.46 | 0.3367–0.3867 | 0.07667 | 0.38 | 0.07 | 0.4067 | b_fan |
| A16-2 | 0.49 | 0.4567–0.5133 | 0.1833–0.29 | 0.03333 | 0.32 | 0.01 | 0.3433 | b_fan |

Sources: `14_test5_analysis.json.<cell>.means.<method>.success` and `14_test5_analysis.json.<cell>.H_star`. Example endpoints: `14_test5_analysis.json.S2.means.student_s701.success` = 0.4967, `...S2.means.student_s705.success` = 0.53, `...A16-2.means.rl_s713.success` = 0.1833.

### 1.3 Test5 travel and probes (G* vs student)

| Cell | G* travel_rad | student travel_rad (min–max) | RL travel_rad (min–max) | G* n_probes | student n_probes (min–max) | RL n_probes (min–max) |
|---|---|---|---|---|---|---|
| S2 | 0.8213 | 0.5000–0.6675 | 2.061–2.545 | 3.863 | 3.94–3.963 | 3.0–3.0 |
| S4 | 0.4046 | 0.1966–0.2909 | 1.210–1.404 | 3.913 | 3.947–3.983 | 2.813–3.01 |
| S8 | 0.1641 | 0.08765–0.09848 | 0.5029–0.6563 | 3.933 | 3.987–3.997 | 3.0–3.083 |
| S12 | 0.1112 | 0.04288–0.05787 | 0.3932–0.4367 | 3.97 | 3.99–4.0 | 3.0–3.097 |
| A16-2 | 0.3704 | 0.2998–0.3554 | 0.7056–2.069 | 2.933 | 2.9–2.973 | 2.0–2.773 |

Sources: `14_test5_analysis.json.<cell>.means.<method>.{travel_rad,n_probes}`. In every cell the student travels less than G*, and RL travels more than both.

### 1.4 Latency (E6, job 1, seed 701)

| Cell | student median (s) | full G* `g2000_512_64` median (s) | ratio G*/student median [ci95] | ratio half_width_ok | job1_complete |
|---|---|---|---|---|---|
| S2 | 0.0004996 | 4.880 | 9933 [8179, 10224] | false | false |
| S4 | 0.0004942 | 3.375 | 6990 [4747, 7270] | false | false |
| S8 | 0.0003577 | 1.234 | 3463 [2680, 3645] | false | false |
| S12 | 0.0003579 | 0.9103 | 2523 [2068, 2675] | false | false |
| A16-2 | 0.0003261 | 2.702 | 8301 [8080, 8472] | true | true |

Sources: `14_e6_analysis.json.<cell>.job1.student.median`, `...job1.g2000_512_64.median`, `...job1.ratio_full_gstar_over_student.{median,ci95,half_width_ok}`, and `14_e6_analysis.json.<cell>.job1_complete`. The other student seeds (job 2, n = 500 each) have medians from 0.0003632 s (`14_e6_analysis.json.S8.job2.703.median`) to 0.0005126 s (`14_e6_analysis.json.S2.job2.704.median`).

---

## 2. Comparative Findings

### 2.1 Student vs G* on test5 (H5a; crossed episode x seed bootstrap)

| Cell | succ diff | ci95 | p (two-sided) | Holm reject (5 cells) | BI diff | BI ci95 | BI p |
|---|---|---|---|---|---|---|---|
| S2 | -0.02467 | [-0.076, 0.02667] | 0.3526 | false | -0.07862 | [-0.1615, 0.004763] | 0.061 |
| S4 | -0.02533 | [-0.08333, 0.03267] | 0.3888 | false | -0.1314 | [-0.2112, -0.05320] | 0.002 |
| S8 | -0.01267 | [-0.06133, 0.03733] | 0.63 | false | -0.06764 | [-0.1392, 0.003764] | 0.0624 |
| S12 | -0.01533 | [-0.06333, 0.03267] | 0.5378 | false | -0.09100 | [-0.1681, -0.01867] | 0.0124 |
| A16-2 | -0.002 | [-0.06267, 0.06067] | 0.9572 | false | +0.08477 | [-0.05888, 0.2320] | 0.2642 |

Sources: `14_test5_analysis.json.<cell>.student_minus_gstar.success.{diff,ci95,p_two_sided,holm_reject_5cells}` and `...student_minus_gstar.ball_info.{diff,ci95,p_two_sided}`.

- All five success point estimates are negative, from -2.533 pp (S4) to -0.2 pp (A16-2), and every ci95 includes 0. **The test does not show equivalence.** Every lower bound is below -delta = -0.04: -0.076, -0.08333, -0.06133, -0.06333 and -0.06267. A student shortfall of 6–8 pp is therefore consistent with the data in every cell.
- The test5 student–G* success gaps are smaller in magnitude than the D5 validation gaps in every cell: S2 -0.02467 vs -0.0328, S4 -0.02533 vs -0.0548, S8 -0.01267 vs -0.0364, S12 -0.01533 vs -0.0324, A16-2 -0.002 vs -0.0596 (`14_test5_analysis.json.<cell>.student_minus_gstar.success.diff` vs `12_d5_analysis.json.<cell>.succ.delta_hat`). This contradicts the pre-registered D5 verdict (m = 0) only in its point estimates. The test5 CIs are wide enough to contain the validation values.
- On ball information, the student is below G* with a ci95 that excludes 0 in S4 (-0.1314) and S12 (-0.0910). These BI contrasts are not Holm-adjusted. In A16-2 the student BI point estimate is above G* (+0.08477, CI includes 0).

### 2.2 Student vs best heuristic H*

| Cell | H* | succ diff | ci95 | p | Holm reject | BI diff [ci95] |
|---|---|---|---|---|---|---|
| S2 | b_cov | +0.05867 | [-0.001333, 0.118] | 0.0558 | false | +0.1441 [0.03379, 0.2520] |
| S4 | b_fan | +0.098 | [0.04667, 0.1487] | 0.0 | true | +0.4180 [0.3301, 0.5094] |
| S8 | b_cov | +0.07067 | [0.01667, 0.1247] | 0.0098 | true | +0.1948 [0.09552, 0.2963] |
| S12 | b_fan | +0.06133 | [0.01067, 0.112] | 0.0178 | true | +0.2361 [0.1568, 0.3168] |
| A16-2 | b_fan | +0.168 | [0.106, 0.23] | 0.0 | true | +0.7842 [0.6135, 0.9579] |

Sources: `14_test5_analysis.json.<cell>.student_minus_hstar.{success,ball_info}.*`. The student beats H* on success after Holm correction in 4 of 5 cells. S2 is the exception: its CI lower bound is -0.001333. The heuristic ranking from pilot data does not always hold on test5. In S4, S12 and A16-2, H* = b_fan, but b_cov scores higher on test5: 0.42 vs 0.3733 (`...S4.means.b_cov.success`, `...S4.means.b_fan.success`), 0.4067 vs 0.38 (S12) and 0.3433 vs 0.32 (A16-2). Against the best heuristic *on test5*, the student's margin would be smaller: about +0.0513 (S4), +0.0347 (S12) and +0.1447 (A16-2) *(derived: G* success + student_minus_gstar.success.diff − b_cov success; no CI)*. This post-hoc comparison is not pre-registered.

### 2.3 Student vs RL

| Cell | student − RL succ [ci95], p | student − RL BI [ci95], p | student − RLsucc succ [ci95], p |
|---|---|---|---|
| S2 | +0.08467 [0.03067, 0.1373], 0.0032 | +0.2297 [0.1469, 0.3139], 0.0 | +0.1087 [0.05933, 0.158], 0.0 |
| S4 | +0.05467 [-0.002, 0.11], 0.0584 | +0.1577 [0.04248, 0.2783], 0.0046 | n/a |
| S8 | +0.032 [-0.01467, 0.07933], 0.19 | +0.08290 [-0.007993, 0.1794], 0.079 | n/a |
| S12 | +0.07267 [0.02467, 0.1207], 0.0032 | +0.2475 [0.1124, 0.3878], 0.0002 | +0.07933 [0.022, 0.134], 0.0078 |
| A16-2 | +0.266 [0.1993, 0.33], 0.0 | +1.025 [0.8492, 1.190], 0.0 | n/a |

Sources: `14_test5_analysis.json.<cell>.student_minus_rl.*` and `...student_minus_rlsucc.success.*` (RLsucc was run only in S2 and S12). The RL policy was tuned on S2 (`12_rl_sweep_selection.json.selected_cfg` = 6). In A16-2 it transfers badly: seeds 712–715 use 2.0 probes and reach success 0.1833–0.2267 (`14_test5_analysis.json.A16-2.means.rl_s712..rl_s715.{n_probes,success}`), where the budget n* = 3 (`12_cal_analysis.json.n_star.A16.n_star`).

### 2.4 H2-v5: student vs RL on the RL objective g_T

| Cell | student − RL g_T | one-sided 95% LB | claim (LB > +0.10) | RL − student g_T [ci95], p | means g_T (student / RL / G*) | inversion |
|---|---|---|---|---|---|---|
| S2 | -0.2044 | -0.4971 | false | +0.2044 [-0.1216, 0.5435], 0.232 | 5.666 / 5.870 / 5.480 | false |
| S4 | -0.3164 | -0.6555 | false | +0.3164 [-0.07608, 0.7258], 0.1152 | 5.506 / 5.822 / 5.385 | false |
| S8 | -0.1712 | -0.4861 | false | +0.1712 [-0.1856, 0.5379], 0.3476 | 5.541 / 5.712 / 5.380 | false |
| S12 | +0.03084 | -0.3044 | false | -0.03084 [-0.4196, 0.3711], 0.8718 | 5.275 / 5.245 / 5.068 | false |
| A16-2 | +0.8332 | +0.5964 | **true** | -0.8332 [-1.117, -0.5464], 0.0 | 6.899 / 6.066 / 6.920 | false |

Sources: `14_test5_analysis.json.<cell>.H2_v5.{student_minus_rl_gT.diff,student_minus_rl_gT.lower_one_sided_95,claim_student_higher_on_rl_objective,rl_minus_student_gT,means_gT,inversion}`. H2-v5 holds only in A16-2. In S2/S4/S8, RL has higher g_T as a point estimate while the student has higher success, but none of the RL-higher CIs excludes 0, so the pre-registered "inversion" is false everywhere. In all four S cells, G* has the lowest mean g_T of the three methods. For example, `...S2.H2_v5.gstar_minus_rl_gT.diff` = -0.3900 [-0.8566, 0.06472] and `...S4.H2_v5.gstar_minus_rl_gT.diff` = -0.4371 [-0.9095, 0.01035], p = 0.056. Neither CI excludes 0.

### 2.5 H5b: travel-cost trend

The WLS slope of test5 Δsucc on G* mean travel over the 5 cells is -0.01571 per rad, ci95 [-0.1041, 0.07277] (`14_test5_analysis.json.H5b.slope_per_rad`, `...ci95_per_rad`), or -0.02741 per 100° [-0.1817, 0.1270] (`...slope_per_100deg`, `...ci95_per_100deg`). The verdict is "no trend detected over 5 cells" (`14_test5_analysis.json.H5b.verdict`). The cell weights range from 1048 (A16-2) to 1643 (S12) (`14_test5_analysis.json.H5b.weights`).

### 2.6 Planner headroom (E7, report-only)

The independent-estimate gap grows when G* considers more candidates. The paired 512-minus-32 `indep_gap` is 0.04838 nats [0.01681, 0.08697] in S2 and 0.01830 [0.004013, 0.03652] in S12 (`12_e7_analysis.json.cells.<cell>.paired_indep_gap_512_minus_32`). The selection bias is positive with a CI excluding 0 in S2: 0.01926 [0.001030, 0.04193] at C1_32 and 0.02179 [0.004270, 0.04013] at C1_512. It is null in S12: 0.004470 [-0.007718, 0.01884] and -0.002040 [-0.01574, 0.01258] (`12_e7_analysis.json.cells.<cell>.<C1_32|C1_512>.selection_bias_nats`). G* is a greedy planner with measurable headroom, not an optimal ceiling.

---

## 3. Statistical Checks

Only the procedures below appear in the data.

1. **Bootstrap 95% CIs and two-sided bootstrap p-values** on test5 contrasts. The resampling is crossed over episodes and seeds: `n_episodes` = 300; `n_seeds` = [5, 1] for student vs G*/H* and [5, 5] for student vs RL (e.g. `14_test5_analysis.json.S2.student_minus_gstar.success.n_seeds`). Several p-values are reported as exactly 0.0 (e.g. `14_test5_analysis.json.S4.student_minus_hstar.success.p_two_sided`). The number of resamples is not in the data, so read these as "below the bootstrap resolution", not as p = 0.
2. **Holm correction over 5 cells** applies only to the success contrasts student − G* and student − H*. Results: 0/5 rejections for student − G* (`...<cell>.student_minus_gstar.success.holm_reject_5cells` all false) and 4/5 for student − H* (S2 false). The BI, RL, RLsucc and g_T contrasts carry no multiplicity correction.
3. **One-sided 95% lower bound** for H2-v5 (`...H2_v5.student_minus_rl_gT.lower_one_sided_95`) against the pre-registered +0.10 nats bar. 1/5 cells qualifies (A16-2, LB 0.5964).
4. **WLS slope with ci95** for H5b (`14_test5_analysis.json.H5b`). The CI contains 0, so no trend is claimed, as pre-registered.
5. **D5 gate**: a point estimate is compared against a per-cell threshold that depends on the SE. For example, S2 has se = 0.02189 and threshold = -0.01454 (`12_d5_analysis.json.S2.succ.{se,threshold}`). Success fails in 5/5 cells and BI passes in 5/5. Per the pre-registration, D5 has no remedy step.
6. **Evaluator resolution check (E5, sub-8 vs sub-16, episodes 0–199)**:
   - Outcome flip rates are 0.065–0.08 (`14_e5_analysis.json.<S2|S12>.<gstar|student_s701>.flip_rate`).
   - G* success moves 0.54 → 0.54 (S2) and 0.48 → 0.505 (S12).
   - Student 701 moves 0.465 → 0.485 (S2) and 0.455 → 0.45 (S12).
   - The student − G* contrast changes by +0.02 (S2) and -0.03 (S12) (`14_e5_analysis.json.<cell>.contrast_change_student_minus_gstar`). Both changes are similar in size to the test5 point gaps themselves (0.02467 and 0.01533).
   - The mean |ΔBI| is at most 0.004034 nats (`14_e5_analysis.json.S2.student_s701.mean_abs_dBI`), which is negligible for BI.
7. **Latency completeness rule** (median CI half-width ≤ 10%): it fails for the full-G* ratio in S2/S4/S8/S12 (`14_e6_analysis.json.<cell>.job1.ratio_full_gstar_over_student.half_width_ok` = false) and passes only in A16-2.
8. **Data integrity**: test5 is complete for every method and cell (`complete` and `gt_complete` = true), and weights were frozen before test5 (`13_freeze.json.cells.<cell>.sha256`, 15 files each for S2/S12 and 10 each for S4/S8/A16-2).

---

## 4. Limitations

1. **Power and equivalence.** With 300 episodes per cell, the student − G* success CIs are about 10–12 pp wide (e.g. S2 [-0.076, 0.02667]). They cannot rule out a gap larger than the pre-registered delta = 0.04 in any cell. "No significant difference" here does not mean "matched". Test5 was cut from 500 to 300 episodes (addendum v5.1e), which widened these CIs.
2. **The validation gate failed everywhere.** D5 gives m = 0/5 (`12_d5_analysis.json.H5a_validation.cells_pass` = []). Under the pre-registration, the favourable-looking test5 point estimates cannot override this. Read together, validation (500 episodes) and test (300 episodes) suggest a true success gap of roughly 1–5 pp, and that range is what the paper should report.
3. **The G* references for D5 are heterogeneous.** The S2 G* validation runs come from v4 files and S12 from v3 files, while S4/S8/A16-2 come from v5 (`12_d5_analysis.json.<cell>.gstar_source`).
4. **G* is a single deterministic arm.** `n_seeds` = [5, 1], so the CIs carry no G* seed variance. E7 also shows that G* is improvable: the 512-vs-32 candidate gap is 0.04838 nats in S2. The student is being compared with a sub-optimal greedy reference.
5. **Evaluator noise is comparable to the effect.** E5 shows that changing posterior resolution flips 6.5–8% of outcomes and moves the student − G* contrast by up to 0.03, which exceeds the S8/S12/A16-2 test5 point gaps. E5 covers only 2 cells, 200 episodes and one student seed (701).
6. **The heuristic baseline depends on the selection sample.** H* was picked on 200 pilot episodes (`12_base_hstar.json.rule`). In 3/5 cells, a different heuristic (b_cov) does better on test5, so the student − H* margins are optimistic relative to the best test heuristic.
7. **RL is under-tuned outside S2.** One configuration (cfg 6, chosen on S2 val_v2 with ball-sPCE 6.300 vs 6.241 for cfg 0; `12_rl_sweep_selection.json.rows[6].final_val_ball_spce`, `rows[0]...`) was reused in every cell. On the sampled-policy metric, cfg 1 scores higher (6.316 vs 6.205; `rows[1].final_val_ball_spce_sampled`, `rows[6]...`). In A16-2, 4/5 RL seeds use only 2.0 probes. The large student-vs-RL margin in A16-2 (+0.266) therefore partly reflects RL failure rather than student strength. RLsucc exists only in S2/S12.
8. **The latency ratio is not a single number.** The medians span 2523× (S12) to 9933× (S2), so the "~7,000–10,000×" framing holds only for S2, A16-2 and S4. The completeness rule fails in 4/5 cells, the CIs are asymmetric (S4 [4747, 7270]), and the hardware was 2-core CPU runners and a sandbox.
9. **Multiplicity.** BI, RL, RLsucc and g_T contrasts (more than 30 tests) are uncorrected. Single p-values of about 0.01 among them (e.g. S12 BI p = 0.0124) should be read with that in mind.
10. **Scope.** The study is simulation-only (TouchBED) with two shape sets and one kappa for A16, and it uses a sub-8 grid read-out for all success metrics. The H5b trend uses only 5 points, with travel ranging from 0.1112 to 0.8213 rad (`14_test5_analysis.json.H5b.gstar_mean_travel_rad`).

---

## 5. Conclusion

- **Primary question (does the student match G*?): not established.** The pre-registered validation gate D5 fails in all 5 cells (success delta_hat from -0.0324 to -0.0596, all below threshold). On test5 the student is below G* in every cell (-0.2 to -2.533 pp), with no Holm rejection. However, every ci95 lower bound (-6.133 to -8.333 pp) lies beyond -delta = -0.04, so equivalence is not shown either. The defensible statement is: "the student's success gap to G* is small (point estimates 0.2–2.5 pp on test5 and 3.2–6.0 pp on validation) but not shown to be within 4 pp."
- **Relative to v4**, the v5 test5 gap in S2 (-0.02467) is much closer to its validation gap (-0.0328) than v4's test gap was, according to the run description. This suggests v4's -10.2 pp test3 result was not reproduced. The v4 values are not in the JSON and are quoted from the run description only.
- **Student vs baselines.** The student beats the pilot-chosen heuristic H* in 4/5 cells after Holm correction (+6.1 to +16.8 pp), and beats cfg-6 RL on success with a CI excluding 0 in S2, S12 and A16-2. H2-v5 (higher on RL's own objective) holds only in A16-2 (LB 0.5964), and no "inversion" is detected.
- **No dependence on travel cost.** H5b slope = -0.01571/rad, ci95 [-0.1041, 0.07277].
- **Cost.** The student decides in about 0.33–0.50 ms. Full G* is 2523× to 9933× slower per decision (median ratios), and the CI-completeness rule is met only in A16-2.
