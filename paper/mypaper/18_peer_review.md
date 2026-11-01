# Stage 18 PEER_REVIEW [v4] — merged record (run 10, 2026-11-01)

Draft: `paper/mypaper/sections/draft_v4.md`. Template verbatim (prompts `paper/mypaper/prompts/stage18_v4_*`), two
fresh opus subagents; run 2 as a strict RSS/CoRL pair. Full reviews: `18_review_v4_run1.md`, `18_review_v4_run2.md`.
v3 record: `v3/18_peer_review_v3.md`.

## Verdict
- Scores: run 1 A 4 / B 3; run 2 A 4 / B 3 (v3: 4/3, 3/4). **CRITICAL_FABRICATION: no** in both runs (> 100 numbers,
  all trial/episode/seed counts, the crossed bootstrap B = 10,000, the D3/D3-B/D4 thresholds, H2-S2 and E5 recomputed
  from raw per-episode files; Holm/TOST correctly described as not run).
- → stage 19 (no rollback). All mismatches are incidental text errors → option (b) (fix the claim).

## Mismatches (fix in stage 19)
| id | location | issue | fix |
|---|---|---|---|
| M1 | §3.1 | "K = 8 … base/variant pairs" — code has 4 bases + 4 variants | "K = 8 identities (4 base/variant pairs)" |
| M2 | Table 2 R1, §1, §3.1 | S2 Cal′ reported "pass"; no S_k2 verify run exists (only S_k12, A_k12) | state τ set by the Cal′ rule, probe-count verification not run (or run it); test3 G\* 3.873 probes reported as observation |
| M3 | §4, §7, Table 5, Fig. 1D | random anchor "215 of 300" stale; follow-up running | fill from final JSON |
| M4 | Table 4, §5.2, Fig. 1B | travel definition omitted; logged travel includes the initial snap onto the 5.625° grid (≈ 1.4° for every policy) | define travel; add discretionary travel (computed from logs by code) |
| M5 | Table 1 | "batch 256" is decisions-equivalent (256 // T episodes per step) | state it |
| M6 | §5.3, §7 | S2 val3 scored inline (`eval3`), S2 test3 by `regrid3` re-read — not named as a candidate cause of the val/test gap | name it; run a pipeline check if cheap |
| M7 | §5.4 | "2.9 half-widths (0.293)": lower half-width is 0.303 → ratio 2.8 | use 0.303 / 2.8 |
| M8 | Table 2 R6, §5.4 | "H2 is rejected" overstates; should be "not detected" (same term as H2-S2) | reword |
| M9 | draft | Figure 1 generation prompt inside the manuscript | keep only in `figures/figure1_prompt.txt` (LaTeX comment in stage 22) |

## Triage of substantive asks
Refine cycles are exhausted (3 of 3), so no new pre-registered experiment. Classified as:
- **Text / analysis of existing logs (stage 19):** M1–M9; BI as the primary metric where success contrasts are within
  the 7.5 % flip rate; consolidate hedging into Limitations; demote C4 (instrument notes) from the contribution list;
  post-hoc minimum detectable effect for H2/D4 from the observed SE (labelled post hoc); test-split reuse disclosed.
- **Cheap report-only diagnostics (allowed by `results/v4/15_decision.md`, ≤ 4 CPU-h):** S_k2 Cal′ verification
  (probe count at τ = 4.7); val3 subset re-read through the test pipeline (M6). Added if they finish before stage 20;
  otherwise listed as not run.
- **Out of scope for this cycle (Limitations / future work):** 512-action or structured two-step H3 screen, V_LA
  selection-bias re-estimate, S2 B-spread/B-cov and an S2 H★, S2 student/RL sweeps, probe-count-constrained RL,
  belief-input capacity fix, regret on student-visited states, sub-16 evaluator check, more cells/seeds, held-out
  shapes, 3D/contact dynamics, hardware.

---

# Second pass (stage 19 pass-1 revision grew the body > 30 %) — run 10

Prompt `paper/mypaper/prompts/stage18_v4_pass2_user.txt` (revised draft, current `results_v4.json`), two fresh opus
reviewers: `18_review_v4_pass2_run1.md`, `18_review_v4_pass2_run2.md`. Scores 4/3 and 4/3; **CRITICAL_FABRICATION: no**
in both (all counts, the bootstrap, H2-S2, D4, the S2 Cal′ 3.875 probes and S2 travel reproduced from raw files).

## Mismatches (fix in stage 19 pass 2)
| id | location | issue | fix |
|---|---|---|---|
| P1 | Abstract, §6, §8 | g_T-vs-grid ordering stated "in both cells"; S12 is marginal (G\* 5.299 vs 5.368; 3 of 6 seeds below G\*; BI ci95 includes 0) | state for S2; S12 marginal |
| P2 | §1 | 79.3 % zero moves attributed to test3 0–299; it is 0–499 (0–299: 80.9 %, `14_review2_checks`) | fix range / number |
| P3 | §5.3 | "≈ 2.0 combined SE" not labelled derived | label |
| P4 | §4, §5.4, Abstract | post-hoc 7.5 pp "BI first" rule: flip rate is per-episode, not a contrast bound; applied unevenly (S12 G\* − RL +7.0 pp); S2 student − B-fan +8.1 pp clears it by 0.6 pp | drop the numeric threshold; lead with BI everywhere and mark every success contrast with its CI; abstract calls +8.1 pp exploratory |
| P5 | §4, Tables 2/5, §7 | random anchor PENDING | fill from final JSON |
| P6 | §1 vs §5.6 | 0.16–0.23 vs 0.16–0.27 nats | say which comparison |
| P7 | §5.2 | random travels "most" in first leg (S2 52 %) | fix |
| P8 | §5.3, §6, §7 | S2 students over-fit: held-out R̄ lowest at epochs 22–130, rises 0.007–0.026 to the kept epoch-200 checkpoint, train loss still falling (`14_review2_checks`) | report; the fixed-200-epoch recipe (pre-registered) keeps the last checkpoint |
| P9 | Abstract, §8 | E5 cell not named | "in S12" |
| P10 | §4, Table 2 R2 | the one counted E′ flip came from set A (A12 B-fan) | state |
| P11 | §5.4 | "cap saturation is rare" counts exact-cap only; RL end-of-training 23–31 % within 0.5 nats of the cap | qualify, cite `v3:14_behaviour.rl_final` |
| P12 | Abstract, §1 | 4.3° / 44.8° come from a report-only post-review analysis | label |
| P13 | §4 | D-gate SE·√0.5 ≈ 88 % one-sided, G\* run once per episode | explain (pre-registered formula, unchanged) |
| P14 | §4 | H3 0.03 threshold registered with a near-identical estimate known | already labelled; keep |
