# Stage 14 · RESULT_ANALYSIS (v1, pre-run checks) — fresh opus subagent, 2026-10-28

> System (pass 1): "You are a quantitative ML analyst. Always cite exact numbers from the provided data."
> System (pass 2): "You are a top-conference area chair who has rejected 80% of papers you've reviewed this cycle. …"
> This file merges both passes. Section 6 lists every claim the second pass flagged and the rewrite that is used in the
> final text. Wherever the two passes disagreed, the final text uses the rewrite.

**Data used (and nothing else):** `results/v1/12_manipulation_checks.md`, `results/v1/12_pfcheck_analysis.json`,
`results/v1/checks/{myopia_S,myopia_A,myopia_identity_S,confusability_S,confusability_A}.json`. **Context:**
`docs/07_hypotheses.md` §1.2–1.5, H2a/H2b (and H1a, H3 for the preconditions they define), `docs/07c_amendment_v1_1.md`,
`docs/10_dev_findings_v1.md`.

**Status of the evidence.** These are pre-registered manipulation and convergence checks, so no hypothesis is tested
here. No trained policy appears in any of the files.

**Statistics computed for this report** (script: numpy, run with `python3 -I`):
- Over the 100 belief rows of each myopia file, I computed the mean, the SE (sample SD with ddof = 1, divided by √n) and
  the median.
- Percentile bootstrap over beliefs: B = 10,000 resamples of the 100 rows with replacement, RNG `default_rng(0)`. I
  report the two-sided 95 % interval (2.5th–97.5th percentiles) and the one-sided 95 % upper bound (95th percentile).
- Exact binomial sign test on the beliefs with a non-zero gap, one-sided H₁: P(gap > 0) > ½.
- Greedy − random success: unpaired normal approximation, SE = √(p₁q₁/n + p₂q₂/n), n = 300 each. The per-episode
  pairing was not available in the cited files.
- Confusability: read directly from the files. C is the mean of `per_shape`.
- PF check: all numbers are copied from `12_pfcheck_analysis.json`. Its CIs are 90 % paired intervals, computed
  upstream.

---

## 1. Metrics Summary

### 1.1 Geometric confusability (§1.2 requirement: C(S) ≥ 0.90, C(A) ≤ 0.80)

| set | C (file) | per-shape max (self or cross) | shapes > 0.80 |
|---|---|---|---|
| S | **0.9709** | 0.977, 0.925, 0.985, 0.976, 0.977, 0.966, 0.985, 0.976 | all 8 (by design) |
| A | **0.7724** | 0.790, 0.791, **0.806**, 0.790, **0.818**, 0.769, **0.818**, 0.597 | **A2, A4, A6** |

- The set-level requirement holds. C(S) is 0.071 above its threshold. C(A) is 0.028 below its threshold.
- §1.2 also has a per-shape acceptance rule for A ("accepted only if … confusability scores ≤ 0.80"). Three of the
  eight A shapes violate it: A2 = 0.806 and A4 = A6 = 0.818, where A4 and A6 are each other's nearest neighbour.
- Per `12_manipulation_checks.md`, the values are multi-start Nelder–Mead maxima and therefore *lower bounds*. The true
  C(A) can only be higher than 0.7724.
- Anomaly: in the S matrix, the diagonal (self near-symmetry) entries of S_rect, S_rtri and S_hex are exactly **0.0**.
  These three base shapes have non-trivial G_k. A 2:1 rectangle rotated just over 10° should have a large IoU with
  itself, so 0.0 looks like a skipped computation or sentinel value, not a measured c_self. It does not change C(S),
  because each of these rows is dominated by its cross-pair value (0.977 / 0.925 / 0.985).

### 1.2 Myopia gap (§1.2 requirement: G(S) ≥ 0.10, G(A) ≤ 0.03)

Run parameters (all three files): 1,000-particle PF, C1 = 16, Y1 = 8, C2 = 16, M = 16. The two selected first actions
are re-estimated with fresh samples (2·Y1 outcomes, 4·M samples). n = 100 beliefs (1 prior, plus beliefs after 1 or 2
probes: S 48/51, A 54/45).

