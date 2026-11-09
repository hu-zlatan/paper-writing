# p2 · Addendum 08h — the last pre-registered secondaries: H1c, H3-S, H4b, D-FID, H2-M mass-noise (run 42, 2026-11-09)

**Status:** written before any fit or quantity below exists. Seen so far: everything in 08f / 08g and their read-outs.
New predictor fits use only the id **train** objects (labels exist), with the same 30-config search, seed 0, as every
other arm (`main.py fit`). Conventions as in 08f / 08g (label route, CI\*\* 1.25 / 98.75, 2,000 object-cluster draws
unless stated). All secondary; Holm not applied.

1. **H1c** (07 §4). Uncalibrated targeters with CertGrip-full features (σ 0.2), F = min(F_max, ĝ) without q̂:
   - RAW-Q: quantile fit at τ = 1 − α for α ∈ {0.01, 0.05, 0.10, 0.20} (α 0.10 = the existing `a010_full_rd_s0.2_seed0`;
     new fits `--alpha 0.01 / 0.05 / 0.20`).
   - RAW-G: `GaussianModel` (μ̂ by squared error, σ̂ from |residual|), configuration = the best config of the α 0.10
     full_rd quantile search (no new search; stated), F = exp(μ̂ + z_{1−α} σ̂).
   - RAW-Qv (**deviation**): 07 says "τ tuned on the selection split until the selection slip equals α", which needs a
     τ-grid of fits per α. Replaced by the log-shift variant: the RAW-Q prediction plus the single constant c that makes
     the selection-split slip rate equal α (c = the empirical (1 − α) quantile of selection scores; pooled over strata).
     This is a validation-tuned targeter with no finite-sample correction — the practitioner baseline 07 meant.
   - Metric: label slip on the 2,800 id test instances, |slip − α|; interval: object bootstrap of test objects (and
     selection objects for RAW-Qv). Rule (07): RAW-Q and RAW-G "miss" iff the CI\*\* of slip − α at α 0.05 excludes
     ±0.5α (= ±0.025); H1c failure iff all three have CI\*\* inside ±0.25α at every α. Small-n arm (n = 50) is not
     applicable without q̂ and is dropped (stated).
2. **H3-S** (constant vs decaying η, same score space, h3_streams): metric = cumulative Σ (slip_t − α) over shifted
   steps 1–500 (steps 501–1,000 of the stream), mean over the 20 orderings; ΔC = C(decay) − C(constant), per shift
   S1 / S2 / S3 / S1m. Interval: the h3_streams object bootstrap (same resampling, orderings regenerated), 2,000 draws.
   Prediction: ΔC > 0; failure iff CI\*\* upper ≤ 0.
3. **H4b** (identifier control). New fits `full_rd_fid` (CertGrip-full σ 0.2 + family one-hot) and `P_fid` (P + family
   one-hot). D_FID = 1 − RE(full_rd_fid)/RE(P_fid), label route; D = 1 − RE(full_rd)/RE(P) on the same draws.
   Prediction D_FID ≥ 0.5·D (reported as D_FID − 0.5·D with CI\*\*); failure iff D_FID's CI\*\* inside ±0.05.
4. **D-FID**: family classification from touch-only features (static touch, preload-slip flag, squeeze-probe deltas; no
   P, no onset): `HistGradientBoostingClassifier(random_state=0)` default settings, trained on id train rows,
   accuracy on the id test rows (chance 0.25); also with the onset features added. Point estimate + test-object
   bootstrap 95 % interval (500 draws).
5. **H2-M mass-noise**: noisy mass m̃ = m · exp(0.1 ε_m), ε_m ~ N(0, 1) drawn once per object from
   `default_rng(sha256("massnoise|family|obj") first 8 hex)` (the same draw for all four disturbances and every
   shifted copy of the object); used everywhere mass enters (features of the learned arms; CSF-1 / Mondrian-CSF
   formulas). New fits `P_mn`, `full_rd_mn` (σ 0.2). COMP re-selected with the 08c selection rule among CSF-1-mn,
   Mondrian-CSF-mn, P_mn (selection split, even / odd halves). D_mn = 1 − RE(full_rd_mn)/RE(COMP_mn), label route,
   next to the noise-free label-route D(H2a) on the same draws; no directional prediction.
