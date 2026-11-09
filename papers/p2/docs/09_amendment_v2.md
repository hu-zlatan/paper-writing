# p2 · Amendment v2 (REFINE loop from stage 20 → stage 13) — written 2026-11-09 (run 43), before any v2 code or run

Trigger: stage-20 gate `paper/mypaper/20_quality_gate.json` 6.5 / 10 < 7.5 with evidence-level weaknesses (stronger
baselines; online study feedback; σ grounding) and missing analyses of the existing replays (frontier,
high-probability certificate, extra contrasts). Refine cycles used 0 → 1 of 3. All v1 numbers and verdicts stay as
they are; v2 adds rows, it does not re-decide v1 hypotheses. Everything below is **secondary**; v1 analyses of record
are untouched. Nothing below has been computed when this file is committed.

Common to all v2 rows: id pool, the v1 cal / test split, the 08c per-stratum CRC (α 0.10, 20-point grids built from
the selection split only), physical binary slip from direct replay, RE = mean (F − F\*_mid) / F\*_mid on avoidable test
rows, intervals CI\*\* = 97.5 % object-cluster bootstrap with λ̂ refitted on every draw (2,000 draws, seed 2026), as
in `code/analysis_crc.py`. Decision labels as in 08c: superiority if CI\*\* lower > 0, inferiority if upper < 0,
otherwise not shown.

## A. Analyses of the existing 08c / 08e replays (no new simulation)
A1 **Risk–efficiency frontier** (the frontier pre-registered in 07 and not produced in v1): for CertGrip-full σ 0.2,
   onset-only σ 0.2, CSF-μ̂ σ 0.2 and CSF-1, shift every stratum's λ̂ index by k ∈ {−4, …, +4} (clipped to the grid)
   and record (test physical slip, RE). Matched-slip comparison: RE of each arm at test slip 0.10, by linear
   interpolation between adjacent k; D_match = 1 − RE_arm / RE_CSF-1 with CI\*\* (the interpolation repeated inside each
   draw). Uses the 08c grids; repeated on the 08e grids as a sensitivity row.
A2 **High-probability certificate (Learn-then-Test, fixed sequence):** per stratum, scan λ from the top of the grid
   downwards and keep λ while the Clopper–Pearson upper bound (one-sided, δ = 0.10) of the calibration physical risk
   at λ is ≤ α; λ̂_LTT = the last kept value (if none, max Λ, flagged). This gives P(risk ≤ α) ≥ 1 − δ per stratum. Report
   RE, test slip and D_LTT(CertGrip-full vs CSF-1), D_LTT(CSF-μ̂ vs CSF-1) with CI\*\*.
A3 **Extra contrasts on the 08c route:** D(CSF-μ̂ σ 0.2 vs CSF-1), D(onset-only σ 0.2 vs CSF-1), CI\*\*; and on 08e grids.

## B. New arms (new replays on the same instances; code committed before any replay)
B1 **CSF-proxy (non-tactile baseline with a friction proxy).** CSF-1 formula with μ̄ replaced by
   μ̃ = clip(μ · exp(σ_p ε_p), 0.1, 3.0), ε_p ~ N(0, 1) drawn per instance from a seed fixed in the code (independent
   of the onset ε), σ_p ∈ {0.2, 0.4, 0.8}. It stands for a non-tactile friction prior (material / vision) of known
   quality; it uses the true μ only through the noisy proxy (an oracle-side construction, stated as such).
   Grid: the 08c recipe (selection split, centred on the label-rule quantile, ±0.4, 20 points); if a stratum's λ̂ lands
   on grid index 0 or 19, the 08e recipe (widened grid) is used for that arm and this is reported.
   Registered read-out H5: D(CertGrip-full σ 0.2 vs CSF-proxy σ_p) with CI\*\* for each σ_p. Prediction (stated
   before running): superiority at σ_p 0.8, the margin shrinking as σ_p falls; we report at which σ_p the CI\*\*
   first includes 0 (or that none does). No σ_p is chosen after seeing results.
B2 **Probe + fixed margin (no calibration).** F = (1 + m) · f_nom_muhat (the CSF-μ̂ σ 0.2 force), m ∈ {0, 0.25, 0.5, 1.0}.
   Replay once per instance at that force (cal and test). Report per-stratum and overall test physical slip and RE.
   Purpose: show what calibration adds (a hand-set margin either over- or under-shoots α per stratum). Descriptive.
B3 **Online study with physical feedback (H3-P).** Conditional on a 5-minute pilot showing ≤ 6 CPU-h total: S1 and
   S3 streams, orderings 0–4, CertGrip-full σ 0.2 and CSF-1, quantile tracker as in 08d but warm-started from the 08c
   CRC λ̂ and fed the physical slip of the replay at the issued force. Report window slip (steps 1–500 and last 500)
   and RE. If the pilot exceeds the budget, downscale in this order: orderings 0–2 only → S1 only → not run (stated).

## C. Not done in v2, with reasons (stay as limitations)
- Reactive slip-tightening controller: needs a new closed-loop controller and a new label definition; out of scope
  for this loop. Correlated-μ object pool: needs new labels (≈ 0.6 CPU-h) and a new COMP selection; deferred unless
  B1 leaves time before 11-20. σ grounding on hardware: impossible here; a literature search for published
  onset-detection error of real tactile sensors goes through the repo's literature workflow.

## Compute
A: seconds. B1: 3 arms × 4,800 instances × 20 replays ≈ 1.2 CPU-h (08c: 14 arms ≈ 5.7 h). B2: 4 × 4,800 single
replays ≈ 0.1 h. B3: ≤ 6 h by its own pilot rule. Total ≤ ≈ 8 CPU-h, on GitHub Actions / the sandbox.
