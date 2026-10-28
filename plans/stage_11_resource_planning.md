# Stage 11 · RESOURCE_PLANNING · v1

## Goal
Schedule JSON (tasks, dependencies, CPU estimates, priorities) for all sweeps of docs/08_experiment_plan.yaml + docs/07c_amendment_v1_1.md, based on a mandatory pilot that prints TIME_ESTIMATE on the actual GitHub Actions runners → docs/11_schedule.json.

## Tasks
- [ ] Run experiments/pfcheck_v1.json on Actions: PF convergence check (A/S × T∈{3,10} × random/greedy × N∈{8k,32k}, 300 pilot episodes) + `main.py pilot` TIME_ESTIMATE for S and A.
- [ ] Decide N_eval from the convergence rule (|Δ success| ≤ 1 pp with CI within ±2 pp; |Δ ball info| ≤ 0.05 nats).
- [ ] Apply `stage_prompts/resource_planning.md` → docs/11_schedule.json; apply scaling rules if over budget.

## Hard-constraint checks
- [ ] TIME_ESTIMATE printed by a real pilot before any sweep.
- [ ] Downscale (not silently exceed) if over budget.
