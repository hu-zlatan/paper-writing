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
