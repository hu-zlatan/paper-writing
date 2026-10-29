# Stage 12 · EXPERIMENT_RUN (pre-run gates) · v3  (started run 5, 2026-10-29)

## Goal
Run the v3 gates in dependency order (docs/08_experiment_plan_v3.yaml, docs/11_schedule_v3.json): Cal′ → (E′, G5′) →
Lat′, G2′; G1′ independent; L0 → HP → D3 (+ D3-B, RL sweep). No main run before G0′, Cal′, E′, G5′, Lat′ and D3 pass.

## Tasks
- [x] G0′: unit tests green (55 at commit 75de776; + g2v3/rl additions), TIME_ESTIMATE pilots done.
- [x] Cal′: S n* 4 / A n* 3; τ S0 4, S12 4.9, A12 3.3; verified S12 3.96, A12 2.98 probes (run 6, status note).
- [x] G1′ (a)(b)(c): all pass (run 6).
- [ ] G5′ S12, S0, A12 (dispatched run 6) → `code/analysis_g5_v3.py` → margins, H★, Flat′ screen, status note.
- [ ] Round-0 labels S12 (dispatched run 6) → HP grid (4 configs, seed 501; train shards 00–11, val 12–14).
- [ ] E′ (regrid3 sub 8 on episodes 0–3 of the first G*/B-fan shards, S12 and A12).
- [ ] G2′ S0/S12 + bias check (dispatched run 6; bias check implemented in run 6 as `touchbed/bias3.py`, 256 full-G*
      rollouts per belief — the pre-registered text gives no sample count); κ = 2 after τ_2 calibration (dispatched).
- [ ] Lat′ (one runner job, interleaved, S12 pilot3, student weights = HP-grid config student; untrained suffices).
- [ ] D3 (DAgger rounds 1–2, seeds 501–503), D3-B, RL sweep (v3.1 D9).
- [ ] 64 × 16 S12 report: needs a ψ-count flag; report-only, deferred.

## Output Summary
(filled as gates complete)
