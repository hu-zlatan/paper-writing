# Stage 7 · SYNTHESIS — paper 2 (CertGrip)

Prompt template: `pipeline/references/stage_prompts/synthesis.md`, verbatim (system "You are a synthesis specialist for
literature reviews."; user "Produce merged synthesis output (topic clusters + research gaps). Output markdown with
sections: Cluster Overview, Cluster 1..N, Gap 1..N, Prioritized Opportunities. Topic: {topic} Cards context:
{cards_context}"), with {topic} from `RESTRICTS.yaml` and {cards_context} = `docs/05_knowledge_cards.json` (52 cards,
all read in one batch). Statements about papers come from the cards, i.e. from abstracts only; "(inferred)" marks
inferences carried over from the cards. Targeted gap check (2026-11-08): two WebSearch queries for conformal / calibrated
grip-force or slip guarantees returned no such work (results: arXiv 2402.11412, 2209.10687, 2603.07040, 2410.18237,
2506.18960, 2604.25897, 1708.00922 — none calibrates grip force to a slip rate). A search can show presence, not
absence; stage 23 re-checks.

## Cluster Overview

| # | Cluster | Cards | What it offers us | What it lacks for our topic |
|---|---|---|---|---|
| 1 | Reactive slip detection and grip-force regulation | 12 | Signals, controllers, detectors; minimal-force motivation | Any statement of *how often* the chosen force fails |
| 2 | Force selection by estimation (friction / margin / learned force) | 5 (1 shared with cluster 1) | The decision variable we calibrate (a force or margin from touch or vision) | Calibrated uncertainty; finite-sample slip-rate control |
| 3 | Guarantees and risk in grasping | 5 | The guarantee-type competitors (deterministic CBF; model-based probabilistic / CVaR) | Distribution-free validity; tactile online force choice |
| 4 | Conformal prediction and risk control (offline) | 9 | Split / quantile conformal, risk control, non-monotone and non-exchangeable variants, conditional coverage | Robotics, force decisions |
| 5 | Online / adaptive conformal under shift and partial feedback | 7 | Long-run coverage from the miscoverage indicator; step-size choice; partial feedback | Physical decisions whose outcome *is* the indicator |
| 6 | Conformal prediction in robotics and control | 9 | Precedents for conformal safety in planning, navigation, verification, decisions | Grasping / contact force |
| 7 | Tactile simulation, benchmarks and human grip | 6 | Simulators, sensor-layout and "does touch help" studies; human adaptation to friction change | Slip fidelity statements; guarantees |

## Cluster 1 — Reactive slip detection and grip-force regulation

`dong2019maintaining` (GelSlim slip field, 86.25 % detection accuracy over 240 tests on 10 objects, used to adjust
force), `james2020slip` (SVM slip detection on a tactile hand), `grover2022detect` (TCN on barometric sensors),
`veiga2020grip` (per-finger slip-prediction controllers), `berman2025autonomous` (slip-triggered force increments),
`ayral2026reactive` (slip onset detected after 20.4 ± 6 ms; ~30 ms response), `feng2026tactilereflex` (thresholds from
sensor-noise statistics; 9/10 pouring successes), `kuo2025tracing` (energy-based learned force control),
`almohammed2022switched` (Lyapunov switched adaptive controller, slip velocities → 0 with minimal force), `lach2024zero`
(sim-trained RL force policy, zero-shot to robot), and the surveys `chen2018tactile`, `romeo2020methods`.
**Pattern:** the field detects slip and reacts, or drives slip velocity to zero under a model. Detector accuracies are
empirical; thresholds are heuristic (noise percentiles, fixed increments). No card reports a target failure rate chosen
in advance and met. Reaction latency (~20–50 ms in `ayral2026reactive`) means a reactive scheme still lets slip start —
relevant to why a *pre-emptive* calibrated force has value under fast disturbances (inferred).

## Cluster 2 — Force selection by estimation

`khamis2021real` (friction-estimate controller with a fixed 20 % safety margin → actual force 9–30 % above the force
needed), `boonstra2024estimate` (CNN point estimate of the tactile safety margin, forces 1–3 N), `niu2026synchronized`
(particle-filter friction coefficient → force), `shang2026exp` (VLM predicts minimum feasible force from one RGB image:
MAE 0.43 N, appropriate-force rate 63 % → 87 % on 30 unseen objects), `chen2018tactile` (argues minimum grip force needs
friction sensing).
**Pattern:** the minimal-force problem is posed and attacked with point estimates plus a hand-set margin. The "87 %
appropriate" and "9–30 % excess" figures are exactly the two numbers a calibrated method would trade off (slip rate vs
excess) — but nobody chooses the margin to hit a slip rate. This is the cluster CertGrip plugs into: the predictor is
replaceable; the calibration layer is the contribution.

