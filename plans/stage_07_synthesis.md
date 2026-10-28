# Stage 7 · SYNTHESIS · v1

## Goal
Cluster the 56 cards and state falsifiable gaps, ranked → docs/06_synthesis.md.

## Tasks
- [x] Full-text check of the closest precursor (Zheng et al. 2026) with WebFetch.
- [x] Run `stage_prompts/synthesis.md` with the cards; sections Cluster Overview, Cluster 1..N, Gap 1..N, Prioritized Opportunities.
- [x] Check: every cluster ≥ 3 cite_keys from the cards; every gap falsifiable; ranking by feasibility / novelty / SMART fit.

## Inputs
- docs/05_knowledge_cards.json

## Expected outputs
- docs/06_synthesis.md

## Hard-constraint checks
- [x] Cited keys exist in the cards (script check).

---

## Output Summary  (filled in AFTER the stage runs)
- 7 clusters, 5 falsifiable gaps. Zheng et al. 2026 full text: next touch = max–min distance heuristic on the MAP shape, one-step, no EIG, no timing → information-theoretic non-myopic amortized selection remains open.
- Core novelty #2 reframed: not "use negative information" (prior art) but "a policy trained to plan for no-contact outcomes under multimodal identity×pose beliefs", defended by ablation.
- **Decision:** PROCEED → stage 8.
