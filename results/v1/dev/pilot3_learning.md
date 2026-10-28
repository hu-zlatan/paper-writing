# Dev pilot 3 — does PPO on sPCE increments learn? (NOT a paper result)

Sandbox, 2026-10-28 ~09:47–09:57 UTC. `Trainer(TrainConfig(setname='S', L=1023, batch=128, val_every=3840,
val_episodes=100))`, method spce_total, seed 0; validation = success at T = 5 on 100 fixed validation states with a
1,000-particle PF (contact-conditioned proposals). The process was stopped by the 10-minute shell limit, so the JSON log
was not written; stdout lines (episodes, mean training g_T, val success, val evidence-IG, log-std, elapsed s), verbatim:

```
3840 6.439 0.14 9.28 [-0.49, -0.53] 55
7680 6.512 0.15 9.52 [-0.49, -0.57] 126
11520 6.606 0.18 11.06 [-0.49, -0.6] 199
15360 6.694 0.18 10.76 [-0.49, -0.63] 274
19200 6.528 0.32 11.87 [-0.49, -0.66] 346
23040 6.678 0.41 13.28 [-0.49, -0.69] 419
26880 6.555 0.43 13.19 [-0.49, -0.72] 491
30720 6.599 0.48 11.84 [-0.49, -0.75] 560
```

Use: implementation sanity only — validation success rises from 0.14 to 0.48 within ~3·10⁴ episodes, so the
rollout/PPO/backprop chain produces a learning signal even at L = 1023 (cap 6.93 nats). Cost ≈ 18 ms per training
episode at L = 1023 including validation on this 2-vCPU sandbox. Training g_T moves little because it is near the cap
(F2 in docs/10_dev_findings_v1.md).
