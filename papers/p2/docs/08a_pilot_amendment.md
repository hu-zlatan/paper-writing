# p2 · Stage-9 design amendment 08a (pilot-driven, before any main-pool data) — DECISION RECORD, run 38

**Status:** decision taken; implementation and the re-pilot under the new protocol are pending (next run). Nothing is
frozen yet; no main-pool (salt 1001 / 2002) data exist.

## Why (pilot evidence, pilot pool only)
`results/pilot/pilot_analysis.json`: with the designed touch features (static preload + 1.5 F0 squeeze) every
non-oracle residual correlates ≈ −0.79 with log μ; cross-fitted conformal RE at α 0.10: P 1.02, S 0.97, full 0.94,
CSF-1 0.76, oracle 0.39 (100 objects, 320 training rows per fold, 5-config search — small). A candidate ramp-down
probe whose onset test uses the true displacement recovers μ almost exactly (corr 0.999,
`results/pilot/pilot_rampdown_floor*.json`) — a perfect friction sensor, so not usable as is.

## Review
A fresh-context skeptic subagent (opus) reviewed the design question with only the files (07_hypotheses, 08 plan,
pilot JSONs, sim.py, featsets.py, the stage-10 plan) and recommended option **C**: the ramp-down probe run for every
method (one protocol, one set of labels), onset detected from simulated pad readings only, with an explicit noise
model, and the touch claim split into two estimands. Its report is summarised below; the decision is ours.

## Decision: option C
1. **Protocol / detector.** Ramp-down after the squeeze, floor 0.005 F0, fixed ramp rate; misses censored at the floor
   for every method. Onset from touch_grid only at 100 Hz, rule fixed in advance (shear/normal ratio rate or pressure
   centroid shift over k frames). Taxel noise: multiplicative per taxel + additive + per-object gain bias. Feature
   log F_onset; onset-noise levels σ ∈ {0, 0.1, 0.2, 0.4} (log units), **primary σ = 0.2**, σ = 0 an upper bound only.
   μ is never estimated from true mass inside the probe.
2. **Probe safety.** No slip-reference reset after the probe: probe-induced displacement > δ_t or contact loss counts
   as a slip, reported per σ. New tests: no drop at σ = 0; bracket consistency under the new protocol. H1-M look and
   UT8 re-run under the probe protocol before the freeze.
3. **Comparators.** Add CSF-μ̂ (F = m(g+a)/(2 μ̂)·exp(q̂), μ̂ from the same noisy onset); add CSF-1 to the COMP candidate
   set; the onset scalar gets its own row in the fairness table (needs touch to detect).
4. **H2.** H2a (primary): CertGrip-full (σ 0.2) vs COMP — "tactile friction probe" wording in C1. H2b (co-primary):
   CertGrip-full vs CSF-μ̂ at the same σ, SESOI 0.10, TOST. Four core decisions → Bonferroni 0.0125 each. Report σ\* at
   which the lower limit of D(H2a) reaches 0.10. Power re-projected from the new pilot.
5. **H4.** H4a in three steps (P → S → S+squeeze → +ramp-down; the pilot expectation that the squeeze adds ≈ nothing is
   stated); H4c shuffles probe features too; H4d estimated with the onset scalar included; new H4e: full vs onset-only.
6. **D-μ** reported as cross-validated R² per arm and σ; the R² ≤ 0.05 premise only for no-probe arms.
7. **S1 / H3.** For the probe arm S1 is partly visible and partly outside the training μ support (μ·0.6 < 0.3 for
   ≈ 42 % of instances): H3-B's location prediction (Δ 0.51) applies to the no-probe arms only; the probe arm gets
   separate in/out-of-support predictions; H3-L's "advantage preserved" TOST becomes two-sided for that arm. η recomputed.
8. **H2-M (no mass)** reported but not used for the friction story (onset confounds m and μ).
9. **Re-pilot** under the frozen protocol on ≈ 100 fresh pilot objects (pilot pool objects 25–124), all disturbances,
   full 30-config search; then write `08b_preregistration.md` (freeze).

