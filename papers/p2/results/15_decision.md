# p2 · Stage 15 RESEARCH_DECISION (v1) — run 42, 2026-11-09

Input: `results/14_analysis.md` (merged pass 1 + binding audit). Template `research_decision.md` with the REFINE option.

## Decision
**PROCEED** to stage 16, with the paper re-scoped to what the evidence supports (below). No REFINE loop is opened now;
the mandatory second loop will come from stages 18–20 / 25 (→ 13 or 16) if the review or the gate finds fixable
evidence gaps.

## Justification (hard rules)
1. *Primary metric difference statistically meaningful* — **met.** H2a (primary, 08c CRC route): CertGrip-full σ 0.2
   vs COMP = CSF-1, D = 0.4168, CI\*\* 97.5 % [0.3484, 0.4778] (2,000 object-cluster draws), superiority with
   F\*_lo / F\*_hi; robust on the label route (0.4292), the post hoc 08e grids (0.4289), seeds 1–4, H2-C vs
   Mondrian-CSF (0.438), H2-n at n = 50 (0.415 / 0.465), all 16 family × disturbance cells (H2-H, every lower ≥ 0.16),
   and the tail (H2-T, P95 ratio 0.59, pass).
2. *Every claimed effective component has a non-degenerate ablation* — **met for the component we will claim: the
   ramp-down friction-onset probe.** H4a: static touch ≡ P (D −0.008, equivalence); squeeze adds nothing shown
   (D −0.026, not confirmed); + onset D 0.474. H4e (vs onset-only) and H2b (vs the physics plug-in CSF-μ̂ with the same
   onset estimate) show the learned model adds no demonstrated gain at σ 0.2 (H2b D 0.0569 [−0.0399, 0.1454], not
   confirmed). H4c (shuffled features) and H4b (family ID given to both arms, D_FID 0.464) rule out capacity and
   identifier artefacts. So the claim is "probe + conformal calibration", **not** "learned tactile model".
3. *No CRITICAL FABRICATION flags* — **met.** The audit re-checked every primary number against the JSON files; its 23
   findings are wording / status / rounding issues, all adopted as binding rewrites (one rejected in part with the
   H3-L numbers).
REFINE is not the default here: the hypothesis that matters (H2a) is not thin — it is the most robust result — and the
weak results (H1-M failed, H2b not confirmed, H3 inconclusive, H2-R reversal) are pre-registered outcomes, not
under-tuned evidence; re-running to change them would be post hoc. PIVOT is not warranted: the primary effect is
large and the "learned touch adds nothing" finding is itself a clear, publishable negative.

## Evidence the paper must carry (with its limits)
- H1 not confirmed: H1-M 8 / 800 non-monotone (limit 7; CP upper 0.0212 > 0.02); validity rests on CRC over the
  physical binary loss; H1-V passes (physical slip ≤ label rule, Δ −0.0014 … −0.0043).
- H2b: learned vs plug-in — plug-in better at σ 0 / 0.1 on the label route, no difference shown at σ 0.2, learned
  better only at σ 0.4 (secondary, all routes); 08c CRC results at σ 0 / 0.1 are unreliable (grid defect, 08e).
- H3 inconclusive on S1 / S2 / S3 (R_E 0.878 / 1.174 / 0.963; CI\*\* half-widths 0.15–0.20, wider than planned);
  matched-rate co-requirement fails on S1 / S2; OQT label-rule window slip 0.0999–0.1016; frozen q̂ breaks under S1
  / S3; H3-S: decaying η costs 58 / 42 extra slips (S1 / S3, confirmed); H3-L not confirmed.
- **Scope limit (H2-R):** in the sub-pool μ ∈ [0.5, 0.8] × mid amplitudes D = −0.261 [−0.532, −0.032] — the gain
  depends on a wide friction range. Must appear in the abstract-level claims.
- H2-M (no mass, mass noise) is reported descriptively only, not as evidence for the friction story (08a / 08b).
- Sim-only; F\* labels exist only in simulation (offline calibration is not deployable as-is; OQT is the hardware
  route); single simulator, 5 families.

## Next actions
- Stage 16 PAPER_OUTLINE (p2) — RSS 2027 Stage 1 extended abstract (≤ 5 pages + 1 page references): template
  `paper_outline.md` verbatim; title / claims built on the re-scoped story above, with the audit's supported rewrites.
- Stage 17 draft, 18 two independent reviews (fresh subagents), 19 revision, 20 gate — target ≈ 11-20 so stages
  21–25 fit before 12-01.
- Literature: verify any citation added beyond `docs/05_knowledge_cards.json` through the repo's literature workflow
  (WebFetch is not available to unattended runs).
