# Amendment v3.1 (2026-10-29, run 5 — still before any v3 run or v3 code change)

Closes the gaps N1–N11 that stage 9 v3 (`docs/08_experiment_plan_v3.yaml`, `inconsistencies` key) found in
`docs/07_hypotheses_v3.md` + amendment v3.0, and the RESTRICTS.yaml compute-field conflict. No data of any v3 run
exists yet, so these are pre-registration additions, not post-hoc changes. Amendment v3.0 stays binding except where an
item below explicitly replaces one of its sentences. `docs/08_experiment_plan_v3.yaml` is read together with this file.

## D1 — Episode indices for label and DAgger streams (N1; replaces the index formula in v3.0 C7)
- The stream key of every label/DAgger episode includes the cell: `stream("state", set, split, salt, κ, i)` for splits
  `label3` and `dagger3` (and `stream("phi0", set, split, κ, i)`); evaluation splits (`cal3`, `pilot3`, `val3`, `test3`)
  keep the v3.0 key without κ, so a test episode index denotes the same initial state in S0 and S12 (paired across κ).
- Round 0 (`label3`): indices 0–1,499; held-out validation-regret set = indices 1,200–1,499. D3 remedy adds indices
  1,500–2,999, all used for training; the held-out set is unchanged.
- DAgger (`dagger3`): index = 100,000·r + 1,000·(seed − 500) + j, round r ∈ {1, 2}, j ∈ [0, 800) (400 nominal, 800 under
  the remedy). Ranges are disjoint across rounds, seeds (incl. 521–523, 531–533) and cells (κ in the key).

## D2 — H1c power rule budget (N2)
- The H1c power rule (pilot gap success(G\*) − success(H★) < 12 pp → that cell's H★ test uses all 1,000 episodes) is
  funded from the reserve before any other reserve use, ≤ 16.7 CPU-h. It is decided at the freeze commit from G5′ data.

## D3 — A0 as a fourth cell (N3)
- If A0 is informative at G5′, it enters as a primary cell only if the reserve after D2 covers its main-run cost
  (≈ 40 CPU-h at the §7 unit costs). Otherwise A0 is reported as "informative on pilot; not tested (compute)" and does
  not enter any hypothesis. Decided at the freeze commit, before any test episode.

## D4 — Power rule for cells without D3 data (N4)
- D3 runs only at S12. For S0 and A12 the projected SE_test uses the S12 D3 paired per-episode SD of the success
  difference, scaled by √(p_c(1−p_c) / p_S12(1−p_S12)) with p = G\* pilot success of the cell. Stated as an assumption.

## D5 — Evaluator switch cost (N5)
- If E′ fails (sub = 8), the re-estimated programme cost is computed by TIME_ESTIMATE; if the main estimate exceeds 150
  CPU-h, the frozen downscale order is applied step by step until it is ≤ 150; if the order is exhausted, the reserve
  pays the remainder, then D2, then D3 (A0 stays pilot-only).

## D6 — Soft-label wording (N6)
- No claim that soft labels (β_T) or the argmax term (λ) improve success or BI is made. The HP-grid comparison is
  reported as validation regret of the four configurations only (config 3 changes λ and batch jointly; stated).

## D7 — Arithmetic (N7)
- The never-reduced core is ≈ 117 CPU-h and the main estimate after the full downscale order ≈ 126.6 CPU-h
  (08_experiment_plan_v3.yaml); the "≈ 120" of 07_hypotheses_v3 §7 is a rounded figure and carries no rule.

## D8 — Students in the D3-fail branch (N10)
- If D3 fails after the remedy and H1-fb is active, the H1-fb students are 3 seeds per primary cell trained with the
  remedied recipe: seeds 501–503 (S12: the remedied D3 students themselves) and 501–503 in S0 and A12 (the stream key
  includes κ and set, D1). Their cost (≈ 3 × 2 cells × remedied DAgger + labels) is paid from the H1-fb reserve line.
  If H1-fb is inactive, no new students are trained (fallback row 4).

## D9 — RL comparator tuning (N11; adds a pre-registered sweep)
- To avoid an unequal-tuning confound in H2, RL-relative gets the same sweep budget as the student (4 configurations,
  1 seed, S12): seed 519, E_train = 5 × 10⁴ each, selected on RL's **own** objective (final validation ball-sPCE of the
  argmax policy on 500 `val3` episodes; ties within 0.02 nats → lower index): config 0 = v2 hp1 (lr 3.63e-4, entropy
  1.33e-4, batch 128, critic lr 1.43e-3); 1 = lr × 1/3; 2 = lr × 3; 3 = entropy × 10. The selected config is used for
  seeds 511–513 at E_train = 2 × 10⁵. Cost ≈ 4 CPU-h from the reserve-independent gate budget (D3 window, 11-08 → 11-12).
  This replaces the "v2 hp1, stated as a limitation" sentence of 07_hypotheses_v3 §2.2.

## D10 — RESTRICTS.yaml compute fields (stage 9 conflict)
- `budget_total_hours: 12` is read as **saturated runner wall-clock** for a full sweep, as the v1 plan already did
  (`docs/08_experiment_plan.yaml`, `wall_clock_budget`): ≈ 6.2–7.5 h on ~40 parallel single-thread processes. The CPU-hour
  total (≈ 246–301) is reported as such and is not hidden.
- `budget_per_run_minutes: 30`: every evaluation, labelling, calibration and timing sweep is sharded into processes of
  ≤ 30 min (episodes are independent; shards write partial JSON under `time_guard`). **Declared exception:** RL training
  (≈ 4 CPU-h per run) and student training per DAgger round run as single processes with `time_guard` at 80 % of a
  330-min job budget and save the last checkpoint and a partial result if halted — the same practice as v2
  (`TrainConfigV2.budget_minutes`). These fields are not marked CRITICAL in RESTRICTS.yaml; the owner is told in
  OWNER_TODO.md and may tighten them. `pilot_required` / `pilot_max_minutes` (CRITICAL) are unchanged: every sweep starts
  with a ≤ 5-min TIME_ESTIMATE.
