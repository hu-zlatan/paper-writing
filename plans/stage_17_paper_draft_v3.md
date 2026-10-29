# Stage 17 PAPER_DRAFT [v3] — plan (run 8, 2026-10-29)

## Goal
Full markdown draft of the row-4 characterisation paper from `paper/mypaper/sections/00_outline.md`, every number
traceable to `results/v3/results_v3.json`.

## Preconditions (stage 15 v3 conditions)
- [x] (1) Exploratory B-fan test3 row complete (300/300) → reading (b); "flat" clause not supported (amendment v3.0
  status note, commit c004577).
- [x] (2) Companion rows in the JSON.
- [ ] (3) G5′ sub-8 (463 episodes left, run 98) and D3-B (2 episodes left) still running. Both are report-only; the
  draft marks their rows `[PENDING:<key>]` and stage 19 fills them from the final JSON. No claim depends on them.
- [x] Missing citations: cards C57–C60 added (DAgger, PPO, Choudhury 2017, Nguyen 2024 arXiv-only).

## Length decision (deviation, recorded)
- Template floors are for a 9-page NeurIPS-style paper (5,000–6,500 words). The venue default is RSS 2027 (Stage 1
  extended abstract ≤ 5 content pages; Stage 2 full paper ≤ 8 pages). `RESTRICTS.yaml` writing floors (total ≥ 4,000;
  intro 700, related 500, method 800, experiments 600, results 500) are the binding floors for this repo; they target
  the 8-page Stage 2 paper.
- Decision: the stage-17 master draft meets the RESTRICTS floors (≈ 4,200–5,000 words). The 5-page extended abstract
  is produced in stage 22 as a separate condensed export (`paper/mypaper/rss_stage1/`), so stage 19's "never shorten"
  rule still applies to the master draft. The outline's ≈ 3,450-word targets are scaled up proportionally.

## Execution
- Fresh-context opus subagent (strongest model), template `pipeline/references/stage_prompts/paper_draft.md` verbatim
  with placeholders: {preamble} (venue + length decision above + row-4 framing), {topic_constraint} (block from
  `pipeline/references/topic_constraint_block.md` with the stage-16 topic string), {exp_metrics_instruction}
  (`results/v3/results_v3.json` in full), {citation_instruction} (cite_keys + titles from cards), {outline}.
- Figure 1 prompt first → `paper/mypaper/figures/figure1_prompt.txt`.
- Output: `paper/mypaper/sections/draft_v3.md`.

## Checks (main session, after the subagent)
- [ ] Number audit: every decimal number in the draft found in results_v3.json (after rounding) or in the frozen
  design docs as a design constant; script `code/tools_number_audit.py`.
- [ ] Every \cite key exists in the cards.
- [ ] Word counts vs RESTRICTS floors.
- [ ] Never-write list of the outline respected.
