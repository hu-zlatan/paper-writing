# p2 · Stage 15 RESEARCH_DECISION [v3] (run 46, 2026-11-10)

Prompt: template `research_decision.md` with the REFINE augmentation; `{analysis}` = `results/14_analysis_v3.md`.

## Decision
**PROCEED** → stage 16 [v3] (revise the v2 outline / draft with the v3 rows as secondary evidence). v1 primary
verdicts unchanged (H2a superiority, H2b not confirmed, H1-M failed, H3 inconclusive); v2 statements of record stand.

## Justification
v3 was opened for the v2 gate's evidence-level actions (re-splits, per-stratum tables, Holm, losing sub-pool on CRC,
shrunk plug-in, tuned margin, force in N, reactive baseline, stronger online study). Every registered row was run
except the A7 integrated-force arithmetic (see Next actions). The claim of record since v2 — *a friction-onset probe
plus per-stratum conformal calibration gives the slip guarantee at substantially less excess force than the
friction-blind conformal baseline; the learned model is not the source of the gain* — is confirmed at pool level on
every route and grid, and v3 sharpens it in two honest directions: (i) a shrunk one-line plug-in of the same probe
estimate does as well or better than the learned model (σ 0.4 −0.1395 [−0.1832, −0.01264]); (ii) the saving is not
uniform — inside the 08e μ ∈ [0.5, 0.8] sub-pools CSF-1 is better (−0.3152 [−0.5231, −0.0172]), grid-dependent.
Neither contradicts the scoped claim (both B1 arms use the probe), so not PIVOT. The remaining gaps (hardware σ,
adaptive preload, correlated-μ pool, detection timing) are out of scope for CPU simulation in this loop (10 §C) or
would not change the claim → REFINE (last available cycle) would not buy evidence the paper needs before 12-04.

## Hard rules
- Primary metric difference meaningful: H2a D 0.4168, CI\*\* [0.3484, 0.4778] (v1, 97.5 % object-cluster bootstrap),
  superiority; v3 pool-level rows (CRC, empirical margin, 08e) keep superiority; A3 Holm keeps every v1 verdict. ✔
- Claimed effective components have non-degenerate ablations: probe (CSF-1 vs CSF-μ̂, v2 A3 D 0.3816 [0.2965,
  0.4505]); calibration (v2 B2 fixed margins; v3 A5 empirical margin, A1 re-splits). The learned model is not claimed.
  ✔
- No CRITICAL FABRICATION in stage 14 (pass 2: 15 findings, 3 numeric wording errors, no fabricated number). ✔

## Evidence (from `results/14_analysis_v3.md`)
- B3: D_RE 0.3107–0.4432; late-window slip 0.1001 / 0.1008 / 0.1018 (ordering-only intervals contain α).
- A1: mean re-split slip ≤ α; per-stratum exceedance frequent → the paper states the guarantee is marginal per
  stratum, not per split.
- B2: registered reactive designs slip ≥ 0.3086 everywhere.
- Force: mean hold force 6.521 vs 7.606 N (CertGrip-full vs CSF-1, 08c test split, no interval).

## Next actions
- Before stage 17 uses them: compute A7's registered integrated force (T ∈ {1, 5, 30} s) and break-even T **by a
  script** from `a_analysis.json` (arithmetic only, no new run), or state them as not produced; pass 1's hand
  reconstruction is not citable.
- Stage 16 [v3]: outline update — Limitations add the sub-pool reversal, the shrunk plug-in result, per-stratum
  exceedance, reactive-baseline failure; Results add B3 (3 shifts × 20 orderings) and A3 Holm; keep the scoped claim.
- Stages 17–20 again (RSS 2027 Stage 1 format) by ≈ 11-24; if the stage-20 gate fails again with evidence-level
  weaknesses, the last refine cycle (3 / 3) is available but likely not before 12-04 → then retarget per AUTOPILOT §1.
