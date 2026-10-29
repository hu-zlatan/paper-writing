# Stage 14 RESULT_ANALYSIS [v3] — merged report (run 7, 2026-10-29)

**How this file was made.** Pass 1 (fresh-context analyst, `14_analysis_pass1.md`) and pass 2 (fresh-context
adversarial area chair, `14_analysis_pass2.md`), both with the stage-14 template verbatim and `results_v3.json` as the
data context. Merge rule: pass 1 is kept as the body; **every pass-2 item (S1–S7, M1–M8, m1–m7) is binding** — where a
pass-1 sentence is listed there, the pass-2 "supported rewrite" replaces it for every later stage (paper drafting cites
the rewrite, never the pass-1 sentence). No pre-registered verdict changed in pass 2: row 4, H1 dead, H1-fb withdrawn,
H2 rejected, H3 Hold, encoder sentence "generalisation / covariate shift, not capacity" (weakly supported).

**Open items carried to stage 15.** (1) No paired heuristic row on test3 (b_fan / b_spread are unpaired pilot3 numbers,
incomplete); (2) H3 bias check direction (V_LA under-read not checked); (3) per-episode latency L_ep not measured;
(4) G5′ sub-8 and D3-B rows still incomplete at merge time.

---

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

---

# Pass 2 (binding corrections)

# Stage 14 · Analysis of the v3 record, pass 2 (area-chair audit of `14_analysis_pass1.md`)

> System: "You are a top-conference area chair who has rejected 80% of papers you've reviewed this cycle. Read the
> analysis below. Identify every claim that is not strictly supported by the cited numbers. For each, output the
> unsupported claim, the contradicting/missing evidence, and a one-sentence rewrite that *is* supported."

**Sources checked.**
- `results/v3/results_v3.json`: every number in pass 1 was compared against it.
- `results/v2/12_g1_analysis.json` and `results/v2/14_analysis.md`: the v2 numbers.
- `code/touchbed/stats.py` and `code/analysis_m4_v3.py`: the bound definitions.
- `docs/07_hypotheses_v3.md` §1.3–§1.9, §3.1–§3.4, §4, §5, and `docs/07c_amendment_v3_0.md` C7, C9, C12 and the status
  notes.
- No per-episode file was needed; every point below can be decided from the JSON, the code or the docs.

**Result.** 22 claims are not strictly supported: 7 serious (S), 8 moderate (M) and 7 minor (m). No pre-registered
verdict changes. Row 4, H1 dead, H1-fb withdrawn, H2 rejected, H3 Hold and the permitted encoder sentence all stand.
The problems are in the interpretive and summary sentences, mostly in §2.3, §2.5 and §5.

---

## A. Unsupported claims

### Serious

**S1. §5 (ii): "the two learned policies are indistinguishable on sPCE and on success".**
- *Evidence.* No equivalence test was run.
  - Δg_T = +0.00023 with one-sided 95 % bounds [−0.3103, +0.3034] (`14_h2_analysis.bootstrap`).
  - Student − RL success = +2.56 pp, ci95 [−3.67, +8.78] pp (`14_m4_analysis.diffs.student-rl:success`).
  - Both intervals are wide. Pass 1 itself (§2.3, §3.3) calls this "a non-detection, not evidence of equality", so the
    conclusion contradicts the body.
- *Rewrite.* "No difference between the two learned policies was detected on g_T (Δ = +0.0002 nats, one-sided 95 %
  bounds [−0.31, +0.30]) or on test success (ci95 [−3.7, +8.8] pp); equivalence was not tested."

