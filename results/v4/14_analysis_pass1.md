# Stage 14 · Analysis of the v4 record (pass 1)

> System: "You are a quantitative ML analyst. Always cite exact numbers from the provided data."
> Task: "Analyze run metrics and produce markdown report with statistical interpretation. Use the ACTUAL quantitative
> values provided above — do NOT invent numbers. Required sections: Metrics Summary (with real values), Comparative
> Findings, Statistical Checks, Limitations, Conclusion."

**Scope and sourcing.**
- **v4 numbers** come only from the data block in `results/v4/prompts/stage14_pass1_user.txt`. They are cited as
  `file.key.path`, where the file is one of `12_d4_analysis`, `14_s2_analysis`, `14_e5_analysis` and
  `students_S2_training`.
- **v3 numbers** come from `results/v3/results_v3.json` (cited `v3:key.path`) or from the binding merged report
  `results/v3/14_analysis.md` (cited `v3-14`).
- **Rules** are quoted from `docs/07c_amendment_v4_0.md` (written before any v4 run) and from the run context in the
  task.
- **(derived)** marks arithmetic I did myself: differences, ratios, means, and sample SDs of listed per-seed values.
- **Statistics.** Every interval comes from the paired crossed bootstrap in `code/touchbed/stats.py`
  (`crossed_bootstrap_diff`: B = 10,000, seed 0, `lower`/`upper` = 5 % / 95 % quantiles). For D4 the SE is the SD of
  that bootstrap (`code/analysis_d4_v4.py`, `boot_sd`). No t-test is used anywhere.
- **Status.** v4 adds rows and changes no v3 verdict. In v3, D3 failed twice (row 4, characterisation paper), H2 was
  rejected in S12 and H3 was Hold. All three stand.

