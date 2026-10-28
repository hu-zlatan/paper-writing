# Project Progress Log

> **This file is the single source of truth for what stage you are at, what version you are on, and what was decided when.**
> Append-only. Every stage writes one entry. Every loop (REFINE / PIVOT) writes a `LOOP MARKER` entry.
> See `pipeline/references/progress_tracking.md` for full conventions, and `AUTOPILOT.md` for how the scheduled runs operate.

**Project:** paper-writing
**Target venue:** TBD — chosen in stage 1 (see AUTOPILOT.md §1)
**Initialised:** 2026-10-28T07:56:44Z
**Current version:** v1
**Latest stage:** Stage 0 PROJECT_INIT — next: stage 1 TOPIC_INIT

---

## Stage 0. PROJECT_INIT     [v1]

- **Started:** 2026-10-28T07:56:44Z
- **Finished:** 2026-10-28T07:56:44Z
- **Inputs used:** the owner's pipeline template (now `pipeline/MEGA_PROMPT.template.md`).
- **Outputs produced:**
  - Project skeleton at the repository root (`code/`, `data/`, `docs/`, `paper/mypaper/`, `plans/`, `results/`)
  - `RESTRICTS.yaml` (project fields filled in stage 1)
  - `AUTOPILOT.md` (run charter), `OWNER_TODO.md`, `AI_USAGE.md`
  - `pipeline/` (stage guide, stage prompt templates, hard constraints, helper scripts)
  - `MEGA_PROMPT.md` is not created yet: stage 1 fills the template's placeholders and saves it.
- **Decision:** PROCEED → stage 1.
- **Summary:** Repository bootstrapped for a scheduled run every 6 hours. Per the owner's directives, Claude chooses the topic (dexterous manipulation, tactile / visuotactile sensing, embodied AI and robot learning) and the target venue in stage 1; compute is CPU-first; gates 5, 9 and 20 auto-approve with logged reasons.
- **Commit:** bootstrap commit (first commit on `main`)

---

<!--
Append further stage entries below this line, in the format:

## Stage <N>. <STAGE_NAME>     [v<version>]

- **Started:** 2026-10-28T07:56:44Z
- **Finished:** 2026-10-28T07:56:44Z
- **Inputs used:**
  - path/to/input1
  - path/to/input2
- **Outputs produced:**
  - path/to/output1 (one-line summary)
  - path/to/output2
- **Decision (if applicable):** PROCEED  [or REFINE → N, or PIVOT → N]
- **Summary:** One paragraph describing what changed and why.
- **Commit:** <git short SHA>

For loop markers (REFINE / PIVOT), use:

## LOOP MARKER — <REFINE|PIVOT> from stage <X> → stage <Y>     [version v<a> → v<b>]

- **Reason:** ...
- **Snapshot taken:** ...
- **Next stage:** <Y> <STAGE_NAME>
- **Resuming under version:** v<b>
-->
