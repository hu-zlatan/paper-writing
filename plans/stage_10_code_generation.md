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
