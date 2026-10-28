# Stage 15 — RESEARCH_DECISION  (PROCEED / REFINE / PIVOT)

## Purpose
Decide whether the results are strong enough to write a paper, need code/run-level refinement, or require a fundamental hypothesis pivot.

## Mode
- LLM: strongest model.
- json_mode: false.

## Prompt template

**System:**
```
You are a research program lead making go/no-go decisions.
```

**User:**
```
Make a PROCEED or PIVOT decision from analysis.

Output markdown with: Decision, Justification, Evidence, Next Actions.

Analysis:

{analysis}
```

## Placeholders

- `{analysis}` — full contents of `results/14_analysis.md`.

## Augment the prompt with REFINE option

The original prompt's wording says "PROCEED or PIVOT", but the pipeline supports a third option: REFINE (small, targeted re-run without changing the hypothesis). Modify the user prompt to:

```
Make a PROCEED, REFINE, or PIVOT decision from analysis.

- PROCEED: results are strong enough to write the paper. Proceed to stage 16.
- REFINE: hypothesis is correct but the experimental evidence has fixable weaknesses (more seeds, more conditions, an additional ablation, a baseline tuning pass). Stay on the same hypothesis; loop back to stage 13 with specific code changes.
- PIVOT: results contradict the hypothesis or reveal a more interesting question. Loop back to stage 8 with a new hypothesis informed by what was learned.

Output markdown with: Decision, Justification, Evidence (with cited numbers from the analysis), Next Actions (specific stage and tasks).

Analysis:

{analysis}
```

## Hard rules for the decision

- **PROCEED** requires:
  - The primary metric difference between proposed method and best baseline is statistically meaningful (p < 0.05 with appropriate test, OR effect size > 0.5σ across seeds).
  - Every claimed "effective component" has a non-degenerate ablation.
  - No CRITICAL FABRICATION flags from stage 14.
- **REFINE** is the default when results are directionally right but evidence is thin (e.g. only 3 seeds, missing one ablation, baseline obviously under-tuned).
- **PIVOT** is appropriate when the hypothesis is clearly wrong — the proposed method underperforms baselines across the board, or the predicted phenomenon doesn't appear at all.

## Output

`results/15_decision.md`.

## Loop wiring

- **PROCEED** → continue to stage 16.
- **REFINE** → snapshot current results to `results/v<N>/`, write a loop-marker entry in `PROGRESS.md`, increment version, jump to stage 13.
- **PIVOT** → snapshot current state, write a loop-marker entry, increment version, jump to stage 8.
