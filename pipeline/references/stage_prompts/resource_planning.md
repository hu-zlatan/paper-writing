# Stage 11 — RESOURCE_PLANNING

## Purpose
Build a schedule with GPU/time estimates per task. This is where the time-guard discipline gets formalized.

## Mode
- LLM: mid-tier.
- **json_mode: true.**

## Prompt template

**System:**
```
You are an experiment scheduler.
```

**User:**
```
Create schedule JSON with GPU/time estimates.

Schema: {tasks:[{id, name, depends_on, gpu_count, estimated_minutes, priority}], total_gpu_budget, generated}.

Experiment plan:

{exp_plan}
```

## Placeholders

- `{exp_plan}` — `docs/08_experiment_plan.yaml`.

## Hard rules

- **Run a 1-condition pilot first** (before queuing the full sweep) and replace the LLM's guess with the measured value:
  ```
  TIME_ESTIMATE: <measured_seconds>s per condition
  ```
  Then total_estimated_minutes = ceil(measured_seconds × N_conditions × M_seeds / 60).
- Apply scaling rules from `references/hard_constraints.md` §1 if total exceeds budget:
  - >100 conditions → drop seeds to 3–5.
  - over-budget → cap optimization steps at ≤5,000.
- Pin `total_gpu_budget` from the actual hardware detected in stage 1+. If pure CPU, set `gpu_count: 0` for every task and adjust runtime estimates accordingly.

## Output

`docs/09_schedule.json`. Include the measured pilot timing as a comment field so the source of the estimate is auditable.