**S2. §5 "Before writing": "a zero-travel heuristic (b_fan, 0.4026 on pilot3) scores as well as the student (0.402
val3 / 0.382 test3)".**
- *Evidence.* No comparison was run, so "as well as" is an equality claim with no test behind it.
  - The b_fan row is incomplete: n = 154 of 200, SE 0.0396 (`12_g5_analysis.cells.S12.b_fan`).
  - It is on a different split (pilot3) from both student numbers, and nothing is paired.
  - Pass 1 §2.4 makes only the weaker claim that "nothing in the record shows that the student beats" the heuristic.
  - B-fan is not zero-travel. It is "travel-nearest": it stays at φ_t only when that is allowed, and otherwise moves to
    the nearest allowed φ′ (`07_hypotheses_v3` §1.7).
- *Rewrite.* "On unpaired splits the travel-nearest heuristic b_fan (0.403 ± 0.040, n = 154 of 200 pilot3 episodes)
  has a point success comparable to the remedied student (0.402 val3, 0.382 test3); no paired comparison exists, so
  nothing in the record shows the student beats it."

**S3. §2.3: "Ball-sPCE (g_T) and grid BI therefore disagree on the ordering of these two policies" (and "RL reaches the
student's g_T with one probe fewer").**
- *Evidence.* g_T gives no ordering at all, only a non-detection.
  - Its interval, [−0.310, +0.303] nats, contains the BI difference of +0.289 nats.
  - The two quantities use different instruments (contrastive ball-sPCE vs the sub-8 grid) and different episode sets
    (test3 0–499 vs 0–299).
  - "Reaches" is again an equality reading of a non-detection.
- *Rewrite.* "Student − RL BI is +0.289 nats (ci95 [+0.117, +0.465]) on test3 0–299, while the g_T difference on 0–499
  is undetected with bounds wide enough (±0.31 nats) to include a gap of that size; RL executes 3.0 probes against the
  student's 4.0."

**S4. §2.5 and §4.7: the bias argument ("bias … about twice the measured absolute headroom"; "safe only if V_LA is
biased the same way").**
- *Evidence, part 1 (direction).* The direction is wrong.
  - G = (V_LA − V_G\*)/V_LA. An under-read of V_G\* on its own inflates G, which works against Hold.
  - Hold is threatened only if V_LA is under-read by more than V_G\*.
  - So "same bias" is a sufficient condition, not a necessary one.
- *Evidence, part 2 (comparison).* The 0.0865-nat bias and the 0.041-nat gap come from different belief sets.
  - The bias check uses 20 beliefs with mean reference V 2.026 (`12_g2_analysis.bias_check`).
  - The κ = 12 gap uses 100 beliefs with mean V_G\* 2.506 (`k12`).
  - The bias has no interval, and 3 of its rollouts were floored.
  - The ratio 2.09 is arithmetic across those sets, not a measured property of the H3 estimate.
- *Rewrite.* "On 20 separate beliefs the estimator reads V_G\* 0.087 nats (4.3 %, no CI) below an independent full-G\*
  rollout, comparable in size to the 0.041-nat κ = 12 gap; this direction alone would inflate G, and Hold could be
  affected only if V_LA were under-read by more, which was not checked."

**S5. §5 (i) and §2.5: "Greedy G\* leaves at most about 2.2 % one-step headroom at κ = 12 on set S."**
- *Evidence, part 1 (completion).* The rollouts are not completed by G\*. Per 07c C12 they use a reduced greedy:
  - N_LA = 500 particles;
  - 128 candidates;
  - M = 16.
- *Evidence, part 2 (bound).* 2.21 % is a one-sided 95 % upper bound (`k12.ub95` 0.02210), not a hard maximum. The
  pre-registered Hold wording also requires "(S, n\* probes)".
- *Rewrite.* "One-step rollout over the reduced greedy completion gains ≤ 2.2 % of the remaining expected ball
  information at κ = 12 (S, n\* = 4; one-sided 95 % UB of G(12) = 0.0221)."

**S6. §1.7 and the §5 H1-fb row: "PF assimilation + neighbour lists = 47.8 % of pruned-16 time"; "The pruned-16 figure
is why candidate pruning cannot reach 10×".**
- *Evidence.* The pre-registered withdrawal sentence (§3.2) asks for x % "of **G\*'s** per-decision time". For G\* full
  that is (t_assim 0.0402 + t_nb 0.0967) / 0.9135 = **15.0 %** (derived from `12_lat_analysis.methods.g2000_512_64`).
- That 15.0 % floor is what bounds pruning: even with zero scoring cost the ratio is at most 0.9135 / 0.1370 = 6.7×.
- The 47.8 % pruned-16 share is a different quantity. Scoring takes another 46.3 % of pruned-16's time (t_score
  0.131 s for 16 candidates).
- *Rewrite.* "PF assimilation and neighbour lists account for 15.0 % of G\*'s per-decision time (component medians), so
  pruning candidates cannot exceed about 6.7× and cannot give 10×; measured full / pruned-16 = 3.22."

**S7. §5 (ii): "Neither PPO nor DAgger distillation … reaches G\*: … −4.4 pp (student)".**
- *Evidence.* The two halves are not equally supported.
  - **RL.** It is clearly below G\*: G\* − RL ci95 [+0.22, +13.67] pp.
  - **Student, success.** On test3 the student − G\* success ci95 is [−9.33, +0.56] pp and includes 0. Only the one-sided
    5 % reading excludes 0.
  - **Student, BI.** ci90 [−0.104, +0.008] includes 0.
  - All of this is descriptive (no pre-registered test). The student's binding evidence is the D3 non-inferiority
    failure on val3.
- *Rewrite.* "Neither learned policy was shown to reach G\*: the student failed the D3 non-inferiority rule on val3
  (Δ̂_succ −4.40 pp vs threshold −1.68 pp), and on test3 it trails by −4.4 pp (significant one-sided only) while RL
  trails by −7.0 pp (ci95 [+0.2, +13.7] for G\* − RL)."

### Moderate

**M1. §2.1: "Doubling round-0 data (train decisions 7,957 → 17,083) cut the BI deficit by about half."**
- *Evidence.* The causal attribution is not supported, and the data size is mislabelled.
  - The remedy doubled round 0 **and** both DAgger rounds, and it trained fresh students (07c status note, §4 D3).
  - 17,083 is the end-of-round-2 total (a 2.15× increase), not the round-0 size.
  - With 3 seeds per arm and no paired test, the change also contains retraining variance. Pass 1 admits it is
    untested, but the verb "cut" still asserts the cause.
- *Rewrite.* "After the one remedy (round 0 and both DAgger rounds doubled; 7,957 → 17,083 training decisions), the
  point estimates moved from −0.199 to −0.096 nats BI and from −5.87 to −4.40 pp success; this change was not tested."

**M2. §2.6: "v3 learned policies are much closer to G\*".**
- *Evidence.* The comparison mixes heads, splits and pipelines.
  - It sets the v3 relative-head RL (−7.0 pp, test3) against the v2 **absolute**-head RL (−20.6 pp, validation).
  - The v2 relative-head RL was 7.5–15 pp short (exploratory; `07_hypotheses_v3` §0.3/§3.3), so v3's −7.0 pp sits at
    the edge of the v2 relative-head range.
  - The student has no v2 counterpart.
- *Rewrite.* "v3 RL with the relative head trails G\* by 7.0 pp on test3, similar to the 7.5–15 pp of v2's exploratory
  relative-head runs and less than v2's absolute head (−20.6 pp, validation); the pipelines differ, so no change is
  attributable."

**M3. §2.3 and §3.3: "only a true Δ above about 0.41 nats could have passed"; "The design could detect only Δ ≳ 0.41
nats".**
- *Evidence.* 0.41 (0.10 + 0.3106) is the **observed** estimate needed to pass, and a true Δ of 0.41 passes only about
  half the time.
- From the bootstrap half-width, SE ≈ 0.3106 / 1.645 = 0.189. 80 % power needs a true Δ ≈ 0.10 + 0.189·(1.645 +
  0.842) ≈ **0.57 nats**.
- *Rewrite.* "Passing required an observed Δ > 0.41 nats; with SE ≈ 0.19, the test had about 80 % power only for a true
  Δ near 0.57 nats."

**M4. §4.5 and §5 (iii): per-episode ratio "roughly 13–18×".**
- *Evidence.* The figure rests on assumptions that are not in the JSON.
  - It assumes decisions per episode equal executed probes (3–4).
  - It sets greedy's L_final to zero, although §1.8 counts greedy's read-out in L_ep. Including it lowers the ratio.
  - L_ep was not measured.
  - Pass 1 labels the figure "derived, not protocol", but it is still presented as a range.
- *Rewrite.* "Assuming 3–4 decisions per episode and no greedy read-out cost, Σ L_dec(G\*) / (Σ L_dec(student) +
  L_final) ≈ 13–18×; the protocol L_ep was not measured and would be lower."

