# Dev pilot 0 — baseline smoke test (NOT a result for the paper)

Command: `python code/dev/pilot0_baselines.py` (sandbox, 2 vCPU, 2026-10-28). 6 pilot episodes per set, T = 5,
N_eval = 10,000, N_dec = 2,000, greedy C = 64, M = 64. Output (verbatim):

```
S random succ 0.16666666666666666 id 0.5 ig 8.43 lat_ms 0.02 ep_s 0.36
S coverage succ 0.5 id 0.8333333333333334 ig 11.6 lat_ms 1.15 ep_s 0.41
S greedy succ 0.16666666666666666 id 0.5 ig 13.66 lat_ms 692.28 ep_s 4.02
A random succ 0.5 id 0.5 ig 8.46 lat_ms 0.02 ep_s 0.19
A coverage succ 0.8333333333333334 id 0.8333333333333334 ig 11.06 lat_ms 1.03 ep_s 0.25
A greedy succ 0.6666666666666666 id 0.6666666666666666 ig 21.53 lat_ms 636.3 ep_s 3.47
```

Use: timing only (6 episodes are far too few for any comparison). Greedy full size costs ≈ 0.65 s per decision on
this CPU (the hypotheses doc assumed 0.1 s) → full greedy evaluation ≈ 2 sets × 2000 × 26 decisions × 0.65 s ≈ 19 CPU-h;
must be sharded on GitHub Actions. Evaluation PF ≈ 0.2–0.4 s per episode.

Observation on the IG estimator: the KDE-based IG_T of the hypotheses doc is strongly biased low when the posterior is
broad (prior-only test: median −2.8 nats instead of 0), so the evidence-based estimator
IG = log p(h|s0) − log Ẑ(h) (deviation D3) is now primary. It is biased *high* when particles are sparse relative to
the posterior (E log Ẑ ≤ log Z); the N vs 4N convergence check in the stage-11/12 pilot must quantify this before IG is
used for any claim.
