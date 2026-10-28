# Stage 8.5 — THEORETICAL_BOUNDS

## Purpose
Preliminary mathematical analysis of the proposed approach: convergence guarantees (where applicable), algorithmic complexity (time / space) in big-O, and any informative inequalities or bounds.

This stage is short but high-value — reviewers consistently ask "what's the complexity?" and "is there a convergence guarantee?". Having even a rough answer ready in stage 17 prevents weak reviews.

## Mode
- LLM: strongest model.
- json_mode: false.

## Prompt template

**System:**
```
You are a theoretical computer scientist with a strong applied math background. You produce concise, honest preliminary analysis — never fabricate proofs or guarantees. When the analysis is informal, mark it clearly as such.
```

**User:**
```
For the hypotheses below, produce a preliminary theoretical analysis in markdown.

Required sections:
1. Setup & notation — define the symbols used.
2. Time complexity (per iteration / per call) — big-O in terms of relevant problem dimensions.
3. Space complexity — big-O.
4. Convergence statement (if applicable) — formal statement, assumptions, and a sketch of the argument. If no rigorous proof is possible at this stage, state explicitly: "Informal argument; full proof deferred to appendix / future work" and explain WHY rigor is hard here.
5. Comparison with the closest baseline's known bounds — qualitative if exact bounds aren't published.
6. Honesty section: what assumptions could fail in practice, and what observed behavior would invalidate the bound.

Hypotheses:

{hypotheses}

Method sketch (if available):

{method_sketch}
```

## Placeholders

- `{hypotheses}` — contents of `docs/07_hypotheses.md`.
- `{method_sketch}` — informal description of the proposed method, if already drafted. If not, leave blank and the bounds will be hypothesis-level.

## Hard rules

- **Never fabricate a proof.** If rigor is out of reach, say so explicitly.
- **Always include the comparison with the closest baseline.** Reviewers want to know "is this asymptotically faster, slower, or the same as method X?" — even a qualitative answer is better than silence.
- **Always include the honesty section.** Stating which assumptions could fail in practice is a strong signal of mature scientific writing.

## Output

`docs/07b_theoretical_bounds.md`. This will feed into the Method section of the paper draft.