| quantity | S, full state | A, full state | S, identity only (exploratory) |
|---|---|---|---|
| **G = mean rel. gap** | **−0.0329** | **−0.0198** | **+0.0029** |
| SE | 0.0102 | 0.0099 | 0.0117 |
| bootstrap 95 % CI | [−0.0538, −0.0143] | [−0.0387, −0.0007] | [−0.0201, +0.0251] |
| one-sided 95 % upper bound | −0.0171 | −0.0038 | +0.0213 |
| median | 0.000 | 0.000 | 0.000 |
| mean abs. gap (nats) ± SE | −0.1101 ± 0.0348 | −0.1116 ± 0.0354 | +0.0053 ± 0.0124 |
| abs. gap bootstrap 95 % CI | [−0.180, −0.045] | [−0.182, −0.045] | [−0.019, +0.029] |
| beliefs with gap = 0 / > 0 / < 0 | 51 / 13 / 36 % | 41 / 21 / 38 % | 57 / 23 / 20 % |
| beliefs with rel. gap ≥ 0.10 | 3 % | 7 % | 12 % |
| range of rel. gap | [−0.537, +0.156] | [−0.338, +0.261] | [−0.331, +0.425] |
| sign test, non-zero beliefs (k/n positive, one-sided p) | 13/49, p = 0.9998 | 21/59, p = 0.991 | 23/43, p = 0.38 |
| mean max EIG₁ (nats) ± SE | 3.066 ± 0.113 | 3.479 ± 0.111 | 0.916 ± 0.035 |
| mean EIG₂ greedy / two-step-selected (nats) | 4.182 / 4.072 | 4.746 / 4.635 | 1.332 / 1.337 |
| **R_NC** (greedy action with P(NC) ∈ [0.2, 0.8]) | **0.03** (3/100) | **0.07** (7/100) | 0.08 (8/100) |
| mean P(NC) of greedy action; share with P(NC) = 0 | 0.043; 45 % | 0.045; 30 % | 0.060; 46 % |

By number of prior probes:

| subset | S full: G / abs. gap | A full: G / abs. gap | S identity: G / abs. gap |
|---|---|---|---|
| 1 probe (n = 48 / 54 / 48) | −0.0405 / −0.139 | −0.0353 / −0.178 | +0.0032 / +0.006 |
| 2 probes (n = 51 / 45 / 51) | −0.0256 / −0.080 | −0.0016 / −0.034 | +0.0027 / +0.004 |

All values above match `12_manipulation_checks.md` (−0.033 / −0.020 / +0.003; −0.110 ± 0.035, −0.112 ± 0.035,
+0.005 ± 0.012; R_NC 0.03 / 0.07; mean max EIG₁ 3.07 / 3.48 / 0.92). The identity-only R_NC (0.08) is not reported
there; it is new here.

### 1.3 Evaluation-PF convergence (N = 8,000 vs 32,000; 300 paired episodes per cell; Δ = 32k − 8k)

| cell | Δ success (90 % CI) | Δ identity (90 % CI) | Δ ball info, nats (90 % CI) | Δ evidence-IG, nats | A3 pass |
|---|---|---|---|---|---|
| A, T3, random | −0.0233 [−0.050, +0.003] | −0.020 | **+0.378** [0.255, 0.500] | −0.188 | no |
| A, T3, greedy | +0.0067 [−0.027, +0.040] | +0.003 | **+0.396** [0.255, 0.545] | −0.738 | no |
| A, T10, random | 0.0000 [−0.020, +0.020] | −0.010 | **+0.089** [0.022, 0.159] | −1.213 | no |
| S, T3, random | +0.0133 [−0.020, +0.047] | +0.020 | **+0.364** [0.242, 0.490] | −0.225 | no |
| S, T3, greedy | −0.0133 [−0.063, +0.037] | 0.000 | **+0.377** [0.223, 0.529] | −0.611 | no |
| S, T10, random | **+0.0600 [+0.013, +0.110]** | **+0.077 [0.030, 0.127]** | **+0.335** [0.193, 0.486] | −0.870 | no |

