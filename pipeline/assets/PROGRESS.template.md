# Project Progress Log

> **This file is the single source of truth for what stage you are at, what version you are on, and what was decided when.**
> Append-only. Every stage writes one entry. Every loop (REFINE / PIVOT) writes a `LOOP MARKER` entry.
> See `references/progress_tracking.md` in the skill for full conventions.

**Project:** <project_name>
**Target venue:** <NeurIPS / ICML / ICLR / etc.>
**Initialised:** <ISO timestamp>
**Current version:** v1
**Latest stage:** (none yet — start at stage 1)

---

## Stage 0. PROJECT_INIT     [v1]

- **Started:** <ISO timestamp>
- **Finished:** <ISO timestamp>
- **Inputs used:** none.
- **Outputs produced:**
  - Project skeleton at `<project_root>/`
  - `RESTRICTS.yaml`
  - `MEGA_PROMPT.md` (if applicable — copied from skill)
- **Decision:** PROCEED → stage 1.
- **Summary:** Project scaffolded; constraints captured.
- **Commit:** <git short SHA>

---

<!--
Append further stage entries below this line, in the format:

## Stage <N>. <STAGE_NAME>     [v<version>]

- **Started:** <ISO timestamp>
- **Finished:** <ISO timestamp>
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