## Cluster 3 — Guarantees and risk in grasping

`kim2024robust` (tactile CBF safe grasping, disturbance-observer, deterministic), `cortez2019control` (robust CBFs:
no slip / overextension / rolling, model-based), `enwerem2026firmgrasp` (CVaR friction risk margin; 53 % of nominally
force-closed grasps lose closure in the adverse friction tail), `enwerem2026variational` (risk-sensitive belief
planning, calibration error < 0.14), `cloutier2018examining` (Monte Carlo failure probability of grasp-force
optimisation under assumed parameter distributions).
**Pattern:** guarantees are either deterministic under bounded-uncertainty models, or probabilistic *with respect to an
assumed distribution* (friction prior, parameter distribution). FIRMGrasp's 53 % figure shows how misleading nominal
margins are under friction tails — and its guarantee holds only if the friction prior is right (inferred).

## Cluster 4 — Conformal prediction and risk control (offline)

`vovk2005algorithmic`, `lei2017distribution` (split conformal, finite-sample marginal coverage),
`romano2019conformalized` (CQR), `angelopoulos2023conformal` (tutorial), `angelopoulos2022conformal` (conformal risk
control, monotone losses, tight to O(1/n)), `angelopoulos2026conformal` (non-monotone losses, stability-dependent
guarantees), `farinhas2023non` (non-exchangeable, weighted), `bian2023training` (split conformal is
training-conditionally valid), `ding2023class` (cluster-conditional calibration).
**Pattern:** everything needed for the offline variant exists. A one-sided upper bound on F\* is CQR with one
quantile; slip-rate control is risk control with the loss 1{slip(F)}, which is monotone in F exactly when slip is
monotone in force — the property stage 2's SQ1 must test. If it fails, `angelopoulos2026conformal` is the fallback
at the price of looser guarantees.

## Cluster 5 — Online / adaptive conformal under shift and partial feedback

`gibbs2021adaptive` (ACI: long-run coverage for any data sequence, updating the level from the miscoverage
indicator), `gibbs2022conformal` (step-size tuning, local-interval regret), `angelopoulos2023conformala` (conformal
PID), `angelopoulos2024online` (decaying steps, per-time coverage when stable), `ge2024stochastic` (semi-bandit /
censored feedback, regret), `zhao2024conformalized` (intermittent labels, asymptotic coverage), `zhang2024bayesian`
(online conformal with safety feedback; controllable non-zero violation rate).
**Pattern:** ACI's update needs only err_t = 1{y_t ∉ C_t}. The cards note that these methods "need the true label"
(inferred) — but in grip control the miscoverage event *is* the physical outcome: with a monotone slip threshold,
err_t = 1{F_t < F\*_t} = 1{slip_t}, which a robot observes without ever measuring F\*. This turns a known algorithm
into a deployable one for grasping; we found no card exploiting it for a physical safety outcome except
`zhang2024bayesian` (safety feedback in BO) and `lekeufack2024conformal` (decisions). Trade-off to quantify: constant
steps track abrupt shift but oscillate; decaying steps are stable but slow (`angelopoulos2024online`).

## Cluster 6 — Conformal prediction in robotics and control

`lekeufack2024conformal` (conformal decision theory: calibrate a decision parameter, long-run risk, non-IID),
`lindemann2025formal` (overview), `dixit2022adaptive` (ACI inside MPC among dynamic agents), `marques2026particle`
(contact-aware conformal regions; reaches the requested coverage in and out of contact, up to 30 % absolute task
success gain), `lindemann2023conformal` (STL runtime verification), `ren2023robots` (LLM planners), `huang2023conformal`
(quantile-conditioned policies under shift), `strawn2023conformal` (safety filter), `kumar2026learnable` (learned
nonconformity scores; 91.5 % vs 87.8 % navigation success).
**Pattern:** conformal methods are established in planning, navigation, verification and high-level decisions; contact
appears only as configuration-prediction regions (`marques2026particle`). Low-level force selection with a slip-rate
target is absent from these cards.

## Cluster 7 — Tactile simulation, benchmarks and human grip

`wang2022tacto`, `akinola2025tacsl` (200× faster contact-force extraction), `leins2025hydroelastictouch` (MuJoCo-based
hydroelastic tactile simulation), `luu2025manifeel` (visuotactile policy benchmark), `birtalan2026impact` (6 sensor
layouts), `willemet2024grip` (humans raise grip force when friction drops but not when it rises).
**Pattern:** simulators target realistic tactile *images* / force fields; none of the cards states slip fidelity.
For us the simulator must provide replayable grasps (exact F\* by bisection), not photorealism; this lowers the bar
(MuJoCo touch grid suffices) but makes "sim-only" the main external-validity threat. The human study gives a natural
shift (friction decrease) and an asymmetry worth mirroring in the shift design.

