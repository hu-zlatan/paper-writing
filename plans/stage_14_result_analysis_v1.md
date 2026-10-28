# Stage 14 · RESULT_ANALYSIS · v1 (pre-run checks)

## Goal
Fresh-context quantitative analysis of the stage-12 evidence (manipulation checks, PF convergence) + adversarial area-chair pass → results/v1/14_analysis.md.

## Tasks
- [x] Fresh opus subagent, `stage_prompts/result_analysis.md` verbatim, given only the result files and the pre-registration.
- [x] Adversarial second pass (area-chair prompt) merged.

## Output Summary
- G(S) = −0.033 (bootstrap 95 % CI [−0.054, −0.014]) fails the ≥ 0.10 requirement; identity-only G = +0.003 [−0.020, +0.025]. G(A) passes. The G estimator used 16/8/16/16 instead of the pre-registered 32/32 (deviation not yet recorded — to be added to the amendment) and has no validated positive control, so "no gap detected" ≠ "no gap".
- PF at 8k fails the convergence rule in all 6 cells (ball information 0.09–0.40 nats lower than 32k; S/T10/random success +6.0 pp [1.3, 11.0] at 32k).
- Confusability: set-level pass, but A2/A4/A6 exceed the per-shape 0.80 rule and three S self-symmetry entries are 0.0 (symmetric shapes: the local optimum converged onto a symmetry element and was excluded — artefact, to fix).
- H3 untestable at R_NC(S) = 0.03. H1 untested (no trained policy yet); realistic claim is non-inferiority at much lower latency.
- **Decision:** PROCEED → stage 15 (after running the H2b-P2 positive control to validate the G estimator).
