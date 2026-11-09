# p2 · Addendum 08d — H3 stream simulation, fixed before any stream result (run 40, 2026-11-09)

**Status:** written before any H3 stream, oracle-recalibration or stream-audit quantity has been computed. Only the
counts of labelled rows per pool / role were looked at (S1 / S1m / S3: 2,096 stream + 704 oracle instances each;
S2: 1,500 stream + 700 oracle). 07_hypotheses H3 / H3-x and 08b §5 stay authoritative; this file fixes the details they
leave open and records how the H1-M failure (08c §1) is handled for H3. Later changes go to a further dated addendum.

## 1. Arms and predictors
- CertGrip = full_rd, σ 0.2, seed 0 (`a010_full_rd_s0.2_seed0`); COMP = CSF-1 (`results/v1/comp_selection.json`).
- Online arms: OQT-CertGrip, OQT-COMP, decaying-step OQT-CertGrip (H3-S); Frozen-CertGrip, Frozen-COMP (offline q̂, never
  updated); Oracle-CertGrip, Oracle-COMP.
- **Trackers are per disturbance stratum** (decided here): one q per stratum, initialised at that stratum's offline
  label-rule q̂ (cal split, n = 500, α 0.10) and updated only on steps of that stratum. Reason: calibration is
  stratified (07 §1.4), so the pre-shift segment then behaves exactly like the offline method. The UT4 identity holds per
  tracker.
- **η** = 0.1 × IQR of the in-distribution calibration scores of CertGrip (label rule, all strata pooled), computed once
  and used for every tracker (07 §1.4). Anti-windup: no update on a step whose force was capped at F_max.
- **Oracle**: label-rule split conformal at α per stratum on the shift pool's oracle objects (S1 / S1m / S3: id objects
  325–368 per family, shifted versions; S2: s2 objects 0–174); used for every post-shift step; pre-shift steps use the
  offline q̂.

## 2. Streams
- T = 2,000; steps 1–500 in-distribution, 501–2,000 shifted. Pre-shift steps: 500 drawn without replacement from the
  unshifted id instances of objects 325–368 (704 instances; for S2 the same set). Shifted steps: 1,500 drawn without
  replacement from the shift pool's stream instances (S1 / S1m / S3: 2,096 instances of objects 369–499; S2: all 1,500,
  i.e. a permutation). Steps are shuffled within each segment.
- 20 orderings per shift (`numpy.random.default_rng([4242, shift index, ordering])`).
- ρ_ID for H3-L: an unshifted stream built the same way, with the 1,500 "shifted" steps drawn from the unshifted id
  instances of objects 369–499.
- Window = steps 1,001–2,000. RE_window = mean over window steps of (F_t − F\*_mid)/F\*_mid on avoidable instances.

## 3. Feedback and the H1-M failure
- **Simulated feedback = label rule** slip_t = 1{F_t < F\*_hi,t}, as designed in 07 ("cheap because it replays labels");
  unavoidable instances give slip_t = 1 (and are capped, so they never update the tracker). This is what makes the 20
  orderings and the regenerated-ordering bootstrap affordable.
- Because H1 is not confirmed (8 / 800 non-monotone flickers just above F\*), the label rule is not the physical
  outcome. Two direct-replay audits (protocol rd, ordering 0 only) measure the difference:
  (a) the pre-registered audit: OQT-CertGrip and OQT-COMP, steps 501–1,000, every shift (4 × 2 × 500 replays);
  (b) added here for 08c §3: OQT-CertGrip and Oracle-CertGrip over the whole window 1,001–2,000, S1 / S2 / S3
  (3 × 2 × 1,000 replays). The matched-rate co-requirement uses the realised **physical** slip rates of (b) (point
  difference ≤ 0.02); label-rule window rates (20 orderings) are reported next to them. The paired disagreement
  Δ = mean(slip_direct − slip_label) is reported per audit with an object-cluster bootstrap CI.
- The force schedules of ordering 0 depend only on labels and the tracker rule, so they are written first
  (`results/v1/h3/schedule_<shift>.json`) and replayed by `main.py replay` jobs; the analysis then joins them.

## 4. Inference and decisions (unchanged from 07 / 08b, restated)
- R_E(s) = RE_window(OQT-CertGrip) / RE_window(Oracle-CertGrip), averaged over the 20 orderings (ratio of the averaged
  RE_windows). CI\*\* (97.5 %) from 2,000 object-cluster bootstrap draws that resample, within family, the stream
  objects and the oracle objects (the pre-shift instances belong to the oracle objects and move with them), then
  regenerate the 20 orderings and refit the oracle q̂. The offline q̂ and η are held fixed (they come from the cal split,
  which is not resampled here).
- H3 passes iff the CI\*\* upper limit of R_E(s) < 1.10 for S1, S2 and S3 and the matched-rate co-requirement holds;
  failure per shift iff the lower limit > 1.10; otherwise inconclusive (08b §5: reduced power stated up front).
- Secondary (H3-B, H3-L, H3-S, Frozen arms, capped-step counts) computed from the same streams.

## 5. Order of work
1. `h3_streams.py` (stream generator, per-stratum OQT, oracle, frozen; bootstrap) + synthetic tests → commit.
2. Write the ordering-0 schedules only (no metric printed) → `main.py replay` manifest → Actions.
3. Run the label-rule read-out and the audit join once → `results/v1/h3_analysis.json`.
