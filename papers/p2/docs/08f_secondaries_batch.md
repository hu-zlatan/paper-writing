# p2 · Addendum 08f — operational choices for the remaining secondaries (run 42, 2026-11-09)

**Status:** written before any quantity below has been computed. Already seen at this point: the H1-M, H1-V, H2 (CRC
08c, CRC 08e, label route), H3 / H3-L and H4a read-outs. Nothing here is new data collection: H4c and H2-M need new
predictor fits on the id **train** objects (labels already exist); everything else reuses existing labels, predictors
and CRC replays. 07_hypotheses §4 / 08b §6 left the operational details below open; they are fixed here. Every item is
secondary or a diagnostic; no primary decision depends on it. CI\*\* = 1.25 / 98.75 percentile, 2,000 object-cluster
draws (cal and test objects resampled within family, q̂ / λ̂ refitted per draw), as in 08c / h4a, unless stated.
Holm is not applied to the CI\*\* rules here; each result is reported with its interval and labelled secondary.

## 1. H2-T (tail non-inferiority, 07 §4)
- Metric: P95 of the per-instance relative excess (F − F\*_mid)/F\*_mid over avoidable id test instances;
  T = P95(CertGrip-full σ 0.2) / P95(COMP = CSF-1).
- Routes: **CRC 08c grids (primary route of 08c)**, CRC 08e grids and the label rule — all three reported.
- Rule (07): pass iff CI\*\* upper < 1.10; failure iff CI\*\* lower > 1.10; else inconclusive.

## 2. H4c (shuffled-touch control)
- Arm `full_rd_shuf` (σ 0.2): the CertGrip-full feature vector in which every non-P column (static touch, preload-slip
  flag, squeeze-probe and onset features — 08b §6 "shuffles the probe features as well") is permuted across rows within
  each (pool, shift, split, disturbance) group with a fixed seed derived from the group name; the P columns (disturbance
  one-hot, commanded acceleration, log mass, aperture) stay with their row. Same 30-config search, seed 0, α 0.10,
  `main.py fit --fset full_rd_shuf`.
- Contrast, label route (08c: arms outside the CRC set use the label rule): D = 1 − RE(shuf)/RE(CertGrip-P seed 0).
- Rule (07): equivalence (pass) iff CI\*\* inside ±0.05; failure iff CI\*\* lower > 0.05 (shuffled beats P by > 5 %);
  else inconclusive.

## 3. H2-M (no-mass condition only)
- Fits with `--no-mass` (log mass removed from the base features): CertGrip-P and CertGrip-full σ 0.2, seed 0.
- COMP re-selected: CSF-1 and Mondrian-CSF need the mass, so the only non-tactile candidate is CertGrip-P (no mass);
  no selection-split run is needed. D_nm = 1 − RE(full_rd, no mass)/RE(P, no mass), label route; reported next to the
  with-mass label-route D(full_rd vs P) on the same draws. No directional prediction (07).
- The 10 % mass-noise condition is **not run in this batch** (its noise draw was never specified); if it is run later
  its draw is fixed in a further addendum first.

## 4. H3-B (offline breakage magnitude)
- Arms (08b §6: the location prediction applies to no-probe arms): CertGrip-P, CertGrip-S, CertGrip-full (squeeze, no
  onset), CSF-1, all seed 0 / formula. The onset arm (full_rd σ 0.2) gets p_obs only: 08b promised "separate in /
  out-of-support predictions" but never specified them, so no test is run for it (stated as a deviation).
- Per stratum d: q̂_d from the id cal split (label rule, n = 500); p_obs = mean 1{F < F\*_hi} over the shift pool's
  test instances (all id test objects 325–499; unavoidable instances count as slips), F = min(F_max, g e^{q̂_d});
  p_pred = 1 − F̂_ID,d(q̂_d − Δ), F̂_ID,d the empirical CDF of the unshifted id test scores of the same objects;
  pooled over strata by instance counts. Δ = 0.511 (S1), 0.105 (S1m). Rule: pass iff CI\*\* of p_obs − p_pred inside
  ±0.02; failure iff CI\*\* excludes ±0.02 entirely; else inconclusive.
- S3: p_obs with CI\*\* (predicted direction up). S2 (pool s2, F5; all stream + oracle instances): break iff
  CI\*\* of p_obs − α excludes ±0.05.

## 5. D-μ (diagnostic)
- Residual r = log F\*_hi − log g per arm on the 4,800 id cal + test instances (out-of-sample for every predictor; the
  07 wording "train objects" is not used because the train rows are in-sample fits — stated as a deviation). CV R² of a
  linear fit log μ → r, 5-fold GroupKFold by object (the pilot's `cv_r2`), point estimate plus a 500-draw
  object-cluster bootstrap 95 % interval. Arms: P, S, full, full_rd σ 0 / 0.1 / 0.2 / 0.4, P_onset σ 0.2, CSF-1,
  CSF-μ̂ σ 0 / 0.1 / 0.2 / 0.4, oracle. Interpretive threshold R² ≤ 0.05 (no-probe arms only, 08b §6).

## 6. UT3 (label-rule split-conformal unit test)
- Pool: the 1,200 id cal + test objects (4 instances each, one per stratum). 1,000 uniformly random object-level
  re-splits (seed 3) into n calibration objects and the rest as test, n ∈ {50, 500}; per stratum q̂ at α ∈ {0.01, 0.05,
  0.10, 0.20}; methods P, S, full, full_rd σ 0.2, CSF-1 → K = 160 cells. Miss = label slip rate on the test objects.
- Pass per cell iff the mean miss over re-splits lies in [α − 1/(n+1) − z·SE, α + z·SE], z = Φ⁻¹(1 − 0.05/(2K)),
  SE = SD/√1000. Report: number of passing cells, worst cell, and the re-split SD (descriptive).
