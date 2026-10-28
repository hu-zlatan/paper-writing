# Stage 10 · CODE_GENERATION · v2

## Goal
Implement docs/08_experiment_plan_v2.yaml on top of the v1 package (v1 code paths kept for the κ = 0 / v1 reproduction test).

## Tasks (commit each with tests)
- [ ] docs/07c_amendment_v2_0.md (equal stroke time for hits/misses; set-A per-shape confusability rule; fixed self-symmetry computation).
- [ ] touchbed/travel.py — shared 256-action set, cost c(a|φ_t), feasibility mask, budget bookkeeping.
- [ ] touchbed/ball.py — ball membership, ball-EIG on a PF belief, ball-sPCE numerator (J in-ball samples).
- [ ] policies: G* (cost-aware ball greedy), ladder rungs, random/coverage over feasible actions.
- [ ] nn: masked categorical head + gradient check.
- [ ] train_v2.py — travel episodes, ball-sPCE rewards, categorical PPO, γ=1 total vs γ=0 rate-myopic, ablations.
- [ ] evaluate_v2 + main.py v2 subcommands; TOST in stats.py.
- [ ] G0 tests: κ=0 τ=3 reproduction of v1, categorical gradient check, ball-EIG/ball-sPCE toy agreement.
- [ ] Exact notch reference + G1 look-ahead estimator (may move to the next run).
