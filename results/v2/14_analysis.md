# Stage 14 · Analysis of the v2 gate record (G0–G5 + exploratory diagnostics)

> System: "You are a quantitative ML analyst. Always cite exact numbers from the provided data."
> Task: "Analyze run metrics and produce markdown report with statistical interpretation. Use the ACTUAL quantitative
> values provided above — do NOT invent numbers. Required sections: Metrics Summary (with real values), Comparative
> Findings, Statistical Checks, Limitations, Conclusion."

**Scope.** No v2 main experiment has run. This analysis covers the pre-registered pre-run gates G0–G5
(`docs/07_hypotheses_v2.md` §4), the amendments B1–B9 and the status notes (`docs/07c_amendment_v2_0.md`), and the
exploratory diagnostics in `12_diag_analysis.json`. All numbers come from `results/v2/12_*.json`,
`12_g3_hp_selection.txt` or the two docs. Derived numbers (differences, means of listed values, fractions of a gap) are
arithmetic on those values and are marked "derived". **Nothing in this file is a test-set result.** Every learned-policy
number is a pilot or validation number.

Notation: Δ = paired difference; pp = percentage points; BI = ball information in nats; 𝒜 = action set.
Cells are named by set and κ: S12 = (S, κ = 12), and so on.

---

## 1. Metrics Summary

### 1.1 Gate verdicts against the pre-registered rules

| Gate | Pre-registered rule (§4 / amendment) | Measured | Verdict |
|---|---|---|---|
| **G0 (ii)/(iii)** confusability | C(A) ≤ 0.80 (set level, B2) and per-shape ≤ 0.85 | C(A) = **0.802**; per-shape 0.755–0.821; C(S) = 0.971 (07c run-2 note) | **FAIL (marginal), reported, B7.** Set A kept. |
| G0 (i), (iv)–(viii) | all 8 items done with commit hash; unit tests green in CI | no output for these items in the analysed record | **Not demonstrated** by the data provided |
| **G1 (a)** notch, relative gap | mean of 5 runs in [0.8, 1.2] × exact 0.7166 = [0.5733, 0.8600] | mean **0.8290** (runs 0.8409, 0.7603, 0.8384, **0.8629**, 0.8425) | **PASS.** One run of 5 (0.8629) is above the band. |
| **G1 (b)** zero-gap bank | mean in [−0.01, +0.02] and one-sided 95 % UB < 0.03, 100 beliefs | mean **0.00254**, UB **0.00374**, n = 100 | **PASS** |
| **G2** headroom (after the one permitted escalation to κ_hi = 12) | G(κ_hi) ≥ 0.10 with LB > 0.05; G(0) ≤ 0.03; G(0) ≤ G(2) ≤ G(κ_hi) | G(12) = **0.0146** (LB 0.0098); G(0) = 0.0049 (UB 0.0071); ordering 0.0049 ≤ 0.0080 ≤ 0.0146 holds | **FAIL** on magnitude (`magnitude_ok: false`). The G(0) and ordering parts pass. |
| G2 (pre-escalation, κ_hi = 6) | same | G(6) = **0.0185** (LB 0.0121) | FAIL on magnitude only, so escalation was eligible (§1.2) |
| **G3 (i)** HP selection | 4 configs × 1 seed; selection metric fixed by B9 | hp0 4.894, **hp1 5.592**, hp2 5.288, hp3 5.291 (final validation ball-sPCE, S κ = 6 τ = 5.0) | Done (no pass rule) |
| **G3 (ii)** learnability at S12 | seed-mean validation success ≥ success(G*) − 5 pp = 0.410 − 0.05 = **0.360** | **0.204** (0.190 / 0.230 / 0.192), n = 500 paired | **FAIL** |
| G3 (ii) remedy (E_train × 2) | same | **0.2433** (0.224 / 0.258 / 0.248) | **FAIL** |
| G3 (ii) plateau within E_train cap | plateau before cap | all 3 seeds `train_status: max_episodes` (100,096 episodes) | **FAIL / not demonstrated**: they hit the cap |
| G3 (ii) objective saturation | < 10 % of training episodes | last-log sat_frac 0.1406 / 0.1016 / 0.1328 (mean 0.125, derived) | **FAIL** (on the last-log reading; see §3.3) |
| **G3 (iii)** notch learnability | seed-mean v_π ≥ 0.8 × 0.6150 = **0.4920** nats | **0.1719** (0.1770 / 0.1698 / 0.1688) = 27.9 % of V_opt; remedy 2× gives the same values | **FAIL** |
| G3 (iv) ball-sPCE vs BI bias | "reported" | **absent** from `12_g3_analysis.json`, although the script docstring promises it | **Not reported** |
| **G4** evaluation PF (as pre-registered) | \|ΔBI\| ≤ 0.05; \|Δsucc\| ≤ 1 pp with 95 % CI inside ±2 pp; 32k vs 128k (3 MH) | ΔBI +0.133 / +0.063 / +0.177 / +0.097 (A-rand / A-G* / S-rand / S-G*) | **FAIL in all 4 cells** |
| G4 pre-registered fallback | 32k × 10 MH vs 32k × 30 MH, same rule | A: ΔBI +0.045, Δsucc +1.17 pp [−0.50, +2.83]; S: ΔBI +0.039, Δsucc +3.67 pp [+0.83, +6.50] | **FAIL** (success) |
| G4 via B5 (final rejuvenation) | same rule vs 32k × 30 MH + 60 | A-G* r10 passes (ΔBI 0.048, Δsucc 0.91 pp [0.00, 1.82]); r30 fails A-G*; both fail A-random (ΔBI 0.116 / 0.080) | **FAIL** (not every cell) |
| G4 via B8 (grid reference) | same rule vs adaptive grid; cheapest method passing every cell | only pf128k_3mh and b5_ref pass, and only in A-G* | **No SMC kernel passes. The grid is adopted as the evaluation** (amendment route, not pre-registered) |
| B8 grid self-check | mean \|ΔBI\| ≤ 0.02 (sub 4 vs 8); no flips outside tie band | n = 8, mean 0.0042, max 0.0259, flips 0 | **PASS** (rule revised after one observation, §3.3) |
| **G5** comparator strength | G* ≥ random + 10 pp in every primary cell (300 pilot) | D(300) derived: A0 0.690, A6 0.430, A12 0.373, S0 0.407 (n = 150), S6 0.420, S12 0.367 | **PASS** in all 6 cells |
| G5 non-degeneracy §1.7 | success(G*) ∈ [0.15, 0.90]; D ≥ 20 pp; BI saturation < 50 % (first 200) | A0: success 0.855, D 0.685, **sat 0.815**; all other cells pass | **A0 FAILS** and is removed from the primary set (n*(A) = 3 cannot be lowered) |
| G5 flatness (§1.5, at S, κ_hi = 12) | \|Δsucc\| ≤ 2 pp and \|ΔBI\| ≤ 0.10 | S12: Δsucc +1.33 pp, **ΔBI +0.170** (n = 300) | **FAIL** → 𝒜 must become 64 × 8 for all methods |
| G5 flatness, S6 (not required) | same | **Δsucc −2.67 pp**, ΔBI +0.0085 | FAIL |
| G5 n* / τ_κ calibration | n* rule (§1.2); verified probes within n* ± 0.3 | n*(A) = 3, n*(S) = 4; all 6 verifications pass (2.745–2.97 on A, 3.885–4.10 on S) | **PASS**, but conditional on 𝒜 = 32 × 8, which the flatness failure voids |
| G5 rollout-planner latency (20 decisions) | "recorded" | **absent** from the record | **Not reported** |

