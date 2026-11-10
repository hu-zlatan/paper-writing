# p2 Stage 13 ITERATIVE_REFINE [v3] — plan (run 45, 2026-11-10)

1. Amendment `docs/10_amendment_v3.md` committed before any v3 code / run (done first).
2. A-rows (existing replays, sandbox): `code/analysis_v3_a.py` + a synthetic test; outputs `results/v3/a_*.json`.
3. B1 shrunk plug-in grids + replay manifest (Actions), B3 pilot then manifest, B2 controller code + tests + pilot.
4. `code/tools_results_v3.py` → `results/v3/results_v3.json`; then stages 14–20 [v3].

## Run 46 addition — A3 (Holm as registered), written before running
- Code `code/analysis_v3_c.py`: re-runs the v1 secondary parts that report CI\*\* (08f tail / label; 08g main / h2n;
  08h h1c / h3s / h4b / massnoise) **in memory** with their recorded seeds and draw counts, capturing every bootstrap
  vector passed to `secondaries_08f.ci`; the v1 JSON files are not rewritten.
- Reproduction check: a captured interval is used only if it equals the stored CI\*\* / interval exactly (float
  equality); otherwise the row is listed as "not adjusted" (amendment A3).
- p = min(1, 2 · min(share ≤ 0, share ≥ 0)) against 0 exactly as registered; rows whose own registered threshold is not
  0 (H2-T ratio vs 1.10, H4c margin, oracle share) are flagged `null_not_registered_threshold` in the output.
- Families by 07 §4 label: H1c; H2-x (H2M, H2-T, H2-C, H2-R, H2-H cells, H2-n, mass-noise); H3-x (H3-S); H4-x (H4b,
  H4c, H4d). Rows outside these labels (oracle decomposition) go only into the all-rows sensitivity.
- Output `results/v3/a3_holm.json`. Descriptive multiplicity adjustment; changes no v1 verdict wording by itself.
