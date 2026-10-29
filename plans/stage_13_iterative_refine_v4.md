# Stage 13 ITERATIVE_REFINE · v4 — plan (run 8, 2026-10-29)

## Goal
Run the evidence-level additions required by stage 20 v3, as frozen in `docs/07c_amendment_v4_0.md`.

## Tasks
- [ ] E1 labels S2 (`experiments/v4_label_S2.json`, 60 × 50 episodes) — dispatched run 8.
- [ ] E3 RL S2 (`experiments/v4_rl_S2.json`, seeds 611–613) — dispatched run 8.
- [ ] E5 reduced G\* on S12 test3 0–299 sub 8 (`experiments/v4_e5_rb_test3.json`) — dispatched run 8.
- [ ] E2 round 0: `distill3 --set S --kappa 2 --tau 4.7 --hp 0 --seed 60x --round 0 --fixed-epochs 200` on label shards
  s0000–s1150 + s1500–s2950, val shards s1200–s1450 (sandbox, ≈ 7 min each).
- [ ] E2 DAgger r1/r2 (800 episodes per seed per round; manifests from `v3_d3rem_r1/r2.json` with κ 2, τ 4.7, v4 paths),
  each round re-trained 200 fixed epochs, warm start.
- [ ] E4 val3 0–499 sub 8 (G\*, students) → D4 (`analysis_d3_v3.py` needs a cell argument + δ = 4 pp: add, default
  unchanged); test3 0–299 sub 8 paired rows (G\*, students, RL, B-fan, random); g_T on test3 0–499.
- [ ] Analyses generalised by a `--cell` flag (default S12 = v3 behaviour unchanged; tests).
- [ ] numpy2 check + tests before any code push.

## Not in v4 (stated as limitations)
H3 full-512 / local-offset screen, in-domain positive control, more seeds than 3, wider sweeps.
