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

## Increment 4a (run 38) — pilot read-out, before any main-pool data
Pilot pool only (salt 3003; main pools untouched). Sandbox, 2026-11-08 ≈ 14:15–14:55 UTC.
- Labels: 4 families × 25 objects × 4 disturbances = 400 instances, paired S1 / S3 (400 each), F5 100
  (`results/pilot/labels/`); monotonicity grids 35 points on 140 instances incl. F5 (`results/pilot/mono/`).
- Read-out `code/pilot_analysis.py` → `results/pilot/pilot_analysis.json`:
  - H1-M pilot look: **0 / 140 non-monotone**. UT8: **0 unavoidable** in every pool; max F\*_hi 19.9 N (ID),
    33.3 N (S1), 26.5 N (S3), 22.5 N (F5) vs F_max 100 N; 0 preload slips; no bracket stuck at F_min.
  - Cross-fitted (5-fold by object, 5-config search — pilot scale, 320 train rows per fold) conformal RE at α 0.10:
    base 1.02, P 1.02, S 0.97, full (CertGrip) 0.94, CSF-1 0.76, oracle 0.39; Mondrian-CSF 2.98 (12 cal objects
    per cell → q̂ near the maximum score; a pilot-size artefact). Label slip ≈ 0.094–0.099 everywhere (as theory says).
  - **Key finding:** the residual of every non-oracle predictor still correlates ≈ −0.79 with log μ (oracle −0.40):
    the static and squeeze touch features carry almost no friction information. A rigidly held object does not
    micro-slip during a 1.5 F0 squeeze, so the squeeze cannot reveal μ. As designed, H2 would most likely come out
    negative for a reason fixed by the protocol, not by the method.
  - η pilot: 0.1 × IQR(scores) = 0.060.
- **Decision (pre-freeze; logged, not hidden):** before freezing, add an **incipient-slip ramp-down probe** (grip
  force lowered from F0 until the first tangential micro-displacement, e.g. 0.3 mm, or a floor, then back to F0 —
  the ramp-down route already budgeted as E5b and the human grip-force strategy) as a protocol step before the force
  ramp, and test in a re-pilot whether it carries μ information. The 1.5 F0 squeeze stays as the PM3 ablation.
  Write the change as `docs/08a_pilot_amendment.md` first (stage-9 design amendment, with the pilot numbers above as
  the reason), then implement it in `sim.py` behind a protocol flag so the current protocol stays reproducible.
  If the ramp-down probe also carries no μ information, keep the original design and report H2 honestly.

## Increment 4b (run 38) — ramp-down probe re-pilot (candidate only, default protocol unchanged)
- `sim.py`: `Sim(..., rampdown=False)`; when on, after the squeeze the force falls log-linearly from F0 to
  RD_FLOOR·F0 over 0.4 s, stops at the first tangential displacement > 0.3 mm or rotation > 1°, returns to F0
  (0.1 s) and holds 0.1 s; slip in steps 3–4 is then measured from the post-probe pose. Default off: the timing digest
  is unchanged (70368455…).
- `pilot_rampdown.py` (D4 instances, 5 families × 25 pilot objects): log(m g / 2 F_onset) vs log μ —
  floor 0.02 F0: corr 0.9995, 27 / 125 onsets not found (light, high-μ objects); floor 0.005 F0: corr 0.999,
  0 / 125 not found, constant offset 0.33 (detection lag), residual SD 0.015 (`results/pilot/pilot_rampdown_floor*.json`).
- **Reading:** in simulation the probe measures μ almost exactly, because the "detector" is the true displacement.
  Adopting it as-is would make the touch gain an artefact of a perfect friction sensor. The amendment (next run) must
  therefore (i) model the robot-observable detector (onset from pad shear/normal ratio or centroid shift, not the true
  displacement) and/or add onset-force noise as a pre-registered sensitivity axis, (ii) re-state H2/H4 and the H3-L /
  D-μ premises (D-μ R² ≤ 0.05 no longer holds for that arm; S1 then becomes partly visible to the predictor), and
  (iii) get a fresh-context skeptic review (stage-8 style) before the freeze. Alternative kept open: no probe change,
  report H2 as designed (pilot D ≈ 0.08 vs the 0.10 target, underpowered pilot).

## Increment 5 (run 39) — amendment 08a implemented; re-pilot under the frozen protocol
- 5a: protocol `"rd"` in `sim.py` (touch-only incipient-slip detector with taxel noise), onset record + ε in
  `features.py`, feature sets `full_rd` / `S_onset` / `P_onset` with σ in `featsets.py`, CSF-μ̂ in `baselines.py`,
  `main.py --protocol`, tests `tests/test_rd_probe.py` (18 / 18 pass). Old protocol default; timing digest unchanged.
- 5b: detector re-tuned on pilot objects 0–24 after attempt 1 (objects 25–124) showed probe-induced unavoidable
  instances above UT8; attempt 1 kept in `results/pilot/rd_attempt1/`, unused. Details in `docs/08a_pilot_amendment.md`.
- 5c: re-pilot on fresh pilot objects 125–224 (`code/repilot_rd.sh`, sandbox): labels ID F1–F4 1,600, F5 400,
  S1 1,600, S3 1,600 → `results/pilot/rd/labels/`; monotonicity 35-point grid on 140 instances → `results/pilot/rd/mono/`.
  Counts only so far: unavoidable 0 in ID / F5, 1 / 3,200 in the shift pools; 0 / 140 non-monotone.
- Predictors (equal 30-config search, 12 arms) are too slow for the sandbox (≈ 600 fits per arm): `main.py pilotoof`
  per arm on Actions (`experiments/p2_pilotoof_rd.json`, 12 jobs), then `python pilot_analysis_rd.py` loads the
  OOF files → `results/pilot/rd/pilot_analysis_rd.json` → write `docs/08b_preregistration.md` (freeze) → stage 12.
