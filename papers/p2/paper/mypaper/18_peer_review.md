# p2 · Stage 18 PEER_REVIEW [v1] — merged record (run 43, 2026-11-09)

Two independent fresh opus runs of `peer_review.md` (verbatim; prompt `prompts/stage18_{system,user}.txt`) on
`draft_v1.md`. Full reviews: `18_review_run1.md` (A robotics 4, B statistics 5; 43 spot-checks),
`18_review_run2.md` (A RSS tactile 4, B RSS conformal 5; 31 spot-checks). Mean 4.5.

**CRITICAL_FABRICATION: no (both runs).** Both recomputed H2a D = 0.4168 and H2b D = 0.0569 from the raw replays
(run 2 also with an independent CRC loop), the 8 / 800 H1-M count, all trial / instance / draw counts; all statistical
procedures named are in code; CRC code matches the equations; 52 / 52 cite keys in cards. The errors found are
method-description errors, not invented results.

## Verified by the main session (code / raw files)
- Object families: F3 is capsules only (`code/certgrip/sim.py` l.68), F5 boxes (MuJoCo half-sizes → 4–10 mm thick),
  no ellipsoids / disks; μ drawn log-uniform on [0.3, 1.0] independently of every other instance attribute (l.377).
- Report-only rows recomputed by `code/tools_stage19_rows.py` → `results/v1/19_report_rows.json`:
  detector at σ = 0 on the 8,000 id rows: found 100 %, r(log mg/2F_onset, log μ) 0.948, bias +0.319, SD 0.110;
  slip displacement at onset median 0.126 mm, max 1.924 mm, none ≥ 2 mm; logged compute 14.5 CPU-h (CRC 08c 5.72,
  08e 8.03, labels 0.60, mono 0.15); per-stratum test slip (08c): CSF-1 D1 0.1157 (above α), CertGrip-full
  0.071–0.097; λ̂ index 0 for CSF-μ̂@0.2 in D1 / D2 (grid floor also binds at the primary σ); H1-M: the 0.00904 maximum
  comes from the two shift-pool violations (S3, S2 1 / 100 each), id max 0.00225.

## Must-fix for stage 19 (paper-level; no new experiment)
1. Method text = code: families (above); D1 / D2 as inertial pseudo-forces on a still hand; static / squeeze touch
   features noise-free; detector wording ("below 1 mN declares onset").
2. State that μ is independent of every non-tactile input by construction, so the H2a margin is partly a property of
   the instance distribution; narrow C2 accordingly ("when friction is not predictable from non-tactile inputs").
3. H2b at the primary σ 0.2 is also affected by the grid floor (CSF-μ̂ λ̂ index 0 in D1 / D2): §5.2, Limitations,
   Deviation 2 and the Figure 1(c) CSF-μ̂ bar must agree; lead H2b with the label route and the post hoc 08e grids.
4. Compute: replace "2–3 CPU-hours" with the logged 14.5 CPU-h breakdown.
5. Online study: feedback is the label rule 1{F < F\*_hi}; physical audit on one ordering; frozen q̂ breaks in S1 /
   S3 only, not S2; S2 R_E interval lies above 1 — fix abstract, C4, conclusion.
6. H1-M: id max 0.00225; report the 2 shift-pool violations separately.
7. Comparators: D_FID, no-mass D and the H4a chain are vs P, not COMP; report heterogeneity Q = 31.04 (15 df) and the
   weaker D3 cells; add per-stratum test slip.
8. Detector: replace the pilot 0.988 by the main-data 0.948 / bias / SD; σ is added on top of this intrinsic error;
   report found rate and onset displacement (probe cost).
9. "Certified" = marginal guarantee in expectation over calibration draws (per stratum); say so where the word is
   used; "pre-registered" wording: the CRC route was fixed after the H1-M gate failed (08c), before any test read-out.
10. Scope C3 (static touch / squeeze carry no friction information) to the rigid-contact simulator; D-μ argument
    qualified (it ignores noise) or dropped. Small: Table 3 Frozen S2 0.1017 → 0.1016; RE excludes unavoidable
    instances (none in cal / test); H3-S S2 / S1m inconclusive results.

## Evidence-level items (cannot be fixed by writing; for stage 20 / the loop)
- E1 a high-probability (PAC / RCPS / Learn-then-Test) variant on the existing replays;
- E2 a non-tactile baseline with a friction proxy, or a pool where μ correlates with observable attributes;
- E3 grounding σ in a published onset-noise value for a real sensor, or headline as D(σ) (curve exists);
- E4 a reactive slip-tightening baseline (or a justified absence);
- E5 classic grip-force citations (Johansson & Westling; Tremblay & Cutkosky; Romano et al. 2011) — need the
  literature workflow (not in the 52 cards).

**Decision:** no fabrication → stage 19 PAPER_REVISION on items 1–10; E1–E5 go to stage 20, which decides whether
the loop returns to stage 13.
