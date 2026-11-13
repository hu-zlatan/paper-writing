# Stage 14 RESULT_ANALYSIS [v6] — merged analysis

Merge of pass 1 (`14_analysis_pass1.md`, fresh subagent, template verbatim on the unaltered
`results/v6/14_v6_analysis.json` + amendment v6.0 rules) and pass 2 (`14_analysis_pass2.md`, fresh subagent, the
template's adversarial area-chair prompt; 2 S / 11 M / 8 m; no pre-registered verdict misreported). Prompts in
`results/v6/prompts/`. **Pass-2 items are binding: where the pass-1 body below disagrees with an item in Appendix A,
the Appendix A rewrite is the analysis of record.** The main session spot-checked item 3 against the JSON
(A16-2 0–499: student − G\* = −0.28 pp, so the student point estimate is below G\* in all 5 cells).

## Binding summary (supersedes pass-1 §5 "Bottom line")

- **H6a (pre-registered):** in every cell and both windows, neither a difference nor equivalence within 4 pp is shown
  (Holm). The student's success point estimate is 0.3–3.7 pp below G\* (both G\* runs) in **all five** cells on 0–499;
  deficits up to about 7–8 pp (ci95) cannot be excluded; in S4 the ci90 lies entirely below 0 on both windows. Ball-info
  is significantly lower for the student in S4 and S8 (S2 not after Holm / not on the fresh window). G\*'s own
  run-to-run difference is of similar size.
- **H6b (pre-registered):** by Holm the student is more accurate than g125_512_16 in all 5 cells and than g500_512_4 in
  S4 and A16-2 (7 / 10 on 0–499, 2 / 10 on the fresh 300–499 window); against g500_512_4 in S2 / S8 / S12 no accuracy
  difference is shown. The student is 62–389× faster than both reduced planners (v5 point medians). Not "dominates".
- **H6c (pre-registered):** no DAgger (round 2) vs behaviour-cloning (round 0) difference detected in any cell.
- **E12 (report-only):** switching the evaluator grid sub 8 → sub 16 flips 4–13 % of episode outcomes in the S cells and
  moves student − G\* by about 4 pp or more in 3 of 4 S cells, i.e. as large as the equivalence margin.
- **Report-only v5-row updates:** student > H\* in all cells, but the pilot-chosen H\* is not the best test5 heuristic
  in S4, S8, S12; the RL-objective inversion persists in S2 / S4; H5b travel-slope test uninformative (CI ≈ 26 pp per
  100°).

---

# Pass 1 body

# Stage 14 (v6), pass 1: analysis of E8–E12

Source: `results/v6/14_v6_analysis.json` (as reproduced in the stage-14 prompt), produced by `code/analysis_v6.py` under the pre-registered rules of `docs/07c_amendment_v6_0.md` (and addendum v6.1). Every number below is either copied from that read-out or is plain arithmetic on its values. Arithmetic results are marked "(derived)" and have no CI attached. Success means sub-8 success, and pp means percentage points. Windows: **0–499** is primary and **300–499** is the fresh check. All cells are complete: 500 episodes per method on 0–499, 200 on 300–499, 100 in E12, and g_T is complete everywhere.

---

## 1. Metrics Summary

### 1.1 Success on test5 0–499 (sub 8)

Student, r0 and RL columns are 5-seed means. "G\* r1" is the v5 record plus E8, and "G\* r2" is E10 (`--run-salt r1`).

| Cell | G\* r1 | G\* r2 | Student r2 (seed range) | Student r0 (BC) | g500_512_4 | g125_512_16 | H\* (which) | RL (cfg 6) |
|---|---|---|---|---|---|---|---|---|
| S2 | 0.518 | 0.532 | 0.4988 (0.464–0.526) | 0.4856 (derived) | 0.462 | 0.406 | 0.432 (b_cov) | 0.4132 (derived) |
| S4 | 0.496 | 0.494 | 0.4576 (0.432–0.482) | 0.4492 (derived) | 0.390 | 0.402 | 0.368 (b_fan) | 0.3964 (derived) |
| S8 | 0.432 | 0.464 | 0.4188 (0.408–0.436) | 0.4116 (derived) | 0.372 | 0.356 | 0.344 (b_cov) | 0.3932 (derived) |
| S12 | 0.434 | 0.434 | 0.4144 (0.398–0.428) | 0.4140 (derived) | 0.390 | 0.358 | 0.358 (b_fan) | 0.3576 (derived) |
| A16-2 | 0.474 | 0.498 | 0.4832 (0.464–0.496) | 0.4884 (derived) | 0.374 | 0.330 | 0.312 (b_fan) | 0.2144 (derived) |

The derived r0 and RL means agree with the read-out's H6c and student − RL differences. For example, in S2 0.4988 − 0.4856 = 0.0132 = H6c diff.

The other baselines, on 0–499:
- b_spread is near zero everywhere (0.006–0.074).
- rl_success (S2 / S12): seed means 0.376–0.420 in S2 and 0.302–0.390 in S12.

### 1.2 Accuracy–latency frontier

Latency is the v5 E6 job-1 median decision latency, not re-timed in v6. Success is on 0–499.

| Cell | G\* latency (s) / success | g500_512_4 | g125_512_16 | Student | G\* / student latency (derived) |
|---|---|---|---|---|---|
| S2 | 4.880 / 0.518 | 0.194 / 0.462 | 0.116 / 0.406 | 0.000500 / 0.4988 | ≈ 9,770× |
| S4 | 3.375 / 0.496 | 0.141 / 0.390 | 0.080 / 0.402 | 0.000494 / 0.4576 | ≈ 6,830× |
| S8 | 1.234 / 0.432 | 0.061 / 0.372 | 0.030 / 0.356 | 0.000358 / 0.4188 | ≈ 3,450× |
| S12 | 0.910 / 0.434 | 0.048 / 0.390 | 0.022 / 0.358 | 0.000358 / 0.4144 | ≈ 2,540× |
| A16-2 | 2.702 / 0.474 | 0.098 / 0.374 | 0.058 / 0.330 | 0.000326 / 0.4832 | ≈ 8,280× |

- The reduced planners are about 19–47× faster than G\* (derived).
- They are still about 60–390× slower than the student (derived). For example, S12 g125 is 0.0220 / 0.000358 ≈ 62×, and S2 g500 is 0.194 / 0.000500 ≈ 389×.
- They lose 4.4–14.4 pp of success relative to G\* run 1. The smallest loss is S12 g500 (−4.4 pp) and the largest is A16-2 g125 (−14.4 pp).
- In S4 the larger-budget g500 (0.390) is slightly below g125 (0.402).

### 1.3 Behaviour and evaluator diagnostics

**Travel (rad, 0–499).** The student travels less than G\* in every cell:

| Cell | Student | G\* run 1 |
|---|---|---|
| S2 | 0.487–0.674 | 0.820 |
| S4 | 0.201–0.281 | 0.405 |
| S8 | 0.091–0.099 | 0.160 |
| S12 | 0.044–0.056 | 0.110 |
| A16-2 | 0.290–0.347 | 0.381 |

- RL travels the most: 2.06–2.55 in S2, and up to 2.07 in A16-2.
- RL uses fewer probes: about 3.0 against a budget of 4 in the S cells. In A16-2, four of five seeds use 2.0 probes against a budget of 3.

**G\* first-decision agreement (run 2 vs run 1, same state at step 0).**

| Window | S2 | S4 | S8 | S12 | A16-2 |
|---|---|---|---|---|---|
| 0–499 | 0.274 | 0.402 | 0.452 | 0.426 | 0.314 |
| 300–499 | 0.245 | 0.415 | 0.445 | 0.420 | 0.305 |

**G\* run 2 − run 1 success.** None of these differences is significant.

| Window | S2 | S4 | S8 | S12 | A16-2 |
|---|---|---|---|---|---|
| 0–499 | +0.014 | −0.002 | +0.032 | 0.000 | +0.024 |
| 300–499 | +0.050 | −0.010 | +0.040 | −0.020 | +0.050 |

On 0–499 the 95% CIs have half-widths of roughly 4–5 pp. For example, S8 is [−0.010, 0.076].

**E12: sub-8 → sub-16 flip rate on episodes 0–99.**

| Cell | G\* | Students (5 seeds) |
|---|---|---|
| S2 | 0.10 | 0.04–0.13 |
| S4 | 0.08 | 0.05–0.13 |
| S8 | 0.07 | 0.06–0.09 |
| S12 | 0.07 | 0.04–0.07 |
| A16-2 | 0.01 | 0.00–0.01 |

---

## 2. Comparative Findings

### 2.1 H6a: student vs G\*, with G\* run variance (Δ = student(5) − G\*(runs 1+2))

| Cell | Δ 0–499 [ci95] | p | ci90 | p_TOST (lower / upper) | Δ 300–499 [ci95] | p_TOST fresh |
|---|---|---|---|---|---|---|
| S2 | −0.0262 [−0.0688, 0.0168] | 0.222 | [−0.0616, 0.0092] | 0.2621 (0.2621 / 0.0014) | −0.036 [−0.114, 0.042] | 0.4524 |
| S4 | −0.0374 [−0.0784, 0.0024] | 0.0678 | [−0.0716, −0.0036] | 0.4559 (0.4559 / 0.0003) | −0.053 [−0.1165, 0.0095] | 0.6561 |
| S8 | −0.0292 [−0.0704, 0.0136] | 0.1666 | [−0.0640, 0.0060] | 0.2908 (0.2908 / 0.0004) | −0.034 [−0.095, 0.028] | 0.4211 |
| S12 | −0.0196 [−0.0532, 0.0148] | 0.2594 | [−0.0480, 0.0088] | 0.1157 (0.1157 / 0.0009) | −0.016 [−0.067, 0.035] | 0.1659 |
| A16-2 | −0.0028 [−0.0496, 0.0436] | 0.9074 | [−0.0412, 0.0358] | 0.0548 (0.0548 / 0.0348) | +0.001 [−0.077, 0.080] | 0.1557 |

**Result.** Under the pre-registered wording, every cell in both windows is **"neither a difference nor equivalence shown"**.

- **Sign pattern.** The point estimate is negative in 4/5 cells on 0–499, with gaps of 0.28 to 3.74 pp. On the fresh window it is negative in 4/5 cells (1.6 to 5.3 pp) and +0.1 pp in A16-2. Following the rule, no pooled estimate is formed.
- **What blocks equivalence.** In every cell the upper margin (+4 pp) is rejected unadjusted (p_upper 0.0003–0.0348). The student is therefore not more than 4 pp *better* than G\*. What fails is the lower margin: the data cannot exclude the student being more than 4 pp *worse*.
- **A16-2 comes closest.** Its gap is −0.28 pp and its ci90 lower bound is −4.12 pp. Its p_TOST of 0.0548 misses even before Holm.
- **S4 is the weakest cell for the student.** Its ci90 [−0.0716, −0.0036] excludes 0, and so does the fresh ci90 [−0.106, −0.0005]. The two-sided 95% interval still includes 0 (p = 0.0678), so no difference is claimed, but S4 is where a real deficit of a few pp is most plausible.
- **The power prediction held.** The design note predicted 90% half-widths of 3.5–4 pp. The observed half-widths are 3.54 (S2), 3.40 (S4), 3.50 (S8), 2.84 (S12) and 3.85 (A16-2) pp (derived). With δ = 4 pp, equivalence needed point gaps of at most about 0.2–1.2 pp. Only A16-2 had such a gap, and its interval was the widest.
- **Against G\* run 1 alone** (v5 row update), the gaps are −1.92, −3.84, −1.32, −1.96 and +0.92 pp. None is significant (p 0.0988–0.6964). This matches v5's "0.2–2.5 pp below, not significant" pattern, except that S4 widens on the fresh window (−5.8 pp, ci [−0.129, 0.012]).
- **Teacher variance is comparable to the gap.** G\* run 2 − run 1 reaches +3.2 pp on 0–499 (S8) and +5 pp on the fresh window (S2, A16-2). These are the same magnitude as the student − G\* gaps, and the student's own seed spread is 2.8–6.2 pp (derived from the seed ranges).

**Ball-info (BI), reported beside success and not Holm-controlled by the rules.** The student's BI is lower than G\*'s in three cells:

| Cell | BI diff [ci95] | p |
|---|---|---|
| S2 | −0.093 [−0.168, −0.014] | 0.0206 |
| S4 | −0.138 [−0.202, −0.075] | 0.0 |
| S8 | −0.103 [−0.172, −0.033] | 0.0048 |
| S12 | −0.055 [−0.115, 0.003] | 0.0664 |
| A16-2 | +0.024 [−0.080, 0.130] | 0.638 |

- A Holm step-down over these 5 BI p-values would keep S4 and S8 only (derived, not a registered test).
- On the fresh window, S4 (−0.128, p = 0.0206) and S8 (−0.093, p = 0.0354) remain below 0.05 unadjusted.
- So the student's posterior is measurably less informative than G\*'s in S2/S4/S8, even where success differences are not detectable.

### 2.2 H6b: student vs reduced planners (Holm over 10 contrasts)

| Cell | Student − g125_512_16 [ci95], p | Holm | Student − g500_512_4 [ci95], p | Holm |
|---|---|---|---|---|
| S2 | +0.0928 [0.044, 0.140], 0.0 | **reject (+)** | +0.0368 [−0.012, 0.087], 0.1378 | no |
| S4 | +0.0556 [0.014, 0.098], 0.0072 | **reject (+)** | +0.0676 [0.024, 0.112], 0.0016 | **reject (+)** |
| S8 | +0.0628 [0.022, 0.104], 0.0022 | **reject (+)** | +0.0468 [0.004, 0.090], 0.0314 | no |
| S12 | +0.0564 [0.013, 0.099], 0.0098 | **reject (+)** | +0.0244 [−0.018, 0.067], 0.2688 | no |
| A16-2 | +0.1532 [0.102, 0.204], 0.0 | **reject (+)** | +0.1092 [0.058, 0.159], 0.0 | **reject (+)** |

**Result: 7/10 contrasts rejected, all with a positive sign.**

- The student is more accurate than g125_512_16 in **all 5 cells**.
- It is more accurate than g500_512_4 in **S4 and A16-2**.
- I verified the Holm step-down by hand. The 7th-smallest p (0.0098) is ≤ 0.05/4 = 0.0125, and the 8th (0.0314) is > 0.05/3 ≈ 0.0167.
- No contrast is negative: all 10 point estimates are positive.
- On the fresh window (200 episodes), only S4 g125 (+0.112, p = 0.0002) and A16-2 g125 (+0.136, p = 0.0012) survive Holm. S12 has a negative point estimate vs g500 (−0.011 [−0.072, 0.051]), which is not significant.

### 2.3 H6c: DAgger (r2) vs behaviour cloning (r0)

| Cell | r2 − r0 success [ci95], p | BI [ci95], p |
|---|---|---|
| S2 | +0.0132 [−0.0224, 0.0480], 0.453 | +0.0448 [−0.0010, 0.0939], 0.0564 |
| S4 | +0.0084 [−0.0228, 0.0400], 0.5968 | +0.0355 [−0.0163, 0.0869], 0.1764 |
| S8 | +0.0072 [−0.0196, 0.0336], 0.5984 | +0.0162 [−0.0157, 0.0482], 0.3078 |
| S12 | +0.0004 [−0.0280, 0.0304], 0.997 | +0.0098 [−0.0278, 0.0491], 0.6188 |
| A16-2 | −0.0052 [−0.0316, 0.0208], 0.6834 | −0.0077 [−0.0773, 0.0590], 0.8056 |

**Result:** "DAgger improves success over BC" is **not detected** in any cell, in either window (fresh p 0.5372–0.9208).

- The point gains are at most 1.3 pp, and the 95% upper bounds are at most 4.8 pp.
- This is not an equivalence result: no TOST was registered for H6c. The data do, however, bound any DAgger benefit to below about 5 pp per cell.

### 2.4 Report-only v5 row updates (0–499), labelled "v6 update of a v5 row"

**Student − H\*.**

| Cell | 0–499 [ci95] | p |
|---|---|---|
| S2 | +0.0668 [0.017, 0.117] | 0.01 |
| S4 | +0.0896 [0.051, 0.128] | 0.0 |
| S8 | +0.0748 [0.033, 0.117] | 0.001 |
| S12 | +0.0564 [0.019, 0.094] | 0.0036 |
| A16-2 | +0.1712 [0.125, 0.217] | 0.0 |

All five CIs exclude 0. On the fresh window, S2 (p = 0.0694) and S12 (p = 0.0672) are not below 0.05.

Caveat: H\* is the v5-selected heuristic, and on test5 0–499 it is not the best heuristic in two cells:
- In S8, H\* = b_cov 0.344, but b_fan has 0.368.
- In S12, H\* = b_fan 0.358, but b_cov has 0.390.

Against the best heuristic on test, the student's point margin would shrink to about +5.1 pp (S8) and +2.4 pp (S12) (derived, untested).

**Student − RL (cfg 6).**

| Cell | 0–499 [ci95] |
|---|---|
| S2 | +0.0856 [0.039, 0.131] |
| S4 | +0.0612 [0.018, 0.104] |
| S8 | +0.0256 [−0.010, 0.062] (not significant) |
| S12 | +0.0568 [0.020, 0.093] |
| A16-2 | +0.2688 [0.212, 0.322] |

**Student − rl_success.**

| Cell | 0–499 [ci95] |
|---|---|
| S2 | +0.1096 [0.066, 0.153] |
| S12 | +0.0708 [0.024, 0.116] |

On the fresh window, S12 has +0.058 with a lower bound of about 0 and p = 0.05.

**H2-v5 g_T.**
- "Student higher on the RL objective" holds **only in A16-2**: +0.709 with one-sided lower bound 0.479, and on the fresh window +0.523 with lower bound 0.121.
- RL − student g_T is significantly positive in S2 (+0.333 [0.061, 0.616]), S4 (+0.404 [0.092, 0.707]) and S8 (+0.386 [0.047, 0.714]).
- The inversion flag is **true in S2 and S4** (both windows) and false in S8, S12 and A16-2. In S2 and S4, RL is ahead on its own objective while the student is ahead on success. In S8 the success contrast is not significant.
- G\* − student g_T is not significant on 0–499 in any cell (p 0.28–0.96). On the fresh window it is significant in S8: +0.631 [0.180, 1.117], p = 0.0068.

**H5b slope (WLS, 5 cells).**
- −0.0040 per rad [−0.078, 0.071], i.e. −0.0070 per 100° [−0.137, 0.124].
- Verdict: "no trend detected over 5 cells". The Δ values feeding it are −0.0192, −0.0384, −0.0132, −0.0196 and +0.0092. The CI is about 15 pp per 100° wide, so the test is uninformative rather than evidence of "no trend".

### 2.5 E12: evaluator grid (episodes 0–99, student − G\* run 1)

| Cell | sub 8 [ci95] | sub 16 [ci95] | Shift (derived) |
|---|---|---|---|
| S2 | −0.026 [−0.114, 0.062] | −0.042 [−0.124, 0.042] | −1.6 pp |
| S4 | −0.036 [−0.136, 0.064] | +0.010 [−0.090, 0.106] | +4.6 pp |
| S8 | −0.020 [−0.116, 0.076] | +0.030 [−0.062, 0.122] | +5.0 pp |
| S12 | +0.008 [−0.060, 0.076] | −0.038 [−0.108, 0.030] | −4.6 pp |
| A16-2 | +0.050 [−0.048, 0.152] | +0.044 [−0.054, 0.142] | −0.6 pp |

- Changing only the read-out grid moves the contrast by up to 5 pp, and the sign changes in 3/5 cells. Neither grid shows any significant difference.
- The shifts do not all go in one direction. Sub 16 does not systematically favour either policy.
- In the 4 S cells, the size of the shift (1.6–5.0 pp) is comparable to or larger than the 4 pp equivalence margin.

---

## 3. Statistical Checks

- **Completeness and blinding.** `complete` and `gt_complete` are true for every cell and window. Episode counts equal `n_required` (500 / 200 / 100). The run context states that no E8–E12 outcome was read before the completeness check reached 100 %, and that the read-out script was committed first. No v5 verdict is re-tested.
- **Internal consistency, spot-checked by arithmetic.**
  - Student means minus G\* means reproduce the H6a and run-1 diffs. For S2, (0.518 + 0.532)/2 = 0.525 and 0.4988 − 0.525 = −0.0262.
  - r0 means reproduce the H6c diffs in all 5 cells.
  - RL and rl_success means reproduce the student − RL and student − rl_success diffs.
  - Frontier success values equal the means table.
- **Holm verification.**
  - H6a difference: the smallest p is 0.0678 × 5 = 0.339, so nothing is rejected.
  - H6a TOST: the smallest p is 0.0548 × 5 = 0.274, so nothing is rejected.
  - H6c: the smallest p is 0.453, so nothing is rejected.
  - H6b: 7 rejections (see 2.2).
  - Fresh-window H6b: the step-down stops at the 3rd p (0.0198 > 0.05/8 = 0.00625), leaving 2 rejections.
  - Every derivation matches the `holm` flags in the JSON.
- **TOST construction.** p_TOST = max(p_lower, p_upper), as registered. The ci90 is the matching interval: in every cell, "ci90 inside ±0.04" corresponds to p_TOST < 0.05. In A16-2 the ci90 lower bound is −0.0412 against p_TOST 0.0548, which is consistent.
- **Bootstrap resolution.** With B = 10,000, the reported p = 0.0 means p < 1e-4 (at the resampling resolution), not exactly zero. This does not affect any Holm decision.
- **Multiplicity outside the registered families.** The BI contrasts, the fresh-window replications, E12, and the report-only v5 rows are not Holm-controlled across families. Single unadjusted p-values near 0.02–0.05 in them should not be read as findings. Examples are S8 fresh G\* − student g_T, and S12 fresh student − rl_success at p = 0.05.
- **Fresh vs reused episodes.** Every primary conclusion has the same direction on 300–499:
  - H6a: no difference and no equivalence.
  - H6b: all positive except the S12 g500 point.
  - H6c: none.

  The fresh window has 200 episodes, so its CIs are about 1.6× wider (derived from the H6a half-widths). It confirms the direction of the results but adds little precision.

---

## 4. Limitations

1. **Teacher variance comes from only two G\* runs.** G\* is strongly stochastic: first-decision agreement is only 0.27–0.45, and run-to-run success differences reach 3.2 pp on 0–499 and 5 pp on 300–499. With 2 runs as "seeds", the G\* component of the bootstrap is poorly estimated. The H6a CIs could be optimistic or pessimistic.
2. **The reduced planners and H\* each have a single run (n_seeds = 1).** Their own stochasticity is not in the H6b CIs. Given G\*'s run-to-run spread, the marginal H6b rejections could be sensitive to a second planner run. The marginal ones are S12 g125 (lower bound +1.3 pp, p = 0.0098) and S4 g125 (lower bound +1.4 pp).
3. **Evaluator sensitivity.** The sub-8 → sub-16 grid change flips 0–13 % of episode outcomes in the S cells and moves the student − G\* contrast by up to 5 pp. That is larger than the 4 pp TOST margin. E12 covers only episodes 0–99 and G\* run 1, so it cannot correct the 0–499 contrasts. It only shows that success contrasts of a few pp sit within evaluator noise. A16-2 is nearly grid-insensitive (flip ≤ 0.01).
4. **The equivalence margin and the power were fixed in advance.** δ = 4 pp and 500 episodes gave the expected 90 % half-widths of 2.8–3.9 pp. Failing to show equivalence is therefore largely a power outcome, not evidence of a gap. Conversely, the S4 ci90 excludes 0, so a small deficit there cannot be ruled out.
5. **The heuristic baseline H\* is stale.** H\* was chosen in v5, and on test5 it is not the best heuristic in S8 or S12. The "student beats the best heuristic" claim is weaker there than the student − H\* row suggests.
6. **Latency is not re-measured.** The frontier uses v5 E6 job-1 medians (one machine, one job), while v6 only adds accuracy. Speed ratios such as G\*/student ≈ 2,500–9,800× and reduced/student ≈ 60–390× are point medians without dispersion.
7. **Scope.**
   - Simulated TouchBED only, 5 cells, frozen v5 policies, and no hardware.
   - Agreement with the teacher is measured only at the first decision.
   - Episodes 0–299 were seen in v5, so the primary 0–499 window is not fully fresh.
   - BI and g_T secondary results are not multiplicity-controlled.
8. **Operations.** Jobs were time-guarded and resumed with identical commands, and one run (221) was cancelled and resumed. The analysis assumes resumption is outcome-neutral, which per-episode determinism supports but this read-out does not directly test.

---

## 5. Conclusion

- **H6a: neither a difference nor equivalence shown.** In no cell can the student be declared different from or equivalent to G\* within 4 pp.
  - With teacher variance included and 500 episodes, the student is 0.3–3.7 pp below G\* in 4/5 cells and level in A16-2.
  - The student is reliably *not more than 4 pp better* (upper margin rejected everywhere), but a deficit beyond 4 pp cannot be excluded.
  - A16-2 came closest to equivalence (p_TOST = 0.0548) and S4 is the weakest cell (ci90 entirely below 0).
  - The gap is the same size as G\*'s own run-to-run variation and the evaluator-grid shift, so success alone at this sample size cannot settle it.
  - Ball-info shows a clearer deficit in S2, S4 and S8.
- **H6b: the learned student is a better fast policy than shrinking the planner.**
  - The student beats g125_512_16 in all 5 cells and g500_512_4 in 2 cells (7/10 Holm rejections, all positive, no negative sign).
  - It does so while being about 60–390× faster than either reduced planner.
  - Shrinking G\* by about 20–45× in latency costs 4–14 pp of success, more than the student loses.
- **H6c: DAgger improvement over BC is not detected.** Round 0 and round 2 differ by at most 1.3 pp, with upper bounds of at most 4.8 pp. Most of the student's accuracy comes from behaviour cloning on G\*.
- **v5 row updates.**
  - The student stays above H\* in all cells and above RL in 4/5 cells.
  - The RL-objective inversion persists in S2 and S4.
  - The H5b travel-slope test remains uninformative.

**Bottom line for the paper.** The defensible claim is "on the accuracy–latency frontier, a distilled student dominates reduced planners and approaches G\* to within a few pp, with no detectable cost and no shown equivalence". It is not "the student matches G\*".

**Possible memory items (for the main session).** None about the user. All facts here come from the stage-14 prompt file, not from memory.


---

# Appendix A — Pass 2 (binding corrections)

# Stage 14 (v6), pass 2: area-chair scrutiny of `14_analysis_pass1.md`

Source checked: the full read-out JSON and pre-registered rules in `results/v6/prompts/stage14_pass1_user.txt`. All arithmetic below was recomputed from that JSON. Keys are written as `cell.window.path`.

Severity: **S** = changes a conclusion, **M** = misstated number or overreach, **m** = wording.

Overall, the tables are transcribed correctly. Every success, CI, p-value, TOST, Holm flag, travel, agreement, flip-rate and latency value in the tables matches the JSON. The derived r0/RL means, the latency ratios (G\*/student 2,544–9,767×, G\*/reduced 19.0–47.0×, reduced/student 62–389×) and the Holm step-downs also reproduce. The problems are in the prose, the summaries and the bottom line.

---

1. **[S] Bottom line: "approaches G\* to within a few pp, with no detectable cost".**
   - *Evidence:*
     - "Within a few pp" is true only of the point estimates (0.28–3.74 pp). The intervals reach much further: `S4.0-499.H6a.success.ci95` = [−0.0784, 0.0024], and the fresh window reaches −0.1165 (`S4.300-499.H6a.success.ci95`). The registered TOST could not exclude gaps beyond 4 pp in any cell.
     - "No detectable cost" contradicts the analysis's own BI section. `H6a.ball_info.p_two_sided` is 0.0 in S4, 0.0048 in S8 and 0.0206 in S2, all with negative diffs.
     - It also contradicts the success data: `S4.0-499.H6a.success.tost.ci90` = [−0.0716, −0.0036] lies entirely below 0, and so does the fresh ci90 [−0.106, −0.0005].
   - *Rewrite:* "The student's success point estimate is 0.3–3.7 pp below G\* in every cell, with no registered difference and no registered equivalence; deficits of up to about 7–8 pp (ci95) cannot be excluded, and its ball-info is significantly lower in S4 and S8."

2. **[S] Bottom line: "a distilled student dominates reduced planners".**
   - *Evidence:*
     - Holm rejects only 7/10 contrasts. Student − g500_512_4 is not rejected in S2 (p 0.1378), S8 (0.0314) or S12 (0.2688) (`*.0-499.holm.H6b_g500_512_4` = false).
     - On the fresh window, only 2/10 contrasts survive (`S4/A16-2.300-499.holm.H6b_g125_512_16`). Student − g500 there is +0.004 in S2 (p 0.9268) and −0.011 in S12 (p 0.7368).
     - The registered wording permits "more accurate than a reduced planner" only where Holm rejects.
   - *Rewrite:* "The student is faster than both reduced planners in every cell (62–389×, v5 point medians) and, by Holm, more accurate than g125_512_16 in all 5 cells and g500_512_4 in S4 and A16-2; against g500_512_4 in S2/S8/S12 no accuracy difference is shown."

3. **[M] §2.1 and §5: "The point estimate is negative in 4/5 cells on 0–499 … 0.28 to 3.74 pp" and "0.3–3.7 pp below G\* in 4/5 cells and level in A16-2".**
   - *Evidence:* `*.0-499.H6a.success.diff` is −0.0262, −0.0374, −0.0292, −0.0196 and −0.0028, so all five are negative. The stated range 0.28–3.74 itself includes A16-2, which makes the "4/5" wording internally inconsistent. (4/5 is correct only for the fresh window, where A16-2 is +0.001.)
   - *Rewrite:* "On 0–499 the point estimate is negative in all 5 cells (−0.28 to −3.74 pp, A16-2 essentially level); on 300–499 it is negative in 4/5 and +0.1 pp in A16-2."

4. **[M] §2.4 and Limitation 5: "on test5 0–499 [H\*] is not the best heuristic in two cells (S8, S12)".**
   - *Evidence:*
     - In S4, H\* = b_fan (`S4.0-499.v5_row_updates.H_star`) with success 0.368, but `S4.0-499.means.b_cov.success` = 0.416. That makes three cells.
     - A16-2 is also not strictly best: b_fan 0.312 vs b_cov 0.314.
     - Against the best heuristic, the student's margin in S4 shrinks from +8.96 to about +4.2 pp (derived: 0.4576 − 0.416).
   - *Rewrite:* "H\* is not the best test5 heuristic in S4 (b_cov 0.416 vs b_fan 0.368), S8 and S12 (and trivially A16-2); against the best heuristic the student's untested point margin would be about +4.2 (S4), +5.1 (S8) and +2.4 pp (S12)."

5. **[M] §2.1: the BI deficit is "measurably less informative … in S2/S4/S8"; §5: "Ball-info shows a clearer deficit in S2, S4 and S8".**
   - *Evidence:*
     - The analysis's own Holm step-down over the 5 BI p-values keeps only S4 and S8. S2 is 0.0206 × 3 = 0.062 > 0.05.
     - The S2 BI result also fails on the fresh window: `S2.300-499.H6a.ball_info.p_two_sided` = 0.1612, ci95 [−0.256, 0.044].
     - BI is not a registered decision family.
   - *Rewrite:* "Student BI is lower than G\*'s in S4 and S8 even after an (unregistered) Holm adjustment and on the fresh window; S2 is nominally lower on 0–499 only (p = 0.0206)."

6. **[M] §2.1: the run-1-only gaps "match v5's '0.2–2.5 pp below, not significant' pattern, except that S4 widens on the fresh window".**
   - *Evidence:*
     - On 0–499, S4 is already −3.84 pp (`S4.0-499.v5_row_updates.student_minus_gstar_run1_success.diff` = −0.0384), outside 0.2–2.5.
     - A16-2 flips sign to +0.92 pp (`A16-2.0-499…diff` = +0.0092). v5 had the student below in all five cells.
   - *Rewrite:* "Against G\* run 1 alone, the gaps are −1.92, −3.84, −1.32, −1.96 and +0.92 pp (none significant). S4 now exceeds v5's 0.2–2.5 pp range, and A16-2 has changed sign."

7. **[M] §3 "Fresh vs reused": "Every primary conclusion has the same direction on 300–499 … H6b: all positive except the S12 g500 point."**
   - *Evidence:*
     - The H6b conclusion (7 Holm rejections) does not replicate. Only 2/10 are rejected fresh: `S2.300-499.holm.H6b_g125_512_16` = false, `S8` false, `S12` false, and g500 false everywhere.
     - S2 student − g500 is +0.004 fresh, effectively zero.
     - For H6a, the A16-2 point sign changes from −0.0028 to +0.001.
   - *Rewrite:* "On 300–499 the point signs mostly agree (all H6b points positive except S12 g500, −1.1 pp), but only 2/10 H6b contrasts survive Holm, so the fresh window replicates the direction, not the significance, of H6b."

8. **[M] §5: "The student is reliably *not more than 4 pp better* (upper margin rejected everywhere)".**
   - *Evidence:* This holds on 0–499 (p_upper 0.0003–0.0348). On the fresh window, `A16-2.300-499.H6a.success.tost.p_upper_margin` = 0.1557 is not rejected. These are also per-cell, unadjusted one-sided tests.
   - *Rewrite:* "On 0–499 the +4 pp upper margin is rejected in every cell (unadjusted p_upper ≤ 0.0348), so the student is not shown to be more than 4 pp better anywhere; on 300–499 this fails in A16-2 (p = 0.1557)."

9. **[M] §2.4 H5b: "The CI is about 15 pp per 100° wide".**
   - *Evidence:* `H5b_update_0_499.ci95_per_100deg` = [−0.1366, 0.1239]. That is about 26 pp wide (half-width about 13 pp).
   - *Rewrite:* "The 95% CI spans about 26 pp per 100° (−13.7 to +12.4 pp), so the test is uninformative."

10. **[M] Limitation 3: "flips 0–13 % of episode outcomes in the S cells".**
    - *Evidence:* In the S cells, `E12.flip_rate` has a minimum of 0.04 (S2 s704; S12 s701/s702) and a maximum of 0.13. The 0.00 values occur only in A16-2.
    - *Rewrite:* "The sub-8 → sub-16 change flips 4–13 % of episode outcomes in the S cells and 0–1 % in A16-2."

11. **[M] §2.5: "In the 4 S cells, the size of the shift (1.6–5.0 pp) is comparable to or larger than the 4 pp equivalence margin."**
    - *Evidence:* The derived shifts are S2 −1.6, S4 +4.6, S8 +5.0 and S12 −4.6 pp. S2's 1.6 pp is well under half the margin, so the claim holds in 3 of the 4 S cells. These are also 100-episode, G\*-run-1-only contrasts, with ci95 half-widths of 7–10 pp (`E12.student_minus_gstar_success_sub8.ci95`).
    - *Rewrite:* "In S4, S8 and S12 the grid change moves the 100-episode student − G\* contrast by 4.6–5.0 pp, comparable to the 4 pp margin; in S2 (1.6 pp) and A16-2 (0.6 pp) the shift is small."

12. **[M] §2.3 and §5: "the data do bound any DAgger benefit to below about 5 pp per cell".**
    - *Evidence:* This is true on 0–499 (max ci95 upper 0.048). On the fresh window, `S2.300-499.H6c.success.ci95` = [−0.049, 0.071], so the upper bound is 7.1 pp. Bounds are also per cell and unadjusted.
    - *Rewrite:* "On 0–499 the per-cell 95% upper bounds on the DAgger gain are at most 4.8 pp (up to 7.1 pp on the fresh window); no equivalence test was registered."

13. **[M] §5: "Shrinking G\* by about 20–45× in latency costs 4–14 pp of success, more than the student loses."**
    - *Evidence:* The derived G\*/reduced ratios are 19.0–47.0× (A16-2 g125 47.0, S12 g500 19.0). "More than the student loses" compares point estimates only, and in 3 g500 cells the student − g500 difference is not significant (see item 2).
    - *Rewrite:* "The reduced planners are 19–47× faster than G\* and lose 4.4–14.4 pp against G\* run 1 (point values), versus a student point loss of −0.9 to 3.8 pp; the difference is Holm-significant in 7/10 contrasts."

14. **[m] Limitation 4: "δ = 4 pp and 500 episodes gave the expected 90 % half-widths of 2.8–3.9 pp."**
    - *Evidence:* The design note expected "roughly 3.5–4 pp". The figures 2.84–3.85 are the observed half-widths (derived from `H6a.success.tost.ci90`). S4 (3.40) and S12 (2.84) came out narrower than predicted, so §2.1's "the power prediction held" is approximately but not exactly true.
    - *Rewrite:* "The design note expected 90 % half-widths of about 3.5–4 pp; the observed half-widths were 2.84–3.85 pp, at or below that."

15. **[m] §2.1: "equivalence needed point gaps of at most about 0.2–1.2 pp. Only A16-2 had such a gap".**
    - *Evidence:* Per cell, the requirement 0.04 − half-width is 0.46, 0.60, 0.50, 1.16 and 0.15 pp. A16-2's gap (0.28 pp) exceeds its own requirement (0.15 pp), so no cell met its threshold. That is consistent with p_TOST 0.0548.
    - *Rewrite:* "Equivalence required |gap| ≤ 0.15–1.16 pp depending on the cell; no cell met its own threshold, with A16-2 closest (0.28 vs 0.15 pp)."

16. **[m] Limitation 4: "the S4 ci90 excludes 0, so a small deficit there cannot be ruled out".**
    - *Evidence:* A ci90 entirely below 0 is the opposite of "cannot be ruled out". It means no deficit is rejected at the one-sided 5 % level (unregistered, unadjusted).
    - *Rewrite:* "In S4 the ci90 lies entirely below 0 on both windows, an unregistered one-sided indication of a small student deficit."

17. **[m] §5: "The student stays above … RL in 4/5 cells."**
    - *Evidence:* The point estimates of `student_minus_rl_success` are positive in 5/5 cells. The S8 ci95 [−0.0104, 0.0624] includes 0. On the fresh window, S8 (p 0.5744) and S12 (p 0.22) are also not significant.
    - *Rewrite:* "The student is significantly above RL cfg 6 in 4/5 cells on 0–499 (S8 not significant), and in 3/5 on the fresh window."

18. **[m] §3 Multiplicity: "Single unadjusted p-values near 0.02–0.05 … Examples are S8 fresh G\* − student g_T".**
    - *Evidence:* `S8.300-499.v5_row_updates.H2_v5_update.gstar_minus_student_gT.p_two_sided` = 0.0068, which is not in 0.02–0.05.
    - *Rewrite:* "Unadjusted p-values in these unregistered families (e.g. S8 fresh G\* − student g_T, p = 0.0068; S12 fresh student − rl_success, p = 0.05) should not be read as findings."

19. **[m] Limitation 3: "success contrasts of a few pp sit within evaluator noise".**
    - *Evidence:* E12 re-reads the same episodes on a different grid. It measures evaluator *sensitivity*, a systematic read-out dependence, not random noise, and it covers only 100 episodes of G\* run 1.
    - *Rewrite:* "On episodes 0–99, changing the read-out grid alone moves student − G\* contrasts by up to 5 pp, so contrasts of a few pp are sensitive to the evaluator choice."

20. **[m] Limitation 1: "first-decision agreement is only 0.27–0.45".**
    - *Evidence:* This is correct for 0–499. On the fresh window, `S2.300-499.gstar_first_decision_agreement_run2_vs_run1` = 0.245.
    - *Rewrite:* "First-decision agreement is 0.25–0.45 across cells and windows."

21. **[m] §5 H6c: "Most of the student's accuracy comes from behaviour cloning on G\*."**
    - *Evidence:* r0 is within 1.3 pp of r2 (`H6c.success.diff`). No baseline without BC was run, so "most of the accuracy" is an attribution the design does not test.
    - *Rewrite:* "The round-0 (BC-only) students already reach the round-2 success level (|r2 − r0| ≤ 1.3 pp), so the DAgger rounds add no detectable accuracy."

---

## Verdict

None of the pre-registered verdicts is misreported. The JSON `holm` flags and the analysis agree on every point:

- **H6a:** "neither a difference nor equivalence shown" in all 5 cells and both windows.
- **H6b:** 7/10 Holm rejections, all positive, on 0–499 (2/10 fresh).
- **H6c:** "not detected" everywhere.
- **Report-only rows:** H5b "no trend detected" and the inversion flags (S2/S4) are copied correctly.

The defects are in the interpretation:

- The bottom line ("dominates reduced planners", "within a few pp, no detectable cost") overstates H6b and ignores the BI and S4 one-sided evidence (items 1–2).
- The 0–499 sign count is wrong: all five cells are negative, not four (item 3).
- The stale-H\* caveat misses S4 (item 4).
- Several ranges are misstated (items 9–13).