**Bottom line of the gate table.**
- Of the gates that must pass before any main run (G0, G3, G4, G5), **none passes cleanly as pre-registered**.
  - G3 fails, including after its one remedy.
  - G4 fails as pre-registered, and its fallback fails too.
  - G5 fails flatness and loses A0.
  - G0 has a recorded marginal failure.
- G1 passes. G2 fails after the single permitted escalation.

### 1.2 Per-metric, per-condition values

**G1: exact notch control** (5 estimator runs; exact V_opt = 0.6150, exact V_greedy = 0.1743).

| Quantity | Run values | Mean (derived) | Exact | Estimate / exact (derived) |
|---|---|---|---|---|
| V_LA | 0.5853, 0.6387, 0.6621, 0.5771, 0.5549 | 0.6036 | 0.6150 | 0.981 |
| V_greedy | 0.0931, 0.1531, 0.1070, 0.0791, 0.0874 | 0.1040 | 0.1743 | **0.597** |
| Chosen action | LA: 71 in all 5 runs; greedy: 31, 20, 30, 28, 25 | — | — | — |

**G2: headroom on S** (100 beliefs per κ; one-sided 95 % bootstrap bounds).

| κ | G | LB95 | UB95 | Absolute gap (nats) | mean V_LA | mean V_G* | frac LA ≠ G* | Beliefs with no budget left |
|---|---|---|---|---|---|---|---|---|
| 0 | 0.00494 | 0.00320 | 0.00714 | 0.0150 | 3.0414 | 3.0264 | 0.58 | 0 |
| 2 | 0.00797 | 0.00506 | 0.01183 | 0.0211 | 2.6446 | 2.6235 | 0.41 | 0 |
| 6 | 0.01849 | 0.01214 | 0.02660 | 0.0495 | 2.6763 | 2.6268 | 0.53 | 2 |
| 12 | 0.01462 | 0.00977 | 0.02081 | 0.0392 | 2.6782 | 2.6391 | 0.53 | 3 |

**G3 (ii): S12 validation** (grid evaluation; 500 paired episodes). G* scores success 0.410, BI 6.337, 4.158 probes.

| Seed | Success | BI | Probes | Last-log g_T | Last-log sat_frac | Last-log entropy | Remedy-2× success / BI / probes |
|---|---|---|---|---|---|---|---|
| 200 | 0.190 | 5.100 | 2.362 | 4.811 | 0.1406 | 0.303 | 0.224 / 5.319 / 2.554 |
| 201 | 0.230 | 5.246 | 2.586 | 4.724 | 0.1016 | 0.441 | 0.258 / 5.373 / 2.612 |
| 202 | 0.192 | 5.104 | 2.248 | 4.489 | 0.1328 | 0.177 | 0.248 / 5.355 / 2.426 |
| mean (derived) | 0.204 | 5.150 (−1.187 vs G*) | 2.399 | — | 0.125 | — | 0.243 / 5.349 / 2.531 |

**G3 (iii): notch control** (exact values). The fraction of gap closed, f = (v_π − V_greedy)/(V_opt − V_greedy), is
derived.

| Seed | Episodes (1× / 2×) | v_π (1× = 2×) | fraction of V_opt | f (derived) | horizontal first |
|---|---|---|---|---|---|
| 100 | 100,096 / 200,064 | 0.17704 | 0.288 | +0.006 | no |
| 101 | 100,096 / 200,064 | 0.16980 | 0.276 | −0.010 | no |
| 102 | 100,096 / 200,064 | 0.16883 | 0.275 | −0.012 | no |
| mean | — | 0.17189 | 0.279 | −0.005 | 0 / 3 |

**G4 and the evaluation-kernel checks** (κ = 0; Δ = reference − candidate; 95 % CI).

| Comparison (file) | Cell | n | ΔBI [CI] | Δsuccess pp [CI] | Rule |
|---|---|---|---|---|---|
| 128k − 32k, 3 MH (g4) | A-random | 600 | +0.133 [0.085, 0.186] | +0.33 [−1.83, +2.50] | fail |
| | A-G* | 600 | +0.063 [0.023, 0.117] | +1.17 [+0.17, +2.33] | fail |
| | S-random | 600 | +0.177 [0.117, 0.245] | +1.83 [−1.33, +5.00] | fail |
| | S-G* | 600 | +0.097 [0.047, 0.149] | +0.67 [−2.17, +3.67] | fail |
| 30 MH − 10 MH, 32k (fallback) | A-random | 600 | +0.045 [0.025, 0.067] | +1.17 [−0.50, +2.83] | fail |
| | S-random | 600 | +0.039 [0.017, 0.062] | +3.67 [+0.83, +6.50] | fail |
| 128k×3 − 32k×30 (fallback diag.) | A-random | 600 | −0.013 [−0.039, 0.015] | −1.33 [−3.33, +0.50] | fail |
| | S-random | 600 | −0.007 [−0.038, 0.024] | −2.83 [−5.83, +0.17] | fail |
| grid − pf32k_3mh (b8) | A-G* / A-rand / S-G* / S-rand | 600/300/600/300 | +0.073 / +0.153 / +0.147 / +0.166 | +1.17 / +0.33 / +1.33 / +3.00 | all fail |
| grid − pf128k_3mh (b8) | A-G* / A-rand / S-G* / S-rand | 600/300/600/300 | +0.010 / +0.030 / **+0.0499** / +0.019 | 0.00 [−0.67, 0.67] / −0.67 [−3.33, 2.00] / +0.67 [−2.00, 3.17] / +1.00 [−3.33, 5.33] | pass / fail (CI) / fail (CI) / fail (CI) |
| grid − b5_ref (30 + 60) (b8) | A-G* / A-rand / S-G* / S-rand | 600/300/**31**/300 | +0.006 / +0.009 / −0.014 / +0.014 | +0.17 / −1.33 / 0.00 [−12.9, 12.9] / +1.67 | pass / fail / fail / fail |

