# Stage 8.5 · THEORETICAL_BOUNDS · v2

## Goal
Complexity and informal statements for the v2 hypotheses → docs/07b_theoretical_bounds_v2.md.

## Output Summary
- Cost-aware greedy O(N·A·(V+M)) per decision (≈ 2.6 s at A = 256, scaled from measured 0.65 s at 64 candidates); policy O(d² + d·A).
- Informal argument why travel cost (order-dependent costs → orienteering-type problem) removes greedy's guarantees and can create look-ahead value; explicitly not a guarantee that it does — G2 measures it.
- Exact enumeration on a discretized notch problem specified as the G1 reference.
- References for 4.1 pending the supplementary OpenAlex lookup.
- **Decision:** PROCEED → stage 9 (v2) — next run.
