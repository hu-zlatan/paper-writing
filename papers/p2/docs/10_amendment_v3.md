# p2 · Amendment v3 (REFINE loop from stage 20 → stage 13) — written 2026-11-10 (run 45), before any v3 code or run

Trigger: stage-20 gate `paper/mypaper/20_quality_gate_v2.json` 5.5 / 10 < 7.5 with evidence-level required actions,
and the stage-18 pass-2 record `paper/mypaper/18_peer_review_v2_pass2.md` (E1–E8). Refine cycles used 1 → 2 of 3.
All v1 / v2 numbers and verdicts stay as they are; v3 adds rows, it does not re-decide earlier hypotheses. Every row
below is **secondary** unless stated. Nothing below has been computed when this file is committed.

Common to all v3 rows (as in 09): id pool, the v1 cal / test split unless a row says otherwise, the 08c per-stratum
CRC (α 0.10; 08c grids, 08e refined grids as the sensitivity row), physical binary slip from direct replay,
RE = mean (F − F\*_mid) / F\*_mid on avoidable test rows, CI\*\* = 97.5 % object-cluster bootstrap with λ̂ refitted on
every draw (2,000 draws, seed 2026), decision labels superiority / inferiority / not shown. Outputs to `results/v3/`.

## A. Analyses of the existing v1 / v2 replays (no new simulation)
A1 **Repeated object re-splits (empirical certificate check).** R = 200 random re-splits of the 4,800 id cal + test
   instances by object, stratified by stratum, with the v1 sizes (500 cal / 700 test per stratum), seed 3031. Each
   split refits the per-stratum CRC λ̂ (and the LTT λ̂, δ 0.10) on its cal part and records test physical slip overall
   and per stratum. Arms: CertGrip-full σ 0.2 seed 0, CSF-μ̂ σ 0.2, CSF-1 (08c and 08e grids). Report: mean slip, the
   share of splits with test slip > α (overall; per stratum), the 90 % quantile; for LTT the share of splits with any
   stratum's test slip > α. Expectation (stated before running): CRC mean slip ≤ α; per-split slip above α in a
   minority of splits. Descriptive; no decision.
A2 **Slip tables.** For every 08c / 08e / 09 arm: test physical slip and RE per stratum, per family × stratum cell and
   per friction quintile (quintiles of true μ on the test rows), primary and refined grids; per-seed rows for
   CertGrip-full σ 0.2 seeds 0–4. Descriptive.
A3 **Holm as registered.** 07 §4 registers Holm at 5 % within each secondary family (H1c / H2-x / H3-x / H4-x); 08f–08h
   dropped it. For every v1 secondary row with a CI\*\* in `results/v1/results_v1.json`, a two-sided bootstrap p-value
   p = min(1, 2 · min(share of draws ≤ 0, share ≥ 0)) is computed from its stored or re-drawn bootstrap (same seed and
   recipe), then Holm within each 07 family. Sensitivity: Holm over all v1 + v2 secondary rows together. Rows whose
   bootstrap draws are not stored are re-drawn with the recorded recipe; if one cannot be reproduced exactly at its
   point estimate, it is listed as not adjusted.
A4 **Losing sub-pool on the CRC route (H2-R on CRC).** 08g H2-R sub-pool (μ ∈ [0.5, 0.8] and mid-half amplitude) and
   the two restrictions separately (μ only; amplitude only). Per-stratum CRC recalibrated inside each sub-pool from the
   existing 08c grid replays; D(CertGrip-full σ 0.2 vs CSF-1) and D(CSF-μ̂ σ 0.2 vs CSF-1) with CI\*\*, arm-level RE and
   slip. No prediction.
A5 **Empirically tuned per-stratum margin (tactile baseline without the conformal correction).** On the CSF-μ̂ σ 0.2
   and CertGrip-full σ 0.2 grid replays: per stratum, λ̂_emp = the smallest grid λ whose calibration physical slip ≤ α
   (plain empirical risk, no (n+1) correction). Report test slip and RE, and D vs CSF-1 with CI\*\*. Purpose: what the
   finite-sample correction costs and whether a hand-tuned margin already holds α out of sample.