Notation:
- Δ = paired difference;
- pp = percentage points;
- BI = ball information (nats, sub-8 grid);
- g_T = ball-sPCE (RL's training objective);
- LB/UB = one-sided 95 % bounds;
- "ci95" = two-sided 95 % interval.

---

## 1. Metrics Summary

### 1.1 Decision table (items with a pre-registered v4 rule)

| Item | Rule (07c v4.0) | Measured | Verdict |
|---|---|---|---|
| **D4 (i)** success | Δ̂_succ(student − G\*) ≥ max(−0.02, −0.04 + 1.645·SE·√0.5) | Δ̂ = −0.0280, SE 0.02180, threshold −0.01464 (`12_d4_analysis.succ`) | **fail** |
| **D4 (ii)** BI | Δ̂_BI ≥ −0.15 nats | −0.1049 (`12_d4_analysis.bi`) | pass |
| **D4 (iii)** seeds | every seed's Δ_succ > −0.04 | −0.036 / −0.028 / −0.020 (`succ.per_seed`; `seeds_ok` all true) | pass |
| **D4 overall** | (i) ∧ (ii) ∧ (iii) | `12_d4_analysis.passes: false`, n = 500, complete | **FAIL** → "not shown to reach G\* in S2 either"; no remedy round |
| **H2-S2** | one-sided 95 % LB of g_T(student) − g_T(RL) > +0.10 nats | Δ = −0.4452, LB −0.7485, UB −0.1616 (`14_s2_analysis.h2.bootstrap`), n = 500, seeds [3, 3] | **not detected** (`h2.passes: false`) |
| **E5** | report reduced-G\* − student success/BI ci95; no claim beyond "at its logged latency" | §1.5 | reported (no verdict by design) |

### 1.2 D4 on val3 0–499, S2, sub 8 (`12_d4_analysis`)

| Quantity | Success | BI (nats) |
|---|---|---|
| Student mean (seeds 601–603) | 0.486 | 6.5626 |
| G\* mean | 0.514 | 6.6674 |
| Δ̂ (student − G\*) | −0.0280 | −0.1049 |
| SE (bootstrap SD) | 0.02180 | 0.03855 |
| Threshold | −0.01464 | −0.15 |
| Per seed 601 / 602 / 603 | −0.036 / −0.028 / −0.020 | −0.1184 / −0.1227 / −0.0735 |
| Passes | false | true |

- Rule (i) is the only failing clause. The estimate is 1.34 pp below its threshold (derived: −0.0280 − (−0.01464)),
  i.e. 0.61 SE (derived: 0.01336 / 0.02180).
- The −2 pp floor does not bind, because the SE term gives the higher threshold (−0.01464 > −0.02). The estimate
  (−2.80 pp) is below the floor as well.

### 1.3 S2 test3 0–299, sub 8 (exploratory; `14_s2_analysis.test3_sub8`)

| Row | n per seed | Success | BI (nats) | Per-seed success |
|---|---|---|---|---|
| G\* | 300 | 0.5533 | 6.6731 | 0.5533 |
| Student (601–603) | 300 ×3 | 0.4511 | 6.4901 | 0.4633 / 0.4133 / 0.4767 |
| RL-relative (611–613) | 300 ×3 | 0.4233 | 6.3103 | 0.3967 / 0.4200 / 0.4533 |
| B-fan | 300 | 0.3700 | 5.9619 | 0.3700 |
| Random (incomplete, unpaired) | **190** | 0.1316 | 3.7104 | — (`random_on_available`) |

Paired contrasts (`test3_sub8.diffs`; ci95, no multiplicity correction):

| Contrast | Success Δ | Success ci95 | BI Δ | BI ci95 |
|---|---|---|---|---|
| student − G\* | −0.1022 | [−0.1656, −0.0433] | −0.1830 | [−0.2694, −0.0944] |
| student − RL | +0.0278 | [−0.0411, +0.0956] | +0.1797 | [+0.0908, +0.2732] |
| G\* − RL | +0.1300 | [+0.0644, +0.1944] | +0.3628 | [+0.2634, +0.4672] |
| student − B-fan | +0.0811 | [+0.0167, +0.1467] | +0.5281 | [+0.4202, +0.6371] |
| B-fan − G\* | −0.1833 | [−0.2467, −0.1200] | −0.7112 | [−0.8299, −0.5936] |

### 1.4 H2-S2, g_T on test3 0–499 (`14_s2_analysis.h2`)

| Quantity | Value |
|---|---|
| g_T student / RL | 5.5341 / 5.9793 |
| Δ (student − RL); LB / UB | −0.4452; −0.7485 / −0.1616 |
| p_greater / p_less | 0.9936 / 0.0064 |
| g_T of G\* / B-fan / random | 5.3972 / 5.2631 / 3.5100 |
| Threshold; passes | 0.10; false |

The data block gives no per-seed g_T values for v4, so the seed spread of g_T on test cannot be reported.

### 1.5 E5: reduced G\* on S12 test3 0–299, sub 8, paired with the v3 rows (`14_e5_analysis`)

| Row | Success | BI (nats) | Probes | Logged median decision latency |
|---|---|---|---|---|
| g125_512_16 | 0.3600 | 5.9690 | 3.843 | 0.02076 s |
| g500_512_4 | 0.3767 | 6.0373 | 3.777 | 0.04599 s |
| G\* (v3 row) | 0.4267 | 6.2483 | 3.963 | null |
| student_rem (v3 row) | 0.3822 | 6.1996 | 4.0 | null |
| student_long (v3 row) | 0.4100 | 6.2402 | 3.994 | null |

The G\*, student_rem and student_long rows reproduce the v3 values. These are `v3:14_m4_analysis.rows.gstar` (0.4267 /
6.2483), `.rows.student` (0.3822 / 6.1996) and `.exploratory_long_student` (0.41 / 6.2402), so the pairing is with the
same v3 episodes and actions.

| Contrast | Success Δ [ci95] | BI Δ [ci95] |
|---|---|---|
| g125 − student_rem | −0.0222 [−0.0689, +0.0244] | −0.2306 [−0.3178, −0.1451] |
| g125 − student_long | −0.0500 [−0.1011, +0.0011] | −0.2712 [−0.3709, −0.1744] |
| g125 − G\* | −0.0667 [−0.1200, −0.0100] | −0.2793 [−0.3809, −0.1791] |
| g500 − student_rem | −0.0056 [−0.0578, +0.0478] | −0.1623 [−0.2607, −0.0649] |
| g500 − student_long | −0.0333 [−0.0889, +0.0233] | −0.2029 [−0.3039, −0.0987] |
| g500 − G\* | −0.0500 [−0.1100, +0.0133] | −0.2110 [−0.3136, −0.1078] |

### 1.6 Behaviour, test3 0–299 no-grid (`14_s2_analysis.behaviour`)

| Row | Travel (deg/episode) | Probes | v3 S12 travel (`v3:14_behaviour.methods`) |
|---|---|---|---|
| G\* | 46.91 | 3.873 | 6.13 (n = 500) |
| Student | 39.14 | 3.926 | 1.52 / 2.05 / 1.88 (per seed) |
| RL | 136.82 | 3.0 | 23.02 / 25.76 / 25.65 (per seed) |
| B-fan | 1.454 | 4.0 | 1.454 (n = 300) |
| Random | 172.20 | 2.367 | 38.45 (n = 500) |

### 1.7 Training records

**Students** (`students_S2_training`). val_R̄ is mean regret on label-distribution validation shards 1,200–1,499. It
is not measured on val3.

| Seed | r0 val_R̄ | r1 | r2 | train decisions r0 / r1 / r2 | status |
|---|---|---|---|---|---|
| 601 | 0.3084 | 0.3193 | 0.3216 | 10,499 / 13,616 / 16,761 | max_epochs ×3 |
| 602 | 0.2999 | 0.3054 | 0.2975 | 10,499 / 13,636 / 16,793 | max_epochs ×3 |
| 603 | 0.3120 | 0.3146 | 0.3101 | 10,499 / 13,609 / 16,729 | max_epochs ×3 |

**RL** (`14_s2_analysis.rl_training`). Every seed ran to max_episodes: 200,064 episodes, plateau at 102,400 (recorded,
not used).
- Final training g_T: 6.3397 / 6.2433 / 5.9895.
- Wall time: 3,601 / 3,544 / 3,051 s.

---

## 2. Comparative Findings

### 2.1 Learnability in a travelling cell (D4 vs v3 D3)

1. **The design goal of S2 is met.** G\* travels 46.9° per episode on test3, against 6.1° in S12
   (`v3:14_behaviour.methods.gstar.travel_deg_mean` 6.132). The student follows it: 39.1°, or 83 % of G\*'s travel
   (derived). In S12 the student travelled about 1.5–2.0°. In S2, then, distillation imitates a moving policy. It is not
   a trivial stay-and-probe regime.
2. **D4 still fails, on clause (i) only.** Against v3 D3 after its remedy (`v3:12_d3_analysis_rem`):

   | Quantity | v3 D3 remedy (S12) | v4 D4 (S2) |
   |---|---|---|
   | Δ̂_succ vs threshold | −4.40 pp vs −1.68 pp | −2.80 pp vs −1.46 pp |
   | Shortfall below threshold (derived) | 2.72 pp | 1.34 pp |
   | Δ̂_BI | −0.096 | −0.105 |
   | Seeds with Δ_succ > −δ | 0 of 3 (−0.046 / −0.046 / −0.040) | 3 of 3 (−0.036 / −0.028 / −0.020) |

   - The S2 student is nearer its non-inferiority threshold than either S12 attempt, but it does not pass.
   - The cells, G\* success levels (0.514 vs 0.446) and training recipes differ, and no paired cross-cell test exists.
     "Closer than in S12" is therefore a description of point estimates, not a finding.
3. **The test3 gap is much larger than the val3 gap.** Student − G\* success is −10.2 pp on test3 0–299, with ci95
   [−16.6, −4.3] excluding 0, against −2.8 pp on val3 (anomaly 4).
   - Per seed on test3 (derived from `per_seed_success` minus G\* 0.5533): −9.0 / −14.0 / −7.7 pp. Every seed is beyond
     −δ on test3, whereas every seed was inside −δ on val3.
   - In v3 the two splits agreed: −4.40 pp on val3 and −4.44 pp on test3 (`v3:14_m4_analysis.diffs.student-gstar:success`).
   - The test3 reading is exploratory and does not change D4. It does mean that the val3 result (−2.8 pp) should not be
     quoted as the S2 gap on its own; §3.3 discusses this.
4. **BI.** Student − G\* BI is −0.105 on val3 and −0.183 on test3 (ci95 [−0.269, −0.094]). In S12 test3 it was −0.049
   (ci95 [−0.114, +0.019], `v3:14_m4_analysis`). In S2 the BI deficit excludes 0.

### 2.2 Distillation versus RL (H2-S2 and the test3 contrasts)

- **H2-S2 is not detected.** The LB is −0.749, far below +0.10.
- **The g_T difference points the other way.** The one-sided 95 % UB of student − RL is −0.162 < 0, with p_less =
  0.0064. RL scores higher than the student on its own training objective by 0.445 nats.
  - This is exploratory: no rule was pre-registered for this direction.
  - In S12 the two were undetected apart: Δ = +0.0002, bounds [−0.310, +0.303] (`v3:14_h2_analysis.bootstrap`).
- **Grid BI orders the two the opposite way.** Student − RL BI is +0.180 nats (ci95 [+0.091, +0.273]). Success is not
  resolved: +2.8 pp, ci95 [−4.1, +9.6].
- **g_T and BI disagree on more than these two rows.**

  | Ordering | Rows (value) |
  |---|---|
  | g_T | RL 5.979 > student 5.534 > G\* 5.397 > B-fan 5.263 > random 3.510 |
  | BI | G\* 6.673 > student 6.490 > RL 6.310 > B-fan 5.962 |

  - G\*, the cost-aware planner, sits 0.582 nats below RL on g_T (derived) and 0.363 nats above it on BI.
  - RL reaches the highest g_T with 3.0 probes and 136.8° of travel, against G\*'s 3.87 probes and 46.9°.
  - In v3 S12, g_T(G\*) 5.299 was also below both learned policies (5.368 each; `v3:14_h2_analysis`).
  - The observation, in two cells, is that g_T and grid BI rank G\* differently. The reason is not identified by this
    record: the instruments differ (contrastive J 16 / L 4,095 vs sub-8 grid) and so do the episode ranges (0–499 vs
    0–299).
- **RL lead over G\* fits RL's travel pattern.** G\* − RL success is +13.0 pp (ci95 [+6.4, +19.4]), against +7.0 pp in
  S12 (ci95 [+0.2, +13.7]). Where travel matters, the RL policy, which always stops at 3 probes and travels 2.9× as far
  as G\* (derived: 136.8 / 46.9), loses more ground on success.
- **Share of the G\*–RL gap covered by the student** (derived, no interval, not pre-registered): (0.4511 − 0.4233) /
  (0.5533 − 0.4233) = 21 %. This should not be reported as gap closure. v4 has no gap-closure rule, and the student −
  RL success ci95 contains 0.

### 2.3 Learned policies versus the travel-nearest heuristic

- **In S2 the student beats B-fan on test3.** Success is +8.1 pp (ci95 [+1.7, +14.7]) and BI +0.528 (ci95 [+0.420,
  +0.637]).
- **In S12 it did not** (`v3:14_m4_analysis.exploratory_b_fan`): success +2.2 pp, ci95 [−2.8, +7.3]; BI +0.226.
- **B-fan − G\*** is −18.3 pp in S2, against −6.7 pp in S12.
- **What this shows.** S2 is a cell where not travelling is costly, and there the distilled student is measurably better
  than a no-learning heuristic.
- **Caveat.** This is the first such evidence in the record, and the most useful positive v4 row, but it is
  exploratory: one cell, ci95, no multiplicity correction, five success contrasts.
- **RL vs B-fan** is +5.3 pp in point terms (derived: 0.4233 − 0.3700), with no interval in the data.
- **Identical B-fan travel in both cells is expected.** B-fan's travel (1.454160502737537°) is the same to all digits as
  v3 S12 (`v3:14_behaviour.methods.b_fan`, n = 300).
  - B-fan is belief-free, and its actions do not depend on κ.
  - I checked the record header of `results/v4/test3/S_k2_b_fan_000.jsonl`: it was run with κ 2.0 and τ 4.7.
  - Success and BI differ between the cells (0.37 vs 0.36; 5.962 vs 5.973), so the row is not a copy.

### 2.4 E5: reduced-compute G\* versus the students (S12)

- **Success differences are not resolved for either reduced planner.**
  - Against student_rem: −2.2 pp and −0.6 pp.
  - Against student_long: −5.0 pp and −3.3 pp.
  - Every ci95 contains 0. The g125 − student_long interval only just does: its upper end is +0.0011.
- **Both reduced planners lose BI against both students, every ci95 excluding 0.**
  - g125: −0.231 / −0.271.
  - g500: −0.162 / −0.203.
- **Against full G\***, g125 is −6.7 pp (ci95 [−12.0, −1.0]) and g500 is −5.0 pp (ci95 [−11.0, +1.3]).
- **Agreement with the v3 pilot.** These complete n = 300 rows sit close to the incomplete pilot3 rows of
  `v3:14_rb_frontier` (g125_512_16 0.3817, n = 186; g500_512_4 0.3898, n = 177). The pilot3 latencies were 0.0182 s
  and 0.0441 s; E5 logs 0.0208 s and 0.0460 s.
- **Permitted reading.** At logged median per-decision latencies of 20.8 ms and 46.0 ms (eval3 on free runners), neither
  reduced G\* exceeds the distilled students. Both are lower on BI, and success is unresolved.
- **No cost claim.** The latencies are not Lat′ numbers. The v3 student figure of 0.408 ms per decision (`v3-14` §1.7)
  comes from a different protocol, and the student also needs a 0.204 s per-episode PF read-out. A ratio across these
  would mix protocols.

### 2.5 Seed behaviour

- **Test3 success range across seeds** (derived): student 6.3 pp (0.4133–0.4767); RL 5.7 pp (0.3967–0.4533).
- **Comparison with S12.** There the student range was 1.0 pp and RL's 7.7 pp (`v3:14_derived`). The S2 students are
  no longer tighter than RL. Seed 602 is the outlier on test3 (0.4133). On val3, seed 603 was the best seed and 601 the
  worst.
- **RL training g_T.** Final values are 6.340 / 6.243 / 5.989: mean 6.191, sample SD 0.181 (derived). This is the
  training stream, not test3.

---

## 3. Statistical Checks

### 3.1 Recomputations (all consistent with the data block)

- **D4 threshold** (derived): −0.04 + 1.645·0.0218039·√0.5 = −0.04 + 0.02536 = −0.01464, which matches `threshold`
  −0.0146379. max(−0.02, −0.01464) = −0.01464.
- **D4 means** (derived):
  - Success: 0.486 − 0.514 = −0.028, and mean(−0.036, −0.028, −0.020) = −0.028.
  - BI: 6.56256 − 6.66743 = −0.10487 = mean(−0.11844, −0.12271, −0.07347).
- **test3 S2 rows** (derived):
  - Student success: mean(0.4633, 0.4133, 0.4767) = 0.4511. RL: mean(0.3967, 0.4200, 0.4533) = 0.4233.
  - All ten point diffs equal the row differences, e.g. 6.4901 − 6.3103 = 0.1797 and 5.9619 − 6.6731 = −0.7112.
- **H2**: 5.53406 − 5.97926 = −0.44520 (derived), and p_greater + p_less = 1.0000.
- **E5**: all twelve point diffs equal the row differences (derived), e.g. 6.0373 − 6.2483 = −0.2110.
- **Provenance check: g125 vs v3 B-fan.**
  - g125_512_16 success (0.36) and its −G\* ci95 [−0.12, −0.01] are identical to v3 B-fan on S12 test3
    (`v3:14_m4_analysis.exploratory_b_fan`).
  - I compared the per-episode files `results/v4/e5/S_k12_g125_512_16_*.jsonl` and
    `results/v3/test3_sub8/S_k12_b_fan_*.jsonl`. Success agrees on 230 of 300 episodes, both total 108 successes, and BI
    matches on 1 of 300 episodes.
  - The two rows are different data whose totals coincide. The row is not a mislabelled copy.

### 3.2 Robustness of the decisions

- **D4.**
  - Complete, n = 500, with all three seeds present.
  - Clause (i) fails by 0.61 SE.
  - With the rule's construction, a student with true Δ = 0 would clear the threshold with probability about Φ(0.01464 /
    0.0218) ≈ 0.75 (derived, normal approximation). The rule is strict by design, but it is pre-registered and stands.
  - There is no remedy round, so the D4 verdict is final.
