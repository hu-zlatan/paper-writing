# p2 · Pre-registration freeze 08b (CertGrip) — FROZEN (run 39, 2026-11-08)

**Status:** FROZEN in the commit that adds this line (`git log -- papers/p2/docs/08b_preregistration.md`), before any
main-pool (salt 1001 / 2002) instance has been simulated. Later changes go to a dated addendum, never into this file.
Canonical design: `07_hypotheses.md` (stage 8) as amended by `08a_pilot_amendment.md`; experiment plan
`08_experiment_plan.yaml` (stage 9 gate). This file only (i) fixes every pilot-dependent constant, (ii) restates the
decisions that 08a changed, and (iii) records the power re-projection. Where it is silent, 07_hypotheses applies.

## 1. Protocol and simulator (frozen)
- Engine: `mujoco==4.0.0` (pinned in `code/requirements.txt`), timestep 0.002 s, elliptic cone, impratio 10,
  condim 6, solref (0.004, 1), solimp (0.95, 0.99, 0.001); identical for every family and shift (UT7).
- Protocol `"rd"` (`Sim(..., protocol="rd")`, `main.py ... --protocol rd`): preload F0 = 32.7 N (m g / μ with m_max 1 kg, μ_min 0.3)
  for 0.4 s → squeeze F0 → 1.5 F0 → F0 (0.3 s) → ramp-down probe with the touch-only detector (constants `RD2`,
  `TAXEL_NOISE` in `code/certgrip/sim.py`, listed in 08a) → ramp to F (0.1 s) + settle 0.1 s → disturbance window
  0.6 s. Slip reference = pose after the squeeze, before the probe (probe slip counts).
- Slip metric (fixed in run 37, before any monotonicity data): tangential displacement > δ_t = 2 mm, or rotation about
  the grasp axis > 3°, or loss of contact with a pad.
- Labels: F\* by log-space bisection on [F_min, F_max] = [0.1, 100] N, 1 + 10 replays; F\*_lo, F\*_hi,
  F\*_mid = √(lo·hi). F_max = 100 N kept: re-pilot max F\*_hi 33 N (ID), 54 N (S1), 47 N (S3), 26 N (F5).
- Replay determinism and cost (UT6, run 38): bit-identical within machine; runner timing jobs a / b in
  `results/pilot/timing_runner_*.json`; ≈ 0.01 s per replay, so no downscale step is needed.

## 2. Onset feature and noise (frozen)
- Feature = [log F_onset + σ·ε, found]; ε ~ N(0, 1) per instance from `instance_seed(inst, "onset_eps")`, stored in
  every label record. σ ∈ {0, 0.1, 0.2, 0.4}; **primary σ = 0.2** (all core decisions); σ = 0 is an upper bound only.
- CSF-μ̂: F = m (g + a_cmd) / (2 μ̂) · exp(q̂), μ̂ = m g / (2 F_onset_noisy) clipped to [0.1, 3], same σ and ε as the
  CertGrip arm it is compared with.

## 3. Arms and names (code feature-set names in brackets)
P [`P`], S [`S`], S+squeeze [`full`], **CertGrip-full = S+squeeze+onset [`full_rd`]**, onset-only = P+onset
[`P_onset`], oracle [`oracle`]; physics plug-ins CSF-1, Mondrian-CSF, CSF-μ̂. COMP = the best of {Mondrian-CSF,
CertGrip-P, CSF-1} by mean RE at α 0.10 on the selection split (objects 200–249), chosen once and logged before any
calibration / test access.

## 4. Core decisions (08a item 4; Bonferroni over four decisions, one-sided 0.0125 each, CI\*\* = 97.5 %)
1. **H1** (H1-M gate + H1-V), as in 07_hypotheses §3, run under protocol `"rd"`; H1-M threshold re-stated for the
   0.0125 level: one-sided 98.75 % Clopper–Pearson upper limit ≤ 2 % on 800 instances (still ≤ 7 non-monotone).
2. **H2a (primary):** D = 1 − RE(CertGrip-full, σ 0.2) / RE(COMP); D ≥ 0.10 and CI\*\* lower limit > 0, with the
   F\*_lo / F\*_hi robustness requirement. Equivalence / inferiority failure conditions as in 07_hypotheses, at 0.0125.
3. **H2b (co-primary):** CertGrip-full vs CSF-μ̂ at σ 0.2, SESOI 0.10: superiority if D ≥ 0.10 and lower limit > 0;
   TOST equivalence within ±0.10 at 0.0125 per side reported as "learned touch adds nothing over the physics plug-in
   with the same friction estimate".
4. **H3** as in 07_hypotheses (R_E upper limit < 1.10 for S1, S2, S3), with the 08a item 7 changes for the probe arm.
Also reported: σ\* = the smallest σ in the grid at which the lower limit of D(H2a) falls below 0.10 (descriptive).

## 5. Pilot-dependent constants and power re-projection
Source: `results/pilot/rd/pilot_analysis_rd.json` (re-pilot, pilot objects 125–224, 1,600 ID + 400 F5 + 1,600 S1 +
1,600 S3 labels, 140 monotonicity grids; 12 predictor arms with the equal 30-config search, OOF files computed on
Actions run 42519521710 and reproduced in the sandbox to 1e-15; 200 random cal / eval object splits, α 0.10).
Pilot numbers are planning inputs, not results.
- **H1-M look / UT8:** 0 / 140 non-monotone; unavoidable 0 / 1,600 (ID), 1 / 1,600 (S1), 0 / 1,600 (S3), 0 / 400 (F5)
  → UT8 (≤ 1 %) holds; F_max = 100 N kept. Onset found 100 %; onset displacement median 0.13 mm (p99 0.4–0.7 mm).