Against the §1.4 rule (|Δ success| ≤ 1 pp, 95 % CI inside ±2 pp, |Δ info| ≤ 0.05 nats):
- The success point-estimate criterion is met in 2 of 6 cells (A-T3-greedy, A-T10-random).
- The ±2 pp CI criterion fails in all 6 cells, even on the narrower 90 % CIs. The narrowest interval is [−0.020, +0.020]
  for A-T10-random.
- The ball-information criterion fails in all 6 cells. The smallest deviation is 0.089 nats, and every 90 % CI excludes
  0 in the direction "32k higher".
- The cells for greedy at T = 10 and for a pilot sPCE-total policy are absent from the JSON. Raw `A_T10_greedy_*`
  files exist in `results/v1/pfcheck/`, but the provided analysis does not include them and I have not analysed them.

### 1.4 Greedy vs random (H1a precondition: greedy ≥ random + 10 pp at T ∈ {3, 5}, both sets)

At T = 3, N_eval = 32k, 300 episodes:

| set | greedy | random | Δ | SE (unpaired) | 95 % CI |
|---|---|---|---|---|---|
| A | 0.767 | 0.123 | +0.643 | 0.031 | [0.583, 0.704] |
| S | 0.420 | 0.133 | +0.287 | 0.035 | [0.219, 0.355] |

T = 5 is not reported.

---

## 2. Comparative Findings

1. **Set S vs set A on the myopia gap.** On the full state, neither set shows a positive mean gap. Both bootstrap CIs
   lie entirely below 0 (S [−0.054, −0.014]; A [−0.039, −0.001]). The pre-registered ordering G(S) ≥ 0.10 > 0.03 ≥ G(A)
   is not observed: G(S) = −0.033 is *lower* than G(A) = −0.020. The two absolute gaps are almost identical
   (−0.110 vs −0.112 nats). By this estimator, S is not more decision-ambiguous than A, even though C(S) = 0.971 vs
   C(A) = 0.772. **Geometric confusability did not translate into a measured myopia gap.**
2. **Full-state vs identity target on S.**
   - Full state: G = −0.033. Identity: G = +0.003 (CI [−0.020, +0.025]).
   - The identity target is the only configuration with a non-negative point estimate. It also has the largest share
     of beliefs with rel. gap ≥ 0.10 (12 % vs 3 %) and the largest single gap (+0.425).
   - Its sign test is consistent with no systematic direction (23/43 positive, p = 0.38).
   - Per-touch identity EIG is small: mean max EIG₁ = 0.916 nats, vs 3.066 nats for the full state on the same beliefs
     (the n_probe pattern matches row for row). This is consistent with F2: most full-state information is fine pose.
3. **NC-relevance.** R_NC(S) = 0.03 < R_NC(A) = 0.07. This is the reverse of the H3 precondition, which requires
   R_NC(S) ≥ 0.20 and R_NC(S) > R_NC(A). The greedy action has P(NC) = 0 for 45 % of S beliefs.
4. **PF size and the evaluation metric.**
   - Going from 8k to 32k particles raises ball information by 0.089–0.396 nats in every cell. It lowers evidence-IG
     by 0.19–1.21 nats.
   - Success is stable within ±2.3 pp in 5 of 6 cells. The exception is S-T10-random, where 32k gives +6.0 pp success
     and +7.7 pp identity, and both 90 % CIs exclude 0.
   - The shift is not uniform across cells: A-T10-random has Δ success = 0.000, while S-T10-random has +0.060. So the
     8k PF does not shift every cell equally.
5. **Greedy vs random.**
   - Greedy beats random by a wide margin at T = 3: by 64.3 pp on A and 28.7 pp on S. The lower 95 % bounds are 58.3 pp
     and 21.9 pp, both well above the 10 pp precondition.
   - S is much harder for greedy than A (0.420 vs 0.767), while random is at a similar level on both (0.133 vs 0.123).

---

## 3. Statistical Checks

