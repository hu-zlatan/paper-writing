# Stage 11 · RESOURCE_PLANNING · v3  (run 5, 2026-10-29)

## Goal
Schedule with measured per-task CPU estimates → docs/11_schedule_v3.json (template schema, gpu_count 0).

## Tasks
- [x] Mandatory 1-condition pilots first: `main.py pilot3` in S12, S0, A12 on GitHub runners (experiments/v3_pilot.json).
- [x] Replace planning unit costs with measured TIME_ESTIMATE values; keep plan values where nothing is measured yet
      (labelled per task in `estimate_source`).
- [x] Check against the downscale rule (main > 150 CPU-h → frozen downscale order at the freeze commit).

## Output Summary
- docs/11_schedule_v3.json: ≈ 273 CPU-h total (gates ≈ 113, main ≈ 160). G* at κ = 0 costs ≈ 5.5 s per decision on the
  runner (all 512 actions feasible), ≈ 3× the 1.7 s planning value; κ = 12 close to plan. Main exceeds 150 → the
  frozen downscale order will be applied at the freeze commit if the post-calibration re-estimate confirms it.
