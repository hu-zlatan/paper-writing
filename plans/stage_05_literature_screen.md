# Stage 5 · LITERATURE_SCREEN [GATE] · v1

## Goal
Strict relevance + quality screen of docs/03_candidates.jsonl → docs/04_shortlist.jsonl (≥30 entries, target 45–70), every original field preserved, with relevance_score, quality_score, keep_reason.

## Tasks
- [ ] Deterministic pre-filter (`code/literature/screen.py prefilter`): year ≥ 2018 (except strategy "seminal"), drop records without abstract and without DOI/arXiv/OpenAlex ID, keyword relevance score to rank.
- [ ] Apply `stage_prompts/literature_screen.md` verbatim (topic, domains, threshold 0.6 for relevance×quality... see notes) to the ranked pre-filtered candidates: the session model reads titles + abstracts and assigns relevance_score, quality_score, keep_reason (`docs/04_screen_decisions.json`), rejecting off-topic papers aggressively.
- [ ] `screen.py merge` joins decisions with the original records (fields preserved verbatim) → docs/04_shortlist.jsonl; check cite_key/doi/arxiv_id unchanged.
- [ ] GATE (auto-approve per AUTOPILOT §1): record count, coverage per theme, reasons in PROGRESS.md.

## Inputs
- docs/03_candidates.jsonl

## Expected outputs
- docs/04_screen_decisions.json, docs/04_shortlist.jsonl

## Hard-constraint checks
- [ ] ≥30 shortlist entries, else loop to stage 3.
- [ ] Original identifiers preserved (script assertion).
- [ ] Year filter applied (seminal exceptions listed explicitly).

## Notes / risks
Keep threshold: relevance ≥ 0.6 and quality ≥ 0.5 (combined ≥ 0.35). Adjacent-but-unrelated (e.g. generic BED in biology, tactile sensor hardware) only kept when they support a specific claim.

---

## Output Summary  (filled in AFTER the stage runs)
- Pre-filter: 681 → 622 (year ≥ 2018 or seminal, has ID and abstract), ranked by a transparent keyword score (docs/04_prefiltered.tsv); top ~330 read by title/abstract/venue.
- Screening decisions in code/literature/screen_decisions_v1.py → docs/04_screen_decisions.json; merged with original records (all fields verbatim, merge asserts identical titles) → docs/04_shortlist.jsonl: **56 papers** (49 with relevance ≥ 0.6; 7 context-only citations at 0.55 flagged). 7 seminal pre-2018 exceptions listed explicitly.
- Coverage: direct active-touch localization/recognition 22, touch-based pose estimation/filtering 14, Bayesian experimental design 12, adaptive-submodularity theory 2, surveys/application context 6.
- **Key finding for stage 7/8:** Zheng et al. 2026 (arXiv:2603.21410) already combine contact and free-space (no-contact) evidence for joint class+pose belief with greedy next-touch selection, and Koval et al. 2015 model contact/no-contact in a manifold particle filter. Using negative information is therefore NOT novel by itself; novelty must rest on the amortized non-myopic policy (and on how it exploits negative information / multimodality). Lim et al. 2022 (RL-DAD, cite_key vincent2022policy — key generated from an "Last, First" author string; kept immutable) already apply RL policy-based BED to non-differentiable simulators, so the contribution is the tactile formulation + evidence, not the BED algorithm.
- **GATE (auto-approved per AUTOPILOT §1):** count 56 ≥ 30, every theme of the search plan represented, all identifiers verifiable (OpenAlex/DOI/arXiv), no off-topic entries (human-touch neuroscience, touch-screen and whisker biology papers rejected). 
- **Decision:** PROCEED → stage 6.
