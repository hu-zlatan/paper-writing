# Stage 19 — PAPER_REVISION  (length-protected)

## Purpose
Apply peer-review feedback to the draft. **Never shorten** — only expand and improve.

## Mode
- LLM: strongest model.
- json_mode: false.
- **max_tokens: 32768.**

## Prompt template

**System:**
```
You are a paper revision expert for NeurIPS/ICML/ICLR submissions. When revising, NEVER shorten existing sections — only expand, improve, and add content. The final paper must be at least as long as the draft.
```

**User:**
```
Revise the paper draft to address all review comments.

CRITICAL: Maintain or INCREASE the paper length. Each section must meet its minimum word count:
Abstract (150-250), Introduction (800-1000), Related Work (600-800), Method (1000-1500),
Experiments (800-1200), Results (600-800), Discussion (400-600), Limitations (200-300), Conclusion (200-300).

Return revised markdown only.

{topic_constraint}Draft:

{draft}


Reviews:

{reviews}
```

## Placeholders

- `{topic_constraint}` — HARD TOPIC CONSTRAINT block from `references/topic_constraint_block.md`.
- `{draft}` — current draft markdown.
- `{reviews}` — full contents of `paper/mypaper/18_peer_review.md`.

## Hard rules

- **Length floor enforcement.** After the revision returns, run a word count per section. If any section is below its floor, **re-prompt** specifically asking to expand that section. Do not proceed to stage 20 with under-length sections.
- **Snapshot before revising.** Save the pre-revision draft to `paper/mypaper/v<N>/` before overwriting. This is what makes rollback safe if revision damages the paper.
- **Don't drop limitations to fit length.** Reviewers value honest limitations. If the revision shortens or softens the limitations section, that's a regression — re-prompt.
- **Numbers stay locked.** The revision must not change any quantitative result unless the experiments were re-run since the draft. Cross-check that revised metric values match `results.json`.

## When to do another peer review

If the revision was substantial (more than 30% added words, or major structural change), loop back to stage 18 for a second review pass. If small/cosmetic, proceed to stage 20.

## Output

Overwrite `paper/mypaper/sections/*.md` (or your `draft_v<N>.md`). Save the pre-revision version to `paper/mypaper/v<previous_N>/`.
