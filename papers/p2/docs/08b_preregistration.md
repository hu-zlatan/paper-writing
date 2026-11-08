# p2 · Pre-registration freeze 08b (CertGrip) — DRAFT, not frozen

**Status:** DRAFT written in run 39 while the re-pilot predictors run. It becomes the freeze only when the line
"FROZEN at commit …" below is filled in and committed **before any main-pool (salt 1001 / 2002) instance is simulated**.
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
[PILOT — filled from `results/pilot/rd/pilot_analysis_rd.json` once all 12 arms exist.]

## 6. Secondary and diagnostics changed by 08a
H4a in steps P → S → S+squeeze → +onset (the pilot expectation that the squeeze adds ≈ nothing is stated up front);
H4c shuffles the probe features as well; H4d estimated with the onset scalar included; H4e: CertGrip-full vs
onset-only. D-μ = cross-validated R² of log μ on each arm's residual, per σ; the R² ≤ 0.05 premise is kept only for
no-probe arms. H2-M (no mass) reported, not used for the friction story. S1 / H3-B location prediction (Δ 0.51)
applies to no-probe arms only; the probe arm gets separate in / out-of-support predictions and a two-sided TOST in H3-L.

## 7. Freeze
FROZEN at commit: — (not yet)
