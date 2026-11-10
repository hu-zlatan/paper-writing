# p2 · Stage 15 RESEARCH_DECISION [v2] (run 44, 2026-11-10)

Prompt: template `research_decision.md` with the REFINE augmentation, `{analysis}` = `results/14_analysis_v2.md`.

## Decision
**PROCEED** → stage 16 (revise the v1 outline / draft with the v2 rows as secondary evidence). v1 primary verdicts
unchanged (H2a superiority, H2b not confirmed, H1-M failed, H3 inconclusive).

## Justification
The v2 loop was opened for evidence-level weaknesses named by the v1 gate (stronger baselines, physical feedback
online, a frontier / high-probability certificate). Every registered v2 row has now been run and read; none of them
reverses the v1 picture, and the two that bite (B1 at σ_p 0.2, no learned-model gain) sharpen the claim rather than
call for more runs: the contribution is *a friction-onset probe whose estimate, under conformal calibration, gives a
per-stratum slip guarantee at ≈ 40 % less excess force than the best non-tactile conformal baseline*; the learned
tactile model and touch per se are not the source of the gain, and against a non-tactile friction prior of
log-error 0.2 no advantage is shown (no equivalence test was run; corrected in stage 16 per the binding audit). That is a scoped, honest measurement claim, not a hypothesis that failed across the board → not
PIVOT. The remaining gaps (hardware σ grounding, reactive controller, correlated-μ pool) cannot be closed with
CPU simulation in this loop or are out of scope (09 §C) → REFINE would not buy evidence the paper needs; they stay
limitations.

## Hard rules
- Primary metric difference meaningful: H2a D 0.4168, CI\*\* [0.3484, 0.4778] (v1, object-cluster bootstrap,
  97.5 %), superiority; v2 routes: matched slip 0.4563 / 0.4475, LTT 0.4043 / 0.4015 (08c / 08e), all superiority. ✔
- Every claimed effective component has a non-degenerate ablation: the claimed component is the onset probe +
  calibration. Probe: CSF-1 (no probe) vs CSF-μ̂ (probe only) A3 D 0.3816 [0.2965, 0.4505]; calibration: B2 fixed
  margins (per-stratum slip 0.0228–0.6571 at m 1.0). The learned model is *not* claimed as effective (H2b). ✔
- No CRITICAL FABRICATION flag in stage 14 (pass 2: 1 truncation-by-0.0001 finding, corrected). ✔

## Evidence (from `results/14_analysis_v2.md`)
- H5: D(CertGrip vs CSF-proxy) 0.8361 at σ_p 0.8, 0.5042 [0.4362, 0.5635] at 0.4, −0.0299 [−0.1903, 0.0816] at 0.2
  (edge-rule row of record) → not shown at 0.2.
- B3 (descriptive, 5 orderings): physical-feedback tracker window slip 0.0936–0.1052 under S1 / S3; D_RE 0.4115–0.4438.
- LTT certificate: CertGrip test slip 0.0696, still superior to CSF-1.

## Next actions
- Stage 16 [v2]: update the outline — title / abstract / contributions say "friction-onset probe + conformal
  calibration"; add the frontier (A1), LTT (A2), H5 (B1), B2, B3 rows as secondary; Limitations add "a friction
  prior of comparable quality (σ_p 0.2) does as well".
- Stages 17–20 again (RSS 2027 Stage 1 format, ≤ 5 pages + references); target draft by ≈ 11-22.
