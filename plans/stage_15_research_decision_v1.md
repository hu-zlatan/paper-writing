# Stage 15 · RESEARCH_DECISION · v1

## Goal
PROCEED / REFINE / PIVOT from results/v1/14_analysis.md → results/v1/15_decision.md.

## Tasks
- [x] Fresh opus subagent with the stage prompt (REFINE-augmented) and the analysis + PC addendum.
- [x] Apply loop wiring (snapshot, LOOP MARKER, version bump).

## Output Summary
- **Decision: PIVOT → stage 8** (results/v1/15_decision.md). The predicted phenomenon behind H2a/H3 did not appear in the pre-run checks (G(S) = −0.033, upper bound −0.017; R_NC(S) = 0.03; no detectable gap even on PC), and redesigning S until the check passes would be a forking path.
- New framing for stage 8 (v2): core idea 1 = amortized goal-oriented touch policy non-inferior to greedy PF-EIG at ≥ 100× lower latency; gated idea 2 = look-ahead pays when the finger must travel between probes under a time budget (travel-cost ratio κ; κ = 0 reproduces v1 as a built-in control). Gates G0–G5 before main runs; fallback by 2026-11-12 if G2 fails.