- **H2-S2.** The LB is 0.85 nats below the threshold (derived: 0.10 − (−0.7485)). No plausible change of instrument
  noise would reverse a non-detection.
- **Random row** (n = 190 of 300, still running). It enters no paired contrast and no rule. The G\* − random success
  difference is 42.2 pp in point terms (derived: 0.5533 − 0.1316), unpaired and on different n.
- **Anomaly 1** (RL re-run after the .gitignore loss): final training g_T differs by about 0.01 nats from the lost run
  (task context). This is small next to the −0.445 H2 difference and the 0.181 training-SD.
- **Anomaly 2** (early-stopped jobs were completed): every v4 analysis block reports `complete: true` with the planned n,
  except the random row.

### 3.3 The val3 / test3 discrepancy (anomaly 4)

| Split | Student − G\* success | Interval | G\* success | Student success |
|---|---|---|---|---|
| val3 0–499 | −2.80 pp | SE 2.18 pp | 0.514 | 0.486 |
| test3 0–299 | −10.22 pp | ci95 [−16.56, −4.33] | 0.553 | 0.451 |

- **Size of the difference** (derived): −7.4 pp.
  - Approximate test3 SE from the ci95 width: 0.1222 / 3.92 ≈ 3.1 pp (derived).
  - Treating the splits as independent (they share students and seeds, so this is crude), the difference is about 1.9
    combined SE (derived).
  - That is borderline, and no test of it was pre-registered.