**M5. §5 (iii): "The student is about 2,238× cheaper per decision".**
- *Evidence.* The figure needs three qualifiers.
  - It is a ratio of medians from a Lat′ protocol that was not completed: `protocol_complete: false`, six CIs above
    10 %, two machines pooled.
  - It is against full-size G\*, not "at its own accuracy" (H1b was never reached).
  - The G\* median CI alone, [0.791, 0.941] s, spans about 1,940–2,310× at the student median.
- *Rewrite.* "Per decision, the student's median latency is about 2,200× below full-size G\* (pooled-machine Lat′,
  protocol incomplete; G\* median CI alone ≈ 1,900–2,300×), not compared at equal accuracy."

**M6. §3.2: "The 5 missing paired episodes can move Δ̂_succ by at most 5/300 = 1.67 pp."**
- *Evidence.* The bound is wrong. The new mean is (295·d + s)/300 with s ∈ [−5, 5] and d = −0.2011, so the largest
  upward shift is (5 − 5d)/300 = **2.0 pp**. The verdict is unaffected: −0.181 is still far below −0.007.
- *Rewrite.* "The 5 missing episodes can raise Δ̂_succ by at most 2.0 pp (to −18.1 pp), still 17 pp below the
  threshold, so the D3-B verdict cannot flip."

