# Amendment v2.0 (2026-10-28, before any v2 code or run)

Recorded deviations and fixes required by docs/07_hypotheses_v2.md (G0) and results/v1/15_decision.md.

- **B1 — Stroke time.** Every probe costs 1 stroke whether it hits or misses (07_hypotheses_v2 §1.2). The stage-15
  decision mentioned an outcome-dependent stroke time; it is not used, because budget consumption would then depend
  on the outcome, a channel unrelated to travel.
- **B2 — Set A per-shape confusability.** Shapes A2, A4, A6 exceed the v1 per-shape rule (0.806, 0.818, 0.818 ≤ 0.80
  required). The rule is amended to the set-level requirement C(A) ≤ 0.80 (0.772 measured) plus per-shape ≤ 0.85,
  instead of replacing shapes, so all v1 reference numbers on A stay valid.
- **B3 — Self-symmetry search artefact.** For symmetric S shapes the multi-start search converged onto a symmetry
  element and the result was excluded, giving 0.0. Fix: evaluate IoU on a fixed rotation grid (2°) outside the ±10°
  neighbourhoods of the symmetry group, then refine locally within the allowed region; recomputed in G0.
- **B4 — Ball-sPCE is a surrogate.** The training reward uses a ball-averaged numerator with J = 16 in-ball samples;
  it is not claimed to be a lower bound; its bias against evaluation-PF ball information is measured in G3.

## Status note (2026-10-28, run 2) — G0 (ii) recomputation
With the B3 search (results/v2/checks/confusability_{S,A}.json): S self-symmetry entries are no longer 0.0
(S_rect 0.825, S_rtri 0.836, S_hex 0.922, S_trap 0.809; C(S) = 0.971, passes). The stronger self-symmetry search also
raises set A's self values: C(A) = 0.802, which now **misses the C(A) ≤ 0.80 requirement by 0.002** (per-shape values
0.755–0.821, all ≤ 0.85). Not resolved in this run. The threshold is not changed after seeing the value; the options
for the next run are to replace the most self-confusable shape(s) of A with the next shapes from the same seeded
generator (re-running the v1-comparable baselines on A) or to report A as marginally failing the pre-registered check.

## B5 — G4 outcome and evaluation-PF kernel change (2026-10-28, run 3; written before the B5 check is run)
**Recorded result (results/v2/12_g4_analysis.json, 12_g4_fallback_analysis.json).** G4 as pre-registered fails in all
four κ = 0 cells on ball information (128k − 32k, 3 MH: A-random +0.133 [0.085, 0.186], A-G* +0.063, S-random +0.177,
S-G* +0.097 nats; success within ±2 pp except A-G* +1.2 pp point). The pre-registered fallback (32k × 10 MH vs
32k × 30 MH, random policy, 600 paired episodes) also fails: ΔBI +0.046 (A) and +0.040 (S) nats pass, but Δsuccess
+1.1 pp (A, CI [−0.5, 2.8]) and +3.7 pp (S, CI [0.8, 6.5]) do not. The diagnostic comparison 32k × 30 MH vs
128k × 3 MH gives ΔBI −0.013 / +0.007: the 3-MH kernel's error is MCMC mixing, not particle count.
**Change.** The evaluation PF gains an optional *final rejuvenation*: after the last probe, one forced systematic
resample followed by R posterior-invariant MH moves on the full history (`ParticleFilter.rejuvenate`, `--final-mh`).
Decisions never read the evaluation PF (G* and learned policies act on their own decision PF / inputs), so this
changes no action sequence. R = 0 is bit-identical to all earlier runs (unit test).
**Check (same G4 rule, |ΔBI| ≤ 0.05, |Δsuccess| ≤ 1 pp with 95 % CI inside ±2 pp).** Candidates: 32k × 3 MH path +
R ∈ {10, 30} final. Reference: 32k × 30 MH path + 60 final (heavier than anything previously run). Cells: S and A at
κ = 0, random and G*, 600 paired pilot episodes each (G* is the comparator whose numbers matter most). The smallest R
that passes in every cell is frozen as the evaluation PF for all v2 numbers. If neither passes, the reference kernel
itself becomes the evaluation PF and its cost (≈ 3× the §6 estimate) enters §6 through the downscale order; the
κ_hi cells are checked when the calibration (G5) fixes τ_κ. The thresholds are unchanged.