- **Candidate explanations** (none tested):
  - (a) episode-sampling noise across disjoint splits;
  - (b) the test3 pipeline: no-grid actions, then a sub-8 re-read, with the students' actions produced in the sandbox
    (Python 3.13.18 / numpy 2.5.3) and G\*'s on runners (Python 3.12.15 / numpy 2.5.4). Against this, the same pipeline
    gave matching splits in v3 (−4.40 vs −4.44 pp);
  - (c) a seed-specific effect: seed 602 drops from −2.8 pp on val3 to −14.0 pp on test3 (derived).
- **Reporting rule.** Both read-outs are pre-registered and should be reported side by side. Only val3 decides D4, and
  that decision is a fail in either reading.

### 3.4 Intervals and multiplicity

- **No multiplicity correction anywhere.** The S2 test3 block has 10 intervals and E5 has 12. Per the amendment, none is
  a test.
- **Which intervals exclude 0.** At the ci95 level:
  - S2 test3: every interval except student − RL success.
  - E5: every BI interval, but only g125 − G\* among the success intervals.
- **These are descriptive statements.** With 22 exploratory intervals, about one is expected to exclude 0 by chance
  under a global null (derived: 22 × 0.05). The large BI effects (|Δ| ≥ 0.16 with intervals well clear of 0) are not at
  risk from this. The borderline ones are, namely student − B-fan success (LB +1.7 pp) and g125 − G\* success (UB −1.0
  pp).
