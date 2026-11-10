# p2 · Amendment v4 (third and last REFINE loop, stage 20 → stage 13) — written 2026-11-10 (run 46), before any v4 code or run

Trigger: stage-20 gate `paper/mypaper/20_quality_gate_v3.json` 6.8 / 10 < 7.5 (v2 5.5, v1 6.5) with evidence-level
required actions 1–4, and the stage-18 v3 pass-2 record E1–E7. Refine cycles used 2 → 3 of 3 (the last one; no
further loop without an owner decision). All v1–v3 numbers and verdicts stay as they are. Nothing below has been
computed when this file is committed. Purpose: turn the exploratory attribution ("the saving comes from the probe;
probe + plug-in + CRC suffices") into a **pre-registered confirmatory test on fresh objects**, and test whether the
saving survives outside the independent-friction design.

## Common definitions (fixed now)
- **Fresh pool `f4`** (salt 4004): the id-pool object generator unchanged (log-uniform μ on [0.3, 1.0], independent of
  every non-tactile input), families F1–F4, objects 0–299 per family: 0–124 cal, 125–299 test (v1 sizes, 125 / 175);
  4 disturbances each → 4,800 instances. No object of `f4` has been simulated before.
- **Correlated pool `c4`** (salt 5005): as `f4` but μ log-uniform inside a family band — F1 [0.30, 0.45],
  F2 [0.40, 0.60], F3 [0.55, 0.80], F4 [0.70, 1.00] (overall range unchanged, friction now predictable from the
  visible family / material class); objects 0–49 selection, 50–174 cal, 175–349 test per family → 5,600 instances.
- **Protocol** `rd` (08a) for every arm, plus protocol `noprobe` (new, C6 only): preload F₀ 0.4 s, then directly the
  ramp to the hold force; no squeeze, no ramp-down, no return / re-hold. Default code paths must reproduce v1 exactly
  (test before any run).
- **Arms** (no model is re-trained; the v1 seed-0 fits and the v3 OLS are frozen): learned `full_rd@σ#0` and plug-in
  `CSF-muhat@σ` at σ ∈ {0.1, 0.2, 0.4}; shrunk plug-in `CSF-shrunk@0.2` with the frozen v3 OLS (a −0.38579,
  b 0.73973); `CSF-1`; on `c4` additionally **`CSF-fam`**: the CSF-1 formula with μ̄ replaced by the geometric-mean
  μ of the family's `c4` selection objects (a deployable non-tactile prior: the class is visible, friction is not
  touched).
- **Wide pre-specified grid (W):** per arm and per disturbance stratum, centre = the 08c pooled label-rule quantile
  at α 0.10 computed on the id-pool selection rows (`c4`: its own selection rows; `CSF-fam` only on `c4`), ±1.6 in
  log force, **81 points** (step 0.04 as 08e). No other grid is used for any v4 decision. If λ̂ of any arm lands on
  index 0 or 80 in any stratum, that arm's decision row is reported as "grid floor / ceiling — not interpretable"
  (no extension, no re-grid).
- **Statistics** as v1: per-stratum CRC on the monotonised physical binary slip loss, α 0.10; RE on avoidable test
  rows; D(a vs b) = 1 − RE(a) / RE(b); CI\*\* = 97.5 % object-cluster bootstrap within family, λ̂ refitted per draw,
  2,000 draws, seed 2027. **Matched slip** = the 09 A1 recipe on W: shift every stratum's λ̂ index by k ∈ −8…+8,
  interpolate each arm's RE at test slip 0.10 inside each draw.
- Bootstrap p (A3 formula) p = min(1, 2 · min(share ≤ 0, share ≥ 0)) of the draws of D (for TOST: of D − 0.10 and
  D + 0.10, one-sided).

## Confirmatory decisions (Holm at 5 % over C1–C5; everything else secondary / descriptive)
- **C1 (probe sufficiency, `f4`, σ 0.2):** D(CSF-muhat@0.2 vs CSF-1) at matched slip. Superiority iff Holm-adjusted
  p < 0.05 and the point is > 0. Prediction (stated now): superiority.
- **C2 (learner adds nothing, `f4`, σ 0.2):** D(full_rd@0.2#0 vs CSF-muhat@0.2) at matched slip. Equivalence iff both
  TOST one-sided p at ±0.10 (SESOI of 07) pass Holm. Prediction: equivalence. Superiority / inferiority reported if
  the CI\*\* excludes 0.
- **C3 (H2a replication, `f4`):** D(full_rd@0.2#0 vs CSF-1) on the CRC route (not matched). Superiority as C1.
  Prediction: superiority.
- **C4 (deployable prior, `c4`, σ 0.2):** D(CSF-muhat@0.2 vs CSF-fam) at matched slip. Superiority as C1. No
  prediction (the gate asked whether D survives a friction-informative prior).
- **C5 (learned vs deployable prior, `c4`):** D(full_rd@0.2#0 vs CSF-fam) at matched slip. As C4.

## Secondary / descriptive rows
- S1 σ band on `f4`: C1 / C2 / C3 at σ 0.1 and 0.4 (CI\*\*, no adjustment) — the σ curve is reported as the result,
  not a single point. S2 shrunk plug-in vs plug-in and vs CSF-1 at σ 0.2, matched slip. S3 **friction-width sweep**
  on `f4` cal + test: nested centred windows of log μ of relative width w ∈ {1.0, 0.75, 0.5, 0.25} (centre log of
  the geometric mean of [0.3, 1.0]); CRC recalibrated inside each window; D(CSF-muhat@0.2 vs CSF-1) and D(full vs CSF-1)
  at matched slip with CI\*\*. Prediction: D shrinks with w (the v3 sign flip on μ ∈ [0.5, 0.8] suggests D ≤ 0 near
  w 0.25). S4 per-family D on `c4`. S5 CRC-route (unmatched) versions of C1, C2, C4, C5. S6 **no-probe CSF-1 grasp**
  on `f4` (protocol noprobe, grid W centred as CSF-1): λ̂, test slip, mean hold force and integrated force-time over
  T ∈ {1, 5, 30} s (preload + ramp + hold, from the replay's commanded profile); **measured break-even** of
  full_rd@0.2#0 and CSF-muhat@0.2 (rd protocol, all phases) against it. S7 A1-style 200 re-splits of `f4` for the
  learned and plug-in arms (descriptive certificate check).
- REACT-probe is not re-run (its design flaw is recorded); a corrected reactive design needs a new detector
  calibration and is left as a limitation.

## Not done (limitations): hardware σ (no hardware; the σ band replaces a point), adaptive / low preload (changes
every label), replay-free one-outcome-per-grasp calibration (new method), reproduction of published controllers.

## Compute (estimate before any pilot)
Labels (bisection + probe records) `f4` 4,800 + `c4` 5,600 instances; W replays: `f4` 8 arms × 81, `c4` 4 arms × 81,
noprobe 1 arm × 81 → ≈ 1.6 CPU-h per arm per 4,800 instances at the v3 per-replay cost ⇒ ≈ 25–30 CPU-h, on GitHub
Actions. Pilot rule: a 2-object-per-family timing pilot before dispatch; if the projection exceeds 60 CPU-h, drop
σ 0.1 (S1) first, then S7. Order: code + tests → pilot → labels → grids (selection-only) → replays → read-out code
committed before the first replay result → read-out.

## Timeline
Stages 13–14 by ≈ 11-15, 15–20 by ≈ 11-24; if the gate fails again the paper goes to the owner (no further loop).