## B6 — G1 instrument details fixed before the G1 run (2026-10-28, run 3)
- **Exact notch reference** (`code/touchbed/notch.py`): the v1 H2b-P2 geometry with the informative observation
  coordinate only (vertical probe → NC or contact height; horizontal probe → contact abscissa), ε-softened as in the
  main model, 401-point x grid, 71 vertical probes (2 mm spacing over ±70 mm) + 1 horizontal probe. Values are exact
  enumeration over the grid with trapezoid quadrature over z (0.25 mm, ±6σ; outside that region the posterior is
  exactly the prior belief). Quadrature check: 0.5 mm / ±6σ and 0.125 mm / ±8σ change V_opt by < 0.002 nats.
  Exact values at the prior: V_opt = 0.615 nats (horizontal first), V_greedy = 0.174 nats, **exact relative gap 0.717**
  (the pre-registration's "≈ 0.69 / 0.2 / 0.7" were analytic approximations).
- **Estimator settings (frozen for G1 and G2)** (`code/touchbed/lookahead.py`): C1 = 32 screened candidates = G*'s own
  first action + one structured set-up move + 30 uniformly drawn actions; screen with M_outer = 64 CRN outer samples;
  re-estimate the top 4 plus G*'s action with 4 × 64 = 256 fresh CRN samples; V_LA = max re-estimate (G*'s action
  included), V_G* = re-estimate of G*'s action; rollouts completed by the Monte-Carlo greedy comparator (M = 64).
  The structured set-up move is defined generically as **the action of maximal full-state EIG** (it localises the
  nuisance); on S it is added next to the two pre-registered structured moves (antipodal travel, travel to the region of
  maximal mode disagreement).
- **G1 (a)** is computed as the mean of 5 independent estimator runs (seeds) at the prior; pass iff the mean is in
  [0.8, 1.2] × 0.717 = [0.574, 0.861]; every run is reported.
- **G1 (b) bank**: beliefs after one horizontal probe on a random true state (fixed seed 2026), two probes left, kept iff
  the exact relative gap ≤ 0.001, until 100 are found. Pass iff the mean estimated relative gap is in [−0.01, +0.02] and
  its one-sided 95 % bootstrap UB < 0.03 (as pre-registered).

## B7 — Decision on C(A) = 0.802 (2026-10-28, run 3)
Set A is kept unchanged and the check is **reported as marginally failed** (0.802 vs ≤ 0.80) in the paper. Reasons:
v2 uses A only as the low-ambiguity contrast to S for H1 (amortization), where C(A) = 0.80 vs C(S) = 0.97 remains a
clear separation; replacing shapes after seeing the value would be a post-hoc selection of the object set, and the
per-shape rule (≤ 0.85, max 0.821) passes. No other rule depends on C(A).

## B8 — Grid reference for the evaluation posterior (2026-10-28, run 3; before any grid-vs-kernel comparison)
**Why.** Partial B5 data (A, random, 600 episodes) show r10 and r30 still differ from the 32k × 30 MH + 60 reference
by +0.12 / +0.08 nats BI: every SMC kernel moves the numbers and none of them can validate itself.
*Correction (same run):* an earlier version of this paragraph also said that success with final rejuvenation was
≈ 0.47 vs ≈ 0.31 with 3 MH. That was a printing bug in code/analysis_g4_b5.py (it printed the identity-correct rate in
the success column); the success rates are 0.307 (r10) vs 0.312 (3 MH). The JSON outputs were correct. Decisions never read the evaluation posterior, which only has to
represent p(s | h_T) for a short, fixed history (≤ 5 probes), so a deterministic reference is possible.
**Reference.** `touchbed/gridpost.py::AdaptiveGridPosterior`: uniform-prior grid over (k, x, y, θ), coarse cells 1 mm ×
1 mm × 2° evaluated everywhere; every coarse cell within 25 nats of the maximum (dilated by one cell) is subdivided
4 × 4 × 4 (0.25 mm, 0.5°). Same likelihood code, same read-outs (MAP identity, Nelder–Mead pose refinement, ball mass,
PF floor convention 1/(2·32,000)). Histories are rebuilt exactly from the recorded actions and the observation stream
(checked: the rebuilt history reproduces the recorded PF ball information bit-for-bit). Check on S/random episode 0:
adaptive 1/2/4 = full 0.25 mm/0.5° grid = 5.9048 nats (3 MH PF 5.586, 10 MH 5.779, 30 MH 5.879, 128k 5.273).
**Self-check before use.** Adaptive sub = 4 vs sub = 8 on ≥ 6 pilot episodes (S; random and G*): mean |ΔBI| ≤ 0.02 nats
and no success flips. Otherwise sub = 8 becomes the reference.
*Revision (same day, after a first sandbox comparison on S/G* episode 0, recorded here):* sub 4 vs 8 gave ΔBI = 0.008
but flipped success because the identity posterior is an exact tie (true-identity mass 0.503 vs 0.499); "no success
flips" is therefore restricted to episodes whose true-identity mass is outside [0.45, 0.55] under both settings; flips
inside that band are reported. The self-check runs on 8 S pilot episodes (4 random, 4 G*) of shard 1, not shard 0.
**Kernel selection.** The G4 rule (|ΔBI| ≤ 0.05; |Δsuccess| ≤ 1 pp with 95 % CI inside ±2 pp) is applied to every
candidate evaluation method against the grid reference on the first 200 recorded pilot episodes of each κ = 0 cell
(S/A × random/G*), paired: PF 32k × 3 MH (G4), × 10 MH, × 30 MH, r10, r30, the 30 + 60 kernel, and the grid itself at
coarser settings. The cheapest method that passes in every cell becomes the evaluation for all v2 numbers; κ_hi cells
are checked the same way when their pilot runs exist. If no SMC kernel passes, the grid is the evaluation and its
measured cost enters §6 through the downscale order. Thresholds unchanged.

