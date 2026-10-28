# Stage 8 — HYPOTHESIS_GEN  (multi-agent debate)

## Purpose
Convert the prioritized gaps into ≥2 falsifiable hypotheses with measurable predictions and explicit failure conditions.

## Mode
- LLM: strongest model.
- json_mode: false.
- **Multi-agent debate:** run the prompt 2–3 times with adversarial roles, then merge.

## The debate protocol

The original pipeline calls for "multi-agent debate" at this stage. Here is how to operationalize it:

1. **Run as Proposer** (default system prompt below). Output: candidate hypotheses.
2. **Run as Skeptic** (modified system prompt). Input: the proposer's output. Output: which hypotheses fail to be falsifiable, where the predicted measurements are vague, where the failure conditions are missing.
3. **Run as Methodologist** (third pass). Input: proposer + skeptic. Output: revised hypotheses that survive both — falsifiable, measurable, with explicit failure conditions.

Use the third-pass output as the canonical artifact.

## Prompt templates

### Pass 1 — Proposer

**System:**
```
You formulate testable scientific hypotheses.
```

**User:**
```
Generate at least 2 falsifiable hypotheses from synthesis.

Output markdown and for each hypothesis provide rationale, measurable prediction, failure condition.

Synthesis:

{synthesis}
```

### Pass 2 — Skeptic

**System:**
```
You are a senior scientific skeptic. Your job is to find ways each proposed hypothesis could be UNFALSIFIABLE, vague, or trivially true. You are intentionally harsh — the goal is to make every hypothesis precise.
```

**User:**
```
For each hypothesis below, identify:
- Is the prediction precise enough that a single experiment could confirm or refute it? If not, what specifically is vague?
- Is the failure condition stated quantitatively? If not, what threshold is missing?
- Could the hypothesis be "confirmed" by any of several different mechanisms? If so, what additional measurement would distinguish them?
- Is the hypothesis trivially true (e.g., "more compute helps")? If so, flag for rejection.

Output markdown: per-hypothesis critique, then a verdict (KEEP / REVISE / REJECT).

Hypotheses:

{proposer_output}
```

### Pass 3 — Methodologist

**System:**
```
You are a methodology lead synthesizing a proposer and a skeptic into final, defensible hypotheses.
```

**User:**
```
Produce the final hypothesis set, addressing every critique. For each surviving hypothesis include: rationale, measurable prediction (with concrete metric and threshold), failure condition (with concrete metric and threshold), and the experiment design sketch (datasets / baselines / ablations needed).

Proposer output:
{proposer_output}

Skeptic critique:
{skeptic_output}
```

## Placeholders

- `{synthesis}` — full contents of `docs/06_synthesis.md`.
- `{proposer_output}` — pass 1 output.
- `{skeptic_output}` — pass 2 output.

## Output

`docs/07_hypotheses.md` — the methodologist (pass 3) output.

## Loop target

Stage 15 may PIVOT back here, in which case re-run all three passes informed by the failure analysis.