- **H2 power.** The one-sided half-width is (−0.1616 − (−0.7485)) / 2 = 0.293 nats (derived), similar to v3's 0.307
  (derived from `v3:14_h2_analysis.bootstrap`). As in v3 (`v3-14` M3), only a large true advantage could have passed,
  and here the estimate lies on the wrong side.

### 3.5 Tests not run (recommendations only)

1. A paired val3 vs test3 contrast for the S2 students, or a re-read of val3 through the test3 no-grid → regrid
   pipeline. This would separate pipeline from split effects (§3.3).
2. A one-sided test of g_T(RL) − g_T(student) > 0, for any sentence claiming that RL wins on g_T. It is currently only
   implied by the bootstrap UB.
3. Per-seed g_T on test3 for v4 (not in the data block).
4. Train-set R̄ and top-1 for the S2 students. The v3 label-fit rule (`v3:14_labelfit`) is defined on train R̄ and top-1,
   which v4 does not report, so the encoder/under-fit diagnosis cannot be made for S2 (§4).

---

## 4. Limitations

1. **One cell.** Every S2 row is S, κ = 2, τ = 4.7, n\* = 4. There is no G5′ S2 cell, so δ = 4 pp is borrowed from S12
   and there is no ε_c (the BI floor −0.15 alone applies).