**M7. §4.2: "at an unchanged true-identity mass of 0.2282, so the flip is a pose boundary, not an identity tie".**
- *Evidence.* The JSON records only the true identity's mass (`12_e_analysis.flips`).
  - The MAP identity can still change if other identities' masses shift.
  - The success decomposition (identity vs pose) is not recorded.
  - 07c says only "outside the tie band".
- *Rewrite.* "The one counted flip occurred with the true-identity mass unchanged (0.228) and outside the [0.45, 0.55]
  tie band; the JSON does not record which part of the success criterion changed."

**M8. §4.2: "Sub-8 read-out costs 40.6 s per episode …, which limited every n in this record."**
- *Evidence.* Several quantities do not use the grid evaluator at all:
  - H2 g_T (M3 on M2, the no-grid actions; n = 500);
  - H3 (100 beliefs per κ);
  - Lat′ (1,000 decisions);
  - label fit.
- *Rewrite.* "Sub-8 read-out costs 40.6 s per episode, which limited the grid-scored rows (G5′ re-reads, D3/D3-B, M4 on
  300 episodes)."

### Minor

**m1. §1.1 E′ row: "mass 0.2282 under both settings".**
- *Evidence.* mass_sub8 = 0.228132, which rounds to 0.2281. Only mass_sub4 (0.228155) rounds to 0.2282.
- *Rewrite.* "true-identity mass 0.2282 (sub 4) / 0.2281 (sub 8)".

