# Stage 10 · CODE_GENERATION · v2

## Goal
Implement docs/08_experiment_plan_v2.yaml on top of the v1 package (v1 code paths kept for the κ = 0 / v1 reproduction test).

## Tasks (commit each with tests)
- [x] docs/07c_amendment_v2_0.md (equal stroke time for hits/misses; set-A per-shape confusability rule; fixed self-symmetry computation).
- [x] touchbed/travel.py — shared 256-action set, cost c(a|φ_t), feasibility mask, budget bookkeeping.
- [x] touchbed/ball.py — ball membership, ball-EIG on a PF belief, ball-sPCE numerator (J in-ball samples).
- [x] policies: G* (cost-aware ball greedy), ladder rungs, random/coverage over feasible actions.
- [x] nn: masked categorical head + gradient check.
- [x] train_v2.py — travel episodes, ball-sPCE rewards, categorical PPO, γ=1 total vs γ=0 rate-myopic, ablations.
- [x] evaluate_v2 + main.py v2 subcommands; TOST in stats.py.
- [ ] G0 tests: κ=0 τ=3 reproduction of v1, categorical gradient check, ball-EIG/ball-sPCE toy agreement.
- [ ] Exact notch reference + G1 look-ahead estimator (may move to the next run).

## Progress (run 2, 2026-10-28)
- Done: amendment v2.0; travel.py (256 actions, costs, feasibility); ball.py (ball membership, ball-EIG on PF beliefs, in-ball sampling) with exact two-hypothesis tests; policies_v2.py (random, coverage, G* incl. ladder subsets and full-state variant); evaluate_v2.py (travel episodes, exact-clip prior ball mass, ball information); train_v2.py (masked categorical DeepSets, ball-sPCE rewards with J in-ball samples, PPO γ=1 / γ=0 rate-myopic, full-state and No-NC-input ablations, validation on ball-sPCE, plateau rule, time guard) with gradient checks; main.py train2 / eval2; TOST in stats.py.
- Measured on the sandbox: training ≈ 68 ms per episode at L=4095, κ=6, τ=10 (3.3 probes, untrained g_T 3.98 nats, far from the 8.32 cap); G* ≈ 2.3 s per decision at M=32 (N=2000, 256 candidates).
- Remaining: G0 unit tests (κ=0/τ=3 reproduction of v1, ball-sPCE toy agreement), exact notch reference + G1 look-ahead estimator, rollout planner, τ_κ / n* calibration (G5), latency ladder protocol.
