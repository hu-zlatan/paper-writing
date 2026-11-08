# p2 Stage 11 — RESOURCE_PLANNING (run 39)

Template `pipeline/references/stage_prompts/resource_planning.md` used verbatim (system "You are an experiment
scheduler."; user "Create schedule JSON with GPU/time estimates. Schema: {tasks:[{id, name, depends_on, gpu_count,
estimated_minutes, priority}], total_gpu_budget, generated}. Experiment plan: {exp_plan}") with exp_plan =
`docs/08_experiment_plan.yaml` as amended by `docs/08a_pilot_amendment.md` and frozen in `docs/08b_preregistration.md`.
Mandatory 1-condition pilot: `main.py label --protocol rd` on 5 pilot objects × 4 disturbances in the sandbox →
TIME_ESTIMATE 0.124 s per instance (1 + 10 replays, ≈ 0.010 s each). CPU only (gpu_count 0).
Execution choice: the whole label set is ≈ 1 CPU-h, so it runs in the sandbox (2 processes, time guard 80 % of
--budget-minutes, outputs committed per batch) instead of waiting ≈ 10 h behind paper 1's Actions queue.
Output: `docs/09_schedule.json`.