**G5 per cell** (grid evaluation). Success values are on 300 paired pilot episodes (first 200 for D and saturation).

| Cell | τ | n | G* success | random success | G* success (200) | D (200) | G* BI sat (200) | G* BI | Non-degenerate |
|---|---|---|---|---|---|---|---|---|---|
| A0 | 3 | 300 | 0.857 | 0.167 | 0.855 | 0.685 | **0.815** | 7.931 | **no** |
| A6 | 3.2 | 300 | 0.460 | 0.030 | 0.470 | 0.440 | 0.290 | 6.651 | yes |
| A12 | 3.3 | 300 | 0.407 | 0.033 | 0.400 | 0.365 | 0.280 | 6.531 | yes |
| S0 | 4 | **150** | 0.680 | 0.273 | 0.690 | 0.460 | 0.450 | 7.141 | yes |
| S6 | 5.0 | 300 | 0.487 | 0.067 | 0.475 | 0.415 | 0.075 | 6.528 | yes |
| S12 | 5.1 | 300 | 0.440 | 0.073 | 0.385 | 0.300 | 0.075 | 6.379 | yes |

**Calibration.**
- n* is set from G* success on the first 200 pilot episodes at κ = 0, τ = 4:
  - A: 0.960 (32k) / 0.965 (128k), above 0.88, so n* = 3;
  - S: 0.665 (32k) / 0.680 (128k), so n* = 4.
- τ_κ is set as n* + mean travel time (mean travel time in parentheses):

  | Set | κ = 2 | κ = 6 | κ = 12 |
  |---|---|---|---|
  | A | 3.3 (0.334) | 3.2 (0.170) | 3.3 (0.292) |
  | S | 4.8 (0.796) | 5.0 (0.950) | 5.1 (1.141) |

- Verified mean probe counts: A 2.745 / 2.97 / 2.85; S 3.885 / 3.95 / 4.10. All are within n* ± 0.3.

**Exploratory diagnostics (NOT pre-registered; S, grid evaluation, validation episodes; "abs" = absolute-action head).**

| κ | Seed | n | Policy success | G* success | Δsucc [95 % CI] | Policy BI | G* BI | Policy probes | G* probes | Distinct first φ |
|---|---|---|---|---|---|---|---|---|---|---|
| 0 | 300 | 200 | 0.420 | 0.655 | −0.235 [−0.320, −0.145] | 6.560 | 7.048 | 4.0 | 4.0 | 1 |
| 0 | 301 | 200 | 0.405 | 0.655 | −0.250 [−0.340, −0.160] | 6.392 | 7.048 | 4.0 | 4.0 | 2 |
| 6 | 200 | 200 | 0.320 | 0.455 | −0.135 [−0.220, −0.050] | 5.774 | 6.481 | 2.32 | 3.96 | 4 |
| 6 | 201 | 200 | 0.260 | 0.455 | −0.195 [−0.275, −0.115] | 5.679 | 6.481 | 2.395 | 3.96 | 3 |
| 6 | 202 | 200 | 0.280 | 0.455 | −0.175 [−0.250, −0.100] | 5.745 | 6.481 | 2.21 | 3.96 | 5 |
| 12 | 200 | 500 | 0.190 | 0.410 | −0.220 [−0.268, −0.170] | 5.100 | 6.337 | 2.362 | 4.158 | 4 |
| 12 | 201 | 500 | 0.230 | 0.410 | −0.180 [−0.228, −0.132] | 5.246 | 6.337 | 2.586 | 4.158 | 4 |
| 12 | 202 | 500 | 0.192 | 0.410 | −0.218 [−0.270, −0.168] | 5.104 | 6.337 | 2.248 | 4.158 | 4 |

---

## 2. Comparative Findings

1. **Learned policy vs G\* (the H1 comparison; pilot/validation only).**
   - At S12 the 3-seed policy reaches 0.204 success against G*'s 0.410, a shortfall of 20.6 pp.
   - That is about 5× the largest possible H1a margin. The margin is δ_c = min(4 pp, 0.15·D_c), and D_c(S12) = 0.300
     gives δ_c = 4 pp.
   - The BI deficit is 1.19 nats (5.150 vs 6.337; derived). ε_c = min(0.05·BI(G*), 0.15·D^BI) is at most
     0.05 × 6.379 ≈ 0.32 nats (derived; G5 pilot BI), so the deficit is at least about 3.7× that margin.
   - Doubling E_train recovers only +3.9 pp of success (0.243) and +0.20 nats of BI (5.349).
   - [AC-corrected] The policy executes fewer probes: 2.25–2.59 against G*'s 4.158 at the same τ = 5.1. Unused
     budget is < 1 stroke by construction (§1.2), so the difference is spent on travel; travel itself is not in the
     analysed JSON.
   - *Exploratory:* the deficit is **not specific to travel**.
     - At κ = 0, where travel is free and both methods execute exactly 4.0 probes, the policy is still
       23.5–25.0 pp below G* (CIs exclude 0, upper ends −14.5 / −16.0 pp).
     - At κ = 6 it is 13.5–19.5 pp below.
     - The run-4 "absolute-angle / travel-overhead" root-cause hypothesis cannot explain a 24 pp deficit at κ = 0,
       where travel costs nothing and the policy chooses 1–2 distinct first angles. At most it explains part of the
       κ > 0 probe-count shortfall.