| check | rule | measured | verdict |
|---|---|---|---|
| C(S) ≥ 0.90 | §1.2 | 0.9709 | pass |
| C(A) ≤ 0.80 (set level) | §1.2 | 0.7724 (lower bound on true value) | pass, margin 0.028 |
| each A shape ≤ 0.80 | §1.2 acceptance rule | A2 0.806, A4 0.818, A6 0.818 | **fail (3/8 shapes)** |
| G(S) ≥ 0.10 | §1.2 | −0.0329; one-sided 95 % upper bound −0.0171 | **fail**; the threshold is far outside the CI |
| G(A) ≤ 0.03 | §1.2 | −0.0198; upper bound −0.0038 | pass |
| G_identity(S) ≥ 0.10 (exploratory, not pre-registered) | — | +0.0029; upper bound +0.0213 | would fail |
| R_NC(S) ≥ 0.20 and > R_NC(A) | H3 precondition | 0.03 vs 0.07 | **fail on both parts** |
| PF N vs 4N | §1.4 / A3 | fails in 6/6 cells (ball info 6/6; CI width 6/6; success point estimate 4/6) | **fail** |
| greedy ≥ random + 10 pp | H1a precondition | T = 3: +64.3 pp (A), +28.7 pp (S) | met at T = 3; T = 5 not reported |

**Additional notes on the tests.**
- **Why G can be negative.** The true gap is EIG₂* − EIG₂^greedy ≥ 0 by definition. With fresh re-estimation, the
  computed quantity is an unbiased estimate of V(â₁) − V(a₁^greedy), where â₁ is the first action picked by the noisy
  two-step estimates among C1 = 16 candidates. Since V(â₁) ≤ V*, the estimate is in expectation a **lower bound** on
  the true gap. It can be negative, and it is here: 36 % of S beliefs, minimum −0.537. So the data show that the
  *procedure* "pick a₁ by noisy two-step MC" does no better than greedy at this budget. **They cannot bound the true
  gap from above.**
- **Sample sizes.** The pre-registered estimator used C = 32 and M = 32 (§1.2). The run used C1 = 16, Y1 = 8, C2 = 16,
  M = 16, plus fresh re-estimation. This deviation is not recorded in `07c_amendment_v1_1.md`.
- **No positive control.** No positive control was run through this estimator. The analytic notch problem of H2b-P2
  (§4: greedy ≈ 0.2 nats, optimum ≈ 0.69 nats, relative gap ≈ 0.7) is the natural check that the estimator can detect
  a gap that is known to exist.
- **PF-check CIs.** The JSON reports paired 90 % CIs, while the pre-registered rule refers to 95 % CIs. Since every
  cell already fails on the 90 % interval or on ball information, the verdict does not depend on this difference.
- **Precision of the PF check.** A 95 % CI of half-width ≤ 2 pp on a paired success difference needs SE ≤ ~1 pp. With
  300 paired binary episodes, that requires a discordant-pair rate of about 3 % or less. The check is therefore near
  the limit of what 300 episodes can show, and fails mostly on precision, except in S-T10-random and on ball
  information.
- **Uncorrected tests.** The bootstrap and sign tests above are not multiplicity-corrected. They are descriptive checks
  of pre-registered thresholds, not hypothesis tests.

---

## 4. Limitations

1. **The myopia-gap estimate is a lower bound, with unknown power.**
   - Fresh re-estimation measures the value of the action that was selected, not the optimum.
   - Only 16 first actions are sampled, so set-up moves may not be among the candidates.
   - The horizon is two steps. On S, a set-up move may need more than one localizing touch before a feature probe pays
     off, and a two-step horizon would not see that.
   - Without a positive control, "no gap detected" cannot be read as "no gap exists".
2. **Bank composition.** The bank holds the prior plus beliefs after 1–2 *random* probes, not beliefs reached by a
   competent policy at T ∈ {3, 5}. The gap may differ on the beliefs that matter for H2a.
3. **Target mismatch.** The pre-registered G uses full-state EIG, which F2 shows is dominated by fine pose. The
   identity-only run is exploratory. Neither target is the success-region ("ball") information that the A2 amendment
   made co-primary.
