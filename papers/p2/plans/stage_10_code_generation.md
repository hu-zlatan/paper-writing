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