2. **Look-ahead vs G\* (the H2 premise).**
   - The validated estimator finds almost no rollout-improvable headroom at any κ:
     - absolute gaps of 0.015 / 0.021 / 0.049 / 0.039 nats at κ = 0 / 2 / 6 / 12;
     - relative gaps 0.5–1.8 %, against the 10 % required.
   - Escalating to κ = 12 did not increase headroom. G(12) = 0.0146 is below G(6) = 0.0185, and their bootstrap
     intervals overlap ([0.0098, 0.0208] vs [0.0121, 0.0266]).
   - The look-ahead's best action differs from G*'s on 41–58 % of beliefs, but the value differences are tiny.
     G*'s choice is near-tied with the alternatives, not dominated.

3. **Set-up moves on the exact notch control.**
   - All six learned notch policies (3 seeds × 1×/2× training) choose a vertical first probe.
   - Their exact value is 0.169–0.177 nats, i.e. greedy-like: exact V_greedy = 0.174, f ≈ −0.005.
   - The exact optimum is 0.615.
   - Doubling training changed nothing: v_π is identical to the last digit per seed. The runs are distinct (100,096 vs
     200,064 episodes), so this is convergence to the same deterministic argmax policy.

4. **G\* vs random (comparator strength).**
   - G* beats random by 36.7–69.0 pp (derived) in every cell, far above the 10 pp rule.
   - G*'s own success falls with travel cost on both sets at probe-matched τ: A 0.857 → 0.460 → 0.407; S 0.680 →
     0.487 → 0.440. This holds even though the calibration keeps the probe count matched (verified 2.75–4.10).

5. **Evaluation methods.**
   - 32k × 3 MH under-reads BI against the grid by 0.073–0.166 nats in all four κ = 0 cells. The grid's own sub-4 vs
     sub-8 discrepancy is 0.0042 nats mean.
   - Success is far less sensitive. Every success point difference between kernels is ≤ 3.67 pp, and most are
     ≤ 1.83 pp.
   - The evaluator choice therefore matters mainly for BI-based contrasts. It also matters for the ±2 pp gates
     (flatness, §3.3).

---

## 3. Statistical Checks

### 3.1 Tests actually implemented and used

| Test (code) | Used for | Statistic / interval |
|---|---|---|
| Nonparametric bootstrap over beliefs, B = 10,000, one-sided 95 % percentile bound of a mean (`analysis_g1.py`) | G1 (b) | mean 0.00254, UB 0.00374 (< 0.03) |
| Bootstrap over beliefs of a **ratio of means**, B = 10,000, one-sided 95 % LB/UB (`analysis_g2.py`) | G2 | G(12) = 0.0146, LB 0.0098 (rule > 0.05); G(6) = 0.0185, LB 0.0121; G(0) = 0.0049, UB 0.0071 |
| Paired bootstrap via `stats.crossed_bootstrap_diff` with one seed column (so episode resampling only), B = 4,000, α = 0.025 per tail → two-sided 95 % percentile CI (`analysis_g4*.py`, `analysis_b8.py`) | G4, fallback, B5, B8 | e.g. G4 S-random ΔBI +0.177 [0.117, 0.245], Δsucc +1.83 pp [−1.33, +5.00] |
| Paired percentile bootstrap of the mean per-episode success difference, B = 10,000, two-sided 95 %, per seed (`analysis_diag.py`) | Exploratory diagnostics | e.g. κ = 12 seed 200: −0.220 [−0.268, −0.170]; κ = 0 seed 300: −0.235 [−0.320, −0.145] |
| Point-estimate rules, no inference (`analysis_g3.py`, `analysis_g5.py`, `analysis_calib.py`, `analysis_gridcheck.py`) | G3 (ii), G5 strength / non-degeneracy / flatness, n*/τ, grid self-check | as pre-registered (flatness is explicitly "paired point estimates") |

`stats.py` also implements `holm`, `tost` and `seed_robustness`. **None of them is used anywhere in the gate record.**
They are reserved for the main analysis. No p-values were computed for any gate.

### 3.2 What the inference supports

- **G2 failure is statistically decisive, not a power problem.**
  - The one-sided 95 % *upper* bound at κ = 12 (0.0208) is below the 0.10 target and below the 0.05 LB requirement.
  - The same holds at κ = 6 (UB 0.0266).
  - Even an optimistic reading of sampling noise cannot reach the threshold.
- **Direction of G1 estimator bias.**
  - On the notch, the estimator gets V_LA nearly right (0.981 of exact) but under-estimates V_greedy by about 40 %
    (0.104 vs 0.174, ratio 0.597).
  - So G1 (a) passes partly because of a downward bias in the greedy baseline. This inflates the relative gap: the
    estimate is 0.829 against an exact 0.717.
  - G1 (b) bounds the bias at zero-gap beliefs at UB 0.0037.
  - If the notch bias carried over to S it would *inflate* G(κ). So G2's refutation is conservative in that direction.
    The record does not test whether it carries over.
- **G3 (ii) failure is outside sampling noise.**
  - G3 (ii) itself has no inferential test.
  - The exploratory script's paired bootstrap on the *same* G3 episodes gives per-seed Δ CIs of
    [−0.268, −0.170], [−0.228, −0.132] and [−0.270, −0.168]. All exclude the −5 pp tolerance.
- **Most G4/B8 "CI" failures on random cells are a sample-size artefact.**
  - The random cells in B8 use n = 300, half of the pre-registered 600. Their success CI half-widths are 2.3–4.3 pp
    (e.g. pf128k S-random [−3.33, +5.33], half-width 4.3 pp) [AC-corrected], so a ±2 pp CI requirement is nearly unreachable whatever the true difference.
  - §4 pre-registered a once-only extension to 1,200 episodes for cells that fail on CI width only. pf128k_3mh is
    CI-only failing in A-random, S-random and S-G*, yet **no extension was run**.
  - The status-note conclusion "no SMC kernel passes in every cell" is therefore partly a power artefact. It is not
    evidence that 128k × 3 MH is inaccurate.
  - Even so, 128k × 3 MH S-G* has ΔBI = 0.0499 against a 0.05 limit, and it was declared "not affordable" in §4 anyway.
