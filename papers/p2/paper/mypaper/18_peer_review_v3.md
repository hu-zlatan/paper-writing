# p2 · Stage 18 PEER_REVIEW [v3] — merged record (run 46, 2026-11-10)

Two fresh opus subagents on `paper/mypaper/draft_v3.md` (template verbatim, `prompts/stage18_v3_user.txt`):
- Run 1 (`18_review_v3_run1.md`): A (conformal / statistical ML) 5, B (grasping / tactile) 4 → 4.5 / 10; main numbers,
  CI, frontier, σ curve, seeds, refined grid, strata and quintiles recomputed from raw replays — all match.
- Run 2 (`18_review_v3_run2.md`, RSS pair): A (robotics / tactile) 4, B (conformal / statistics) 5 → 4.5 / 10; ≈ 40
  numbers recomputed with independent scripts, all match within Monte-Carlo error.
- **CRITICAL_FABRICATION: no** (both runs).

## Code-level finding, fixed by the pipeline before revision (both runs, verified in `certgrip/sim.py`)
A7 force-time omitted the probe's return to F₀ over t_up 0.02 s and the 0.1 s re-hold at F₀. `analysis_v3_a.py::a7_force`
now adds them (return_mean 0.3490, rehold_mean 3.27 N·s); A re-run on both grids, every other block byte-identical in
value; `analysis_v3_d.py` → `a7_integrated.json`: shared 31.0448, probe-specific 17.9648 N·s, **break-even 16.557 s
(probe phases) / 28.613 s (all phases)** (were 13.22 / 25.28). The draft must use the new values.

## Paper-level must-fix (stage 19)
1. Force-time: replace 13.22 / 25.28 s and the integrated values everywhere (Fig. 1 prompt / caption, C2, §5.1,
   Table 1, §6, §8) with `a7_integrated.json`.
2. Framing: the only confirmatory result (H2a) is for the **learned** arm; "the saving comes from the probe / the
   plug-in suffices" rests on secondary, post hoc, grid-dependent rows — say so in abstract and contributions; keep
   the conditionality on assumed σ and the iid friction range in the headline.
3. Sub-pool: the primary-grid sub-pool "superiority" coincides with CSF-1 at λ̂ index 0 in D1 / D2 (slip 0.033);
   the refined-grid μ-only reversal (−0.1717) is not explained by slip (CSF-1 slip not higher there). State: the
   method loses where the friction spread is narrow relative to the probe's error (as a reading, not a tested cause).
4. Monotonicity gate statistic: 0.00225 for the 800-instance gate set (`19_report_rows.json`), 0.00904 is over all
   recorded violations incl. shift pools.
5. Report existing rows: mass-noise D 0.4603 [0.4106, 0.5050] (change 0.031 [−0.008, 0.071]); D-FID touch-only family
   accuracy 0.726 (chance 0.25).
6. Label simulator-only ingredients: the shrunk plug-in's OLS uses true μ of selection objects; learned model trains
   on bisection labels.
7. Scope: "certified" = simulation, marginal per stratum, offline bound needs counterfactual replays; the reactive
   controllers are a negative control (start 0.5–0.75 × nominal), not an attribution ablation; friction independent of
   non-tactile inputs makes the friction-blind baseline weak by construction — state in Limitations.
8. CSF-1 primary λ̂ index 1 in D1 / D2 (frontier lower end clipped) — mention in Fig. 1 caption / §5.1.
9. Smaller: online orderings reuse the same instances (identical in S2); data-dependent grid choice; σ_p 0.2 row
   label (−0.0299 is the same-grid value); CP gate level 98.75 % one-sided; unadjusted labels in the abstract.
10. Length: compress (≈ 9,800 words); stage 22 will produce the 5-page RSS Stage-1 version.

## Evidence-level (not to be simulated in text; limitations / future work)
E1 matched-slip versions of the σ 0.4 shrunk row and the sub-pool rows; E2 calibrated-start reactive hybrid; E3
correlated-friction pool; E4 one-outcome-per-grasp calibration; E5 hardware σ; E6 adaptive / low preload.
