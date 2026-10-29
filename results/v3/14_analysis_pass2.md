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
