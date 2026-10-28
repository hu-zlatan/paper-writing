# TouchBED experiment code

Amortized, non-myopic active tactile localization (docs/00_topic_init.md). Pure numpy/scipy (+ shapely for shape
construction, MuJoCo for the physics check); no deep-learning framework — the policy network and PPO use hand-written
backpropagation (gradient-checked in tests/test_nn.py).

| Module | Content |
|---|---|
| `touchbed/shapes.py` | object libraries A / A4 / A16 / S / PC (procedural, fixed seeds), symmetry groups, confusability |
| `touchbed/geometry.py` | vectorized ray–polygon intersection (probe model) |
| `touchbed/likelihood.py` | ε-softened observation model: sampling and log-likelihood (single code path for all methods) |
| `touchbed/pf.py` | particle filter with resample-move (random walk + contact-conditioned independence MH), estimate, success, ball information, IG diagnostics |
| `touchbed/policies.py` | random, coverage (max–min distance), greedy PF-EIG (nested MC) |
| `touchbed/nn.py` | numpy DeepSets / MLP, backprop, Adam, Gaussian policy utilities |
| `touchbed/train.py` | batched sPCE rollouts (L contrastive samples), PPO with γ = 1 (ours) / γ = 0 (myopic control), No-NC ablations, RL-success baseline, plateau rule, 80 % time guard |
| `touchbed/evaluate.py` | deterministic episode sets and the shared evaluation loop |
| `touchbed/stats.py` | crossed episode × seed bootstrap, Holm, seed robustness |
| `main.py` | CLI: `pilot` (TIME_ESTIMATE), `train`, `eval` |
| `dev/` | development pilots (outputs in results/v1/dev/, not paper results) |

Run tests: `cd code && python -m pytest -q tests`. Install: `pip install -r requirements.txt`.
Sweeps run on GitHub Actions via `.github/workflows/experiments.yml` reading a manifest in `experiments/`.

Not yet implemented (planned for H4): MuJoCo fingertip-contact evaluation (`touchbed/mujoco_eval.py`).
