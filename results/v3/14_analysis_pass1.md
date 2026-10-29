# Stage 14 · Analysis of the v3 record (pass 1, outcome row 4)

> System: "You are a quantitative ML analyst. Always cite exact numbers from the provided data."
> Task: "Analyze run metrics and produce markdown report with statistical interpretation. Use the ACTUAL quantitative
> values provided above — do NOT invent numbers. Required sections: Metrics Summary (with real values), Comparative
> Findings, Statistical Checks, Limitations, Conclusion."

**Scope and sourcing.**
- Every number is taken from `results/v3/results_v3.json` and cited as `key.path` (top-level key first).
- Numbers marked **(derived)** are arithmetic on those values: differences, ratios, sample SDs of listed per-seed values.
- Pre-registered rules are quoted from `docs/07_hypotheses_v3.md` (§3.3, §3.4, §4, §5). Decisions are quoted from the
  status notes at the end of `docs/07c_amendment_v3_0.md`. The frozen run set is in
  `plans/stage_12_experiment_run_v3_main_row4.md`.
- v2 numbers come from `results/v2/14_analysis.md`, and that file's AC wording applies to them.
- No per-episode file was re-read for this pass. Where the JSON cannot settle a point, the text says so.

**Outcome row.** D3 failed on the first attempt and again after the one remedy. H1-fb was withdrawn at Lat′. That puts
the project in **row 4** (characterisation paper).

Under row 4 the only pre-registered decisions still open are:
- **H2** (one test);
- **H3** (outcome regions);
- the **encoder sentence** of §3.3.

All other v3 numbers are gate data or reported rows with no threshold.