**m2. §1.2: "The RL seed spread (5.18 to 5.65) is about 3.3 times the student's".**
- *Evidence.* The range ratio is 0.4767 / 0.1376 = 3.46; 3.3 is the ratio of the sample SDs (0.253 / 0.077).
- *Rewrite.* "The RL per-seed SD of g_T is about 3.3× the student's (0.253 vs 0.077 nats; range ratio 3.5)."

**m3. §3.4 item 6: "Sub 4 → 8 flips 7.5 % of S0 calibration successes".**
- *Evidence.* `success_flip_rate_vs_sub4` = 0.075 is the share of the 200 episodes (about 15) whose success flips, not a
  share of the successes.
- *Rewrite.* "Sub 4 → 8 flips the success outcome of 7.5 % of the 200 S0 calibration episodes."

**m4. §2.4: "That is 2.3 pp below G\* on the same pilot (0.426)."**
- *Evidence.* G\* has n = 500 and b_fan n = 154, so the episode sets are not the same. Nothing is paired, and the
  2.3 pp gap is smaller than b_fan's SE of 4.0 pp.
- *Rewrite.* "That is 2.3 pp below G\*'s pilot3 success (0.426, n = 500), unpaired and within b_fan's SE (0.040)."

**m5. §2.3: "RL is unstable across seeds."**
- *Evidence.* There are 3 seeds and no test of seed variance, so "unstable" is a characterisation the data cannot carry.
- *Rewrite.* "RL varies more across its 3 seeds than the student (test success range 7.7 vs 1.0 pp; g_T range 0.48 vs
  0.14 nats)."

**m6. §2.3 and §3.4 item 1: "No TOST is implemented for H2."**
- *Evidence.* `tost()` exists in `code/touchbed/stats.py`. It was pre-registered only for student vs G\* success (§1.9)
  and was not run for H2.
- *Rewrite.* "No equivalence test (TOST) was pre-registered or run for H2."

**m7. §1.1 G5′ row: "PASS in all 3 cells".**
- *Evidence.* §4 defines G5′ on random 200 per cell. The random rows have n = 62 (S0), 199 (S12) and 161 (A12), and the
  δ_c, ε_c and D_c values rest on them. The JSON `passes: true` is computed on incomplete rows.
- *Rewrite.* "Provisional PASS in all 3 cells on incomplete random rows (n = 62 / 199 / 161 of 200); D_c ≥ 0.35
  everywhere, so δ_c = 0.04 (cap) is unlikely to move."

---

## B. Numbers verified as correct

- **Cal′.**
  - n\*: S 0.605 → 4 and A 0.985 → 3. At sub 8: S 0.62, A 0.985, n\* unchanged.
  - Verification: S12 3.96, A12 2.98.
  - S0 sub-4 vs sub-8 flip rate 0.075.
- **E′.**
  - mean |ΔBI| 0.0126, max 0.0523; 1 counted flip of 16 episodes; 40.6 s per episode.
- **G1′.**
  - (a) mean 0.8290; run 0.8629 is above the 0.86 band edge.
  - (b) mean 0.00254, UB 0.00374, n = 100.
  - (c) 0.7438 vs exact 0.7166, band [0.5733, 0.8600].
  - (a) and (b) are identical to `results/v2/12_g1_analysis.json` at full double precision, so "bit-for-bit" holds.
- **G5′ (sub 8 and sub 4).**
  - G\*: S0 0.660 ± 0.0212, BI 7.012; S12 0.426 ± 0.0221, BI 6.290; A12 0.470 ± 0.0223, BI 6.714.
  - Random and heuristic rows, all values and n as tabulated.
  - D_c: 0.402 / 0.351 / 0.445. ε_c: 0.2184 / 0.3145 / 0.3357.
  - Flags: H_star_success −1.0 in S0; flat_screen in S12 only.
  - Sub 4: b_fan S12 0.395, A12 0.390; b_spread S0 0.465 (all n = 200).
  - ε_S12 = min(0.05·6.2901, 0.15·3.2918) = 0.31451, and D_c(S12) = 0.3506.
