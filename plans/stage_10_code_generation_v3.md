# Stage 10 · CODE_GENERATION · v3  (run 5 start, 2026-10-29)

## Goal
Implement everything amendment v3.0 + v3.1 and docs/08_experiment_plan_v3.yaml need for the gates (G0′ green by 11-05),
following `pipeline/references/stage_prompts/code_generation.md` and `hard_constraints.md` §2 and §5.

## Tasks (each a small, complete, tested commit)
- [x] 1. `TOUCHBED_NPHI` flag in travel.py (32 default, 64 for v3), `rung_subset` relative to N_PHI; tests: 32 × 8
      unchanged (bit-identical arrays), 64 × 8 masks/costs, nested subsets 512 ⊃ 128 ⊃ 32.
- [x] 2. Split salts (cal3 … bank3) + κ-keyed label/DAgger state streams (v3.1 D1); test disjointness.
- [x] 3. `GStar.score_vector()`; test argmax = act on the same RNG state.
- [x] 4. Heuristics B-spread, B-fan, B-cov with budget reservation; determinism tests.
- [x] 5. `distill.py`: soft-label loss (+ gradient check), floored regret, label I/O, DAgger driver.
- [ ] 6. Greedy grid (27 configs) + component timers; timers sum to L_dec test.
- [ ] 7. Belief-summary features (48) for the belief-input student.
- [ ] 8. Travel-notch control (G1′ (c)).
- [ ] 9. Provenance scripts analysis_g3_notch.py, analysis_g3_hp.py (reproduce or diff).
- [ ] 10. main.py subcommands (label / distill / eval3 / latency3 / calib3) + experiments/v3_*.json manifests; TIME_ESTIMATE pilots.
- [ ] numpy2 check (`pipeline/scripts/check_numpy2_compat.py code/`), forbidden-pattern check, full test suite.

## Output Summary
(filled as items land)
