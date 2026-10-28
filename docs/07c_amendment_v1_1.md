# Amendment v1.1 to docs/07_hypotheses.md and docs/08_experiment_plan.yaml (2026-10-28, before any main run)

Version stays v1: no main experiment has run; these changes come from development pilots (docs/10_dev_findings_v1.md,
results/v1/dev/). They are recorded here, dated, with reasons, instead of silently editing the pre-registration.

## A1 — Contrastive count L (resolves deviation D1)
The D1 pilot rule (saturation < 10 % at T = 10) cannot be met by any affordable L: an untrained policy on S already
has 89–97 % of T = 10 episodes within 0.5 nats of log(L+1) for L ∈ {255, 1023, 4095}. As pre-registered in D1,
**L = 4095** (cap 8.32 nats). Interpretation recorded for the paper: log(L+1) ≈ −log P(success region) ≈ 8.1 nats
(asymmetric shapes), so the capped bound stops rewarding information beyond the resolution the task needs; this is a
calibration argument, not a theorem, and the L ablation (A4: 255, 1023, 4095) reports its effect. Per D2, core seeds
are 6 (seed-robustness rule ≥ 5 of 6), and the training cap is E_train = 10⁵ episodes per run with the plateau rule
(cap doubles for all methods in a comparison if any has not plateaued), because one L = 4095 run costs ≈ 2 CPU-h.

## A2 — Co-primary information metric (deviation D3, revised)
IG_T (KDE) is biased low for broad posteriors and the evidence-based IG drifts with particle count (15.9 → 11.8 nats
from 2k to 32k particles on the same episodes). Both are kept as diagnostics only. **Co-primary metric: ball
information** = log P̂(B(s0) | h_T) − log P(B(s0)), B = success region (same identity, translation < 5 mm, folded rotation
error < 5°), computed from evaluation-PF masses (converged 7.70 vs 7.73 nats at 8k vs 32k particles in the dev pilot).
All margins stated in nats for IG_T apply unchanged to ball information. H2b (oracle two-step EIG) keeps using
nested-MC EIG on full-state beliefs, which is a separate computation.

## A3 — Evaluation particle filter
Resample-move now mixes a random-walk kernel with an independence MH kernel whose proposal is contact-conditioned
(defensive mixture with the prior; closed-form density, unit-tested). Without it the bootstrap PF collapsed onto wrong
modes (success 0.50 at 4k vs 0.90 at 40k particles on the same episodes). N_eval is fixed by the pre-registered N vs 4N
check (start N = 8,000; compare with 32,000; ≥ 300 episodes per (set, T ∈ {3, 10}) for random and greedy).

## A4 — Costs (re-estimated)
Greedy PF-EIG full size ≈ 0.65 s per decision (planned 0.1 s); evaluation PF ≈ 1 s per episode at 8k particles;
training ≈ 18 ms per episode at L = 1023 and ≈ 65–80 ms at L = 4095. All sweeps run as sharded GitHub Actions jobs
(≤ 5 h each with time_guard). If the total exceeds the Actions capacity, the pre-registered downscale order of
docs/07_hypotheses.md §7 applies, then test episodes per cell 2,000 → 1,000 for secondary rows only.

## A5 — Encoder ablation
A3's GRU variant is dropped (numpy GRU with hand-written backprop is not worth its cost for a secondary row); the
padded-concatenation MLP variant is kept.