- **Flatness verdicts depend on the evaluator.**
  - Same rule, different read-outs (07c run-3 note: 32k PF; run-4 note / `12_g5_analysis.json`: grid):

    | Cell | 32k PF read-out | Grid read-out |
    |---|---|---|
    | S6 | Δsucc +1.3 pp, ΔBI −0.015 (pass) | Δsucc −2.67 pp, ΔBI +0.0085 (fail) |
    | S12 | +7.7 pp, +0.19 | +1.33 pp, +0.170 |

  - A 4 pp swing in the S6 success difference produced by the evaluator alone shows that the ±2 pp point rule at
    n = 300, with no CI, is within measurement noise.
  - The S12 BI failure (+0.170 vs 0.10) is consistent across both read-outs and is the more credible part of the verdict.
- **Small-sample anomaly in G5 S12.**
  - G* success is 0.385 on the first 200 episodes but 0.440 on all 300. The last 100 episodes therefore run at 0.55
    (derived).
  - The non-degeneracy D (0.300) and δ_c are computed on the first 200 only. The pilot estimate of G*'s success at S12
    is unstable at the ±8 pp level.

### 3.3 Inconsistencies, rules applied differently from the pre-registration, and exploratory/confirmatory traps

**Numbers that disagree between files.**
- **B5 sign error.** B5 quotes the diagnostic "32k × 30 MH vs 128k × 3 MH" as "ΔBI −0.013 / +0.007". In
  `12_g4_fallback_analysis.json` the S value is **−0.0066**: `S_k0_random_30mh_vs_128k3mh`, diff_ref_minus_cand =
  −0.006575. Only the A value (−0.0126) matches.
- **G4 status note.** B5 says success was "within ±2 pp except A-G* +1.2 pp point". The pre-registered point tolerance
  is 1 pp, not 2. S-random's point Δsucc is **+1.83 pp** (> 1 pp), and all four CIs leave ±2 pp (A-random upper
  +2.50, A-G* upper +2.33, S-random [−1.33, +5.00], S-G* [−2.17, +3.67]) [AC-corrected]. The note understates the success failures. The BI failure
  alone suffices, so the verdict is unchanged.
- **B8 status note.** It says the 30 + 60 kernel agrees with the grid on BI "0.006–0.019". In `12_b8_analysis.json`
  the b5_ref |ΔBI| range is **0.006–0.014**. 0.019 is the pf128k S-random value. In addition, b5_ref S-G* rests on
  **31** episodes only.
- **Episode counts in the B8 note differ from the JSON.** The note says "S random 250"; the JSON has 300. B8 said
  selection would use "the first 200 recorded pilot episodes of each κ = 0 cell"; the JSON uses 600 (G*), 300
  (random), 277 (S-G* r30) and 31 (S-G* ref).
- **G5 S0 is under-sized.** It has n = 150, not 300. Its "first 200" non-degeneracy statistics are computed on at most
  150 episodes, although §1.7 requires 200.
- **The "8.7–9.9 %" saturation figure** (earlier, mean over training) and the "10.2–14.1 %" figure (last log; JSON
  0.1016–0.1406) describe the same runs. The pre-registered wording "< 10 % of training episodes" is ambiguous between
  the two. The last-log reading rests on one logged batch (values in multiples of 1/128, e.g. 18/128 = 0.1406).
- **Run-4 numbers not in any analysed JSON**, so they cannot be verified:
  - validation ball-sPCE 4.85/5.03/4.96 vs 4.76/4.87/4.67;
  - mean travel 0.54–0.63 rad vs G* 0.13;
  - remedy plateau episodes 1.6–1.7 × 10⁵.
- **Provenance gap.** No `code/analysis_*.py` writes `12_g3_notch_analysis.json` or `12_g3_hp_selection.txt`.

**Rules applied differently from the pre-registration.**
- **G4 scope.**
  - Pre-registered: 600 episodes per cell over S/A × κ = 0/κ_hi, with 200 each from random, G* and a G3 pilot policy.
  - Run: κ = 0 cells only, split by method (600 random, 600 G*), with **no pilot-policy episodes and no κ_hi cells**.
- **G4 failure route.**
  - §4 gives one fallback (10 MH vs 30 MH) and says "N_eval > 32k is not affordable". The fallback failed.
  - B5 (final rejuvenation) and B8 (grid reference, which becomes the evaluator) are routes that were **not
    pre-registered**. They were written before their own checks, but after G4 and the fallback had failed.
  - Every G3/G5 number is now on an evaluator that §1.6/§4 never anticipated.
  - The grid has been validated only against itself (sub 4 vs 8, 8 episodes, S only) and never at κ > 0.
- **Grid self-check rule changed after seeing data.**
  - After one sandbox episode flipped success at an exact tie (0.503 vs 0.499), "no flips" was narrowed to flips
    outside the [0.45, 0.55] tie band, and the check was moved from shard 0 to shard 1.
  - The change is disclosed, but it is a post-observation relaxation.
- **B2 relaxed the A per-shape rule** (≤ 0.80 → set-level ≤ 0.80 + per-shape ≤ 0.85) after seeing per-shape values
  0.806/0.818/0.818. The set-level value then itself failed (0.802) after the B3 fix.
- **G3 (i) selection** used ball-sPCE at κ = 6 (B9, written when 2 of 4 logs had finished). This matches §4 (only
  (ii) is re-run at κ = 12), but it means the configuration was tuned at a κ the primary cells no longer use.
- **G1 estimator details.**
  - §4 specified rollouts "completed by G* rollouts at rung R3"; B6 uses "the Monte-Carlo greedy comparator (M = 64)".
  - The G1 (a) rule changed from a single estimate to the mean of 5 runs (B6, pre-run). One of the 5 runs (0.8629)
    would fail on its own.
- **n* and τ calibration** used the 32k × 3 MH read-out (G4 runs), which B8 later rejected as the evaluator. n* is not
  sensitive to this, since the 128k values give the same n*. τ depends only on G*'s actions, not on the evaluator.
- **Bootstrap B** is 4,000 in the G4/B8 scripts. §1.8 states B = 10,000 for CIs (stated for the main analysis; the
  gates do not specify B).

