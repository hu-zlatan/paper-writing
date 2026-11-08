# p2 Stage 8.5 · THEORETICAL_BOUNDS — plan (run 37, 2026-11-08)

- Template `stage_prompts/theoretical_bounds.md` verbatim; {hypotheses} = `docs/07_hypotheses.md`, {method_sketch} =
  its §1.4. Strongest model (this session). Never fabricate a proof; mark informal parts.
- Output `docs/07b_theoretical_bounds.md` with the 6 required sections.

## Outputs
- Restated G1 (split-conformal label coverage, object-level exchangeability caveat, label → slip via monotonicity) and
  G2 (OQT identity and long-run bound on uncapped steps, assumption-free; boundedness of q argued informally).
  Complexity: labelling O(k·C_sim) with k ≈ 10 replays dominates; decision O(B d); online update O(1).