A6 **Direct learned vs plug-in contrasts.** D(CertGrip-full σ 0.2 vs CSF-μ̂ σ 0.2) at matched slip (09 A1 recipe,
   interpolation inside each draw) and under LTT (09 A2 recipe), CI\*\*, both grids.
A7 **Force in newtons.** Per arm (CRC primary grid): mean and median absolute hold force F and excess F − F\*_mid in N on
   avoidable test rows; distribution (quantiles 10 / 50 / 90 / max) of F\*_mid over test rows; share of test rows with
   F\*_mid above the preload 32.7 N and above the squeeze peak; the protocol force profile (preload, squeeze, probe,
   hold) as constants from the design docs. Integrated force over a hold of T seconds = protocol phases + F·T, reported
   for T ∈ {1, 5, 30} s with the break-even T at which the saving exceeds the probe's extra force-time. Descriptive.

## B. New arms (new replays on the same instances; code + tests committed before any replay)
B1 **Shrunk plug-in (tests the paper's untested "shrinkage" reading).** log μ̂_s = a + b · log μ̂ with (a, b) the OLS fit
   of log μ on log μ̂ over the **selection split** only, per σ ∈ {0.2, 0.4}; force = CSF-μ̂ formula with μ̂_s; grid by the
   08c recipe on the selection split (08e recipe if λ̂ lands on index 0 or 19, reported). Read-out:
   D(CertGrip-full σ vs shrunk plug-in σ) with CI\*\*, σ ∈ {0.2, 0.4}. Prediction (stated before running): at σ 0.4 the
   learned arm's advantage over the plug-in shrinks, and its CI\*\* includes 0 (i.e. shrinkage explains it).
B2 **Reactive slip-tightening controller (tactile competitor).** After the same preload, the grip is lowered to
   F₀ = c · (CSF-1 nominal force), c ∈ {0.5, 0.75}; during the hold the same touch-only onset detector (σ 0.2) watches
   for slip; on each detection the force steps up by 25 %, at most 4 steps; no probe. Physical slip = the v1 slip
   criterion over the whole hold (so slip before tightening counts). Report test slip, RE of the final force, mean
   number of steps, per stratum. Descriptive; also as a CRC arm (λ on log c, 08c recipe) if the pilot shows ≤ 2 CPU-h.
B3 **Online study with physical feedback, stronger.** As 09 B3 but S1, S2 and S3, orderings 0–19, windows 1–500,
   501–1,000 (transient) and last 500; ordering-bootstrap 95 % intervals (2,000 draws) of window slip and RE; oracle
   reference recalibrated on the post-shift pool as in 08d (reported with its own slip). Pilot rule: if the pilot
   projects > 8 CPU-h, downscale orderings 0–9 → S2 dropped (stated).

## C. Not done in v3, with reasons (stay as limitations)
- σ grounding on hardware: impossible here. A literature search for published onset / incipient-slip detection error
  of real tactile sensors (via the repo's literature route) is reported as context only and does not choose a σ.
- Adaptive / low preload: changes the probe protocol and therefore every label; out of scope for this loop.
- A pool with friction correlated with non-tactile inputs: needs new labels and a new COMP selection; deferred.

## Compute (estimate, before any pilot)
A: minutes (bootstrap-heavy A1: 200 splits × 3 arms × 2 grids, no replays). B1: 2 arms × 4,800 × 20 replays ≈ 0.8
CPU-h. B2: 2 × 4,800 closed-loop replays, pilot-timed. B3: ≤ 8 CPU-h by its pilot rule. Total ≲ 12 CPU-h on GitHub
Actions / the sandbox. Order: A (sandbox) → B1 → B3 → B2.