**Places where exploratory numbers could be mistaken for confirmatory ones.**
- **`12_diag_analysis.json` "k12" entries are the G3 (ii) gate data, not new data.** The values match exactly (0.19,
  0.23, 0.192; BI 5.0996…). Citing them alongside G3 as "replication" would double-count one experiment.
- **The diag κ = 0 and κ = 6 CIs look like H1a non-inferiority tests, but they are not.**
  - They are validation episodes, n = 200, 2–3 seeds, per-seed (not crossed) bootstrap, two-sided rather than one-sided.
  - They have no pre-registered margin.
  - The κ = 0 policies (seeds 300/301) and their training are not described in any amendment.
  - The diag script also targets "rel_sd400–402" (relative-action head) at κ = 12, but the JSON contains no such
    entries.
  - The κ = 6 entries use seed labels 200–202, the same as the G3 pilot seeds. The record does not say whether these
    are the pre-escalation κ = 6 G3 (ii) runs.
- **The run-4 "root cause" (ignores φ₀) is explicitly exploratory.** As noted in §2, it is contradicted by the κ = 0
  deficit at equal probe counts.
- **G3 (ii), G5 and the diagnostics all report G\* success at S12, on different episode sets:** 0.410 (500 validation),
  0.440 (300 pilot) and 0.385 (first 200 pilot). These are not inconsistencies, but they must not be mixed when
  quoting "G*'s success".

---

## 4. Limitations

1. **No test-set data.** All learned-policy evidence is 3 pilot seeds (S12, S κ = 6) or 2 exploratory seeds (S κ = 0)
   on validation episodes. The pre-registered unit (6 seeds, 1,000 paired test episodes, crossed bootstrap) has never
   been run. No H1 or H2 failure condition has formally been evaluated.
2. **The action set is invalid by the record's own rule.** Flatness fails at S12 (ΔBI +0.170 > 0.10). Under §1.5,
   𝒜 = 32 × 8 must become 64 × 8. Every gate result obtained on 32 × 8 would then have to be repeated:
   - the τ calibration (all 6 cells);
   - G2 (κ = 0/2/6/12);
   - G3 (ii) (S12);
   - all G5 non-degeneracy values.
3. **The evaluator is not the pre-registered one, and is barely validated.**
   - The adaptive grid passed only a sub-4 vs sub-8 self-check on n = 8 S episodes at κ = 0, with mean |ΔBI| 0.0042
     and max 0.0259.
   - No κ > 0 check exists. The B8 note: "κ_hi cells are checked the same way when their pilot runs exist."
   - The grid costs 66–76 s per random episode on Actions (07c).
4. **Success is discontinuous in the posterior.** MAP-identity ties produce success flips: one exact tie (0.503 vs
   0.499) was observed. Kernel comparisons on random cells therefore cannot meet a ±2 pp CI at n = 300. This makes
   G4-type rules uninformative for the random arm.
5. **Learnability failure modes named in the record:**
   - collapse to a greedy-like vertical first probe on the notch (0/3 seeds horizontal; v_π 0.169–0.177 vs V_opt
     0.615; doubling training changes nothing);
   - **fewer executed probes** at S12 within the same τ (2.25–2.59 vs 4.158) [AC-corrected];
   - **hitting the E_train cap** (100,096 episodes, `max_episodes`, all seeds);
   - training-objective saturation 10.2–14.1 % at the last log;
   - low first-angle diversity (4 distinct first φ at S12; 1–2 at κ = 0; exploratory);
   - the hp choice rests on a single seed per config (spread 4.894–5.592 nats).
6. **The G2 estimator measures one-step-deviation (rollout) headroom only.** That lower-bounds the true optimum's
   headroom (§3 scope statement). Its notch calibration shows a 40 % under-estimate of V_greedy. The refutation covers
   only κ ≤ 12, n* = 4, set S, 𝒜 = 32 × 8, and the 100-belief G*-reached distribution.
7. **Set A is weakened.**
   - A0 is saturated (BI saturation 0.815, success 0.855), so A contributes only κ > 0 cells to success-based H1a.
   - C(A) = 0.802 marginally fails G0.
   - On A the travel calibration is nearly flat (mean travel 0.17–0.33 strokes), so "cost-aware" on A means little
     added budget.
8. **Missing pre-registered outputs:**
   - G3 (iv) bias of ball-sPCE vs BI;
   - G5 rollout-planner latency;
   - G0 items (i) and (iv)–(viii);
   - G4 pilot-policy and κ_hi cells.
9. **Small-n pilot instability.** S12 G* success moves from 0.385 (200) to 0.440 (300). S0 has 150 episodes in place
   of 300. B8 b5_ref S-G* has 31 episodes.
10. **Compute and tooling.** The PPO is numpy-only on 2-vCPU CI runners and a 2-vCPU sandbox. The 10⁵-episode cap and
    the 2 × 10⁵ remedy are small for a 256-way categorical head. The record cannot separate "objective/architecture
    cannot learn it" from "under-trained at this budget", beyond the observation that 2× training gave +3.9 pp at S12
    and nothing on the notch.

---

## 5. Conclusion: implications for H1 and H2 under the pre-registered routing

This section does not make the PROCEED/REFINE/PIVOT decision.

### H2 (Idea 2, gated look-ahead under travel)

- **G1 passes:**
  - (a) 0.829 in [0.573, 0.860];
  - (b) mean 0.0025, UB 0.0037 < 0.03.
- **G2 fails after the single permitted escalation:**
  - G(12) = 0.0146 with LB 0.0098, against ≥ 0.10 with LB > 0.05;
  - the G(0) part passes (0.0049 ≤ 0.03), and the ordering part passes.
- This is the pre-registered row "**G1 pass / G2 fail → Idea 2 refuted in the tested range**" (§3, H2 gate table).
  The paper statement is fixed by the pre-registration: "validated rollout-improvable headroom over cost-aware greedy
  G(12) = 0.0146 (UB 0.0208), G(0) = 0.0049 (UB 0.0071)", scoped to κ ≤ 12, n* = 4, set S. H2 policies are not trained.
- Two qualifications must accompany that statement:
  - **The record says G2 must be repeated.** The flatness failure's pre-registered consequence (𝒜 → 64 × 8) means
    "G2 … would have to be repeated on the new set" (07c run-4 note). On the current record the refutation holds only
    for the 32 × 8 set that G5 itself rejected.
  - **G3 (iii) adds a learnability finding.** Even on the exact notch, where headroom exists (0.615 vs 0.174), the
    total-objective policy recovers f ≈ −0.005 of the gap (pre-registered H2b-P2 needs f ≥ 0.6). Training could not
    have exploited set-up value even if G2 had found it.

