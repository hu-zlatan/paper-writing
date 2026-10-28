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

---

## Output Summary
- Pilot TIME_ESTIMATE on Actions runners (results/v1/logs/pilot_{S,A}.log): training 28.7 / 56.1 ms per episode at L=4095 (S / A) → 0.8–1.6 CPU-h per 1e5-episode run; greedy evaluation 3.7–5.4 s per T=5 episode (≈ 21–31 CPU-h for the full test grid); random 0.4–0.7 s.
- docs/11_schedule.json: 10 tasks (T0–T9), CPU only, ≈ 150–200 CPU-h total on ~20 concurrent Actions jobs; scaling decisions recorded (seeds 6 for core, 3–5 for non-core, 1e5-episode cap).
- PF convergence check (T0) results are analysed in stage 12 (they decide N_eval).
- **Decision:** PROCEED → stage 12.
