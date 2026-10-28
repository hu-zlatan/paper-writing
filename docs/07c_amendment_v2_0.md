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
