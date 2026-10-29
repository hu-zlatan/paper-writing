# Amendment v4.0 — REFINE from stage 20 → stage 13 (run 8, 2026-10-29; written before any v4 run)

## Why
Stage 20 QUALITY_GATE (v3) scored 5.5 < 7.5 (`paper/mypaper/v3/20_quality_gate.json`); its required actions 1–6 are
evidence-level, so the decision table of `stage_prompts/quality_gate.md` sends the loop to stage 13. This is refine
cycle 3 of `RESTRICTS.yaml` `max_refine_cycles: 3` (v1→v2, v2→v3 were cycles 1–2): **the last one allowed**. Row 4 of
v3 and all v3 numbers stay as they are (`results/v3/`, `paper/mypaper/v3/`); v4 adds rows, it changes no v3 verdict.

## Core change: a cell where the planner travels
- v3's only learner cell S12 (S, κ = 12, τ = 4.9) is a stay-and-probe regime (G\* mean travel 6.1° per episode on test3).
- **S2 = (set S, κ = 2, τ = 4.7, n\* = 4)**: τ from Cal′ (`12_cal_analysis.tau.S_k2_nstar4`, mean unbudgeted G\* travel
  0.73 strokes). Design pilot (not a paper number): budgeted G\* travels 62° per episode on 6 pilot3 episodes
  (`results/v4/pilot/`). H3 at κ = 2 already exists (v3 G2′).

## v4 runs (frozen here; seeds and sizes fixed before any run)
- **E1 labels.** `label3` S2, indices 0–2,999 (shards of 100); held-out = 1,200–1,499 (as S12).
- **E2 student (budget-matched recipe).** Same head and hp 0 (no new HP grid: deviation, the S12 selection is reused);
  every round trains a **fixed 200 epochs** (`--fixed-epochs 200`, the long-training recipe), DAgger 2 rounds × 800
  episodes (β 0.5 then 0, the remedy sizes), seeds 601–603, round 0 on label3 0–1,199 + 1,500 extra label episodes
  (1,500–2,999) as in the S12 remedy. Last checkpoint kept.
- **E3 RL.** v3 config 2 (lr 1.09e-3, ent 1.33e-4, batch 128, critic lr 1.43e-3), relframe head, seeds 611–613,
  2 × 10⁵ episodes, plateau recorded not used (`--no-plateau-stop`).
- **E4 read-outs.** val3 0–499 sub 8: G\*, students → D4 rule (below). test3 0–299 sub 8 paired: G\*, students, RL,
  B-fan, random. g_T (H2) on test3 0–499 no-grid. Behaviour diagnostics as `14_behaviour`.
- **E5 reduced-G\* at matched protocol (S12, closes gate action 3).** g125_512_16 and g500_512_4 (the two best pilot
  rows of `14_rb_frontier.json`) on test3 0–299 S12 sub 8, paired with the v3 S12 rows; latency of both under the
  Lat′ protocol is out of scope (eval3-logged median only, stated).

## Decision rules (fixed now)
- **D4 (S2 learnability, val3 0–499, sub 8):** the D3 rule unchanged in form, with δ = 4 pp (the S12 cap; G5′ has no S2
  cell): pass iff (i) Δ̂_succ(student − G\*) ≥ max(−2 pp, −δ + 1.645·SE·√0.5), (ii) Δ̂_BI ≥ −0.15 nats, (iii) every seed's
  Δ_succ > −δ. Pass → "in a cell where the cost-aware planner travels, a budget-matched distilled student was within δ of
  G\* on validation (one cell)". Fail → "not shown to reach G\* in S2 either". No remedy round in v4.
- **H2-S2:** as v3 (g_T student − RL, one-sided 95 % LB > +0.10 nats → "distillation scores higher on RL's own
  objective"; else not detected). Reported with the success and BI contrasts on test3 (ci95).
- **E5 reading:** reduced-G\* − student (S12 test3) success/BI ci95, reported; no claim beyond "at its logged latency".
- Exploratory status: E5 and all S2 test rows are reported with ci95, no multiplicity correction; S2 is one cell.

## Compute (estimate, free GitHub runners)
Labels ≈ 16 CPU-h (sandbox test: 19 s per S2 label episode), DAgger ≈ 20, RL ≈ 3 × 1.2, val3 read-out ≈ 22, test3 ≈ 30, E5 ≈ 7 → ≈ 100 CPU-h (≈ 6–8 h wall on
20 runners). Over the 12-h reading of `RESTRICTS.yaml` only if run serially; recorded per the owner's default.

## Order
E1 → E2 round 0 → DAgger r1/r2 → E4 val3 (D4) ; E3 in parallel with E1/E2 ; E5 anytime. Then stages 14 → 15 → 16–20
for the v4 paper (v3 text is the base; S2 rows added).
