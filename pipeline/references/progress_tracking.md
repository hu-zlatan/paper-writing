# Progress Tracking & Planning Discipline

The pipeline is **non-linear** — stage 15 may bounce you back to stage 13 or 8; stage 25 may bounce you back to 13 or 16. Without disciplined progress tracking you cannot tell which version of which artifact is current. This file describes the two artifacts that make resumability and rollback work.

---

## `PROGRESS.md` — the single source of truth

Lives at the project root. Append-only. Every stage writes one entry; every loop writes a version-marker entry.

### Entry format

```markdown
## Stage <N>. <STAGE_NAME>     [v<version>]

- **Started:** <ISO timestamp>
- **Finished:** <ISO timestamp>
- **Inputs used:**
  - docs/01_problem_tree.md
  - docs/05_knowledge_cards.json
- **Outputs produced:**
  - docs/06_synthesis.md (3 clusters, 2 gaps identified)
  - results/06_clustering_evidence.csv
- **Decision (if applicable):** PROCEED  [or REFINE → 13, or PIVOT → 8]
- **Summary:** One paragraph describing what changed and why.
- **Commit:** <git short SHA>
```

### Loop markers

When stage 15 emits REFINE or PIVOT, write a loop-marker entry **before** the next stage starts:

```markdown
## LOOP MARKER — REFINE from stage 15 → stage 13     [version v1 → v2]

- **Reason:** Result analysis flagged baseline tuning insufficient (see results/14_analysis.md, sections "Comparative Findings" and "Limitations").
- **Snapshot taken:** results/v1/, paper/mypaper/v1/
- **Next stage:** 13 ITERATIVE_REFINE
- **Resuming under version:** v2
```

This is what lets you reconstruct, three days later, why you ended up at v3.

### Versioning rule

- **Linear progress** keeps the same version (v1, v1, v1...).
- **Loop entry** (REFINE or PIVOT) bumps the version (v1 → v2). All subsequent stage entries are tagged v2 until the next loop.
- The version on a stage entry tells you which version of the inputs/outputs it used.

---

## `plans/` — per-stage planning files

Lives in `plans/` at the project root. **One markdown file per stage, written *before* the stage executes.**

### File naming
```
plans/stage_01_topic_init.md
plans/stage_02_problem_decompose.md
...
plans/stage_25_rebuttal.md
```

For looped stages, append `_v<N>`:
```
plans/stage_13_iterative_refine_v1.md
plans/stage_13_iterative_refine_v2.md
```

### File template (also in `assets/plan.template.md`)

```markdown
# Stage <N> · <STAGE_NAME> · v<version>

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
```

### Why write the plan before running

- **It pre-commits to checkable success criteria.** If you can't list outputs and constraint checks, you don't yet understand what the stage should do.
- **It catches missing inputs early.** Many stage failures are "the previous stage's output isn't where I expected".
- **It makes loops debuggable.** When you re-enter stage 13 for the third time, you have stage_13_iterative_refine_v3.md sitting next to v2 and v1, showing exactly what changed.

---

## Commit rules

After every stage completes:
```bash
git add -A
git commit -m "stage <N> <NAME>: <one-line summary>"
```

After every loop marker:
```bash
git add -A
git commit -m "loop v<N>: <REFINE|PIVOT> from stage <X> to stage <Y>"
```

**Why this matters:** when stage 20 fails and the user wants to roll back to a prior good state, `git log --oneline` shows you exactly the commit to check out. Without per-stage commits, you cannot.

---

## What "resume" looks like in practice

When the user comes back and says "continue":

1. Read `PROGRESS.md`. Find the most recent stage entry.
2. If the entry's "Finished" timestamp is filled and the decision was PROCEED, the next stage is the linear next.
3. If the most recent entry is a loop marker, the next stage is the loop's target.
4. If the most recent stage entry is missing a "Finished" timestamp, that stage was interrupted — re-read its `plans/stage_<N>_*.md` and resume from there.
5. Read the current version's `plans/` files for that stage to understand what was already attempted.
