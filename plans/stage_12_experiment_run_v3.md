# Stage 12 · EXPERIMENT_RUN (pre-run gates) · v3  (started run 5, 2026-10-29)

## Goal
Run the v3 gates in dependency order (docs/08_experiment_plan_v3.yaml, docs/11_schedule_v3.json): Cal′ → (E′, G5′) →
Lat′, G2′; G1′ independent; L0 → HP → D3 (+ D3-B, RL sweep). No main run before G0′, Cal′, E′, G5′, Lat′ and D3 pass.

## Tasks
- [x] G0′: unit tests green (55 at commit 75de776; + g2v3/rl additions), TIME_ESTIMATE pilots done.
- [ ] Cal′: n* (experiments/v3_cal.json part 1), τ_12 (part 2, n* = 4 speculative; rerun if n* changes) → status
      note in amendment v3.0 with commit hash; then budget verification (G*, 200 per cell).
- [ ] G1′ (a)(b)(c): experiments/v3_g1.json → analysis script `code/analysis_g1_v3.py`.
- [ ] G5′, E′, round-0 labels S12, HP grid, D3, D3-B, RL sweep, G2′, Lat′ (later runs).

## Output Summary
(filled as gates complete)
