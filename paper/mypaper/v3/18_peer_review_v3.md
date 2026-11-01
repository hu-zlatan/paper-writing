# Stage 18 PEER_REVIEW [v3] — merged record (run 8, 2026-10-29)

Two independent runs of the stage-18 template (fresh opus subagents; full reviews in `18_review_run1.md`,
`18_review_run2.md`). Four reviewer perspectives in total.

| run | reviewer | score | verdict |
|---|---|---|---|
| 1 | A (methodology) | 4 / 10 | borderline, leaning reject |
| 1 | B (significance) | 3 / 10 | reject |
| 2 | A (significance, RSS/CoRL) | 3 / 10 | reject |
| 2 | B (methodology–evidence) | 4 / 10 | borderline reject |

**CRITICAL_FABRICATION: no** (both runs; 43 spot-checks against code and result files). Trial counts, statistical tests,
hyperparameters and headline numbers match. → no rollback; proceed to stage 19 with the fixes below.

## Factual mismatches (must fix in stage 19)
1. Random-row counts "62 / 199 / 161 of 200" are stale → 162 / 199 / 197 (`12_g5_analysis`, sub 8).
2. "One pinned core" — v3 `latency3` does not pin a core (threads = 1 only). Rewrite.
3. E′ covers S12 **and** A12 (16 episodes), and the counted flip is A12/B-fan — fix the table heading.
4. The latency student is the round-0 checkpoint — say so.
5. `[CONST?]` values exist: PPO clip 0.2, 4 epochs (`results/v3/rl/*.json` config); Python 3.12.15, numpy 2.5.4
   (run headers); runner CPU model is not logged → say "GitHub-hosted standard runners, model not logged".
6. `[PENDING]`: fill G5′ / D3-B with the current (provisional, marked incomplete) values or drop the cells.
7. Student context also contains absolute φ_t (cos, sin) — document.

## Substantive points and triage
| # | point (reviewers) | action |
|---|---|---|
| S1 | Travel barely happens in the tested cell: G\* moves the finger between probes in 21 % of decisions, > 1 grid step in 6 %; mean logged travel 6.1° per episode; students 1.5–2.0°, B-fan 1.5°, RL 23–26°, random 38° (all 4 runs) | **Report** (`14_behaviour.json`) and re-frame: at κ = 12 with τ = 4.9 travel is so costly that the cost-aware planner mostly stays; the learnability findings are for this "stay-and-probe" regime. Title/abstract get the regime qualifier. A travel-binding cell is new design → owner (OWNER_TODO). |
| S2 | Students stop after 4–16 epochs (3–28 s) → under-training? | **Exploratory row run now** (amendment v3.0 status note, readings written first): 200 fixed epochs, same data. |
| S3 | H3 estimator screens 32 of ≤ 512 first actions; checks (a)/(c) share one construction | **Narrow** C1/abstract wording to the screened set; describe (a)/(c) as one construction re-used from v2 plus a zero-gap bank. A full-512 screen → owner/next loop. |
| S4 | Disclose v2 G(12) = 0.0146 (UB 0.0208), known before the v3 threshold | **Report** (results/v2/12_g2_analysis.json); call H3 a replication on the 64 × 8 action set. |
| S5 | g_T vs BI disagree; saturation | **Report** saturation at log(L+1): G\* 5.8 %, students 2.4–3.4 %, RL 0.4–1.2 % on test3 0–499 (exact cap; the reviewer's 15–26 % could not be reproduced with this definition and is not used; the RL trainer's own `sat_frac` on its last training batch is 22.7–31.3 %, a different quantity). RL always uses 3 probes, final entropy 0.002–0.013. |
| S6 | RL sweep thin (4 configs × 1 seed; winner at the lr edge); H2 under-powered | **Limitations** (state edge-of-grid and power ≈ 80 % only at 0.57 nats). Extension → owner. |
| S7 | Reduced-G\* configurations (4–40 ms) are a cheaper baseline; latency ratio vs full G\* overstates amortization value | **Report** as a frontier in words: accuracy of reduced G\* was not measured → state in Limitations; ratio sentence keeps "per decision, vs full G\*". |
| S8 | Both learners tie the stay-and-fan heuristic (B-fan) | **Abstract + Discussion** with pre-written reading (b). |
| S9 | Move gate bookkeeping to an appendix; demote evaluator note from contribution | **Do** in stage 19. |
| S10 | List pre-registered but unexecuted items (Holm, TOST, BC/abs-frame rows, R_b) with routing reason | **Do** (one paragraph). |
| S11 | Teacher tie fraction | **Report**: 0.0 in all 210 logged evaluations. |
| S12 | More cells / seeds; in-domain positive control for H3 | → owner / next loop. |