## Gap 1 — No grip-force method states and meets a pre-chosen slip probability

No card in clusters 1–3 selects a grip force so that P(slip) ≤ α for a user-chosen α with a guarantee that does not
assume a friction or disturbance model. *Falsifiable as:* a method that does so would show, on held-out grasps, an
empirical slip rate inside the finite-sample band around α for every α tested, while uncalibrated margins (fixed
safety factors, point predictors) fall outside it for at least one α. If heuristic margins already land inside the
band for all α, the gap is practically empty.

## Gap 2 — The cost of a guarantee in grip force has not been measured against the strongest simple alternative

Margins are hand-set (`khamis2021real` 20 %) and the resulting excess (9–30 %) is reported, but no work compares
force excess at a *matched, guaranteed* slip rate. The strongest simple alternative — a single safety factor on a
nominal force, calibrated on the same calibration set — is itself conformal (one parameter, no touch). *Falsifiable
as:* at equal α, does a tactile per-grasp predictor + conformal bound give lower mean excess E[F − F\*] than the
calibrated factor? Either answer is informative; a tie would refute the value of per-grasp tactile adaptation for this
purpose.

## Gap 3 — Online slip-rate control from binary slip feedback under shift is undemonstrated

ACI-type methods guarantee long-run coverage from the miscoverage indicator (cluster 5), and the slip event is that
indicator, yet no card applies this to grasping. *Falsifiable as:* under pre-registered shifts (lower friction, new
object family, stronger disturbance), offline split conformal's slip rate should leave the α band in a predicted
direction while the online variant's running slip rate converges to α within the ACI bound; if offline calibration
stays valid under all three shifts, the online variant has no work to do.

## Gap 4 — Monotonicity of slip in grip force (the premise linking quantile coverage to slip rate) is unchecked

Clusters 1–3 assume more force → less slip; cluster 4 needs it for monotone risk control. No card measures how often
it fails in simulation or hardware (e.g. ejection, solver artefacts, rolling). *Falsifiable as:* on a fine force grid,
the fraction of grasps with a non-monotone slip outcome is measurable; above a pre-set tolerance the quantile route is
invalid and the non-monotone fallback (`angelopoulos2026conformal`) is required.

## Gap 5 — The value of touch for force selection has no common currency

"Does touch help" studies (`luu2025manifeel`, `birtalan2026impact`) measure task success; force-selection work uses
different sensors and metrics (`shang2026exp` vision-only MAE; `boonstra2024estimate` tactile). With validity guaranteed
for any input set, force excess at fixed α is a single currency for proprioception vs touch vs touch + probe squeeze.
*Falsifiable as:* if the tactile and proprioceptive predictors give equal excess at equal guaranteed α, touch adds
nothing for this decision.

## Gap 6 — Marginal slip-rate validity may hide groups with high slip rates

Conditional coverage (`ding2023class`, cluster 4) is not discussed for grasping. *Falsifiable as:* slip rate per
object group (low friction, off-centre grasp, heavy) under marginal calibration; if all groups stay inside the band,
group-conditional calibration is unnecessary here.

## Prioritized Opportunities

Scored on (a) feasibility within CPU / free Actions and the 2026-12-01 internal deadline, (b) novelty likelihood
given clusters 1–6, (c) match with the stage-1 SMART goal (criteria 1–4).

| Rank | Opportunity | (a) Feasibility | (b) Novelty | (c) SMART match | Note |
|---|---|---|---|---|---|
| 1 | Gap 4 → Gap 1: measure monotonicity, then offline slip-rate validity | high (labels by bisection; conformal is cheap) | medium-high | criterion 1 | Gatekeeper; must run first in the pilot. |
| 2 | Gap 2: excess at matched α vs calibrated safety factor and conformalized point / quantile / σ predictors | high (same labels) | high (no card measures it) | criterion 2 | The paper's main comparative claim; negative result acceptable. |
| 3 | Gap 3: online ACI from binary slip feedback under 3 shifts | high (sequential replay of labelled grasps) | high | criterion 3 | Second core idea; hardware-relevant. |
| 4 | Gap 5: tactile / probe-squeeze ablation in force excess | high (extra predictors only) | medium | criterion 4 | Shares runs with rank 2. |
| 5 | Gap 6: per-group slip rate; Mondrian only if needed | high (analysis) | low-medium | honesty | Report regardless. |

The study stays "sushi": one calibration layer (offline + online) on one decision variable, evaluated where ground
truth is exact. Stage 8 turns ranks 1–3 into falsifiable hypotheses; the skeptic should attack the simulator-fidelity
and "it is just conformal prediction" objections.