Notation:
- Δ = paired difference;
- pp = percentage points;
- BI = ball information in nats;
- g_T = ball-sPCE (RL's training objective);
- LB/UB = one-sided 95 % bounds, unless an interval is labelled "ci90" or "ci95" (two-sided).

---

## 1. Metrics Summary

### 1.1 Decision table (everything with a pre-registered rule)

| Item | Rule | Measured (key) | Verdict |
|---|---|---|---|
| **Cal′ n\*** | n\* rule at κ = 0 | S: G\* success 0.605 → n\* 4; A: 0.985 → n\* 3 (`12_cal_analysis.n_star`). At sub 8: S 0.62, A 0.985, n\* unchanged (`n_star_sub8`) | Done |
| **Cal′ verification** | mean probes within n\* ± 0.3 | S12 3.96, A12 2.98 on 200 episodes (`12_cal_analysis.verify`) | **PASS** |
| **E′** evaluator | mean \|ΔBI\| ≤ 0.02; no flips outside the tie band | mean \|ΔBI\| 0.0126 (max 0.0523), but `counted_flips` = 1 (A12 b_fan ep. 1, mass 0.2282 under both settings) (`12_e_analysis`) | **FAIL** → sub = 8 everywhere |
| **G1′ (a)** notch | mean in [0.573, 0.860] | 0.8290; one of 5 runs (0.8629) is above the band (`12_g1_analysis.a`) | PASS |
| **G1′ (b)** zero-gap bank | mean in [−0.01, 0.02], UB < 0.03 | mean 0.00254, UB 0.00374, n = 100 (`12_g1_analysis.b`) | PASS |
| **G1′ (c)** travel-notch | estimate within ±20 % of exact | 0.7438 vs exact 0.7166; band [0.5733, 0.8600] (`12_g1_analysis.c`) | PASS |
| **G5′** (sub 8) | G\* ≥ random + 10 pp and §1.7 | D_c: S0 0.402, S12 0.351, A12 0.445; all non-degeneracy flags true (`12_g5_analysis.cells.*`) | PASS in all 3 cells, but random and heuristic rows are **incomplete** (§1.6) |
| **Lat′ / H1-fb activation** | G\* full / pruned-16 ≥ 10 | 3.224 (`12_lat_analysis.ratio_full_over_pruned16`) | **H1-fb withdrawn** |
| **D3**, first attempt | (i) Δ̂_succ ≥ thr; (ii) Δ̂_BI ≥ thr; (iii) every seed Δ̂_succ > −δ | (i) −0.0587 vs thr −0.0143; (ii) −0.1988 vs thr −0.15; (iii) −0.042 / −0.080 / −0.054 vs −0.04 (`12_d3_analysis`) | **FAIL** on (i), (ii) and (iii) |
| **D3**, remedy | same | (i) −0.0440 vs thr −0.0168 ✗; (ii) −0.0962 vs −0.15 ✓; (iii) −0.046 / −0.046 / −0.040 ✗ (`12_d3_analysis_rem`) | **FAIL** on (i) and (iii) → H1 dead → row 4 |
| **D3-B** belief input (report-only) | same as D3 | (i) −0.2011 vs −0.0073; (ii) −1.0105 vs −0.15; every seed between −0.173 and −0.217 (`12_d3_analysis_belief_student`, **295 of 300 episodes**) | **FAIL** (cannot flip; see §3.2) |
| **Label fit** | under-fit := train R̄ > 0.25 or train top-1 < 0.50 | first attempt and remedy: all 6 `under_fit: false`; belief input: all 3 `under_fit: true` (`14_labelfit`) | see §1.4 |
| **H2** | LB(g_T(student) − g_T(RL)) > +0.10 nats, 500 test3 episodes | diff +0.00023, LB **−0.3103** (`14_h2_analysis.bootstrap`) | **REJECTED** |
| **H3** | Hold iff UB95(G(12)) < 0.03; Hold needs bias ratio ≤ 1.02 and G1′ (c) | G(12) 0.01624, UB **0.02210**; bias ratio 0.957 (`12_g2_analysis.k12`, `.bias_check`, `.H3`) | **HOLD** (not downgraded) |

### 1.2 H2: g_T on test3 0–499 (S12, fixed per-episode contrastive draws)

| Row | Value (`14_h2_analysis`) |
|---|---|
| Student (remedied, seeds 501–503), mean g_T | 5.3678 (per seed 5.2795 / 5.4070 / 5.4171) |
| RL-relative (seeds 511–513), mean g_T | 5.3676 (per seed 5.6543 / 5.2709 / 5.1776) |
| Δ (student − RL) | +0.000232 nats |
| One-sided 95 % LB / UB (`lower` / `upper`, i.e. 5 % and 95 % bootstrap quantiles) | −0.3103 / +0.3034 |
| Bootstrap p_greater / p_less | 0.4883 / 0.5117 |
| B; seeds | 10,000; [3, 3] |
| Threshold; passes | 0.10; `false` |

- Sample SD of the per-seed means (derived): RL 0.253 nats; student 0.077 nats.
- The RL seed spread (5.18 to 5.65) is about 3.3 times the student's (derived).

### 1.3 M4: success, BI and probes on test3 0–299 (sub-8 grid; reported rows with no test)

| Method | Success | BI (nats) | Probes | Per-seed success |
|---|---|---|---|---|
| G\* | 0.4267 | 6.2483 | 3.963 | 0.4267 (1 deterministic column) |
| Student (remedied) | 0.3822 | 6.1996 | 4.0 | 0.3833 / 0.3767 / 0.3867 |
| RL-relative | 0.3567 | 5.9102 | 3.0 | 0.3667 / 0.3900 / 0.3133 |

Paired crossed-bootstrap differences (`14_m4_analysis.diffs`). The ci90 lower end is the one-sided 95 % LB.

| Contrast | Δ | ci90 | ci95 |
|---|---|---|---|
| student − G\*, success | −0.0444 | [−0.0856, −0.0033] | [−0.0933, +0.0056] |
| student − G\*, BI | −0.0487 | [−0.1035, +0.0078] | [−0.1138, +0.0190] |
| student − RL, success | +0.0256 | [−0.0267, +0.0778] | [−0.0367, +0.0878] |
| student − RL, BI | +0.2893 | [+0.1402, +0.4397] | [+0.1170, +0.4652] |
| G\* − RL, success | +0.0700 | [+0.0122, +0.1256] | [+0.0022, +0.1367] |
| G\* − RL, BI | +0.3380 | [+0.1866, +0.4894] | [+0.1585, +0.5196] |

- Gap closure is **not reported** (`gap_closure_reported: false`). The rule needs LB(success(G\*) − success(RL)) >
  δ_S12 = 0.04, and the LB is 0.0122.
- The pre-registered H2 companion rows "g_T of G\*", "RL plateau status" and "CPU-h of both methods" are **not in
  `results_v3.json`**. They cannot be reported from this file.

### 1.4 Label fit (end of round 2; `14_labelfit.groups`)

| Group | train R̄ | train top-1 | held-out R̄ | held-out top-1 | train decisions | under_fit |
|---|---|---|---|---|---|---|
| First attempt 501 / 502 / 503 | 0.1875 / 0.2064 / 0.1853 | 0.5304 / 0.5107 / 0.5278 | 0.2102 / 0.2253 / 0.2068 | 0.4916 / 0.4833 / 0.4883 | 7,957 / 7,957 / 7,959 | false ×3 |
| Remedy 501 / 502 / 503 | 0.1795 / 0.1687 / 0.1774 | 0.5233 / 0.5344 / 0.5275 | 0.1865 / 0.1841 / 0.2012 | 0.5067 / 0.5059 / 0.4916 | 17,083 / 17,083 / 17,089 | false ×3 |
| Belief input 521 / 522 / 523 | 0.3675 / 0.3787 / 0.3380 | 0.3337 / 0.3270 / 0.3620 | 0.4018 / 0.3942 / 0.3842 | 0.2968 / 0.3085 / 0.3052 | 7,957 / 7,951 / 7,955 | true ×3 |

- The belief-input students were trained with the **first-attempt** data size (about 7,950 decisions), not the remedy
  size.
- The fair belief-free comparator for them is therefore the first-attempt group.

### 1.5 H3: one-step rollout headroom over G\* (set S, 64 × 8, 100 beliefs per κ; `12_g2_analysis`)

| κ | G | LB95 | UB95 | abs. gap (nats) | mean V_LA | mean V_G\* | frac LA ≠ G\* | no budget left |
|---|---|---|---|---|---|---|---|---|
| 0 | 0.00637 | 0.00403 | 0.00940 | 0.0179 | 2.8157 | 2.7978 | 0.58 | 0 |
| 2 | 0.01418 | 0.00962 | 0.01974 | 0.0371 | 2.6171 | 2.5800 | 0.54 | 4 |
| 12 | 0.01624 | 0.01148 | 0.02210 | 0.0414 | 2.5476 | 2.5062 | 0.62 | 1 |

- Ordering G(0) ≤ G(2) ≤ G(12): true (`H3.ordering_G0<=G2<=G12`).
- Bias check, 20 beliefs (`bias_check`):
  - estimator V_G\* = 1.9396;
  - reference = 2.0261;
  - ratio = 0.9573 (≤ 1.02, so `hold_available: true`);
  - 3 floored rollouts.

### 1.6 G5′ pilot at sub 8 (`12_g5_analysis.cells`; partial for every non-G\* row)

| Cell | G\* success (n = 500) ± SE | G\* BI | random (n) | b_spread (n) | b_fan (n) | b_cov (n) | δ_c | ε_c | H★ |
|---|---|---|---|---|---|---|---|---|---|
| S0 | 0.660 ± 0.0212 | 7.012 | 0.258 (62) | — (0) | — (0) | — (0) | 0.04 | 0.2184 | b_spread, `H_star_success` = **−1.0** |
| S12 | 0.426 ± 0.0221 | 6.290 | 0.0754 (199) | 0.0642 (187) | **0.4026 (154)** | 0.3563 (174) | 0.04 | 0.3145 | b_fan, `flat_screen: true` |
| A12 | 0.470 ± 0.0223 | 6.714 | 0.0248 (161) | 0.0526 (76) | — (0) | — (0) | 0.04 | 0.3357 | b_spread (0.0526) |

- The superseded sub-4 version (`12_g5_analysis_sub4`) has complete heuristic rows in S12 and A12.
- At sub 4, H★ was b_fan in both: S12 0.395 (n = 200) and A12 0.390 (n = 200).
- At sub 4, S0 H★ was b_spread 0.465 (n = 200).

### 1.7 Latency (Lat′, 1,000 decisions on 253 S12 pilot episodes, two machines pooled; `12_lat_analysis`)

| Quantity | Median | 95 % CI | rel. half-width |
|---|---|---|---|
| Student L_dec | 0.408 ms | [0.4036, 0.4137] ms | 0.012 |
| G\* full (2,000, 512, 64) | 0.9135 s | [0.7910, 0.9413] s | 0.082 |
| Pruned-16 | 0.2833 s | [0.2811, 0.2853] s | 0.007 |
| L_final (student read-out, per episode) | 0.2043 s | [0.1929, 0.2135] s | 0.050 |

- Ratios: G\* full / student = **2,238**; G\* full / pruned-16 = **3.22**.
- `protocol_complete: false`. Six configurations have CI half-widths above 10 % (`ci_too_wide`), as large as 0.146
  (g500_128_16).
- Component split (derived, from component medians; a sum of medians is not the median of a sum):
  - G\* full: t_score = 78.5 % of its median.
  - Pruned-16: t_assim + t_nb = 47.8 %.
  - The pruned-16 figure is why candidate pruning cannot reach 10×.

---

## 2. Comparative Findings

### 2.1 Distillation versus its teacher (learnability, the core of row 4)

1. **The remedy helped, but not enough.** These are point estimates on the same 500 val3 episodes against the same G\*
   (`12_d3_analysis` vs `12_d3_analysis_rem`):

   | Quantity | First attempt | Remedy | Change (derived) |
   |---|---|---|---|
   | Δ̂_succ | −5.87 pp | −4.40 pp | +1.47 pp |
   | Δ̂_BI | −0.199 nats | −0.096 nats | +0.103 nats |

   - Doubling round-0 data (train decisions 7,957 → 17,083) cut the BI deficit by about half.
   - The success deficit fell by about a quarter.
   - These improvements were **not tested**: no paired first-attempt-vs-remedy bootstrap exists.

2. **On test the gap persists.** On test3 0–299 (`14_m4_analysis`), student − G\* success is −4.44 pp:
   - one-sided 95 % LB −8.56 pp;
   - UB −0.33 pp, which excludes 0 on the one-sided reading.
   - BI is −0.049 nats, ci90 [−0.104, +0.008].

   This is descriptive only, because H1 died at D3. Had H1a been run on these 300 episodes:
   - the success LB (−8.56 pp) would fall below −δ = −4 pp;
   - the BI LB (−0.104) would sit inside −ε_S12 = −0.3145.

   The success LB, not BI, is the binding failure. This agrees with the D3 verdict.

3. **Seed consistency without parity.** The remedied students agree closely with each other but are all short of G\*:
   - val3 per-seed Δ̂_succ: −4.6 / −4.6 / −4.0 pp;
   - test3 per-seed success: 0.3833 / 0.3767 / 0.3867.

   The deficit looks systematic, not seed noise. **Seed 503 sits exactly on the boundary**: per-seed −0.04 against the
   strict rule "> −0.04" (`seeds_ok.503: false`). Rule (i) fails regardless (−0.0440 < −0.0168), so the verdict does
   not depend on that tie.

### 2.2 Encoder sentence (§3.3), applied mechanically, and why it is weak

- **Pre-registered reading.** No history student is under-fit (train R̄ 0.169–0.206 ≤ 0.25; train top-1 0.511–0.534 ≥
  0.50), yet D3 fails. The permitted sentence is therefore:

  > "generalisation / covariate shift, not capacity".

- **Problems with the evidence behind that sentence.**
  - **(a) Thin margins.** "Fits" is decided by a top-1 margin of 1.1–3.4 pp over 0.50 (502 first attempt: 0.5107).
    The student matches G\*'s argmax on only about half of the training decisions.
  - **(b) Below 0.50 on held-out data.** Held-out top-1 is under 0.50 for 4 of 6 history students (0.4833–0.4916). The
    other two are 0.5059 and 0.5067.
  - **(c) The held-out set cannot show covariate shift.** It is the round-0 G\* label set (`val_shards`), i.e. states
    visited by G\*, not by the student. Train-to-held-out R̄ gaps are small (derived 0.007–0.024). The JSON contains no
    measurement on student-visited states, so it does **not** show covariate shift directly.
  - **(d) No scale for R̄.** The pre-registered scale references (teacher noise-floor R̄ and tie fraction, §1.6) are
    absent from `results_v3.json`. Without them it is unknown whether R̄ ≈ 0.18 is near the irreducible floor.
- **Belief-input control.**
  - It fails more severely than the history student on both label fit (train top-1 0.327–0.362) and D3 (−20.1 pp
    success, −1.01 nats BI).
  - With under-fit ∧ belief-input-fails it cannot isolate the representation.
  - It shows only that this 48-feature PF summary, trained on first-attempt-size data, is a worse input than the
    relative history.
- **Allowed wording.** "Students fit the teacher's training labels to the pre-registered criterion (top-1 0.51–0.53)
  but fail validation; the label-fit rule assigns this to generalisation rather than capacity. The held-out regret is
  measured on teacher-visited states, so covariate shift is inferred, not observed."

### 2.3 Distillation versus RL (H2 and the M4 rows)

- **On RL's own objective there is no difference.**
  - Δg_T = +0.00023 nats, one-sided 95 % bounds [−0.310, +0.303].
  - H2 is **rejected**.
- **Pre-registered fail branch.** The paired two-sided 95 % CI of student − RL success is [−3.67, +8.78] pp and contains
  0. The prescribed reading is therefore:

  > "dense supervision does not improve on RL with this head".

  The "objective mismatch" reading is **not** available.
- **Not a positive finding of equality.**
  - The ±0.31-nat interval means only a true Δ above about 0.41 nats could have passed (derived: 0.10 + 0.3106).
  - Equivalence was not tested. No TOST is implemented for H2.
  - "RL and distillation reach the same sPCE" is an overstatement. Correct wording: "no difference detected; differences
    up to about ±0.3 nats are not excluded".
- **BI and success give a different picture (exploratory, no rule).**
  - Student − RL BI = +0.289 nats, ci95 [+0.117, +0.465], excluding 0.
  - G\* − RL success = +7.0 pp, ci95 [+0.22, +13.67] pp.
  - RL executes **3.0** probes against the student's **4.0** and G\*'s 3.963 (`14_m4_analysis.rows.*.probes`).
  - So RL reaches the student's g_T with one probe fewer, yet trails on BI. Ball-sPCE (g_T) and grid BI therefore
    disagree on the ordering of these two policies.
  - Without g_T(G\*) (missing) and RL's travel, the reason cannot be found from this file. It should be reported as an
    observation, not as a mechanism.
- **RL is unstable across seeds.**
  - Per-seed test success: 0.3133–0.3900, a range of 7.7 pp.
  - Per-seed g_T: 5.18–5.65.
  - The student's ranges are 1.0 pp and 0.14 nats (derived).
  - Most of the H2 interval width probably comes from seed resampling of RL. This is inferred from the per-seed SDs (0.253
    vs 0.077), not from a variance decomposition.

### 2.4 Learned policies versus a trivial heuristic (not paired; exploratory)

- At S12, the belief-free, zero-travel heuristic **b_fan** scores 0.4026 success, ± 0.0396 SE, n = 154, on pilot3 at sub
  8 (`12_g5_analysis.cells.S12.b_fan`). That is 2.3 pp below G\* on the same pilot (0.426).
- The remedied student scores:
  - 0.402 on val3 (`12_d3_analysis_rem.succ.student_mean`);
  - 0.3822 on test3 0–299.
- These are **different episode sets and not paired**, and the heuristic row is incomplete. Still, nothing in the record
  shows that the distilled student beats a no-learning heuristic in success.
- The flat-screen flag is set in S12 (`flat_screen: true`).
- This is the single most damaging fact for any "learning" sentence in the row-4 paper.

### 2.5 Look-ahead headroom (H3)

- **The headline holds.** At κ = 12, one-step rollout over G\* gains at most 2.21 % of the remaining expected ball
  information (UB of G(12) = 0.02210). The absolute gap is 0.041 nats.
- **"LA differs from G\*" is not "headroom".** LA differs from G\* in 62 % of beliefs while the mean gain stays small.
  That pattern fits near-ties among top actions.
- **Concern not covered by the pre-registered guard.**
  - The bias check finds that the estimator under-reads V_G\* by 0.0865 nats (derived: 2.0261 − 1.9396), about 4.3 %.
  - That is **about twice the measured absolute headroom** at κ = 12 (0.041 nats).
  - The rule only guards over-reading (ratio > 1.02), so Hold stands as pre-registered.
  - The paper should still state that the bias is of the same order as the gap. It is safe only if V_LA is biased the
    same way (shared reduced G\* completion, CRN), and that was not checked.
  - The check uses 20 beliefs with 3 floored rollouts.

### 2.6 Comparison with v2 (`results/v2/14_analysis.md`; v2 numbers are validation/pilot on the voided 32 × 8 set)

| Quantity | v2 | v3 | Comment |
|---|---|---|---|
| G(12) (UB) | 0.0146 (0.0208) | 0.01624 (0.02210) | Point estimate up 0.0016 (derived). Difference not tested. Grids differ (32 × 8 vs 64 × 8). |
| G(0) / G(2) | 0.0049 / 0.0080 | 0.00637 / 0.01418 | Ordering holds in both |
| G1 (a) / (b) | 0.8290 (runs 0.8409…0.8425) / 0.00254, UB 0.00374 | **identical to all printed digits** | The v3 re-run "on the v3 code path" reproduces v2 bit-for-bit. Either the notch path does not touch the 64 × 8 change or the values were carried over. The JSON alone cannot tell which, so this is not independent confirmation. |
| Learned policy vs G\*, S12 success | RL absolute head, 3 seeds: 0.204 vs 0.410 (−20.6 pp, validation); remedy 0.2433 | RL relative head (test3): 0.3567 vs 0.4267 (−7.0 pp, ci95 [+0.22, +13.67] for G\* − RL); student −4.44 pp | v3 learned policies are much closer to G\*. The pipelines differ (action set, head, evaluator, sweep config, test vs validation), so no v2→v3 improvement can be attributed. |
| Evaluator | 32k × 3 MH under-reads BI vs grid by 0.073–0.166 nats; grid sub-4 vs 8 self-check passed (n = 8, 0 flips) | Grid sub-4 vs 8 E′ **failed** (1 counted flip in 16); S0 cal flip rate 7.5 % (`n_star_sub8.S.success_flip_rate_vs_sub4`) | The grid self-check that v2 passed on 8 episodes fails on 16 in v3. Grid resolution itself moves success. |

---

## 3. Statistical Checks

### 3.1 Recomputations from the JSON (all consistent)

- **D3 remedy thresholds** (derived):
  - Success: max(−0.02, −0.04 + 1.645·0.019940·√0.5) = max(−0.02, −0.01681) = −0.01681, which matches `threshold`.
  - BI: max(−0.15, −0.31427 + 1.645·0.028079·√0.5 = −0.28160) = −0.15, which matches.
- **Per-seed means**:
  - M4 student success: mean(0.3833, 0.3767, 0.3867) = 0.3822, which matches.
  - M4 RL success: mean(0.3667, 0.3900, 0.3133) = 0.3567, which matches.
  - H2 means are reproduced from the per-seed values (5.3678, 5.3676).
- **Margins**:
  - ε_S12 = min(0.05·6.2901, 0.15·3.2918) = 0.31451 (`12_g5_analysis`).
  - D_c(S12) = 0.426 − 0.0754 = 0.3506.
- **Gap-closure gate**: LB 0.0122 < 0.04, so it is correctly not reported.

### 3.2 Robustness of decisions to incomplete inputs

- **D3-B (295/300 episodes).**
  - The 5 missing paired episodes can move Δ̂_succ by at most 5/300 = 1.67 pp (derived).
  - The observed −20.1 pp is 19.4 pp below its threshold, so the verdict cannot flip.
  - BI: −1.01 vs −0.15, so it cannot flip either.
- **D3 margins (stale ε).**
  - `12_d3_analysis*` carry `eps_S12` = 0.314266, while the current `12_g5_analysis` gives 0.314507. The D3 files were
    computed from an earlier G5′ read, which implies a G\* BI of 6.2853 (derived).
  - This does not matter: the BI threshold is the −0.15 floor under either value, and δ = 0.04 (cap) in both.
  - It is still a provenance mismatch and should be regenerated or footnoted.
- **First-attempt status note vs JSON.**
  - The 07c note quotes −6.8 pp, −0.19 nats and per-seed −5.1 / −8.5 / −6.6 pp on 468 episodes.
  - The complete JSON (500 episodes) gives −5.87 pp, −0.199 nats and −4.2 / −8.0 / −5.4 pp.
  - The verdict is the same, but the **JSON values are binding** and the note's numbers must not be quoted.
  - On the complete data, seed 501 (−4.2 pp) is only 0.2 pp beyond −δ.
- **G5′ sub 8.**
  - S0 has `H_star_success = −1.0`, a sentinel for "no heuristic data". Its H★ = b_spread comes only from the
    tie-ordering default. The S0 random row has n = 62 of the planned 200.
  - A12 b_fan and b_cov have n = 0, so A12's H★ = b_spread (0.0526) is an artefact. At sub 4 it was b_fan, 0.39.
  - `flat_screen_cells = 1` and `flat_prime_likely: false` are therefore **not established** at sub 8.
  - The sub-4 file agrees with 1 flat cell (S12), but it is superseded.
  - None of this changes a row-4 decision, because H1c is dropped. It does affect the §2.4 reading.

### 3.3 Power and interval interpretation

- **H2.**
  - The one-sided interval half-width is 0.3106 nats against a 0.10 threshold. The design could detect only Δ ≳ 0.41
    nats.
  - The p-values (0.4883 / 0.5117) are what a null-centred estimate gives.
  - This is a non-detection, not evidence of equality.
- **M4 student − G\* success.**
  - ci90 excludes 0 (UB −0.33 pp), so the student is worse than G\* at the one-sided 5 % level.
  - ci95 [−9.33, +0.56] pp includes 0.
  - Report the deficit as "significant at one-sided 5 % only, descriptive (no pre-registered test)".
- **M4 student − RL success**: the ci95 [−3.67, +8.78] pp includes 0. With 300 episodes and 3 + 3 seeds a gap of
  about 2.6 pp is not resolvable.
- **H3**: one-sided bootstrap over 100 beliefs (ratio of means). Hold is decided on UB 0.0221 < 0.03 with a margin of
  0.0079.
- **No multiplicity issue in the decisions.** H2 and H3 are separate claims with one test each (§1.9). M4 has six
  reported intervals with no decision and no correction. They must not be presented as tests.

### 3.4 Tests that would be needed but are not implemented (recommendations only)

1. TOST/equivalence for g_T(student) − g_T(RL), to support any "same sPCE" statement.
2. A variance decomposition of the H2 bootstrap: episode-only vs seed-only resampling. This would separate RL seed
   instability from episode noise.
3. A paired first-attempt-vs-remedy bootstrap on val3, to support "the remedy halved the BI gap".
4. Held-out regret and top-1 on **student-visited** (DAgger round-2) states, with the teacher noise-floor R̄. Without
   these the "covariate shift" sentence rests on inference.
5. A paired b_fan row on test3 0–299 (reported-only, outside the frozen set, labelled exploratory). This would settle
   §2.4.
6. A sub-16 grid check on a subset. Sub 4 → 8 flips 7.5 % of S0 calibration successes, so evaluator convergence at sub 8
   is not shown.

---

## 4. Limitations

1. **Single cell.** Every row-4 result except H3's κ levels is S12 only: one shape set, one κ, n\* = 4.
   - S0 and A12 contribute only G5′ pilot rows, and those are mostly incomplete.
2. **Evaluator is not shown converged.**
   - E′ failed: 1 counted flip in 16 episodes, at an unchanged true-identity mass of 0.2282, so the flip is a pose
     boundary, not an identity tie.
   - The sub-4→8 success flip rate on S0 calibration is 7.5 % (`12_cal_analysis.n_star_sub8.S`).
   - All success numbers carry this unquantified instrument noise. Sub 8 vs a finer grid was never checked.
   - Sub-8 read-out costs 40.6 s per episode (`12_e_analysis.mean_wall_s_sub8`), which limited every n in this record.
3. **The RL comparator was selected off-protocol.**
   - The 4-config sweep was selected on the trainer's `val_v2` stream, not val3 (`12_rl_sweep_selection.validation_stream`).
   - Sweep configs were trained to only 50,048 episodes.
   - The selected cfg 2 (lr 1.09e-3) beat the others by 0.919 nats in final validation ball-sPCE (5.666 vs ≤ 4.747;
     derived). That margin makes it unlikely, though not demonstrated, that val3 would have picked differently.
   - RL ends at 3 probes against about 4 for G\* and the student. Its budget use differs, and travel is not in the JSON.
4. **Missing pre-registered report items**:
   - g_T(G\*);
   - RL plateau status;
   - CPU-h including labelling;
   - teacher noise-floor R̄ and tie fraction;
   - per-episode L_ep.
5. **Latency.**
   - Lat′ pooled two runners with different speeds; six CIs are above 10 %, and `protocol_complete` is false. The
     2,238× per-decision ratio depends on the machine.
   - The 07c note records student medians of 0.38 vs 0.60 ms across runners.
   - **Per episode the advantage is far smaller.** The student needs a 0.204 s PF read-out (L_final). With 3–4
     decisions per episode, the per-episode ratio is roughly **13–18×** (derived: n·0.9135 / (n·0.000408 + 0.2043)).
   - This is not a protocol L_ep. Any "2,000×" sentence must say "per decision".
6. **Label-fit thresholds are coarse.** Top-1 ≈ 0.52 passes "fits" (§2.2), and the held-out set is teacher-visited.
7. **H3 scope.**
   - H3 measures one-step-deviation headroom over a **reduced** greedy completion (07c C12), not the gap to optimal.
   - The estimator's V_G\* under-read (0.087 nats) is twice the κ = 12 gap.
   - G1′ values are bit-identical to v2, so they are not new evidence of instrument validity.
8. **Episode-set mismatch.** G\* success is 0.426 on pilot3, 0.446 on val3 and 0.4267 on test3 0–299. Cross-split
   comparisons (§2.4) are not paired.
9. **Process.** Total compute exceeded the 12-hour RESTRICTS reading (the owner was informed). The D3-B validation and the
   G5′ re-reads were still running when this analysis was written.

---

## 5. Conclusion

**Outcome row 4 applies.**
- D3 failed on the first attempt (Δ̂_succ −5.87 pp, Δ̂_BI −0.199 nats) and after the one remedy (−4.40 pp vs threshold
  −1.68 pp).
- H1-fb was withdrawn (full / pruned-16 = 3.22 < 10).

Pre-registered labels:

| Claim | Label | Evidence |
|---|---|---|
| H1 | **dead at D3** (not tested) | D3 rule (i) and (iii) fail after the remedy |
| H1-fb | **withdrawn** | ratio 3.22; PF assimilation + neighbour lists = 47.8 % of pruned-16 time (derived from component medians) |
| H2 | **rejected** | Δg_T = +0.0002 nats, LB −0.310 ≤ +0.10. Fail-branch reading: "dense supervision does not improve on RL with this head" (success ci95 [−3.67, +8.78] pp contains 0). Non-detection, not equality. |
| H3 | **Hold** | UB95 G(12) = 0.0221 < 0.03; bias ratio 0.957; G1′ (a)–(c) pass. Report the 0.087-nat V_G\* under-read next to the 0.041-nat gap. |
| Encoder sentence | **"generalisation / covariate shift, not capacity"** (rule-permitted) | No history student under-fit (top-1 0.511–0.534, R̄ 0.169–0.206). Weakly supported: covariate shift was not measured on student-visited states, and the belief-input control (under-fit, D3-B −20.1 pp) isolates nothing. |

What the evidence supports for a characterisation paper:
- (i) Greedy G\* leaves at most about 2.2 % one-step headroom at κ = 12 on set S.
- (ii) Neither PPO nor DAgger distillation with the same relative DeepSets head reaches G\*:
  - test3 success −7.0 pp (RL) and −4.4 pp (student);
  - the two learned policies are indistinguishable on sPCE and on success;
  - only BI separates them (+0.289 nats for the student).
- (iii) The student is about 2,238× cheaper **per decision** but only about 13–18× per episode (derived, not protocol).

**Before writing.** The most serious open issue is in the record but untested: a zero-travel heuristic (b_fan, 0.4026
on pilot3) scores as well as the student (0.402 val3 / 0.382 test3). No learning claim of any kind should be written
until a paired heuristic row exists.
