# Stage 19 PAPER_REVISION [v4] — plan (run 10, 2026-11-01)

- Snapshot: `paper/mypaper/v4/draft_v4_stage17.md`.
- Template `pipeline/references/stage_prompts/paper_revision.md` verbatim, fresh opus subagent; {topic_constraint}
  (v4 block), {draft} (draft_v4.md), {reviews} = `18_peer_review.md` + both full reviews + a binding instruction/data
  block (M1–M9 fixes; `14_travel_split.json`; PENDING markers for the S2 Cal′ verify, the val3 pipeline check and the
  random anchor). Prompts `paper/mypaper/prompts/stage19_v4_*.txt`.
- Checks: per-section word counts (never shorter than the stage-17 draft per section; limitations not softened), number
  audit, cite keys, PENDING list. If > 30 % words added or major restructuring → second stage-18 pass.
- After the diagnostics finish: fill PENDING markers from JSON (code-produced), re-audit.

## Done (run 10, pass 1)
- Revised `draft_v4.md`: Abstract 249, Intro 1,219, Related 757, Method 2,164, Experiments 1,831, Results 3,052,
  Discussion 805, Limitations 641, Conclusion 289 (every section ≥ stage-17 draft). M1–M9 addressed; BI-first reading
  stated as a revision-time rule (not pre-registered; changes no gate verdict); old C4 moved to methods notes;
  test-split reuse disclosed; post-hoc sensitivity (normal approx., z 1.645 / 0.842) labelled post hoc; Lat′ timings
  of the two E5 configs from `v3:12_lat_analysis.methods` (20.2 / 40.0 ms).
- Checks: number audit — 6 unmatched, all benign (97.5 quantile; z = 0.842; SE = 0.311/1.645 derived); 31 cite keys
  all in cards; PENDING markers: random anchor, S2 Cal′ verify, val3 pipeline check.
- Body grew > 30 % → second stage-18 pass after the PENDING markers are filled.