- **Lat′.**
  - Medians: student 0.408 ms [0.4036, 0.4137]; G\* full 0.9135 s [0.7910, 0.9413]; pruned-16 0.2833 s; L_final 0.2043 s.
  - Relative half-widths 0.012 / 0.082 / 0.007 / 0.050.
  - Ratios 2,238 and 3.224.
  - Six configurations in `ci_too_wide`, maximum 0.146 (g500_128_16).
  - Component shares: t_score = 78.5 % of G\* full; t_assim + t_nb = 47.8 % of pruned-16.
- **D3, first attempt.**
  - Δ̂_succ −0.0587 vs −0.0143; Δ̂_BI −0.1988 vs −0.15.
  - Per seed −0.042 / −0.080 / −0.054.
  - The threshold reproduces as −0.04 + 1.645·0.022056·√0.5 = −0.01435.
- **D3, remedy.**
  - −0.0440 vs −0.0168; −0.0962 vs −0.15 (passes); per seed −0.046 / −0.046 / −0.040.
  - Seed 503 is exactly −0.04, so `seeds_ok.503: false`.
  - Recomputed thresholds −0.01681 and −0.28160 → −0.15.
  - The val3 G\* means (0.446, 6.3808) are the same in both files.
  - Changes from the first attempt: +1.47 pp and +0.103 nats; ratios 0.484 (BI) and 0.75 (success).
- **D3-B.**
  - −0.2011 vs −0.0073; −1.0105 vs −0.15; per seed −0.173 to −0.217.
  - n = 295 of 300; 19.4 pp below the threshold.
  - The stale eps_S12 is 0.314266 vs 0.314507, which implies a G\* BI of 6.2853.
- **First-attempt note vs JSON.** The 07c note values (−6.8 pp, −0.19, −5.1 / −8.5 / −6.6 on 468 episodes) and the JSON
  values (−5.87, −0.199, −4.2 / −8.0 / −5.4 on 500) are both quoted correctly.
- **Label fit.** All 54 table entries match `14_labelfit`.
  - Ranges: train R̄ 0.169–0.206; train top-1 0.511–0.534.
  - Held-out top-1 is below 0.50 for 4 of 6 history students.
  - Train-to-held-out R̄ gaps are 0.007–0.024.
- **H2.**
  - Means 5.3678 / 5.3676 and all six per-seed values.
  - diff +0.000232; bounds −0.3103 / +0.3034; p 0.4883 / 0.5117; B = 10,000.
  - Per-seed SDs 0.077 / 0.253.
  - "lower / upper = 5 % / 95 % quantiles" is confirmed in `stats.crossed_bootstrap_diff` (alpha = 0.05).
- **M4.**
  - All three rows (success, BI, probes, per-seed values).
  - All six diffs with their ci90 and ci95; ci90 = one-sided 95 % is confirmed in `code/analysis_m4_v3.py`.
  - Gap closure is correctly withheld (LB 0.0122 < 0.04).
- **H3.**
  - All 24 table values for κ = 0, 2 and 12.
  - Bias check: 1.9396 / 2.0261, ratio 0.9573, 3 floored rollouts, difference 0.0865 nats (4.3 %).
  - Ordering flag true; region Hold, not downgraded; margin 0.0079.
- **RL sweep.** 50,048 episodes; cfg 2 at lr 1.09e-3 scored 5.666 against at most 4.747 (+0.919); validation stream
  `val_v2`.
- **v2 quotes.** G(12) 0.0146 (UB 0.0208); G(0) / G(2) 0.0049 / 0.0080; 0.204 vs 0.410 (−20.6 pp); remedy 0.2433; B8
  n = 8 with 0 flips; 0.073–0.166 nats.
- **Per-episode arithmetic.** The arithmetic of 13.3× (n = 3) and 17.7× (n = 4) is correct; the assumptions are what M4
  questions.
