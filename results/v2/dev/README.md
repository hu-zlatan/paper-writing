# results/v2/dev — development pilots (not paper results)

- `learn_v2_sanity_S_k6_tau10.log`: sandbox sanity run of `TrainerV2(setname='S', kappa=6, tau=10, batch=128,
  val_every=2560, val_episodes=128, max_episodes=25600)` (process ends with the session; partial log). Columns: episodes,
  mean training ball-sPCE g_T (sampled actions), validation ball-sPCE of the argmax policy, entropy, probes.
  Observation: the sampled policy's training g_T rises (4.28 → 5.51 nats by 10k episodes) while the argmax policy's
  validation value falls (3.17 → 2.75). Deterministic (argmax) evaluation of a high-entropy categorical policy may
  understate the learned policy early in training; to be checked in G3 with the sampled-policy diagnostic now logged
  (`val_ball_spce_sampled`). Any switch to sampled evaluation must be pre-registered (amendment) before G3 runs.

- Notch-control learner (code/touchbed/train_notch.py) dev check, sandbox, run 3, default PPO settings (lr 3e-4,
  ent 1e-3, batch 128, seed 0, 1e5 episodes, ≈ 25 s): the argmax policy converges to a vertical first probe; exact
  value 0.179 nats vs exact greedy 0.174 and exact optimum 0.615 (29 % of the optimum; the G3 (iii) rule needs ≥ 80 %).
  Not a gate result: G3 (iii) runs with the configuration selected in G3 (i), 3 seeds. Logged here so the gate outcome
  cannot be tuned after the fact.