4. **Confusability values are lower bounds** of IoU maxima. Three S self-symmetry entries are 0.0, which is
   unexplained.
5. **The PF check is incomplete.**
   - Greedy at T = 10 and the pilot policy cells are absent.
   - The claim that "mixing, not particle count" is the bottleneck rests on a 40-episode comparison (0.50 / 6.53 vs
     0.525 / 6.60) whose data are not in the cited JSON. With n = 40, a binomial SE is about 8 pp, so that comparison
     cannot distinguish the explanations.
   - N_eval = 32,000 is the reference arm but has not been shown converged itself. The greedy and random success values
     in 1.4 inherit that uncertainty.
6. **Greedy vs random** used an unpaired SE, because per-episode pairing was not in the cited files, and only T = 3 was
   reported.
7. **Independence of beliefs.** 100 beliefs per bank are treated as i.i.d. for the bootstrap. They come from random
   true states, which is reasonable, but the bank generation code was not inspected.

---

## 5. Conclusion

**What these checks show.**
- In this environment and with this estimator, **no positive two-step advantage over greedy was detected**, for either
  the full state or identity on S. The pre-registered manipulation check G(S) ≥ 0.10 fails decisively: the point
  estimate is −0.033 and the one-sided 95 % upper bound is −0.017.
- The H3 precondition fails: R_NC(S) = 0.03 against a required 0.20, and it is below R_NC(A) = 0.07.
- The evaluation PF fails the N vs 4N rule at N = 8,000.
- Confusability passes at set level but violates the per-shape rule for three A shapes.
- The H1a precondition is met at T = 3 only.

**What follows under the pre-registration.**
- §1.2 states that "Main runs do not start until it passes." S must therefore be redesigned or the check re-specified,
  for example with a larger C1 and Y1, a validated positive control, or a success-region target.
- Each such change must go into a dated amendment written *before* re-running, because iterating S until G passes is a
  forking path.
- N_eval must be re-chosen: 32k, or a better-mixing kernel validated on ≥ 300 episodes per cell.
- H3 is "untestable" by its own rule unless the redesign raises R_NC(S).

**Implications for the hypotheses** (judgements, not tests):
- **H2 (non-myopic > myopic).** The current evidence gives no a-priori support. It does not refute a non-myopic
  advantage, because the estimator is a lower bound with no positive control. But the best-case configuration (identity
  target, S) has an upper bound of +0.021, about one-fifth of the 0.10 threshold. **Expect H2a to be hard to confirm
  on the current S.** The project should either (i) validate the estimator on the H2b-P2 notch control and redesign S
  until a gap is *measured*, or (ii) pre-register H2a as a likely null, with TOST, and move the paper's weight to H1.
- **H3 (planning for no-contact outcomes).** With R_NC(S) = 0.03, misses are rarely decision-relevant for greedy
  choices. H3 is untestable under its precondition as the set stands.
- **H1 (amortization vs greedy).** There is no policy data yet. Greedy is a strong comparator: it beats random by
  28.7–64.3 pp at T = 3. The near-zero myopia gap suggests that little headroom exists *above* greedy. The realistic H1
  claim is therefore non-inferiority at much lower latency (H1a/H1b), not superiority. Full-size greedy costs ≈ 0.65 s
  per decision (A4 amendment), which leaves room for a large H1b latency ratio. Both remain untested.

---

## 6. Adversarial pass (area chair): unsupported claims and supported rewrites

