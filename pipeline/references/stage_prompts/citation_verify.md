# Stage 23 — CITATION_VERIFY (relevance audit per citation)

## Purpose
Walk through every reference in the manuscript and prove — for each one — that the cited paper genuinely supports the claim that points to it. This is the stage that catches **the second most common rejection cause: irrelevant or hallucinated citations** (the first being fabricated experiments, caught at stage 18).

A reviewer who finds even one citation that does not say what the paper claims it says will assume the rest of the bibliography is similarly sloppy. One bad citation poisons the whole reference list.

## Mode
- LLM: strongest model.
- json_mode: false (markdown report).
- max_tokens: 8192.
- Run **once per ~20 references**; chunk if the reference list is large.

## Inputs
- `paper/mypaper/main.tex` (or `paper/mypaper/main.md`)
- `paper/mypaper/references.bib`
- `docs/05_knowledge_cards.json` (the original literature snapshot — gives ground truth for what each cited paper actually said)
- The HARD TOPIC CONSTRAINT block from `references/topic_constraint_block.md`

## Procedure

For every `\cite{key}` (or markdown `[@key]`) in the manuscript:

1. **Locate the citing sentence.** Quote it verbatim, with the surrounding 1–2 sentences for context.
2. **Locate the cited paper's record** in `knowledge_cards.json` (or fall back to the bib entry's title + abstract if the knowledge card is missing — flag this as a yellow warning).
3. **Classify the citation's role:**
   - `support_claim` — paper is used as evidence for a factual or empirical claim.
   - `support_method` — paper is the source of a method/technique being used or extended.
   - `position` — paper is part of related work / positioning the contribution.
   - `contrast` — paper is cited to disagree with or differentiate from.
4. **Audit the match** against three traffic-light flags:

### 🟢 Green flag — keep as-is
The cited paper's actual contribution clearly supports the role assigned to it. Example: paper claims "Transformer architectures dominate NLP benchmarks [Vaswani2017]" and Vaswani 2017 is indeed the Transformer paper.

### 🟡 Yellow flag — rewrite the citing sentence
The cited paper is *related* but does not specifically say what the citing sentence implies. Example: paper writes "prior work has shown method X is brittle under distribution shift [Smith2020]" but Smith 2020 only studied method X under adversarial perturbation, not distribution shift. The citation is in the right neighbourhood but the claim overshoots the evidence.

### 🔴 Red flag — REMOVE or REPLACE
The cited paper is irrelevant, the cite_key resolves to a different paper than the one quoted in the bib, or the paper does not exist (hallucinated). Examples:
- A 2019 paper is cited for a result that paper does not contain.
- The cite_key `kingma2014adam` is used but the bib entry's title points to a paper about variational inference.
- The paper appears to be made up — no DOI, no arXiv ID, the title returns no hits when searched.

## Output

`paper/mypaper/23_citation_audit.md` with this structure:

```markdown
# Citation Audit — v<N>

Total citations checked: <NN>
- 🟢 Green (keep): <NN>
- 🟡 Yellow (rewrite sentence): <NN>
- 🔴 Red (remove/replace): <NN>

## Per-citation findings

### [cite_key_1] — 🟢 GREEN
- **Citing sentence:** "..."
- **Role:** support_method
- **Cited paper's actual contribution:** ...
- **Verdict:** match.

### [cite_key_2] — 🟡 YELLOW
- **Citing sentence:** "..."
- **Role:** support_claim
- **Cited paper's actual contribution:** ...
- **Mismatch:** the citing sentence claims X; the paper only shows Y.
- **Suggested rewrite:** "..."

### [cite_key_3] — 🔴 RED
- **Citing sentence:** "..."
- **Role:** support_claim
- **Cited paper's actual contribution:** N/A — paper does not exist / contains no such result.
- **Action:** REMOVE the citation; the underlying claim must either be removed or supported by a different paper.
- **Suggested replacement search:** keywords to find a real paper that does support the claim.

## Summary actions
1. Apply all yellow rewrites to main.tex.
2. Either remove the claims behind every red citation, or replace them with a green-class citation found via the suggested searches.
3. After applying changes, re-run this stage on the updated manuscript.
```

## Hard rules

- **No paper passes stage 23 with any 🔴 red flag still open.** The pipeline must loop back to stage 19 (PAPER_REVISION) to either remove the offending claim or supply a real source.
- **Hallucinated citation = critical failure.** Same severity as a fabricated experiment: log it, flag it loudly in PROGRESS.md, and do not advance to stage 24 until cleared.
- The "knowledge_cards.json" check is non-negotiable. If a cite_key has no corresponding knowledge card, that citation is at minimum 🟡 yellow until you re-fetch the paper and confirm what it actually says.
- Do not invent DOIs or arXiv IDs to "rescue" a citation. If you cannot verify the paper exists, mark it 🔴 red.

## Loop behaviour

If the audit returns ≥1 🟡 yellow OR ≥1 🔴 red:
- The pipeline loops back to stage 19 (PAPER_REVISION) under the same version.
- After revision, re-run stage 23 on the new manuscript.
- Only when the audit is all-green does the pipeline advance to stage 24.

## Why this stage exists

Real submissions get desk-rejected for citation hygiene. A reviewer's reaction to a single fabricated reference is not "interesting mistake" — it is "the authors did not read what they cited, so I cannot trust anything else they claim." This stage exists to make sure that reaction never happens.
