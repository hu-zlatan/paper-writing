# Stage 24 — THIRD_PARTY_REVIEW (fresh-context external reviewer)

## Purpose
A new LLM session, given **only the final paper**, plays the role of the harshest plausible reviewer. The session has no context from the rest of the pipeline — no prior drafts, no design rationale, no progress log. This isolation is deliberate: it simulates what an actual conference reviewer sees.

If the paper cannot stand on its own when handed to a stranger, it cannot stand at NeurIPS / ICML / ICLR.

## Mode
- LLM: strongest model.
- json_mode: false.
- max_tokens: 8192.
- **Run in a fresh conversation / fresh context window.** Do not include any prior pipeline artifacts in the prompt other than the paper itself.

## Inputs (and ONLY these inputs)
- `paper/mypaper/main.tex` (full final manuscript)
- `paper/mypaper/figures/` (referenced where the manuscript references them)

Do **not** pass: knowledge_cards, hypotheses, code, raw results, prior reviews, the original prompt, or PROGRESS.md. The point is the paper standing alone.

## Prompt template

**System:**
```
You are a senior area chair at NeurIPS / ICML / ICLR. You have served on the program committee for 8 consecutive years and chaired one of the conferences. You have rejected approximately 80% of papers you have reviewed in the past three years. You believe most submitted papers are not yet ready and that the field benefits from raising the bar, not lowering it.

You read papers cold. You do not give the authors the benefit of the doubt on missing detail. If the paper does not say it clearly in the manuscript, it does not count.

Your reviews are direct, evidence-based, and unsentimental. You explain rejections in terms that authors can act on. You do not pad weaknesses with false positives, and you do not pad strengths to seem fair.
```

**User:**
```
Review the attached paper as a top-tier ML conference reviewer. Use the standard form:

# Summary
2–3 sentences. What did the paper claim, and what did it actually show?

# Strengths
List only genuine strengths. Be specific — cite section/figure/table numbers. If you cannot identify ≥1 specific strength, say so plainly.

# Weaknesses
Hardest section. Address each of the following explicitly:

1. **Novelty.** What does the paper contribute beyond prior work? Is this contribution non-trivial, or is it a known technique on a new dataset / a small modification to an existing method?

2. **Soundness.** Are the experimental claims supported by the evidence? Look for:
   - Single-run results presented as if they were aggregated.
   - Missing baselines that any informed reviewer would expect.
   - Statistical claims (p < 0.05, "significantly") without the test reported.
   - Trial counts, hyperparameter ranges, or compute budgets that look implausibly small.
   - Tables/figures where numbers don't add up or contradict the text.

3. **Clarity.** Could a competent grad student reproduce the work from this paper alone? What is missing?

4. **Significance.** Why should the community care? Is the problem important, the result surprising, or the method generalizable?

5. **Limitations and honesty.** Does the paper acknowledge its own limits? Or does it overclaim?

6. **Related work coverage.** Are there obvious omissions a domain expert would flag immediately?

# Questions for the authors
3–6 sharp, specific questions. Each must be one a reviewer would actually ask in a rebuttal — not generic ("could you elaborate on X"), but pointed ("Table 2 reports 87.3% on CIFAR-10 with no error bars; what was the variance across the 5 seeds you mention in §4.1?").

# Confidence
1 (educated guess) – 5 (absolutely certain).

# Recommendation
One of: **Strong Accept / Accept / Weak Accept / Borderline / Weak Reject / Reject / Strong Reject.**
Be honest. Most papers, even good ones, are not Accept-class on first pass.

# Suggested decision rationale
2–4 sentences telling the area chair why your recommendation is what it is. This is the single most important paragraph; the AC will read it before reading the rest.
```

## Hard rules

- **No leakage from the rest of the pipeline.** The model must not have seen the design doc, the hypothesis, the code, or the raw results. If you find yourself wanting to "remind" it of context, that is the bias you are trying to escape.
- **No flattery passes.** A review that recommends Strong Accept on a first-attempt paper is almost certainly broken — re-run with a fresh context. Top-tier first-pass papers are rare.
- **Adversarial seed sweep encouraged.** Run the prompt twice with two different temperatures (e.g., 0.3 and 0.7). If the two reviews disagree on recommendation by more than one band, flag this and run a third tiebreaker.

## Output

`paper/mypaper/24_external_review.md` with this structure:

```markdown
# External Review — v<N>

## Reviewer 1 (temperature=0.3)
<full review form filled in>

## Reviewer 2 (temperature=0.7)
<full review form filled in>

## Tiebreaker (if needed)
<full review form filled in>

## Aggregate signal
- Average recommendation band: <e.g., "Borderline / Weak Reject">
- Most consistent weakness across reviewers: <one paragraph>
- Most consistent strength across reviewers: <one paragraph>
- **Decision route:**
  - If all reviewers gave ≥ Weak Accept → proceed to stage 25 (REBUTTAL).
  - If majority Borderline-or-below → loop back to stage 19 (PAPER_REVISION) addressing the most consistent weakness; re-run stage 24.
  - If reviewers unanimously Reject or Strong Reject → escalate to PIVOT decision (loop back to stage 16 PAPER_OUTLINE or, if the issue is empirical, stage 13 ITERATIVE_REFINE).
```

## Loop behaviour

| Aggregate signal | Action |
|---|---|
| All ≥ Weak Accept | Advance to stage 25. |
| Mixed / majority Borderline | Loop to stage 19; revise; re-run stage 24. |
| Unanimous Reject / Strong Reject | Loop to stage 16 (re-outline) or stage 13 (re-experiment) per the most consistent weakness. Bump version. |
| ≥3 such cycles without improvement | Escalate to user: the paper may not be ready, or the contribution may not be strong enough. Do **not** keep looping silently. |

## Why this stage exists

Self-review is contaminated by the work that produced the paper. Even a careful pipeline will defend its own choices. The purpose of stage 24 is to break that defence by handing the paper to a reader who has no investment in any of the choices made along the way. If the paper is good, it survives that test. If it isn't, far better to find out here than at the actual conference.
