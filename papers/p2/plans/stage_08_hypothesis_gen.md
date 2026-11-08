# p2 Stage 8 · HYPOTHESIS_GEN (multi-agent debate) — plan (run 37, 2026-11-08)

- Template `stage_prompts/hypothesis_gen.md`, three passes verbatim, each a fresh Opus subagent (AUTOPILOT §3,
  independent context; given only the files, not this session's reasoning):
  pass 1 Proposer ← `docs/06_synthesis.md` (+ stage 1/2 constraints) → `docs/07a_proposer.md`;
  pass 2 Skeptic ← 07a → `docs/07b_skeptic.md`; pass 3 Methodologist ← 07a + 07b → `docs/07_hypotheses.md` (canonical).
- Checks: ≥ 2 falsifiable hypotheses, each with metric + threshold + failure condition; theorem-backed outcomes not
  posed as hypotheses; no citation outside the synthesis; no results claimed.

## Outputs
- Proposer: 4 hypotheses (H1 validity, H2 efficiency vs calibrated safety factor, H3 online under shift, H4 touch).
- Skeptic: H1b REJECT (theorem on its own labels), H1c / H2 / H3 / H4 REVISE; main issues: comparator strength and
  information, circular label-based validity, wrong predicted direction for the friction shift, no power analysis.
- Methodologist: 3 core hypotheses (H1 monotonicity gate + physical-replay validity; H2 primary endpoint D = relative
  force-excess reduction vs the better of Mondrian safety factor / no-touch predictor, at α = 0.10; H3 online quantile
  tracking from binary slip feedback vs a label-requiring oracle recalibration under 3 shifts), secondary H1-x…H4-x,
  unit tests for theorem-backed properties, hardware route stated as a limitation, ≈ 90 CPU-h with a 7-step downscale
  order, and a 60+ row critique → resolution table.
