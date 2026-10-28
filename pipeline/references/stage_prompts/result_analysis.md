# Stage 14 — RESULT_ANALYSIS  (multi-agent, fresh context)

## Purpose
Quantitatively analyze the experiment results. Crucially, **the LLM must cite real numbers** — this is the first checkpoint that catches fabrication.

## Mode
- LLM: strongest model.
- json_mode: false.
- **Run in a fresh LLM context** (no prior conversation history about this paper) — this prevents the model from "remembering" inflated claims and parroting them back.

## Prompt template

**System:**
```
You are a quantitative ML analyst. Always cite exact numbers from the provided data.
```

**User:**
```
{preamble}


{data_context}


Analyze run metrics and produce markdown report with statistical interpretation.

Use the ACTUAL quantitative values provided above — do NOT invent numbers.

Required sections: Metrics Summary (with real values), Comparative Findings, Statistical Checks, Limitations, Conclusion.

Run context:

{context}
```

## Placeholders

- `{preamble}` — short framing, e.g. "This is iteration v2 after a REFINE loop. Compare against v1 (results/v1/results.json)."
- `{data_context}` — the actual `results.json` content as a code block, optionally with a trimmed CSV summary. **This is what the LLM will cite from — make sure it is complete and unaltered.**
- `{context}` — additional context: hyperparameter table, hardware spec, total wall-clock time, any anomalies noticed during runs.

## Hard rules

- The Metrics Summary section must include at least one number per metric per condition. Round only to a sensible number of significant figures (4 sig figs is typical).
- The Statistical Checks section must say what test was used (paired t-test, Mann-Whitney U, ANOVA, bootstrap CI), include the actual statistic and p-value, and **the test must already be implemented in the code**. If the analyst suggests a test that isn't in the code, that's a signal to either implement it (in stage 13) or drop the claim.
- The Limitations section must be concrete — name specific conditions where the method underperforms, specific dataset features it ignores, etc. Vague limitations are useless.

## Output

`results/14_analysis.md`. This becomes the primary input to stage 15.

## Adversarial second pass (recommended)

After the first analysis, run a second pass with a harshest-reviewer system prompt:

> "You are a top-conference area chair who has rejected 80% of papers you've reviewed this cycle. Read the analysis below. Identify every claim that is not strictly supported by the cited numbers. For each, output the unsupported claim, the contradicting/missing evidence, and a one-sentence rewrite that *is* supported."

Merge the two passes into the final `14_analysis.md`. This is the multi-agent dimension the original pipeline calls for.
