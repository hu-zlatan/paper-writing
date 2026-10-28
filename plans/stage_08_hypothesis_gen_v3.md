# Stage 8 · HYPOTHESIS_GEN (multi-agent debate) · v3  (PIVOT target, run 4)

## Goal
Final v3 hypotheses informed by the v2 gate record → docs/07_hypotheses_v3.md.

## Tasks
- [ ] Pass 1 Proposer (fresh opus): pass-1 prompt verbatim with {synthesis} = docs/06_synthesis.md, preceded by the
      PIVOT preamble ("this is iteration v3; previous results showed …") pointing to results/v2/14_analysis.md and
      results/v2/15_decision.md (+ v1 15_decision for history) → docs/07a_proposer_v3.md.
- [ ] Pass 2 Skeptic (fresh opus) on the proposer output → docs/07b_skeptic_v3.md.
- [ ] Pass 3 Methodologist (fresh opus) → docs/07_hypotheses_v3.md with pre-run gates, numeric rules, fallback, timeline
      to the 2026-12-04 extended-abstract milestone.

## Hard-constraint checks
- Sushi, not curry: ≤ 2 core ideas. Falsifiable numeric thresholds. CPU-feasible (numpy, GitHub Actions).
- Last loop before escalation (RESTRICTS max_refine_cycles = 3; 2 used).