2. **Exploratory status.** All S2 test3 rows, H2's reverse-direction reading and all of E5 use ci95 with no multiplicity
   correction.
3. **No new HP grid** (a stated deviation). Students reuse S12 hp 0 and train a fixed 200 epochs per round, keeping the
   last checkpoint. Every round ended at `max_epochs`, so no convergence evidence exists.
4. **Student validation regret does not improve over DAgger.**
   - val_R̄ moves from 0.300–0.312 (r0) to 0.298–0.322 (r2). It rises for 601 (0.3084 → 0.3216) and is roughly flat for
     602 and 603.
   - Training decisions grow 10,499 → about 16,760, i.e. 1.60× (derived).
   - val_R̄ is on label-distribution shards, not student-visited states.
   - The v3 regret scale (held-out R̄ 0.184–0.201 for the remedy; `v3:14_labelfit`) comes from a different κ, so the
     values cannot be compared.
   - The v3 under-fit threshold (train R̄ > 0.25) cannot be applied, because v4 reports no train R̄. That the v4 held-out
     values all exceed 0.25 is a raw fact, not a rule outcome.
5. **The RL comparator** is v3 config 2, selected in S12 on `val_v2` (`v3-14` §4.3), and was not re-tuned for S2. It
   ran to the episode cap without using the plateau. RL always ends at 3.0 probes.
