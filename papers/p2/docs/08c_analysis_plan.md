# p2 · Addendum 08c — analysis plan after the H1-M failure (run 39, 2026-11-08)

**Status:** written after the H1-M gate result and before any predictor exists, any calibration or test statistic has
been computed, or any CRC replay has run. Only the H1-M counts (`results/v1/h1m_analysis.json`) and the UT8 counts were
looked at. 08b stays frozen; this file fixes what 07_hypotheses left to the analysis and what the pre-registered H1-M
failure branch requires. Changes after this point go to a further dated addendum.

## 1. H1 outcome
H1-M failed (8 / 800, upper limit 2.11 % > 2 %), so **H1 is not confirmed** (07_hypotheses: "H1 is confirmed iff H1-M
passes and H1-V passes"). H1-V is still run and reported (label-to-physics gap Δ, CI\*\*), as a secondary result.

## 2. Validity route for H2 / H3: conformal risk control on the binary slip loss (07 H1-M failure branch)
- For an arm with predictor g and a calibration instance i, the force at level λ is F_i(λ) = min(F_max, g(x_i) e^λ);
  the loss is L_i(λ) = 1{slip in a direct replay at F_i(λ)} (physical outcome, not the label rule).
- **λ-grid (20 points, fixed per arm before calibration):** Λ_arm = q̂_sel + linspace(−0.4, 0.4, 20), where q̂_sel is the
  label-rule conformal quantile at α of the arm's scores on the **selection split** (objects 150–199), pooled over
  strata. The selection split is disjoint from cal and test.
- **Monotonised loss:** L̃_i(λ) = max over λ' ≥ λ in Λ of L_i(λ') (non-increasing in λ, L̃ ≥ L), so the risk-control
  guarantee for L̃ implies it for the physical slip loss.
- **CRC (per disturbance stratum, n = 500 calibration instances each):** λ̂ = the smallest λ ∈ Λ with
  (n R̃_n(λ) + 1)/(n + 1) ≤ α; if none, λ̂ = max Λ (reported). Guarantee: E[slip at λ̂] ≤ α for an exchangeable test
  instance.
- Replays: every calibration and test instance on the full grid (20 replays each) for the arms in §4, so bootstrap
  draws need no new simulation. Unavoidable instances count as slips at every λ.

## 3. Primary predictors, COMP selection, bootstrap
- **Seed:** the primary analysis uses the seed-0 predictor of every learned arm; seeds 1–4 are refit identically and
  D(H2a), D(H2b) are reported per seed (secondary; no decision depends on them).
- **COMP** (08b §3): candidates CSF-1, Mondrian-CSF, CertGrip-P (seed 0). On the selection split, objects with even
  index calibrate and odd index evaluate, then the roles swap; mean label-rule RE at α 0.10 over both halves; the
  smallest wins. Chosen and committed (`results/v1/comp_selection.json`) before any cal / test file is read.
- **H2a / H2b primary:** RE under the CRC route of §2 for both arms of each contrast (same λ-grid construction, same
  calibration draw), D = 1 − RE(CertGrip-full, σ 0.2) / RE(comparator). The label-rule conformal versions are reported
  as secondary (they were the pre-H1-M plan).
- **Bootstrap:** 2,000 object-cluster draws, resampling calibration objects and test objects within family (all four
  instances of an object move together); λ̂ (or q̂) is recomputed in each draw; percentile CI\*\* = 97.5 % two-sided
  (0.0125 one-sided, 08b §4). Robustness: F\*_lo and F\*_hi in place of F\*_mid in RE.
- **H3:** OQT already uses the binary physical outcome (label-free), so it is unchanged; the oracle recalibration
  reference uses the label rule as pre-registered, and the matched-rate co-requirement compares realised physical
  slip rates in the window.

## 4. Arms that get CRC replays
CertGrip-full at σ 0.2 (primary) and at σ 0, 0.1, 0.4 (σ\*); the COMP winner; CSF-μ̂ at σ 0.2 (and the other σ for the
σ curve); onset-only at σ 0.2 (H4e). Other arms are reported under the label rule only.

## 5. Order of work (each step committed before the next)
1. `main.py fit` per arm × seed (train objects only; Actions manifest `experiments/p2_fit_a010.json`).
2. COMP selection on the selection split → commit.
3. λ-grids from the selection split → commit; CRC replay jobs (cal + test, 20 λ) → commit outputs.
4. Analysis script with a synthetic-data test → commit; then run it once on the real files.
