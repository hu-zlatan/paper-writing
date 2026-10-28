# Stage 8.5 · THEORETICAL_BOUNDS · v1

## Goal
Preliminary complexity / bound analysis for the hypotheses → docs/07b_theoretical_bounds.md.

## Tasks
- [x] Run `stage_prompts/theoretical_bounds.md` with {hypotheses} = docs/07_hypotheses.md, {method_sketch} = its §2–3.
- [x] Six required sections; no fabricated proofs; informal parts labelled; comparison with closest baselines; honesty section.

## Expected outputs
- docs/07b_theoretical_bounds.md

## Hard-constraint checks
- [x] No proof claimed where none exists (PPO convergence explicitly informal).
- [x] Unverified citations flagged "(to verify)".

---

## Output Summary  (filled in AFTER the stage runs)
- Greedy PF-EIG: O(N·C·(V+M)) per decision; policy: O(d²) independent of N, C, M, K; training O(E·T·(L+1)·V).
- **Finding:** sPCE ≤ log(L+1); with the planned L = 255 the training signal caps at ≈ 5.55 nats, below the ≈ 8.1 nats the success criterion needs (informal estimate). Stage 9 must raise L (e.g. 4095) or justify otherwise, and the pilot must measure g_T saturation.
- **Decision:** PROCEED → stage 9.
