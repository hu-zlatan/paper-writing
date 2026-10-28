# Stage 2 · PROBLEM_DECOMPOSE · v1

## Goal
Decompose the TouchBED topic into ≥4 prioritized sub-questions with risks and mitigations → `docs/01_problem_tree.md`.

## Tasks
- [ ] Fill `stage_prompts/problem_decompose.md` with `{topic}` (RESTRICTS.yaml project.topic) and `{goal_text}` (docs/00_topic_init.md), run it verbatim.
- [ ] Output sections: Source, Sub-questions, Priority Ranking, Risks (each risk with a one-sentence mitigation).
- [ ] Update PROGRESS.md, commit, push.

## Inputs (must exist before starting)
- docs/00_topic_init.md

## Expected outputs
- docs/01_problem_tree.md

## Hard-constraint checks for this stage
- [ ] ≥4 sub-questions, each answerable with an experiment that runs on CPU.
- [ ] Every risk has a mitigation.
- [ ] Sub-questions stay on the stated topic (topic constraint block).

## Notes / risks
Keep it to the two core novelties; secondary questions (SE(3), physics transfer) are lower priority.

---

## Output Summary  (filled in AFTER the stage runs)
- 6 sub-questions (SQ1–SQ6), ranked; 7 risks each with mitigation. SQ1 (non-myopic benefit) and SQ3 (negative information & multimodality) map to the two core novelties; SQ6 (SE(3)) is a stretch goal.
- **Decision:** PROCEED → stage 3.