Pilot caveats recorded with the decision: pilot too small to judge CSF-1 vs learned at 3,200 rows; oracle underfits
(residual corr −0.40); Mondrian-CSF degenerates at ≈ 12 calibration objects per cell (also in H2-n at n_cal 50 —
declare or drop Mondrian there); 0/140 non-monotone only bounds the rate at ≈ 2.1 %; the "pilot D ≈ 0.08" is vs P,
not COMP, with split-to-split SD ≈ 0.16.

## Transparency statement (paper / supplement)
After a pilot on 100 disjoint objects showed that the designed preload and squeeze touch features carried almost no
friction information, we added a ramp-down incipient-slip probe before freezing. Because a displacement-based detector
recovered μ almost exactly in simulation, we model a tactile detector with pre-registered noise levels, keep the
squeeze-only design as a pre-registered arm, and test whether learned touch improves on a physics plug-in using the
same friction estimate. No main-pool data existed when the change was made.

## Implementation record (run 39, 2026-11-08 ≈ 20:10–21:30 UTC) — before any main-pool data
`code/certgrip/sim.py` protocol `"rd"` (`Sim(..., protocol="rd")`, `main.py ... --protocol rd`; the old protocol stays
the default, timing digest 70368455… unchanged). Detector constants `RD2` / `TAXEL_NOISE` were set on the **first
pilot objects 0–24 only** (already used in run 38) and are frozen from here.
- **Probe:** after the squeeze, force F0 → 0.005 F0 log-linearly over 0.25 s; on detection, back to F0 in 0.02 s,
  hold 0.1 s. Slip reference = pose **before** the probe (probe slip counts, item 2).
- **Detector (touch only):** 500 Hz frames; noisy shear/normal ratio r = Σ_pads |shear sum| / Σ normal from noisy
  taxels (per-taxel multiplicative lognormal 0.05, additive 0.002 N, per-instance channel gain lognormal 0.10, seeded
  per instance); log r smoothed over 6 frames; onset = 2 consecutive frames whose 8-frame rise is < ½ of the stick
  rise, armed only when smoothed r > 0.1 (below the lowest μ of any pool, 0.3 × 0.6), or normal reading < 1 mN.
  Not found → censored at the floor. Feature = [log F_onset + σ·ε, found], ε ~ N(0,1) per instance (stored),
  σ ∈ {0, 0.1, 0.2, 0.4}, primary 0.2. CSF-μ̂: μ̂ = m g / (2 F_onset_noisy) clipped to [0.1, 3].
- **Tuning log (objects 0–24 only, 5 families × 4 disturbances, ID and S1, F = 100 N; criteria: probe slips, early
  triggers, onset accuracy):** 100 Hz / 3-frame rule → 3 false early triggers on light objects; 100 Hz / 2 × 5-frame →
  long lag, the probe made 156 / 250 slip; 1 s ramp / 20-frame → 91 / 250 probe slips; 0.5 s / 10-frame / 4 consec →
  ID 3 / 500, S1 34 / 500 probe slips. Faster ramps help (post-onset displacement ∝ ramp rate × lag³ and the lag falls
  with the rate): 0.25 s / w 6 / k 8 / 2 consec → **0 / 500 probe slips in ID and in S1, 0 early triggers**, onset
  displacement median 0.13 mm (p99 0.4 / 0.7 mm), log(m g / 2F_onset) vs log μ corr 0.988 (ID) / 0.984 (S1), offset
  0.32 (detection lag), SD 0.05 at σ = 0 — near-perfect, which is why σ = 0 is only an upper bound and σ = 0.2 primary.
- **Attempt 1 discarded (transparency):** with the 0.5 s rule, a re-pilot on objects 25–124 was started; only its
  unavoidable counts were looked at (ID 26 / 1,600 = 1.6 %, S1 F1 38 / 400 — probe-induced, light low-μ objects, onset
  displacement 1.5–3 mm), which fails UT8 (≤ 1 %). No predictor was fitted on it. The detector was re-tuned on objects
  0–24 (above) and those files were moved to `results/pilot/rd_attempt1/` (kept, not used). The re-pilot under the
  frozen protocol uses fresh pilot objects **125–224** (`N_OBJ["pilot"]` = 225).
- Tests: `code/tests/test_rd_probe.py` (determinism / force independence of the probe, onset vs Coulomb force,
  no drop at F_max + monotone bracket, old protocol unchanged, CSF-μ̂, feature sets with σ) — 18 / 18 pass.