6. **Evaluator.** Sub-8 grid convergence is still unshown (the v3 E′ gate failed). The test3 rows mix machines
   (runners vs sandbox) and pipelines (no-grid then regrid), unlike val3.
7. **E5 latency** is the eval3-logged median on free runners, not Lat′. No speed or cost comparison is permitted.
8. **Incomplete row.** Random on test3 is n = 190 of 300.
9. **Not in v4** (already declared): the H3 full-512 / local-offset screen, an in-domain positive control, more than 3
   seeds, wider sweeps, and Lat′ latency for the reduced G\*.
10. **Compute and process.** About 100 CPU-h in total. This is the last allowed refine cycle, so no further remedy is
    possible in this record.

---

## 5. Conclusion

| Claim | Verdict | Evidence |
|---|---|---|
| **D4** (S2 learnability) | **FAIL** → "not shown to reach G\* in S2 either" | (i) −2.80 pp < −1.46 pp ✗; (ii) −0.105 ≥ −0.15 ✓; (iii) −3.6 / −2.8 / −2.0 pp > −4 pp ✓; n = 500; no remedy |
| **H2-S2** | **not detected** | Δg_T = −0.445, LB −0.749 ≤ +0.10. Exploratory: UB −0.162 < 0, i.e. RL scores higher on its own objective |
| **E5** | reported | At logged latency (20.8 / 46.0 ms per decision), both reduced G\* lose BI against both students (ci95 exclude 0, −0.16 to −0.27 nats); success is unresolved (−0.6 to −5.0 pp, all ci95 contain 0) |
| **v3 verdicts** | **unchanged** | Row 4 (D3 failed twice), H2 rejected in S12, H3 Hold |

What v4 adds to the characterisation paper (all exploratory, one cell):
- (i) **S2 travels, as designed.** G\* travels 46.9° per episode against 6.1° in S12, and the student imitates the
  travel (39.1°) but still falls short of G\*: −2.8 pp on val3 (D4 fail) and −10.2 pp on test3 (ci95 [−16.6, −4.3]).
- (ii) **Student vs the travel-nearest heuristic.** In S2 the student exceeds B-fan on success (+8.1 pp, ci95 [+1.7,
  +14.7]) and BI (+0.53 nats). In S12 it was not separable from B-fan (+2.2 pp, ci95 [−2.8, +7.3]).
- (iii) **Student vs RL depends on the instrument.** On grid BI the student is ahead (+0.18 nats, ci95 [+0.09, +0.27]).
  On g_T, RL's own objective, RL is ahead (−0.445 nats, UB −0.162). Success is unresolved. g_T ranks G\* below both
  learned policies in both cells.
- (iv) **Reduced G\* does not beat the student** at 20–46 ms per logged decision. It is lower on BI, and success is
  unresolved.

**Before writing.**
- The val3 / test3 gap discrepancy (−2.8 vs −10.2 pp) must be stated next to the D4 result. Its cause is untested.
- The B-fan and g_T findings are exploratory and must not be worded as tests.
