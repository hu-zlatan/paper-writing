# Stage 9 — EXPERIMENT_DESIGN  [GATE]

## Purpose
Translate hypotheses into a concrete experiment plan: datasets, baselines, proposed methods, ablations, metrics, risks, compute budget.

## Mode
- LLM: strongest model.
- json_mode: false (output is YAML).
- This is a **GATE** — pause for human review before stage 10.

## Prompt template

**System:**
```
You are a principal investigator designing ML experiments.
```

**User:**
```
{preamble}


Design an experiment plan as YAML.

Required keys: objectives, datasets, baselines, proposed_methods, ablations, metrics, risks, compute_budget.

Hypotheses:

{hypotheses}
```

## Placeholders

- `{preamble}` — usually empty for the first pass; on PIVOT loops, include "this is iteration v<N>; previous results showed <summary>".
- `{hypotheses}` — contents of `docs/07_hypotheses.md`.

## Hard rules — read before sending

- **Every "effective component" claimed in `proposed_methods` must have a matching ablation.** This is the only way to satisfy the stage-18 evidence audit. If the LLM omits an ablation, edit the YAML to add it.
- **Baselines must be strong.** For each baseline, include a `tuning_protocol` field describing how it will be tuned (sweep budget, search method). "Used default hyperparameters" is the wrong answer.
- **Metrics must be operationalizable.** Each metric needs a precise formula or a citation to a standard implementation. "Quality score" is too vague; "ROUGE-L F1 (Lin 2004)" is fine.
- **Compute budget must be honest.** Estimate (conditions × seeds × per-condition runtime) before approving. If over the project's wall-clock budget, apply scaling rules from `references/hard_constraints.md` §1.

## Gate

Present the YAML to the user. They can approve or reject. Reject → loop back to stage 8 with the failure reason captured.

## Output

`docs/08_experiment_plan.yaml`.
