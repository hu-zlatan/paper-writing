# Stage 10 development findings (v1, 2026-10-28) — blockers to resolve before stage 11

These come from development pilots (code/dev/*.py, outputs in results/v1/dev/). They are engineering/method checks,
not paper results. Next run: resolve F1 and F2 (re-opening the stage-9 design for the affected parts), then finish
stage 10.

## F1 — The evaluation particle filter is far from converged at the planned sizes (CRITICAL)
Same 20 episodes (set A, random policy, T = 10), only the PF size changes (results/v1/dev/pilot2_pf_convergence.json):

| N_eval | success | identity acc. | mean IG (evidence) | s / episode |
|---|---|---|---|---|
| 4,000 | 0.50 | 0.55 | 25.6 | 0.20 |
| 40,000 | 0.90 | 0.95 | 12.6 | 1.51 |

Precise contacts (σ_p = 1 mm, σ_n = 5°) make the posterior extremely peaked; a bootstrap PF with random-walk +
prior-independence resample-move cannot find the true mode, so it locks onto wrong identities/poses and the evidence
estimate collapses (IG inflated). Every method's score — and greedy PF-EIG's decisions — depend on this, so no
comparison is meaningful until fixed. Planned N_eval = 10,000 is not enough.

Candidate fixes (to decide next run, then validate against an exact grid posterior on a reduced problem):
1. **Contact-conditioned proposals** (manifold / scaling-series style, cf. koval2015pose, petrovskaya2011global): sample
   (k, perimeter point) and align its outward normal and position with an observed contact; use as an MH independence
   proposal with its density evaluated (mixture over contacts and edges) or as an importance-sampling rejuvenation.
2. **Annealed SMC / tempering** over the history likelihood with more MH moves.
3. **Coarse-to-fine grid** (exact on a 0.5 mm / 0.5° grid is ≈ 2·10⁷ cells × 8 identities — feasible only as a
   reference on a subset of episodes).
Acceptance test for the fix: success / identity / IG change by < 1 pp / < 1 pp / < 0.05 nats from N to 4N (the
pre-registered convergence check), and agreement with the grid reference on a reduced problem.

## F2 — sPCE with prior contrastive samples saturates; total-state information is misaligned with success
Untrained policy, one batch of 128 episodes on set S (rollout timing on the 2-vCPU sandbox):

| L | cap log(L+1) | rollout s / 128 ep | mean g_T (T=3 / 5 / 8 / 10) | fraction within 0.5 nats of cap (T=3 / 5 / 8 / 10) |
|---|---|---|---|---|
| 255 | 5.55 | 0.40 | 5.00 / 5.40 / 5.51 / 5.51 | 0.75 / 0.89 / 0.97 / 0.97 |
| 1023 | 6.93 | 1.61 | 5.40 / 6.12 / 6.86 / 6.93 | 0.42 / 0.64 / 0.93 / 1.00 |
| 4095 | 8.32 | 8.29 | 6.54 / 7.49 / 8.21 / 8.10 | 0.29 / 0.55 / 0.97 / 0.89 |

So the planned L = 255 gives almost no training signal, and the pre-registered rule D1 (saturation < 10 % at T = 10)
cannot be met by any affordable L. Moreover, most of the information is about fine pose, which the success criterion
does not need, while the decision-relevant ambiguity (identity and which symmetric image on set S) is a small part of
it (dev pilot 1, random policy on S: identity accuracy 0.25 / 0.33 / 0.43 at T = 3 / 5 / 10 although measured IG is
large — partly also an F1 artefact).

Options for the design revision (stage 9 re-opened, version stays v1 because no experiment has run yet):
- (a) Keep total-state sPCE with L = 4095 for small budgets only (T ≤ 5, where headroom exists); costs ≈ 65 ms per
  training episode on the sandbox.
- (b) **Decision-relevant (goal-oriented) information objective**: information about z = (identity, symmetry-mode /
  coarse orientation bin) with the continuous pose as a nuisance; bounded by log |Z| so it does not saturate the way
  total-state sPCE does, matches the success criterion, and connects to EC²-style decision-region objectives
  (javdani2012efficient, chen2015submodular) and goal-oriented BED (zhang2025goal, chakraborty2024likelihood). Needs a
  nested estimator of p(h | z) (marginalizing pose), which again needs good inference (F1).
- (c) Contrastive samples from a history-dependent proposal with importance weights (ACE-style bound) — valid but needs
  a good amortized posterior.
Recommendation recorded for the next run: fix F1 first; then prefer (b) if it can be estimated cheaply, else (a);
whichever is chosen, update docs/07_hypotheses.md (as a dated v1.1 amendment, with reasons) and
docs/08_experiment_plan.yaml before any main run, and keep the greedy baseline on the same objective.

## F3 — Costs measured so far
- Greedy PF-EIG full size (N = 2000, C = 64, M = 64): ≈ 0.65 s per decision (planned 0.1 s).
- Evaluation PF: 0.2 s / episode at N = 4k, 1.5 s / episode at N = 40k (T = 10).
- Training rollout: 3 ms / episode at L = 255, 65 ms / episode at L = 4095 (+ PPO update).
