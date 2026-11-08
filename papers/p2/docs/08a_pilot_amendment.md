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
