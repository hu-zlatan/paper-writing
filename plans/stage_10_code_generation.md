# Stage 10 · CODE_GENERATION · v1

## Goal
A runnable, tested experiment package `code/touchbed/` implementing docs/08_experiment_plan.yaml with real algorithms (ray casting, Bayesian filtering, MC EIG, sPCE, PPO with hand-written backprop), deterministic seeds, time_guard, convergence checks and structured results.json output.

## Tasks (each committed separately, tests first-class)
- [ ] shapes.py — polygon sets A / S / A4 / A16 / positive control, symmetry groups, confusability (shapely IoU).
- [ ] geometry.py — vectorized ray–polygon intersection (hit, contact point, outward normal) for batches of states × actions.
- [ ] likelihood.py — ε-softened observation model: sampling and log-likelihood for many states (one code path for all methods).
- [ ] pf.py — particle filter with ESS-triggered systematic resampling + resample-move (MH on full history); point estimate; IG_T with KDE.
- [ ] policies: random, coverage, greedy PF-EIG (vectorized nested MC).
- [ ] nn.py — numpy MLP / DeepSets with manual backprop + Adam (gradient-checked by finite differences).
- [ ] spce.py + ppo.py — batched episodes with L contrastive samples, sPCE increments, PPO (γ=1 total / γ=0 myopic), plateau rule, time_guard.
- [ ] evaluate.py, stats.py (crossed bootstrap, Holm), main.py with pilot TIME_ESTIMATE and results.json.
- [ ] mujoco_eval.py (can follow in a later commit; needed for H4 only).
- [ ] `pipeline/scripts/check_numpy2_compat.py code/` passes; README; requirements.txt.

## Environment note
PyTorch cannot be installed (download.pytorch.org blocked by the sandbox egress proxy; PyPI torch pulls multi-GB CUDA deps). The network is therefore written in numpy with hand-written backprop, which also matches MEGA_PROMPT's "prefer numpy" rule. Gradients are verified with finite-difference tests.

## Hard-constraint checks
- [ ] No fake metrics / random curves; forbidden calls (subprocess, os.system, eval, exec, network) absent.
- [ ] Real convergence criteria (plateau rule in training; ESS/MH in PF).
- [ ] time_guard in long scripts; pilot TIME_ESTIMATE printed.
- [ ] NumPy 2.x compatibility check passes.

---

## Output Summary  (filled in AFTER the stage runs)
- Package code/touchbed (shapes, geometry, likelihood, pf, policies, nn, train, evaluate, stats) + main.py CLI (pilot / train / eval) + 17 passing tests (analytic ray casts, likelihood normalization, exact two-hypothesis EIG, finite-difference gradients, proposal-density normalization, statistics). NumPy-2 check: 0 errors. No forbidden calls. Real convergence/stop rules: PPO plateau rule + 80 % time guard; PF ESS-triggered resample-move; eval jobs stop at 80 % of their budget with an EARLY_STOP marker.
- Dev pilots found and fixed: PF collapse (contact-conditioned MH proposal), sPCE saturation (L = 4095 by the pre-registered rule), unstable IG metric (ball information) — all recorded in docs/10_dev_findings_v1.md and the dated amendment docs/07c_amendment_v1_1.md. Learning sanity: validation success 0.14 → 0.48 in 3·10⁴ episodes (results/v1/dev/pilot3_learning.md).
- Episode states are now generated per index (stable across shards and n).
- Deferred (documented in code/README.md): MuJoCo fingertip evaluation for H4 — to be written before stage 12 reaches H4; GRU encoder variant dropped (amendment A5).
- GitHub Actions experiment runner: .github/workflows/experiments.yml (manifest-driven matrix, commits results back).
- **Decision:** PROCEED → stage 11.

## Continuation plan (run 2, 2026-10-28 09:45 UTC; must push before 13:49 UTC — next scheduled run)
- [ ] Learning sanity pilot: does PPO on sPCE increments improve validation success at all (S, L=1023, ~20 min)?
- [ ] Decide F2: L=4095 "decision-calibrated" sPCE (cap ≈ −log P(success region) ≈ 8.1 nats) vs goal-oriented objective; write dated amendment docs/07c_amendment_v1_1.md (D1 resolved, D3 ball information, PF proposal, cost re-estimates).
- [ ] stats.py (paired crossed bootstrap, Holm, seed-robustness) + tests.
- [ ] Learned-policy evaluation adapter + main.py CLI (train / eval / pilot with TIME_ESTIMATE, results.json) + shard workflow for GitHub Actions.
- [ ] PF convergence check (N vs 4N) as the first Actions job.
