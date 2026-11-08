# p2 Stage 10 · CODE_GENERATION — plan (started run 37, 2026-11-08)

Template `stage_prompts/code_generation.md` (requirements: real algorithms, no fake results, deterministic seeds,
results.json, time_guard, no subprocess/os.system/eval/exec/network). Built in increments, each committed working:

1. **Simulator core + pilot smoke (run 37, done):** `code/certgrip/sim.py` (MuJoCo parallel-jaw grasp, replay at any
   force, log-bisection for F\*, instance sampler from the 07_hypotheses ranges), `code/pilot_smoke.py` →
   `results/pilot/pilot_smoke.json`. Slip metric fixed at the 07_hypotheses assumption (2 mm / 3° / contact loss)
   before the monotonicity look.
2. Features (preload / probe touch statistics, aperture), label generation CLI `main.py label` with time_guard and
   shard outputs (JSONL), runner-image timing + determinism (UT6) via Actions with `workdir: papers/p2/code`.
3. Predictors (GBDT quantile, equal tuning), conformal (CQR, Mondrian strata), OQT, baselines, unit tests UT1–UT9.
4. Pilot (~100 instances): H1-M look, F_max / UT8, score IQR → η, variance inputs → power re-projection → write
   `docs/08b_preregistration.md` (freeze) before any non-pilot data.

Design deviations recorded so far:
- D1/D2 hand motions are applied as the exact inertial pseudo-force −m·a_hand(t) at the object's CoM in the
  non-rotating hand frame (a kinematic mocap hand does not drag the object through MuJoCo's velocity-level friction).
  D1 profile: +a for 0.15 s then −a for 0.15 s. The lift-to-hold phase is a hold in the hand frame (object supported
  by the grasp alone from the start; no table).

## Increment 2 (run 38, 2026-11-08) — done
- `code/certgrip/data.py`: instances as a pure function of (pool, family, object, disturbance, shift); object
  parameters seeded by (salt, family, object), per-instance draws by (…, disturbance) → the 4 instances of an object
  share it; disjoint pool salts (id / s2 / pilot); object-index splits id: 0–199 train, 200–249 selection,
  250–374 cal, 375–499 test; s2: 0–124 oracle, 125–499 stream; paired shifts S1 (μ×0.6), S1m (μ×0.9), S3 (amp×1.5).
  `pilot_smoke.py` keeps its own older sampler (its record stays reproducible).
- `code/certgrip/features.py`: compact per-frame touch statistics (7 per pad: normal / tangential sums, centroid,
  spread, active cells) for the preload frame and all 10 probe frames, plus apertures. touch_grid layout checked:
  channel-first 3 × 8 × 8 per pad, channel 0 normal (sums to F0 = 32.7 N), channel 1 tangential (≈ m g / 2 per pad).
- `code/main.py`: `label` (F_max replay with record + 10 log halvings), `mono` (35-point grid), `timing`
  (fixed pilot set, 3 forces × 2 replays, sha256 digest); JSONL with header, time guard at 80 % of
  `--budget-minutes`, stopping only at object boundaries (`next_index` = object).
- `code/tests/test_data.py` (UT1 splits/salts, determinism, shift pairing, label CLI bracket): 5 passed.
- Sanity (not a result): pilot F4 objects 0–1, D1 F\* = 2.57–2.58 N vs m(g+a)/(2μ) = 2.58 N — Coulomb scaling holds.
- Sandbox timing (`results/pilot/timing_sandbox.json`): median 0.0078 s per replay, 1,440 replays, within-machine
  bit-identical. Runner check `experiments/p2_timing.json` (2 identical jobs) dispatched; UT6 compares the digests.
- **Consequence for the budget:** at ≈ 0.008 s per replay the full simulation budget (≈ 230 k replays) is ≈ 0.5 CPU-h,
  not 64.5; no downscale step is needed.
- Next: increment 3 (predictors, conformal, OQT, baselines, UT2–UT9), then increment 4 (pilot + freeze).

## Increment 3 (run 38) — done
- `certgrip/conformal.py` (q̂ order statistic, Mondrian calibrate, capped decision, OQT with anti-windup, decaying
  variant, UT4 identity/bound bookkeeping); `certgrip/baselines.py` (CSF nominal force; D2 a_cmd = A(2πf)²);
  `certgrip/featsets.py` (base / P / S / full / oracle per the fairness table; no μ, external amplitude, CoM or
  family ID outside the oracle); `certgrip/models.py` (HGB quantile on log F\*_hi, the same 30-config search with
  4-fold object-grouped CV for every input set; RAW-G Gaussian model).
- `sim.py`: slip displacement factored into `tangential_disp` (behaviour-preserving: timing digest unchanged,
  70368455…); `requirements.txt` + scikit-learn 1.9.1.
- `tests/test_conformal.py`: UT2 (exact leave-one-out indexing), UT4 (identity < 1e-8, bound < α), UT7 (compiled
  timestep / cone / integrator / impratio / condim / solref / solimp identical over F1–F5 × D1–D4 × {none, S1, S3}),
  UT9 (3 mm normal → 0, 3 mm tangential → slip), feature shapes. 12 passed in total.
- Not yet: UT3 (needs calibration + test labels, runs at analysis time), UT5 (bracket replays, analysis time),
  UT6 (runner job dispatched), UT8 (pilot).