## B9 — G3 (i) selection details (2026-10-28, run 3; written when 2 of the 4 logs had finished)
- Configurations: the first four of the pre-drawn v1 random configurations (experiments/hpsearch_v1.json), seed 100,
  (S, κ = 6, τ = 5.0), E_train = 10⁵.
- Selection metric: the final logged validation ball-sPCE of the argmax policy (500 fixed validation episodes);
  ties within 0.02 nats go to the lower configuration index. The sampled-policy value is reported, not used.
- The weights of these four runs were not kept (a .gitignore rule excluded *.npz; fixed afterwards); G3 (ii) retrains
  the selected configuration with 3 pilot seeds, whose weights are kept.

## Status note (2026-10-28, run 3) — G3 (iii) notch learnability
With the G3 (i)-selected configuration (hp1: lr 3.63e-4, entropy 1.33e-4, batch 128, critic lr 1.43e-3), 3 seeds:
exact value of the argmax policy 0.177 / 0.170 / 0.169 nats = 28 % of the exact optimum 0.615 (rule ≥ 80 %); all
three choose a vertical first probe (greedy-like; exact greedy 0.174). The pre-registered remedy (E_train doubled to
2·10⁵) gives the same values. **G3 (iii) fails.** Per §4 this sends the gate to stage 15 with learnability of set-up
moves as a finding; the routing is decided at the gate decision together with G2, G3 (ii)/(iv), G4 (B8) and G5.

## Status note (2026-10-28, run 3, ~17:15 UTC) — B8 kernel comparison (partial) and B5 cancellation
On the grid-reference episodes completed so far (A/S × G*: 600 each; A random 300; S random 250), **no SMC kernel
passes the G4 rule in every cell**: 32k × 3 MH under-reads BI by 0.07–0.18 nats in every cell; 128k × 3 MH and the
heavy 30 + 60 kernel agree with the grid on BI (|ΔBI| ≤ 0.05; 0.006–0.019 for 30 + 60) but the success criterion's 95 %
CI (±2 pp) is not met on the random cells by any kernel, because MAP-identity ties and the point-estimate refinement
make success discontinuous in the posterior approximation. Under B8 the grid therefore becomes the evaluation,
subject to its own sub 4 vs 8 self-check (G* part: mean |ΔBI| 0.007, no flips outside the tie band; random part
pending). The remaining B5 jobs (heavy kernels on S) were cancelled because they can no longer change this outcome.
Measured grid cost on Actions: G* episodes 2.4 s (A) / 4.6 s (S) per episode; random episodes 66 s / 76 s.

## Status note (2026-10-28, run 3, ~17:25 UTC) — G5 provisional (32k × 3 MH read-outs; grid re-evaluation dispatched)
- G* vs random (300 pilot episodes): A0 (τ 3) 0.837 vs 0.197; A6 0.457 vs 0.037; A12 0.413 vs 0.027; S0 (τ 4, G4 runs)
  0.645 vs 0.210; S6 0.417 vs 0.033; S12 0.357 vs 0.067 — the +10 pp and D ≥ 20 pp rules hold everywhere.
- **Non-degeneracy (§1.7) at A0:** success(G*) 0.835 on the first 200 is inside [0.15, 0.90], but **BI saturation of G* is
  75 %** (≥ 50 %). n*(A) is already 3, the lowest value the n* rule allows, so the rule cannot be applied again; if the
  grid read-out confirms it, A0 is removed from the primary set (§1.7), reported.
- **Flatness (§1.5):** at κ = 6, Δsuccess +1.3 pp and ΔBI −0.015 (pass); **at κ_hi = 12, Δsuccess +7.7 pp and ΔBI +0.19
  nats (fail)**. If the grid read-out confirms it, the pre-registered consequence is 𝒜 → 64 × 8 for all methods (once),
  which also invalidates the τ calibration, G2-at-12 and G3 (ii)-at-12 runs made on the 32 × 8 set. This, the G3 (iii)
  failure and G2's refutation of Idea 2 go to the stage-15 gate decision together.
