# Stage 1 · TOPIC_INIT — paper 2 (CertGrip)

Prompt template: `pipeline/references/stage_prompts/topic_init.md` (system "You are a rigorous research planner.";
user: "Create a SMART research goal in markdown." with Topic / Domains / Project / Quality threshold filled below).

- **Topic:** Distribution-free risk control for minimal-force tactile grip regulation — calibrate a learned predictor of
  the per-grasp minimal no-slip normal force with (adaptive) conformal prediction, so that the slip rate is ≤ α by a
  finite-sample guarantee while grip force stays close to the per-grasp minimum.
- **Domains:** tactile sensing, robotic grasping, conformal prediction / uncertainty quantification, robot learning.
- **Project:** CertGrip (paper 2, `papers/p2/`).
- **Quality threshold:** 7.5.

## Topic
Grippers holding unknown objects trade off two failures: too little normal force → the object slips (drops, rotates);
too much → fragile objects are crushed, and energy and wear go up. Practical controllers pick a force from a nominal
friction model times a safety factor, or react to detected slip with fixed thresholds. Neither says *how often* the
chosen force will fail on new objects. We ask for a controller that, from tactile readings taken right after contact
and during a brief probe squeeze, outputs a force with a **user-chosen slip probability α** that is guaranteed without
assuming a correct friction or noise model, and that keeps the guarantee in the long run when the object distribution
drifts.

## Scope
- In scope: parallel-jaw grasps of rigid objects in MuJoCo; disturbance episodes (lift with acceleration, shake,
  lateral pull, added payload); simulated tactile arrays on the finger pads; a learned regressor of the minimal
  no-slip force F\*; split conformal / conformal risk control (offline, exchangeable); adaptive conformal inference
  with binary slip feedback (online, shift); baselines listed in `MEGA_PROMPT.md`.
- Out of scope: real hardware (no robot available; stated as a limitation), multi-finger dexterous regrasping,
  deformable objects, vision. Grasp *pose* selection is fixed (given); only force is chosen.
- Key enabler: in simulation each grasp instance can be replayed with different forces, so F\* is measured exactly
  (bisection over force with identical disturbance). This gives ground-truth labels for training, calibration and
  evaluation; on hardware only the binary outcome would be observable, which the online variant is built around.

## SMART Goal
By 2026-12-01, produce (S) a CPU-only, reproducible study in which a conformally calibrated tactile force predictor
(M) achieves an empirical slip rate within the finite-sample band of the target α ∈ {0.01, 0.05, 0.1, 0.2} on held-out
objects (≥ 5 seeds, ≥ 10 conditions), with lower mean force excess over F\* than the best baseline that also meets the
slip target, and an online variant whose long-run slip rate tracks α under three pre-registered shifts; (A) on free
GitHub Actions runners and the sandbox; (R) written up as an RSS 2027 Stage 1 extended abstract; (T) stage 20 passed
before 2026-12-01, otherwise retarget (see Constraints).

## Constraints
- CPU only; MuJoCo via pip; free GitHub Actions (shared 20-runner cap with paper 1); no paid services or accounts.
- All numbers from real runs of code in `papers/p2/code/`; pre-registration before any main run (stage 9 gate).
- RSS 2027 Stage 1: 5 pages + 1 page references, no supplement; Stage 2 (if invited) 8 pages.
- Shares no text, results or unpublished claims with paper 1 (AUTOPILOT §7).
- If stage 20 is not passed by 2026-12-01: do not rush a submission; retarget to the next AI / robot-learning venue
  whose deadline is posted (ICML 2027, CoRL 2027 or NeurIPS 2027) and tell the owner.

## Success Criteria
1. Validity: calibrated CertGrip's test slip rate lies within the binomial / Beta finite-sample band around α for every
   α and seed in the exchangeable setting; failures reported as such.
2. Efficiency: among methods that meet the slip target, CertGrip has the lowest mean force excess E[F − F\*] (paired
   test over grasps, Holm across conditions) — or an honest negative result if a tuned safety factor matches it.
3. Shift: under each pre-registered shift (new object family, lower friction, stronger disturbance), offline split
   conformal over- or under-covers as predicted, and the online variant's running slip rate converges to α.
4. Tactile value: an ablation (no tactile features vs tactile + probe squeeze) shows how much the tactile input reduces
   force excess at equal guaranteed slip rate.
5. Quality gate ≥ 7.5, citation audit zero red flags, page limit met on the compiled PDF.

## Generated
2026-11-08, Claude (Cowork, owner's chat session), stage 1 of paper 2. Literature mentioned is only what was opened
on this date; stage 4 collects and verifies the full set.
