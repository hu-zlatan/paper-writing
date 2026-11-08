# Stage 2 · PROBLEM_DECOMPOSE — paper 2 (CertGrip)

Prompt template: `pipeline/references/stage_prompts/problem_decompose.md`, verbatim. System: "You are a senior research
strategist." User: "Decompose this research problem into at least 4 prioritized sub-questions. Topic: {topic} Output
markdown with sections: Source, Sub-questions, Priority Ranking, Risks. Goal context: {goal_text}", with {topic} =
the stage-1 topic and {goal_text} = the full text of `docs/00_topic_init.md`.

## Source

- Topic (stage 1, `RESTRICTS.yaml` `project.topic`): distribution-free risk control for minimal-force tactile grip
  regulation — a learned predictor of the per-grasp minimal no-slip normal force F\*, calibrated by (adaptive)
  conformal prediction so that the slip rate is ≤ α while grip force stays close to F\*.
- Goal context: `docs/00_topic_init.md` (SMART goal, scope, constraints, success criteria 1–5).
- Nothing here is a result. No experiment has been run for paper 2.

## Sub-questions

**SQ1 — Is F\* a well-defined, measurable label in the simulator?**
For a fixed grasp instance (object, pose, disturbance), is "slip" monotone in normal force, so that bisection
over force returns one threshold F\* to a known tolerance ε? How often is it non-monotone (e.g. high force causing
ejection or contact-solver artefacts), how sensitive is F\* to the slip threshold and to MuJoCo solver settings, and
what does one label cost in CPU seconds?
Why it matters: the split-conformal guarantee on P(F < F\*) only equals a guarantee on P(slip) if slip ⇔ F < F\*;
otherwise the method must switch to conformal risk control on the binary slip loss.
Deliverable: a pilot report (monotonicity rate, ε, label cost) feeding stage 9.

**SQ2 — Does split-conformal calibration give the promised slip rate on held-out grasps (exchangeable case)?**
With F = g(x) + q̂ (additive) or g(x)·exp(q̂) (multiplicative) and q̂ the ⌈(n+1)(1−α)⌉-th calibration score, is the
test slip rate within the finite-sample band around α for α ∈ {0.01, 0.05, 0.1, 0.2} and n ∈ {100, 500, 2000}, across
predictor seeds and calibration/test resamples? The guarantee is a theorem given exchangeability and monotonicity; the
empirical question is whether the simulator pipeline satisfies its premises (labels with tolerance ε, no leakage
between splits).

**SQ3 — Is it more force-efficient than the strongest simple alternative at equal guaranteed slip rate?**
The decisive comparison is not against fixed safety factors but against a nominal-friction force × a safety factor
*calibrated on the same calibration set* to meet α (itself a one-parameter conformal method without tactile input),
and against conformalized point / quantile / Gaussian-σ predictors. Does tactile, per-instance adaptation reduce the
mean force excess E[F − F\*] at matched slip rate, by how much, and in which conditions (object family, disturbance
type, α)? An honest negative result (the calibrated safety factor matches it) is an acceptable outcome.

**SQ4 — How much of the efficiency comes from touch, and from the probe squeeze?**
Ablation at equal guaranteed α: (a) proprioception only, (b) + static tactile features after contact, (c) + the brief
probe squeeze. Since validity is guaranteed for every input set, the ablation reads only on force excess, which makes
"value of touch" measurable in a single currency (newtons above F\*).

**SQ5 — Does the online variant keep the long-run slip rate at α under distribution shift, using only binary slip
feedback?**
Adaptive conformal inference updates the quantile level from the error indicator; under monotonicity the indicator is
exactly "slip happened", so F\* is never needed online. Under three pre-registered shifts (new object family, lower
friction, stronger disturbance): does offline split conformal mis-cover in the predicted direction, does the online
running slip rate converge to α within the known O(1/(γT)) bound, and what does adaptation cost in force excess and in
transient slips before convergence? Which step size γ (fixed or a pre-registered small grid / aggregation) is used?

**SQ6 — How uneven is coverage across object groups?**
Marginal validity can hide groups (e.g. low-friction or off-centre grasps) with much higher slip rates. Report slip
rate per object group; if the spread is large, test group-conditional (Mondrian) calibration and its force cost.

## Priority Ranking

1. **SQ1** — gatekeeper: without a reliable F\* label, every later number is uninterpretable. Must be settled in the
   stage-10/12 pilot before any pre-registered run.
2. **SQ2** — the core claim (finite-sample slip-rate control); cheap once labels exist.
3. **SQ3** — the contribution that makes it a paper rather than a sanity check; requires the calibrated-safety-factor
   baseline to be strong and fairly tuned.
4. **SQ5** — the second core idea (validity under shift with binary feedback only; the hardware-relevant variant).
5. **SQ4** — explanatory; shares runs with SQ3 (only extra predictors to train).
6. **SQ6** — robustness / honesty; analysis on existing runs, Mondrian only if needed.

For the RSS Stage 1 extended abstract (5 pages), SQ1–SQ3 + SQ5 are the minimum; SQ4 and SQ6 go in if space and time
allow.

## Risks

| # | Risk | Mitigation |
|---|---|---|
| R1 | Slip is non-monotone in force in MuJoCo (soft contacts, solver artefacts), so F\* is ill-defined. | Measure the non-monotone rate on a fine force grid in the pilot; if non-negligible, switch to conformal risk control on the binary slip loss (which needs no monotone threshold) and say so. |
| R2 | One label needs ~10 replays per instance; with thousands of instances the cost may exceed the CPU budget shared with paper 1. | Time a pilot (5 min, RESTRICTS) and size the dataset from the TIME_ESTIMATE; shorter disturbance windows and fewer bisection steps (larger ε, added to the bound) are the pre-registered downscale order. |
| R3 | The calibrated safety-factor baseline matches CertGrip, leaving no efficiency gain. | Pre-register it as the primary comparator and report the result either way; the validity and online-shift results stand on their own. |
| R4 | MuJoCo tactile signals are too coarse to predict F\* (low R² of g), so conformal bounds are wide. | Check predictive signal in the pilot; enrich features (probe-squeeze response, contact-patch statistics); report force excess honestly even if gains are small. |
| R5 | Sim-only evaluation is a standard reviewer objection for RSS. | Claim only the calibration mechanism's validity (which holds independently of simulator fidelity) and list the hardware interface (binary slip feedback) as the transfer path; state the limitation plainly. |
| R6 | Too little novelty: "apply conformal prediction to grip force" may look incremental. | Position the contribution as an end-to-end slip-rate guarantee with exact simulator labels, the calibrated-safety-factor comparison, and the binary-feedback online variant; stage 4–7 must confirm no prior work does this. |
| R7 | Time: RSS Stage 1 is 2026-12-04 AoE and paper 1 shares the 20-runner Actions cap. | Keep the study small (one gripper, ≤ 4 object families); run labels in short shards; if stage 20 is not passed by 2026-12-01, retarget instead of rushing (stage-1 constraint). |
| R8 | Leakage between train / calibration / test (e.g. same object meshes or seeds) silently inflates validity. | Independent salts per split, object identities disjoint across splits for the shift tests; a unit test asserts disjointness. |