| # | Claim (source) | Contradicting or missing evidence | Supported rewrite (used above) |
|---|---|---|---|
| 1 | "there is no sign of a positive gap to detect" (12_md) | The estimator is a lower bound on the true gap (fresh re-estimate of a noisy argmax over C1 = 16). No positive control was run, and C/M were halved from the pre-registered 32/32. | At C1 = 16, Y1 = 8, C2 = M = 16, the procedure detected no positive gap (G(S) = −0.033, upper bound −0.017). Whether a gap exists that this estimator cannot see is untested. |
| 2 | "the two-step estimator is noisy at this budget" (12_md) | Plausible, but the estimator's variance was never measured (no repeated estimates per belief). The only evidence is indirect: 36 % negative gaps, minimum −0.537. | Negative gaps on 36 % of S beliefs (minimum −0.537) are consistent with selection noise in the two-step estimates; their variance was not measured directly. |
| 3 | "mixing, not particle count, is the bottleneck" (12_md) | One 40-episode comparison (binomial SE ≈ 8 pp) whose data are not in the analysis JSON. No 32k × 30-MH arm. | On 40 episodes, 2k particles × 30 MH steps gave 0.50 / 6.53 nats vs 0.525 / 6.60 at 32k × 3 MH. That is suggestive that mixing matters, but too small to rank the explanations. |
| 4 | "Confusability … PASS" (12_md) | Three A shapes exceed the per-shape 0.80 acceptance rule of §1.2 (0.806, 0.818, 0.818), and the values are lower bounds. | The set-level confusability requirement passes (C(S) = 0.971, C(A) = 0.772), but A2, A4 and A6 violate the per-shape acceptance rule. |
| 5 | "Greedy vs random … met" (12_md) | The precondition is for T ∈ {3, 5}, and only T = 3 is reported. N_eval = 32k is not shown converged. | At T = 3, greedy beats random by 64.3 pp (A) and 28.7 pp (S), lower 95 % bounds 58.3 / 21.9 pp. T = 5 is still to be checked. |
| 6 | "+6 pp on a 40-episode subset of S, T=10 (0.425 vs 0.525)" (12_md) | Understates the evidence: the full 300-episode cell itself shows +6.0 pp (0.46 → 0.52, 90 % CI [1.3, 11.0] pp) and +7.7 pp identity. | On all 300 S-T10-random episodes, success rises by 6.0 pp from 8k to 32k particles (90 % CI [1.3, 11.0]). |
| 7 | "success differences up to −2.4 pp (A, T=3, random)" (12_md) | The largest absolute difference is +6.0 pp (S-T10), and the A-T3 value is −2.33 pp. | Success differences range from −2.33 pp (A-T3-random) to +6.0 pp (S-T10-random). |
| 8 | "ball information systematically 0.1–0.4 nats higher" (12_md) | The minimum is 0.089 nats (A-T10-random). | Ball information is 0.089–0.396 nats higher at 32k in all 6 cells (every 90 % CI > 0). |
| 9 | Pass 1 draft: "greedy is near-optimal in this environment" | Measured only at a two-step horizon, over 16 sampled first actions, on random-probe beliefs. | Within a two-step horizon over 16 sampled first actions, no first action outperformed the greedy one on re-estimation. |
| 10 | Pass 1 draft: "S is not more ambiguous than A" | Confusability says S is far more ambiguous geometrically (0.971 vs 0.772). Only the *estimated myopia gap* fails to separate the sets. | The estimated myopia gap does not separate S from A (−0.033 vs −0.020), despite C(S) = 0.971 vs C(A) = 0.772. |
| 11 | Pass 1 draft: "H2 is unlikely to hold" | No policy has been trained. G is a lower-bound estimate. | The manipulation check supporting H2a failed, so there is currently no measured premise for a non-myopic advantage on S. |
| 12 | Pass 1 draft: "H1 non-inferiority is likely" | No sPCE policy data exist in any cited file. | H1 is untested. The checks show only that greedy is a strong comparator at T = 3. |
| 13 | "PF check FAIL at N = 8,000" (12_md) | Correct, but the check is incomplete (greedy T = 10 and pilot policy absent) and uses 90 % rather than 95 % CIs. | N = 8,000 fails the A3 rule in all 6 completed cells, mainly on ball information (Δ 0.089–0.396 nats). The greedy-T10 and pilot-policy cells are not yet analysed. |
| 14 | "NC-relevance is low (3–7 %)" (12_md) | Supported, but it omits that R_NC(S) < R_NC(A), which reverses the H3 precondition. | R_NC(S) = 0.03 and R_NC(A) = 0.07, so the H3 precondition (≥ 0.20 and S > A) fails on both parts. |