### H1 (Idea 1, amortization; not gated by G1/G2)

- §4 says "No main run starts before G0, G3, G4 and G5 pass". None of the four has passed cleanly:
  - **G3 failed after its one remedy.** S12 success 0.204 → 0.243 against the 0.360 threshold. The pre-registered
    consequence is literal: "halt and go to stage 15 with learnability failure as the finding".
  - **G4 failed as pre-registered, and its fallback failed.** It was satisfied only by switching to an evaluator (the
    adaptive grid) that the pre-registration did not foresee.
  - **G5 failed flatness**, requiring 𝒜 = 64 × 8 and a re-run of the calibration and of G3 (ii).
  - **G0 records C(A) = 0.802 > 0.80.**
- So H1 cannot be tested under its pre-registered conditions on the present record.
- **Primary cells.** After removing A0, 3 of the 4 primary cells (A12, S0, S12) are informative for success. That
  meets the "≥ 3 of 4" threshold of failure condition (d), so H1 would not be "inconclusive on success". A0 still
  enters the BI part of H1a.
- **The pilot evidence points strongly against H1a.** This is validation data, not a test, so it is not a formal
  rejection.
  - At S12 the policy is 20.6 pp below G* in success, against δ_c = 4 pp. It is 1.19 nats below in BI, against
    ε_c ≤ 0.32.
  - If this carried over to test, failure condition (a) would apply, and the label rule makes a κ_hi-only failure
    "H1 rejected as titled".
  - The exploratory κ = 0 deficit (−23.5 / −25.0 pp, CIs excluding 0) suggests that even the fallback label
    "amortization supported for free repositioning only" would not be available. Being exploratory, this may inform
    the stage-15 decision but cannot be reported as a confirmatory result.

---

## Area-chair adversarial pass (fresh context)

Every number in §1–§5 was re-checked against `12_*_analysis.json`, `12_g3_hp_selection.txt`, `12_diag_analysis.json`,
the `code/analysis_*.py` scripts and `docs/07_hypotheses_v2.md` §1–§4 / `docs/07c_amendment_v2_0.md`. Table values in §1
match the JSON to the stated precision, apart from the four items marked [AC-corrected]. The rows below list claims
that the cited numbers do not strictly support.