- **Shift sizes:** S1 mean Δlog F\* = 0.509 (Coulomb prediction 0.511), S3 0.189.
- **Onset quality (log μ̂ vs log μ, ID):** corr 0.97 / 0.93 / 0.84 / 0.64 at σ 0 / 0.1 / 0.2 / 0.4.
- **Pilot RE at α 0.10 (mean over splits):** CSF-1 0.80, P 0.89, S 0.88, S+squeeze 0.90, oracle 0.16;
  CertGrip-full 0.26 / 0.34 / 0.46 / 0.68 and onset-only 0.23 / 0.33 / 0.45 / 0.68 at σ 0 / 0.1 / 0.2 / 0.4;
  CSF-μ̂ 0.19 / 0.27 / 0.43 / 0.93. Mondrian-CSF was not run in the pilot (it enters COMP on the selection split).
- **D-μ (CV R² of log μ on the residual):** P 0.75, S 0.75, S+squeeze 0.74, CSF-1 0.60; CertGrip-full 0.00 / 0.06 /
  0.15 / 0.49 by σ; CSF-μ̂ ≈ 0 (the onset feature is the friction channel).
- **η:** pilot 0.1 × IQR = 0.035; the frozen η is computed from the main ID calibration scores (07_hypotheses §1.4).
  Score density at the 0.9 quantile f ≈ 0.69 per log unit (KDE; 07_hypotheses assumed 1.5).
- **Power, H2a** (COMP proxy CSF-1, the best non-tactile arm in the pilot): D ≈ 1 − 0.46/0.80 ≈ 0.43; projected
  SE(D) ≈ 0.051 × √(200/500) / 0.80 ≈ 0.040 → the decision is well powered.
- **Power, H2b** (vs CSF-μ̂, σ 0.2): pilot D ≈ 1 − 0.456/0.430 ≈ −0.06; projected SE(D) ≈ 0.025 × √(200/500) / 0.43 ≈
  0.037 > 0.035 → **pilot rule applied: 50 train objects per family move to test** (`split_of`: train 0–149,
  selection 150–199, cal 200–324, test 325–499; n_cal = 500 per stratum unchanged; 2,800 test instances), giving
  SE(D) ≈ 0.031. **Stated expectation:** at the pilot effect, superiority is very unlikely, TOST equivalence has
  ≈ 17 % probability and inferiority (upper limit < 0) ≈ 40 %; the likely report is "learned touch does not beat a
  physics plug-in that uses the same onset estimate".
- **Power, H3:** with f ≈ 0.69 the oracle's quantile SE per stratum at 125 objects is ≈ 0.039 log units and the
  projected CI\*\* half-width of R_E ≈ 0.14 (> 0.06) → **pilot rule applied: oracle share 175 objects** (S1 / S1m / S3:
  `h3_role` — id test objects 325–368 per family are oracle-recalibration objects, 369–499 (524 objects, 2,096
  instances) the stream; the 500 pre-shift steps are drawn from the unshifted instances of the oracle objects. S2:
  `N_OBJ["s2"]` = 550, oracle 0–174, stream 175–549, 1,500 instances; pre-shift steps from the ID test objects).
  The half-width stays ≈ 0.12 > 0.06, so **H3 is pre-registered with reduced power**: it can pass only if the true
  R_E is ≲ 0.97; an inconclusive H3 is the expected outcome and will be reported as such.
- **Compute:** ≈ 0.01 s per replay → main simulation ≈ 2–3 CPU-h; the 90 CPU-h plan is far from binding.

## 5b. Code state at the freeze (sha256, first 16 hex)
  - `code/certgrip/__init__.py` e3b0c44298fc1c14
  - `code/certgrip/baselines.py` ce7eca030940ea09
  - `code/certgrip/conformal.py` 9a2f82f8dfe8892c
  - `code/certgrip/data.py` 003ae695f3f47bfc
  - `code/certgrip/featsets.py` ace7f4be11ee7c5a
  - `code/certgrip/features.py` c95885e878972bf4
  - `code/certgrip/models.py` efa9f726504e1240
  - `code/certgrip/sim.py` 07947aba0465489d
  - `code/main.py` 718a169ad2624dc1
  - `code/requirements.txt` cf08783c1bd06a0e
Tests: `code/tests` 18 / 18 pass; `pipeline/scripts/check_numpy2_compat.py papers/p2/code` 0 errors.

## 6. Secondary and diagnostics changed by 08a
H4a in steps P → S → S+squeeze → +onset (the pilot expectation that the squeeze adds ≈ nothing is stated up front);
H4c shuffles the probe features as well; H4d estimated with the onset scalar included; H4e: CertGrip-full vs
onset-only. D-μ = cross-validated R² of log μ on each arm's residual, per σ; the R² ≤ 0.05 premise is kept only for
no-probe arms. H2-M (no mass) reported, not used for the friction story. S1 / H3-B location prediction (Δ 0.51)
applies to no-probe arms only; the probe arm gets separate in / out-of-support predictions and a two-sided TOST in H3-L.

## 7. Freeze
FROZEN: run 39, 2026-11-08, in the commit "p2 stage 10 ... 08b FROZEN". No file under `papers/p2/results/` from the id or
s2 pools existed at that commit (checked: `ls papers/p2/results` → `pilot`, `v1/logs` only).
