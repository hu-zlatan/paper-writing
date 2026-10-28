# Stage 8 · HYPOTHESIS_GEN (multi-agent debate) · v2  (PIVOT target)

## Goal
Final v2 hypotheses informed by the v1 pre-run evidence → docs/07_hypotheses_v2.md.

## Tasks
- [x] Pass 1 Proposer (fresh opus): pass-1 prompt verbatim with {synthesis} = docs/06_synthesis.md, plus the v1 failure analysis (results/v1/14_analysis.md, results/v1/15_decision.md) as the PIVOT preamble required by the pipeline ("this is iteration v2; previous results showed …").
- [x] Pass 2 Skeptic (fresh opus) on the proposer output.
- [x] Pass 3 Methodologist (fresh opus) → docs/07_hypotheses_v2.md, including pre-run gates G0–G5 and a fallback if G2 fails.

## Hard-constraint checks
- [ ] Sushi, not curry: ≤ 2 core ideas.
- [ ] Every hypothesis falsifiable with numeric thresholds, CPU-feasible before the 2026-12-04 extended-abstract milestone.

---

## Output Summary
- Proposer (docs/07a_proposer_v2.md): H1 amortization (non-inferiority to greedy at ≥100× lower latency) + H2 look-ahead under travel cost/time budget (gated).
- Skeptic (docs/07b_skeptic_v2.md): both REVISE — κ confounded with horizon/saturation; latency matched to the wrong accuracy; H2 escape routes and weak mechanism tests; objective/action-resolution mismatch between policy and greedy.
- Methodologist (docs/07_hypotheses_v2.md, canonical): H1 non-inferiority to cost-aware ball-information greedy G* on {A,S}×{κ=0, κ_hi} with gap-relative margin δ_c = min(4 pp, 0.15×random→G* gap) + H1b latency ladder; H2 (set S, gated) beats G* and a cost-aware myopic policy at κ_hi with an interaction test vs κ=0 and TOST negative control; mechanism P1–P3. Same target (ball information) and the same 256-action set for all methods; probe-matched budgets (n* ∈ {3,4,5}); cell rule. Gates G0–G5 with dates (decision 2026-11-12); G1/G2 failure does not block H1. Main runs ≈ 121 CPU-h (≈ 99 fallback) + gates ≈ 47 CPU-h.
- Open: verify ≥ 3 references (budgeted informative path planning, budgeted adaptive submodularity, cost-aware BED) before stage 9; write docs/07c_amendment_v2_0.md items (equal stroke time for hits/misses; set-A per-shape confusability rule amended).
- **Decision:** PROCEED → stage 8.5 (v2).