| # | Unsupported claim (location) | Contradicting / missing evidence | Supported rewrite |
|---|---|---|---|
| 1 | "The policy does not use its budget" (§2.1); "under-use of the budget" (§4.5) | §1.2: the episode ends when τ_rem < 1, so unused budget is < 1 stroke for every method by construction. The JSON reports executed probes only (2.248–2.586 vs 4.158) and has no travel or leftover-time field. | "At the same τ = 5.1 the policy executes 2.25–2.59 probes against G*'s 4.158, so it spends the difference on travel." (applied in place) |
| 2 | "The deficit is not specific to travel"; the root-cause hypothesis "cannot explain" the deficit (§2.1); it "is contradicted by the κ = 0 deficit" (§3.3) | The κ = 0 numbers come from *different*, separately trained policies (seeds 300/301, training not documented in any amendment, n = 200, 2 seeds). A κ = 0 deficit shows that some non-travel failure exists. It does not show that travel overhead plays no part at κ = 12, where probe counts do differ (2.40 vs 4.16) while at κ = 0 they do not (4.0 vs 4.0). | "Exploratory: separately trained κ = 0 policies also trail G* by 23.5–25.0 pp at equal probe counts, so travel overhead cannot be the *only* cause of the learned-policy deficit. The record does not apportion the κ = 12 deficit between travel and other causes." |
| 3 | "G*'s choice is near-tied with the alternatives, not dominated" (§2.2) | `12_g2_analysis.json` gives only mean V_LA − V_G* and `frac_la_differs`. V_LA is the maximum over up to 5 noisy re-estimates (B6), so part of the 41–58 % disagreement can come from selecting the argmax of noisy estimates. Even at exact-zero-gap beliefs 21 % of estimated gaps are positive (G1 (b) `frac_positive` 0.21). No per-alternative values are recorded. | "The look-ahead's selected action differs from G*'s on 41–58 % of beliefs, yet the mean value gain is only 0.015–0.049 nats. The record does not separate genuine near-ties from argmax-selection noise." |
| 4 | "their bootstrap intervals overlap ([0.0098, 0.0208] vs [0.0121, 0.0266])" as support for "did not increase headroom" (§2.2) | These are pairs of one-sided 95 % bounds, i.e. two-sided 90 % intervals. Overlap of two marginal intervals is not a test of G(12) − G(6), and no such test was run. | "The point estimate G(12) = 0.0146 is below G(6) = 0.0185. Their two-sided 90 % intervals overlap, and the difference was not tested." |
| 5 | "Success is far less sensitive … The evaluator choice therefore matters mainly for BI-based contrasts" (§2.5) | pp and nats are not commensurable. In relative terms S-random grid − pf32k is +3.00 pp on 0.223 (≈ 13 %) against ΔBI +0.166 on 5.05 (≈ 3 %). On the random cells the success CIs have half-widths of 2.3–4.3 pp (`12_b8_analysis.json`), so success differences are mostly unresolved rather than shown to be small. The evaluator alone moved flatness Δsucc by 4.0 pp (S6) and 6.4 pp (S12). | "32k × 3 MH under-reads BI by 0.073–0.166 nats in every κ = 0 cell. Kernel-to-kernel success differences are ≤ 3.67 pp but mostly not resolvable at these n, and the evaluator alone shifted flatness Δsucc by 4.0–6.4 pp." |
| 6 | "Most G4/B8 'CI' failures on random cells are a sample-size artefact"; "no SMC kernel passes" is "partly a power artefact" (§3.2) | G4's random cells (n = 600) fail on BI (+0.133, +0.177), not on CI. In B8, only 4 of the 14 random-cell comparisons fail on CI width alone (pf128k A/S, pf32k_mh10 S, pf32k_mh30 S). The other 10 fail on \|ΔBI\| or on the 1 pp point rule. S-G* pf128k fails on CI at the pre-registered n = 600 too (half-width 2.58 pp). | "In B8, 4 of 14 random-cell comparisons fail on CI width alone. pf128k_3mh fails only on CI width in A-random, S-random and S-G*, so for that kernel the failure reflects the unextended sample size (the 1,200-episode extension was not run), not demonstrated inaccuracy." |
| 7 | The S6 swing shows that the ±2 pp rule "is within measurement noise" (§3.2) | The swing is a systematic evaluator difference on the same pilot runs, not sampling noise. The larger swing is at S12 (+7.7 → +1.33 pp, 6.4 pp), which the sentence omits. No CI was computed for either read-out. | "Re-reading the same pilot runs with a different evaluator moved Δsucc by 4.0 pp (S6) and 6.4 pp (S12), more than the ±2 pp tolerance, so the success part of the flatness verdict is not robust to the evaluator." |
| 8 | "The pilot estimate of G*'s success at S12 is unstable at the ±8 pp level" (§3.2) | No source or computation gives ±8 pp. The derived numbers are 0.385 (first 200), 0.55 (last 100) and 0.440 (all 300). | "G* success at S12 is 0.385 on the first 200 and 0.55 on the last 100 pilot episodes (derived), a 16.5 pp split. D (0.300) and δ_c rest on the first 200 only." |
| 9 | B8 note's "0.006–0.019" is an error and "0.019 is the pf128k S-random value"; the note's "S random 250" "differs from the JSON" (§3.3) | The note says it reports episodes "completed so far" (S random 250). The JSON (300) is the later, complete read-out. The 0.019 may come from the partial sample, so attributing it to the pf128k cell is a conjecture. | "The B8 note (partial data, S-random 250) quotes 0.006–0.019. The complete JSON (S-random 300) gives 0.006–0.014. The note should be updated to the final values." |
| 10 | G3 (ii) objective saturation verdict "**FAIL**" (§1.1) | The rule is "< 10 % of training episodes". The JSON holds only the last logged batch (13–18 of 128 per seed: 0.1016–0.1406). The 07c run-4 note gives 8.7–9.9 % as the mean over training, which would pass. §3.3 itself calls the rule ambiguous. | "Saturation is indeterminate: 10.2–14.1 % in the last logged batch (one batch of 128 per seed) and 8.7–9.9 % as a training mean (07c, not in the JSON)." |
| 11 | "hitting the E_train cap (… all seeds)" (§4.5); remedy plateau episodes "cannot be verified" (§3.3) | This is true only for the 1× runs. The raw logs `results/v2/g3/pilot2x_S_k12_sd20{0,1,2}.json` record status `plateau` at 163,840 and 174,080 episodes (sd200, sd201) and `max_episodes` at 200,064 (sd202). That matches the 07c run-4 note, although it is absent from `12_g3_analysis.json`. | "All three 1× runs hit the 10⁵ cap. Under the 2× remedy two seeds met the plateau rule (163,840 and 174,080 episodes) and one hit the cap (raw training logs). Success still failed (0.243 < 0.360)." |
| 12 | "Training could not have exploited set-up value even if G2 had found it" (§5) | The evidence is 3 seeds of one configuration, selected on S κ = 6, with ≤ 2 × 10⁵ episodes. H2b-P2 pre-registers 6 seeds. Other configurations and budgets were not tried. | "With the G3 (i)-selected configuration and up to 2 × 10⁵ episodes, none of 3 seeds learned the set-up move (f ≈ −0.005 vs the pre-registered f ≥ 0.6)." |
| 13 | "A0 still enters the BI part of H1a" (§5) | §1.7 removes a pilot-failing cell "from the primary set before any test episode is run". H1a-2 refers to "all 4 cells". The pre-registration does not settle which applies, and A0's failure is precisely BI saturation (0.815). | "Whether A0 still enters the BI part of H1a is not settled by the pre-registration (§1.7 vs H1a-2). It must be fixed by amendment before any test run." |
| 14 | "3 of the 4 primary cells (A12, S0, S12) are informative … so H1 would not be 'inconclusive on success'" (§5) | S0's non-degeneracy rests on 150 episodes, not the 200 that §1.7 requires. All values are on 𝒜 = 32 × 8, which the flatness failure voids. §1.7 also requires informativeness on test. | "On the current pilot record (S0 on 150 episodes, 𝒜 = 32 × 8), 3 of 4 primary cells are informative, which would meet condition (d). This must be re-established after the 𝒜 change and on test." |
| 15 | "The 10⁵-episode cap and the 2 × 10⁵ remedy are small for a 256-way categorical head" (§4.10) | No sample-complexity evidence in the record supports "small". | "The record cannot separate 'cannot learn' from 'under-trained at this budget'. 2× training gave +3.9 pp at S12 and no change on the notch." |
| 16 | "Their success CIs are about ±3.3 pp wide" (§3.2) | `12_b8_analysis.json` random-cell half-widths are 2.33–4.33 pp. The quoted example [−3.33, +5.33] is itself ±4.33. | Corrected in place: "half-widths 2.3–4.3 pp". |
| 17 | "three of four CIs leave ±2 pp" (§3.3, G4 status note) | `12_g4_analysis.json` A-G* success CI is [+0.17, +2.33] pp, so all four leave ±2 pp. | Corrected in place: "all four CIs leave ±2 pp (… A-G* upper +2.33 …)". |

**Corrections applied**
- §2.1, bullet 1: "The policy does not use its budget" was replaced by a fewer-probes statement that notes leftover
  budget is < 1 stroke by construction (§1.2) [AC-corrected]. This contradicts the pre-registered design, not a JSON value.
- §3.2, B8 sample-size bullet: "about ±3.3 pp wide" was changed to "half-widths 2.3–4.3 pp … half-width 4.3 pp" to
  match `12_b8_analysis.json` [AC-corrected].
- §3.3, G4 status note: "three of four CIs leave ±2 pp" was changed to "all four", adding A-G* upper +2.33 from
  `12_g4_analysis.json` [AC-corrected].
- §4 item 5: "under-use of the budget" was changed to "fewer executed probes … within the same τ" [AC-corrected].
- Rows 2–15 above are over-interpretations, not wrong numbers. They are left in place and their supported rewrites are
  given in the table.
