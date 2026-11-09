# p2 · Addendum 08g — operational choices for the remaining pre-registered secondaries, part 1 (run 42, 2026-11-09)

**Status:** written before any quantity below has been computed. Seen so far: everything listed in 08f plus the 08f
read-outs (H2-T, H4c, H2-M, H3-B, D-μ, UT3). No new simulation or fit. Same conventions as 08f: label-rule route
(08c: arms outside the CRC set use the label rule), CertGrip = full_rd σ 0.2 seed 0, COMP = CSF-1, id cal / test
splits, q̂ per disturbance stratum unless stated, RE against F\*_mid, CI\*\* = 1.25 / 98.75 percentiles of 2,000
object-cluster draws (cal and test objects within family, q̂ refitted). All secondary; Holm not applied.

1. **H2-C** (07 §4): D = 1 − RE(CertGrip)/RE(Mondrian-CSF) (CSF-1 formula, one q̂ per family × disturbance cell,
   family ID privileged). The D against CSF-1 is H2a itself and is not repeated. Rule: the H2a rule (superiority iff
   D ≥ 0.10 and lower > 0; equivalence iff CI\*\* inside ±0.10; inferiority iff upper < 0).
2. **H2-n**: per draw, n = 50 calibration instances per stratum = the first 50 calibration objects of a random
   object-level subsample (the same objects for both arms; 2,000 draws, each also resampling test objects); α 0.10 and
   0.20; D = 1 − RE(CertGrip)/RE(CSF-1). Point = mean over draws, interval = 1.25 / 98.75 percentiles. Prediction:
   lower > 0; failure: interval inside ±0.10.
3. **H2-H**: the 16 family × disturbance test cells, cell D_c = 1 − RE_c(CertGrip)/RE_c(CSF-1) with the pooled per-stratum
   q̂; cell variance from the bootstrap; DerSimonian–Laird pooled D and τ. Safety guard: no cell with a Holm-adjusted
   (16 cells, one-sided 5 %, normal approximation from the bootstrap SE) lower limit of −D_c > 0.10. Reported: pooled D,
   τ, the 16 cell D_c with CI\*\*.
4. **H2-R**: sub-pool = id cal + test instances with μ ∈ [0.5, 0.8] **and** the disturbance amplitude inside the middle
   50 % (25th–75th percentile of that disturbance's amplitude over all id cal + test instances; D1–D4 each). q̂
   recalibrated inside the sub-pool (cal instances of the sub-pool, per stratum). D and CI\*\* reported (no prediction).
5. **H4d** (CoM mechanism): per family F, D_F = 1 − RE_F(CertGrip-full)/RE_F(CertGrip-P) on F's test instances with the
   pooled q̂ (touch vs no-touch, the comparison where a pressure-centroid feature could matter); also with the
   squeeze-only arm `full` in place of CertGrip-full. Prediction: D_F4 − D_F1 > 0 with lower > 0; failure: upper ≤ 0.
6. **D-loc**: over the paired S1 / id instances (same object and disturbance, both avoidable): mean and SD of
   log F\*_mid,S1 − log F\*_mid,ID (Coulomb predicts 0.511, SD 0); for P, S, full, CertGrip: mean |Δĝ|/ĝ between the S1
   and the id copy of each instance (touch features change under the shift); preload-slip rates per pool (id, S1,
   S1m, S3, s2).
7. **Oracle decomposition** (H2 ceiling): label-route RE of the oracle arm (privileged inputs) next to CertGrip and
   CSF-1, and the share of the CSF-1 → oracle gap closed by CertGrip, (RE_CSF − RE_CG)/(RE_CSF − RE_oracle), with CI\*\*.

Not in this part (need new fits or stream code; a later addendum fixes them first): H1c (RAW-Q / RAW-Qv / RAW-G),
H3-S, H4b, D-FID, the 10 % mass-noise condition of H2-M.
