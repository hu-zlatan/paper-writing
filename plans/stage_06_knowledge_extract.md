# Stage 6 · KNOWLEDGE_EXTRACT · v1

## Goal
One evidence card per shortlisted paper → `docs/05_knowledge_cards.json` ({cards:[{card_id,title,cite_key,problem,method,data,metrics,findings,limitations,citation}]}).

## Tasks
- [ ] Run `stage_prompts/knowledge_extract.md` verbatim (mid-tier model via an Agent subagent, json output) on docs/04_shortlist.jsonl, in batches.
- [ ] Cards use only the record's title/abstract/venue metadata; quantitative findings only when the abstract states numbers; "not stated in abstract" otherwise; limitations specific.
- [ ] Validate: every card cite_key ∈ shortlist, titles identical, 56 cards, citation string built from record metadata.

## Inputs
- docs/04_shortlist.jsonl

## Expected outputs
- docs/05_knowledge_cards.json

## Hard-constraint checks
- [ ] cite_key preserved verbatim (script check).
- [ ] No invented numbers: every digit-bearing finding must appear in the abstract (script check).

## Notes / risks
Abstract-level cards are shallow; full-text reading of the ~10 closest papers happens in stage 7 via WebFetch.

---

## Output Summary  (filled in AFTER the stage runs)
- 56 cards written by a fresh sonnet subagent using the stage prompt verbatim; title/cite_key/citation filled programmatically (code/literature/build_cards_v1.py). Validation (re-run by the main session): 56 cards, cite_keys and titles identical to the shortlist, every number in data/metrics/findings appears in the source abstract.
- Gap signals: greedy/one-step touch selection everywhere (Hebert 2013, Javdani 2013, Vien 2015, Murali 2022/2024, Gordon 2026, Zheng 2026); learned tactile policies use task rewards, never information bounds (Riou 2021/2024, Niemann 2024, Fleer 2020, TANDEM3D, TACTFUL, AcTExplore); policy-based BED (DAD, iDAD, RL-BED, RL-DAD, Step-DAD) has no tactile/robot evaluation in its abstracts; no touch-selection paper reports per-decision latency.
- **Decision:** PROCEED → stage 7.
