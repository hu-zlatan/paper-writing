# Stage 18 — PEER_REVIEW  (evidence audit)

## Purpose
Simulate ≥2 reviewer perspectives, with a strict methodology-evidence consistency check. **This is the stage that catches CRITICAL FABRICATION before it reaches reviewers.**

## Mode
- LLM: strongest model.
- json_mode: false.
- **max_tokens: 8192.**
- Recommend: run the prompt twice with different temperature seeds to get genuinely diverse Reviewer A vs B perspectives.

## Prompt template

**System:**
```
You are a balanced conference reviewer who is rigorous about methodology-evidence consistency.
```

**User:**
```
Simulate peer review from at least 2 reviewer perspectives.

Output markdown with Reviewer A and Reviewer B, each including strengths, weaknesses, and actionable revisions.

Check specifically:

1. Does the paper stay on topic ({topic})? Flag any sections where the paper drifts to unrelated topics or presents environment issues as contributions.

2. METHODOLOGY-EVIDENCE CONSISTENCY: Compare the paper's claims about experimental setup (number of trials, statistical tests, hyperparameters, baselines) against the actual experiment evidence provided below. Flag any discrepancies where the paper claims something that is NOT supported by the actual code or results. For example:
- Paper claims N trials but code shows a different number
- Paper claims statistical tests (ANOVA, t-test) but code has none
- Paper reports metrics not present in actual results
- Paper describes methods not implemented in code

3. TRIAL COUNT: The actual number of experiment runs is stated in the evidence below. If the paper claims a DIFFERENT number of trials (e.g., "100 independent trials" when only 1 was run), flag this as a CRITICAL fabrication that MUST be corrected.

4. PAPER LENGTH: This paper targets NeurIPS/ICML submission (9 pages). Check that each section has adequate depth. Flag sections that are too short: Abstract (<150 words), Introduction (<700 words), Related Work (<500 words), Method (<800 words), Experiments (<600 words), Results (<500 words). A paper with fewer than 4000 total words is CRITICALLY under-length.

5. REVIEW LIKE A TOP-CONFERENCE REVIEWER:
- Is the contribution novel, or is it incremental over well-known work?
- Are baselines properly tuned and competitive?
- Are ablation studies present and meaningful?
- Is every claim supported by evidence from the experiments?
- Does the paper acknowledge its limitations honestly?
- Would you recommend this paper be presented at NeurIPS/ICML? Why or why not?
- Score the paper 1-10 following this rubric: 1-3 Reject (fundamental flaws), 4-5 Borderline (significant weaknesses), 6-7 Weak Accept (solid but not exciting), 8-9 Accept (strong contribution), 10 Strong Accept (exceptional).

Paper draft:

{draft}

{experiment_evidence}
```

## Placeholders

- `{topic}` — the research topic.
- `{draft}` — the full markdown draft from stage 17.
- `{experiment_evidence}` — concatenated:
  - `results/results.json` (full)
  - First 200 lines of the longest run log
  - List of statistical tests actually present in `code/` (grep for `scipy.stats.`)
  - Number of distinct condition×seed combinations counted from `results.json`

## Action on CRITICAL FABRICATION

If either reviewer flags a CRITICAL FABRICATION:

1. **Stop**. Do not proceed to stage 19.
2. Identify which kind of fabrication:
   - Number-of-trials mismatch → either (a) loop to stage 13 and run more trials, or (b) revise the paper claim to match the evidence.
   - Missing statistical test → either (a) implement the test in `code/` and re-run, or (b) drop the claim.
   - Hallucinated metric → drop or recompute.
   - Method-not-in-code → either (a) implement and re-run, or (b) drop the claim.
3. Pick option (a) when the contribution depends on the claim; pick (b) when the claim is incidental.
4. Either way, write a loop-marker entry in `PROGRESS.md` and proceed.

## Output

`paper/mypaper/18_peer_review.md`.
