# Stage <N> · <STAGE_NAME> · v<version>

> Write this file *before* running the stage. Fill `Output Summary` *after*.

## Goal
What this stage must produce. One sentence.

## Tasks
- [ ] Task 1 — concrete, checkable.
- [ ] Task 2
- [ ] Task 3

## Inputs (must exist before starting)
- path/to/input1
- path/to/input2

## Expected outputs
- path/to/output1
- path/to/output2

## Hard-constraint checks for this stage
- [ ] Stage's red-line check #1 (e.g. "Mandatory pilot run printed TIME_ESTIMATE")
- [ ] Stage's red-line check #2

## Notes / risks
Anything that might trip this stage up.

---

## Output Summary  (filled in AFTER the stage runs)
What actually happened. What changed from the plan. Decision (if any).

- **Started:** <ISO timestamp>
- **Finished:** <ISO timestamp>
- **Decision:** PROCEED / REFINE → <stage> / PIVOT → <stage>
- **Commit:** <git short SHA>
