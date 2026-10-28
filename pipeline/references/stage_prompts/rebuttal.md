# Stage 25 — REBUTTAL (final decision loop)

## Purpose
Respond, point by point, to the external review from stage 24, and decide whether the paper:
- (a) goes out as-is (with the rebuttal as supplementary author response),
- (b) loops back to stage 13 for more experiments (REFINE), or
- (c) loops back to stage 16 to be re-framed (PIVOT).

This is the **last decision point in the pipeline**. After this stage, the manuscript is either submitted or sent back for another version.

## Mode
- LLM: strongest model.
- json_mode: false.
- max_tokens: 8192.

## Inputs
- `paper/mypaper/main.tex`
- `paper/mypaper/24_external_review.md`
- `results/` (so you can quote actual numbers when defending)
- `docs/05_knowledge_cards.json` (so you can supply real citations when defending)

## Prompt template

**System:**
```
You are the corresponding author preparing the author response to a NeurIPS / ICML / ICLR review. You are scrupulously honest. You concede every point that is correct. You defend, with cited evidence, only the points where the reviewer is mistaken or where the manuscript already addresses the concern but the reviewer missed it.

You never argue from authority ("we believe", "in our experience"). You argue from artifacts: the manuscript, the supplementary, the released code, the numbers in the tables.

When a reviewer point cannot be addressed without new experiments, you say so plainly and propose what would have to be done.
```

**User:**
```
Read the external review (24_external_review.md) and produce a structured author response.

Structure the response as follows:

# Author Response

## Acknowledgement (≤3 sentences)
Thank the reviewer for the specific things they got right. Be specific, not generic. If they identified a real weakness, say so.

## Point-by-point response

For each weakness AND each question raised, in the order the reviewer raised them:

### W1 / Q1 — <reviewer's point, paraphrased in 1 sentence>

- **Status:** one of `CONCEDE`, `CLARIFY`, `DEFEND`, `NEEDS_NEW_EXPERIMENT`.
- **Response:** the response itself, directly addressing the point.
  - For `CONCEDE`: state what change you will make in the camera-ready or revision (e.g., "We will weaken the claim in §3.2 from 'significantly outperforms' to 'consistently outperforms with non-overlapping IQR'").
  - For `CLARIFY`: point to the place in the manuscript that already addresses this (e.g., "§4.3 reports the variance across 5 seeds; we will move this from supplementary to the main text"). If the manuscript does not already address it but easily could, mark this `CONCEDE` instead, not `CLARIFY`.
  - For `DEFEND`: cite the evidence — table, figure, or section — that supports keeping the original claim. Do not defend with rhetoric; defend with artifacts.
  - For `NEEDS_NEW_EXPERIMENT`: state plainly that this would require additional experimentation. List what would be required, what compute budget, and what the expected timeline is.

## Aggregate verdict (filled by the pipeline, not the reviewer)
- **CONCEDE count:** N
- **CLARIFY count:** N
- **DEFEND count:** N
- **NEEDS_NEW_EXPERIMENT count:** N

## Recommended pipeline action

Based on the aggregate verdict and the severity of the weaknesses:

- **PROCEED (submit):** if all weaknesses are CLARIFY or minor CONCEDE (none of them require experimental changes), and the rebuttal can stand as the author response. The manuscript is ready.

- **REFINE → stage 13:** if ≥1 weakness is NEEDS_NEW_EXPERIMENT and the experiment is feasible inside the original compute budget. Loop back to stage 13 (ITERATIVE_REFINE) to add the missing experiment, then re-run stages 14 → 25.

- **REFINE → stage 19:** if ≥1 weakness is CONCEDE and the concession requires substantive rewriting (>1 paragraph, or new figure/table). Loop back to stage 19 (PAPER_REVISION) to apply the rewrites, then re-run stages 20 → 25.

- **PIVOT → stage 16:** if the reviewer's central objection is to the framing of the contribution itself (the paper is positioned wrongly), loop to stage 16 (PAPER_OUTLINE) and re-frame.

- **PIVOT → stage 8:** if the reviewer's central objection is that the underlying hypothesis is wrong or already known, loop all the way back to stage 8 (HYPOTHESIS_GEN). This is severe — flag it loudly in PROGRESS.md and confirm with the user before executing.

State the action explicitly, with the reasoning.
```

## Output

`paper/mypaper/25_rebuttal.md` containing the full structured response above, plus the `Recommended pipeline action` block.

If the action is PROCEED, also produce `paper/mypaper/CAMERA_READY_DIFF.md` listing every change that will be applied to the manuscript before submission (each CONCEDE produces one entry).

## Hard rules

- **DEFEND must cite evidence.** A `DEFEND` entry that argues from rhetoric alone ("we believe our method is sufficient") is not acceptable; either find the supporting artifact and cite it, or change the status to CONCEDE.
- **NEEDS_NEW_EXPERIMENT cannot be silently downgraded.** If the reviewer's question genuinely requires a new run, do not paper over it with a CLARIFY response. Either run the experiment (loop to 13) or concede the limitation in the manuscript (loop to 19).
- **The cycle counter applies.** If the manuscript has already been through stage 25 three times without converging on PROCEED, escalate to the user. The paper may not be ready, or the contribution may not be strong enough for the target venue. Do not loop indefinitely.
- **Camera-ready honesty rule.** Every CONCEDE must produce a corresponding manuscript change. A rebuttal that promises a change but does not later apply it is itself a fabrication — the same severity as a fabricated experiment.

## Loop behaviour summary

```
Stage 25 emits action ──┐
                        ├─→ PROCEED         → submit (pipeline ends)
                        ├─→ REFINE → 13     → re-experiment, then 14..25
                        ├─→ REFINE → 19     → re-write, then 20..25
                        ├─→ PIVOT  → 16     → re-outline, then 17..25
                        └─→ PIVOT  → 8      → re-hypothesise (escalate first)
```

## Why this stage exists

A paper that has not been challenged and successfully defended is not ready for a real reviewer. Stage 25 forces the pipeline to actually argue with the external review from stage 24, in writing, with citations. The output of this stage is two things at once: a deliverable (the author response, which is reused at the actual conference) and a decision (whether the manuscript is done or whether it needs another loop).
