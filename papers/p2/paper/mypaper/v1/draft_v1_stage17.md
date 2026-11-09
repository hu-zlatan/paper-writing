```
FIGURE 1 PROMPT
Full-width, three-panel vector figure for a robotics paper (RSS style), white background, sans-serif labels,
colour-blind-safe palette (probe arm = deep blue, non-tactile baseline CSF-1 = orange, physics plug-in CSF-mu-hat =
teal, onset-only = light blue, alpha line = dashed grey). Title strip above the panels: "Probe, then certify".

(a) Protocol timeline. x-axis: time within one grasp episode; y-axis: grip force (log scale). Segments, left to right:
"preload F0 = 32.7 N (same for every object)" as a flat line; "squeeze F0 -> 1.5 F0 -> F0" as a small triangular bump;
"ramp-down probe" as a log-linear descent from F0 towards 0.005 F0 over 0.25 s, cut short by a red marker labelled
"incipient-slip onset F_onset" followed by a fast return to F0; then "ramp to F = g(x) e^lambda-hat" and a shaded
"disturbance window (0.6 s)" with four small icons D1 lift acceleration, D2 shake, D3 lateral pull, D4 payload.
Shade only the probe segment in light blue and label it "only friction channel". Inset next to the onset marker: the
pad shear/normal ratio vs time, rising during stick and flattening at onset, with the detector rule
"8-frame rise < 1/2 stick rise, 2 consecutive frames" annotated.

(b) Certification. For one disturbance stratum, x-axis: lambda (log force multiplier) on a 20-point grid centred on
the selection-split quantile; y-axis: monotonised empirical slip risk (n R_n(lambda) + 1)/(n + 1). Two staircase
curves decreasing in lambda: CertGrip-full (blue) and CSF-1 (orange). Horizontal dashed line at alpha = 0.10. Mark
lambda-hat as the first grid point where each curve falls below alpha, with a vertical tick. Caption tag inside the
panel: "schematic; drawn from the per-stratum lambda-hat indices". Note "loss = 1{physical slip in direct replay}".

(c) Result bars (test set, alpha = 0.10, conformal-risk-control route). Four bars of mean relative excess force
(F - F*)/F* with 97.5 % object-cluster bootstrap error bars: CSF-1 0.7832 [0.6968, 0.8583]; CSF-mu-hat (sigma 0.2)
0.4843 [0.4435, 0.5219]; CertGrip-full (sigma 0.2) 0.4567 [0.4079, 0.5033]; onset-only (sigma 0.2) 0.4336
[0.3983, 0.4833]. On a secondary right axis, one dot per bar for the physical test slip rate: 0.1021, 0.0657, 0.0829,
0.0857, against a dashed alpha = 0.10 line. Bracket between the CSF-1 and CertGrip-full bars annotated
"D = 0.4168 [0.3484, 0.4778]". A small grey footnote marker at the bottom right: "narrow-friction, mid-amplitude
sub-pool: D = -0.2614 (method worse)". Footer line under all panels: "Simulation (MuJoCo), modelled tactile
detector, onset noise sigma = 0.2".
```

# Probe, Then Certify: Minimal-Force Grasping with a Tactile Friction-Onset Probe and Conformal Slip-Risk Control

## Abstract

A grasp controller that squeezes as little as possible should still come with a statement about how often the object slips. Two lines of work address this separately: tactile grip controllers react to slip or estimate friction but give no distribution-free bound on the slip rate, and conformal calibration can bound the slip rate of any force rule but stays conservative when the rule cannot see friction. We study whether a short tactile probe closes this gap. After a fixed preload that carries no mass or friction information, the gripper ramps its force down until a touch-only detector reports incipient slip. A gradient-boosted quantile predictor uses this onset, and conformal risk control (CRC) on the binary *physical* slip loss sets the force per disturbance stratum so that the expected slip rate is at most α. In MuJoCo simulation at α = 0.10, under pre-registered decisions, the probe arm needs less relative excess force than the strongest non-tactile conformal baseline, which was selected beforehand: D = 0.4168 (97.5 % CI [0.3484, 0.4778]), with test physical slip 0.0829. Ablations place the saving in the probe. Static touch is equivalent to proprioception, adding the onset gives D = 0.4739, and at onset noise σ = 0.2 the learned model shows no demonstrated gain over a physics plug-in that uses the same onset (not confirmed). In a sub-pool with narrow friction (μ ∈ [0.5, 0.8]) and mid-amplitude disturbances the method is worse than the baseline (D = −0.2614). Under three distribution shifts, online quantile tracking from binary slip feedback keeps the window slip rate near α where frozen calibration fails. Its efficiency relative to oracle recalibration is inconclusive.

## 1 Introduction

Grasping fragile, compliant or valuable objects calls for the smallest grip force that still holds the object through the motions and loads the task imposes. Excess force damages soft or brittle objects, and slip prevention with limited force is a central concern in prosthetic hands \cite{berman2025autonomous}. Too little force drops the object. Tactile grip regulation has made steady progress on this trade-off. Controllers detect incipient slip and tighten the grasp \cite{dong2019maintaining, veiga2020grip}, estimate friction online and add a margin \cite{khamis2021real, niu2026synchronized}, or learn a map from tactile signals to a gentle grasp force \cite{boonstra2024estimate}. Human studies show that people regulate grip force in response to sudden changes of friction and load \cite{willemet2024grip}. What these controllers do not provide is a quantitative, distribution-free statement of the form "this force rule slips on at most a fraction α of grasps". Margins are set by hand, and their slip rate is whatever the experiment happens to show.

Conformal methods supply exactly this kind of statement. Split conformal prediction \cite{lei2017distribution} and conformal risk control \cite{angelopoulos2022conformal} turn any predictor into a rule whose expected loss on an exchangeable test point is bounded by a target level, using a held-out calibration set and no distributional assumptions. Applied to grasping, the predictor proposes a force and the calibration step inflates it until the empirical slip risk on calibration grasps is at most α. The guarantee is cheap, but its price in force depends on what the predictor knows. A rule that cannot see friction must cover the whole friction range with a single inflation factor. With μ spanning a factor of more than three, the calibrated force is then conservative for most objects. The relevant comparison for any tactile method is therefore not an uncalibrated controller but the *strongest non-tactile conformal baseline*: a method that uses everything a robot knows without touch (mass, commanded motion, aperture, even privileged object-family identity) and is calibrated to the same α. In our study this comparator was selected on a disjoint selection split before any calibration or test data were accessed. The physics plug-in CSF-1 (mean relative excess 0.7686) beat Mondrian-CSF with privileged family identity (0.8294) and a learned proprioceptive predictor CertGrip-P (0.8335).

This framing raises three questions. First, can a short tactile probe supply enough friction information to cut excess grip force at a certified physical slip rate of at most α? Second, which component carries the saving: static touch, a probing squeeze, the friction-onset probe, or the learned model on top? Third, does calibration survive distribution shift when the only feedback available on a robot is whether the object slipped?

Our answer is built around one mechanism and one statistical tool. The mechanism is a ramp-down friction-onset probe. After a fixed preload F₀ = 32.7 N, identical for every object and therefore uninformative about mass and friction, the gripper lowers its force log-linearly until a touch-only detector reports incipient slip, then returns to F₀. Under Coulomb friction the onset force gives an estimate μ̂ = m g/(2F_onset). In simulation this estimate is nearly perfect, so we add pre-registered onset noise and take σ = 0.2 log units as the primary level. The statistical tool is conformal risk control on the binary physical slip loss, applied per disturbance stratum. We need CRC rather than plain split conformal because our pre-registered monotonicity gate failed: in 8 of 800 instances slip was not monotone in force. A certificate on bisection labels therefore does not automatically carry over to the physical outcome. For the online question we use score-space online quantile tracking \cite{angelopoulos2023conformala}, which updates a log-force offset from binary slip feedback alone.

**Contributions.**
- **(C1) A certifiable grasp protocol.** A fixed preload carries no mass or friction information, so a ramp-down onset probe is the only friction channel. CRC is applied on the monotonised physical slip loss, a route that stays valid when the bisection label rule is not exactly monotone in force (8 of 800 instances).
- **(C2) A pre-registered comparison against the best non-tactile conformal comparator.** At α = 0.10 the probe arm reduces mean relative excess force by D = 0.4168 (CI\*\* [0.3484, 0.4778]) relative to CSF-1. The result holds under label-quantisation, seed, label-route, per-cell, small-calibration and post hoc grid checks.
- **(C3) An ablation chain that locates the saving in the probe.** The saving does not come from static touch, the squeeze, or the learned model. The chain also reports a regime where the method loses, a narrow-friction, mid-amplitude sub-pool with D = −0.2614.
- **(C4) An online binary-feedback study under three shifts.** Frozen calibration breaks, while score-space quantile tracking restores the window slip rate near α. Its efficiency relative to a label-requiring oracle recalibration is inconclusive, and we report it as such.

We state the confirmatory record plainly. Of the four pre-registered core decisions, one was confirmed (H2a, the main comparison). The validity premise H1 was not confirmed, the learned-versus-plug-in contrast H2b was not confirmed, and the online efficiency decision H3 was inconclusive in all three shifts. These outcomes are reported as they came out. Section 2 positions the work, Section 3 defines the problem and method, Section 4 gives the experimental protocol and the deviations from the pre-registration, Section 5 reports results, and Sections 6 to 8 discuss, list limitations and conclude.

## 2 Related Work

**Tactile slip detection and friction estimation for grip control.** Surveys of tactile friction estimation and slip detection \cite{chen2018tactile, romeo2020methods} describe a mature sensing literature in which incipient slip, the partial slip at the contact periphery that precedes gross sliding, is the key cue for friction. Slip detectors on multifingered hands \cite{james2020slip}, learned temporal detectors on barometric sensors \cite{grover2022detect}, and reactive multifingered controllers that combine slip onset with internal-force optimisation \cite{ayral2026reactive} trigger corrective tightening. Closer to minimal-force grasping, \cite{dong2019maintaining} keep grasps within slipping bounds by monitoring incipient slip, \cite{khamis2021real} estimate friction in real time and apply a safety margin to the target force, \cite{boonstra2024estimate} learn to estimate incipient slip for gentle grasping, and \cite{niu2026synchronized} couple online friction estimation with adaptive grasp control. Learned and reflex controllers extend this to dynamic interaction \cite{kuo2025tracing}, vision-tactile reflexes \cite{feng2026tactilereflex}, and sim-to-real force-control policies \cite{lach2024zero}. Adaptive analytical controllers for novel objects come with Lyapunov stability arguments \cite{almohammed2022switched}, and vision-language models select pre-grasp forces from experience \cite{shang2026exp}. Our probe uses the same physical cue as these works. They convert it into a reactive response or an estimated margin, and none of them states a distribution-free bound on the resulting slip rate. We keep the cue and replace the margin with a calibrated quantity.

**Robust and safe grasping under uncertainty.** Model-based approaches bound the risk of losing a grasp through assumed uncertainty sets. Grasping-force optimisation has been examined under parameter uncertainty \cite{cloutier2018examining}. Control barrier functions enforce friction-cone constraints in mechanical systems \cite{cortez2019control} and, with disturbance observers and tactile sensing, give robust adaptive safe grasping \cite{kim2024robust}. Friction-informed risk margins \cite{enwerem2026firmgrasp} and variational belief parameterisations \cite{enwerem2026variational} make grasp synthesis robust to multimodal uncertainty. These guarantees hold relative to the model and its uncertainty set. Our certificate instead holds relative to the data-generating distribution of grasps, without a friction model. The price is that it is marginal over grasps and needs calibration data from that distribution.

**Conformal prediction and risk control.** Conformal prediction gives finite-sample, distribution-free guarantees under exchangeability \cite{vovk2005algorithmic, lei2017distribution, angelopoulos2023conformal}. Conformalized quantile regression adapts interval width to the input \cite{romano2019conformalized}. Training-conditional \cite{bian2023training} and class-conditional or clustered \cite{ding2023class} variants refine the marginal statement. Conformal risk control generalises coverage to bounded monotone losses \cite{angelopoulos2022conformal}, and has been extended to non-monotone losses \cite{angelopoulos2026conformal} and non-exchangeable data \cite{farinhas2023non}. Under distribution shift, adaptive conformal inference \cite{gibbs2021adaptive, gibbs2022conformal}, conformal PID control and quantile tracking \cite{angelopoulos2023conformala}, decaying step sizes \cite{angelopoulos2024online}, and semi-bandit feedback \cite{ge2024stochastic} keep long-run coverage near target. In robotics, conformal tools certify decisions \cite{lekeufack2024conformal}, verification and control \cite{lindemann2025formal, lindemann2023conformal}, motion planning among dynamic agents \cite{dixit2022adaptive}, contact-aware state estimation \cite{marques2026particle}, LLM planners that ask for help \cite{ren2023robots}, sensorimotor policies under shift \cite{huang2023conformal}, RL safety filters \cite{strawn2023conformal}, safe Bayesian optimisation \cite{zhang2024bayesian}, interactive imitation learning \cite{zhao2024conformalized}, and perception-planning pipelines \cite{kumar2026learnable}. In these works the controlled quantity is a prediction set, a trajectory region or a decision loss. None of them certifies a physical contact outcome, the slip of a grasp, as a binary loss over a family of grip forces. None asks which sensing channel makes the certified force small. Our work sits at this intersection. The statistical machinery is standard, and the robotics content lies in the probe that makes the certificate cheap, in the attribution of the saving, and in the measured behaviour of binary-feedback recalibration under shift.

## 3 Problem Formulation and Method

### 3.1 Certified minimal-force grasping

A grasp instance x comprises an object (family, geometry, mass m, friction coefficient μ, centre-of-mass offset), a grasp pose offset, and a disturbance of known type d ∈ {D1, D2, D3, D4} (lift acceleration, shake, lateral pull, payload added mid-hold) with an amplitude. A parallel-jaw gripper commands a grip force F, and slip(F, x) ∈ {0, 1} is the physical outcome of a full episode. An episode counts as a slip if the object's displacement relative to the pad frame, projected onto the pad plane, exceeds δ_t = 2 mm, or if its rotation about the grasp axis exceeds 3°, or if contact with a pad is lost. The minimal no-slip force F\*(x) is bracketed in simulation by log-space bisection on [F_min, F_max] = [0.1, 100] N with one replay at F_max and 10 halvings (11 replays). This gives F\*_lo < F\*_hi with a relative bracket width of about 0.7 % and F\*_mid = √(F\*_lo F\*_hi). A force rule F(·) is evaluated by its mean relative excess

$$\mathrm{RE}(F) = \mathbb{E}_x\big[(F(x) - F^*_{\mathrm{mid}}(x))/F^*_{\mathrm{mid}}(x)\big],$$

which is signed and includes slipped instances, and by its physical slip rate $\mathbb{E}_x[\mathrm{slip}(F(x), x)]$. The task is

$$\min_F \ \mathrm{RE}(F) \quad \text{s.t.} \quad \mathbb{E}_x[\mathrm{slip}(F(x), x)] \le \alpha,$$

where the constraint must hold without a model of the contact physics, using a calibration set of instances drawn from the same distribution as the test instances. Two rules A and B are compared by the paired ratio of means on identical test instances,

$$D = 1 - \mathrm{RE}(A)/\mathrm{RE}(B),$$

so D > 0 means A needs less excess force than B. The labels F\* exist only in simulation. This is why the certificate below is defined on the physical outcome and why Section 3.5 gives a label-free online route.

### 3.2 Grasp protocol and the friction-onset probe

Every method runs the same protocol, so every method sees the same physical history up to the moment it chooses F. The gripper first closes to a constant preload F₀ = 32.7 N (m g/μ with m_max = 1 kg and μ_min = 0.3) and holds it for 0.4 s. Because F₀ is the same for every instance, it encodes neither mass nor friction. A probe squeeze F₀ → 1.5 F₀ → F₀ follows over 0.3 s. Then comes the **ramp-down probe**: the force falls log-linearly from F₀ towards 0.005 F₀ over 0.25 s. A detector that reads only the pad touch grids at 500 Hz computes the noisy shear/normal ratio r = Σ_pads |shear sum| / Σ normal, smooths log r over 6 frames, and declares onset at the first 2 consecutive frames whose 8-frame rise is below half the stick-phase rise. The detector is armed only once the smoothed r exceeds 0.1, or once the normal reading falls below 1 mN. Taxel readings carry per-taxel multiplicative lognormal noise (0.05), additive noise (0.002 N) and a per-instance channel gain bias (lognormal 0.10). At onset the force returns to F₀ within 0.02 s and holds for 0.1 s. If no onset is found, the probe is censored at the floor. The gripper then ramps to the chosen F (0.1 s), settles (0.1 s), and runs the 0.6 s disturbance window. The slip reference is the pose before the probe, so a slip caused by the probe counts as a slip of the grasp.

The onset force gives a Coulomb friction reading μ̂ = m g/(2 F_onset), clipped to [0.1, 3]. In simulation the detector is close to a perfect friction sensor: in tuning, log(m g/2F_onset) correlated with log μ at 0.988. We therefore treat it as an upper bound and model a realistic tactile detector by adding onset noise in log units, $\tilde f = \log F_{\mathrm{onset}} + \sigma\varepsilon$ with $\varepsilon \sim \mathcal{N}(0,1)$ drawn once per instance and σ ∈ {0, 0.1, 0.2, 0.4}. All core decisions use **σ = 0.2**. The same noisy onset is passed to every arm that uses it.

### 3.3 Predictors and baselines

Learned arms use gradient-boosted quantile trees ĝ(x) at level τ = 1 − α, trained on disjoint training objects with the same 30-configuration random search and 4-fold object-grouped cross-validation for every feature set. The feature sets are nested. **P** (proprioception) contains the disturbance type (one-hot), the commanded acceleration, log mass and the aperture at contact. **S** adds static touch at the lifted preload and a preload-slip flag. **full** adds the probe-squeeze features. **CertGrip-full** adds the onset feature $(\tilde f, \text{found})$. **Onset-only** is P plus the onset feature. Mass is given to every method in the main analysis, on the stated assumption that a robot can weigh the object during the lift. External disturbance amplitudes (D3, D4) are hidden from all methods. The physics plug-ins are:

- **CSF-1:** $F = F_{\mathrm{nom}}\, e^{\hat q}$ with $F_{\mathrm{nom}} = m(g + a_{\mathrm{cmd}})/(2\bar\mu)$ for D1/D2 and $m g/(2\bar\mu)$ for D3/D4, where $\bar\mu$ is the geometric mean of the μ range.
- **Mondrian-CSF:** the same formula with one $\hat q$ per family × disturbance cell (16 cells) \cite{ding2023class}. It is given the privileged family identity.
- **CSF-μ̂:** $F = m(g + a_{\mathrm{cmd}})/(2\hat\mu)\, e^{\hat q}$, with μ̂ from the same noisy onset as the CertGrip arm it is compared with.

The comparator COMP is the best of {CSF-1, Mondrian-CSF, CertGrip-P} by mean label-rule RE at α = 0.10 on the selection split (even-index objects calibrate, odd-index objects evaluate, then the roles swap). It was chosen and committed before any calibration or test file was read. An oracle predictor on privileged inputs (μ, amplitude, CoM offset, geometry, mass) gives a ceiling.

### 3.4 Conformal risk control on the physical slip loss

For an arm with predictor g and calibration instance i, define the force family and the physical loss

$$F_i(\lambda) = \min\big(F_{\max},\, g(x_i)\, e^{\lambda}\big), \qquad L_i(\lambda) = \mathbb{1}\{\text{slip in a direct replay at } F_i(\lambda)\}.$$

The loss is the outcome of a fresh simulated episode, not the bisection label. Slip need not be monotone in force, so we use the monotonised loss

$$\tilde L_i(\lambda) = \max_{\lambda' \ge \lambda,\ \lambda' \in \Lambda} L_i(\lambda'),$$

which is non-increasing in λ and satisfies $\tilde L_i \ge L_i$. A risk bound on $\tilde L$ therefore implies the same bound on physical slip. The grid is fixed per arm before calibration: $\Lambda = \hat q_{\mathrm{sel}} + \mathrm{linspace}(-0.4, 0.4, 20)$, where $\hat q_{\mathrm{sel}}$ is the label-rule conformal quantile of the arm's scores on the selection split, pooled over strata. Within each disturbance stratum, with n = 500 calibration instances,

$$\hat\lambda = \min\Big\{\lambda \in \Lambda : \frac{n \tilde R_n(\lambda) + 1}{n + 1} \le \alpha\Big\}, \qquad \tilde R_n(\lambda) = \frac{1}{n}\sum_{i=1}^n \tilde L_i(\lambda),$$

and λ̂ = max Λ if no grid point qualifies. By \cite{angelopoulos2022conformal}, a test instance exchangeable with the stratum's calibration instances satisfies E[slip at F(λ̂)] ≤ α. Because each object contributes one instance per stratum, exchangeability holds at the object level, and the guarantee holds per stratum and hence marginally. Unavoidable instances (F\*_hi > F_max) count as slips at every λ.

```
Algorithm 1: CertGrip-CRC (per arm, per disturbance stratum d)
input : predictor g, selection-split quantile q_sel, calibration instances {x_i} in stratum d, level alpha
1  Lambda <- q_sel + linspace(-0.4, 0.4, 20)
2  for i in calibration set, for lambda in Lambda:
3       L[i, lambda] <- slip of a direct replay at min(F_max, g(x_i) * exp(lambda))
4  Ltilde[i, lambda] <- max_{lambda' >= lambda} L[i, lambda']        # monotonise
5  lambda_hat <- first lambda in Lambda with (sum_i Ltilde[i, lambda] + 1)/(n + 1) <= alpha, else max(Lambda)
6  deploy: probe, compute g(x), command F = min(F_max, g(x) * exp(lambda_hat))
```

**Design rationale.** The originally pre-registered certificate was split conformal on bisection labels with the one-sided CQR score $s = \log F^*_{\mathrm{hi}} - \log \hat g(x)$ \cite{romano2019conformalized}, $\hat q$ = the ⌈(n+1)(1−α)⌉-th smallest score in the stratum, and $F = \hat g\, e^{\hat q}$. This certifies the label event F < F\*_hi. It transfers to physical slip only if slip is monotone in F. The pre-registered monotonicity gate (H1-M) tested this on 800 instances with a 25-point global grid, a 10-point dense local grid on [F\*_hi, 1.5 F\*_hi] and the bisection points, and it failed (Section 5.4). Following the pre-registered failure branch, the primary route became CRC on the physical loss. The label route is reported as a secondary analysis. The monotonised loss makes CRC valid without assuming monotonicity, at the cost of slight conservatism wherever the raw loss flickers.

**Cost.** The certificate needs |Λ| = 20 direct replays per calibration instance and per test instance for evaluation, which is 20 × 4,800 replays per arm. Choosing λ̂ is O(|Λ| n) per stratum. Because every instance is replayed on the full grid, the 2,000-draw bootstrap recomputes λ̂ without new simulation.

### 3.5 Online calibration from binary slip feedback

On hardware, F\* labels and replays are unavailable, but whether the object slipped is observed after every grasp. Score-space online quantile tracking (OQT) \cite{angelopoulos2023conformala} updates a per-stratum log-force offset:

$$q_{t+1} = q_t + \eta\,(\mathrm{slip}_t - \alpha), \qquad F_t = \min\big(F_{\max},\, \hat g(x_t)\, e^{q_t}\big),$$

initialised at the stratum's offline $\hat q$. The step size is pre-registered as η = 0.1 × IQR of the in-distribution calibration scores, which gave η = 0.03412. Anti-windup suppresses the update on a step whose force was capped at F_max. We track in score space rather than with adaptive conformal inference's level update \cite{gibbs2021adaptive}, because a friction drop shifts every score by about +0.51 in log-force. That can exceed the largest offline score, at which point a level-indexed tracker saturates at F_max. Reference arms are decaying-step OQT \cite{angelopoulos2024online}, frozen offline calibration, and an oracle that recalibrates with labelled instances from the shifted distribution.

## 4 Experimental Setup

**Simulator and objects.** All experiments run in MuJoCo 4.0.0 (timestep 0.002 s, elliptic friction cone, impratio 10, condim 6, solref (0.004, 1), solimp (0.95, 0.99, 0.001)). The physics configuration is identical for every family and every shift, which a unit test asserts on the compiled models. The parallel-jaw gripper has a force-controlled closing axis and one touch grid per pad. Fast simulated tactile sensing has been demonstrated at scale \cite{wang2022tacto, akinola2025tacsl, leins2025hydroelastictouch}, and tactile configuration and modality matter for learned manipulation \cite{luu2025manifeel, birtalan2026impact}. We use MuJoCo's built-in pad grids with the explicit noise model of Section 3.2 rather than a rendered visuotactile sensor. The in-distribution families are F1 boxes, F2 cylinders, F3 ellipsoids and capsules, and F4 two-body composites with an off-centre CoM. F5, thin plates (box geoms of at most 5 mm thickness) and disks, is held out as a new-family shift and uses the same collision primitives as F1/F2. Friction is log-uniform on [0.3, 1.0] and mass log-uniform on [0.05, 1.0] kg. The CoM offset is uniform up to 40 % of the half-extent along the jaw-parallel axis, and up to 60 % for F4. Disturbances are D1 lift acceleration U[1, 10] m/s², D2 shake of amplitude U[5, 20] mm at U[2, 5] Hz, D3 lateral pull U[0.5, 2]·m g, and D4 payload U[0.2, 1.0]·m added mid-hold. Every object receives exactly one instance per disturbance type, each with its own pose offset.

**Splits.** Splits are by object within each family: train objects 0–149, selection 150–199, calibration 200–324, test 325–499. Calibration therefore has n = 500 instances per disturbance stratum (2,000 in total) and test has 2,800 instances. The selection split (800 instances from 200 objects) is used only to choose COMP and to centre the λ-grids. Pilot objects, used to set the detector constants and project power, are disjoint from all of these.

**Shifts and streams.** We use four shifts: S1 lowers friction (μ × 0.6), S1m lowers it mildly (μ × 0.9, not a primary shift), S3 scales every disturbance amplitude by 1.5, and S2 introduces the new family F5. S1, S1m and S3 re-simulate the id test objects with only the shifted parameter changed. Test objects 325–368 per family serve as oracle-recalibration objects, and objects 369–499 (2,096 instances) form the stream. S2 uses 550 F5 objects, with objects 0–174 for the oracle and 175–549 (1,500 instances) for the stream. A stream has T = 2,000 steps: steps 1–500 are in-distribution, drawn from the unshifted instances of the oracle objects, and steps 501–2,000 are shifted. The evaluation window is steps 1,001–2,000. Each shift has 20 orderings. Feedback in the 20-ordering streams is the label rule slip_t = 1{F_t < F\*_hi,t}. Two direct-replay audits on ordering 0 measure the physical outcome: OQT-CertGrip and OQT-COMP over steps 501–1,000, and OQT-CertGrip and Oracle-CertGrip over the whole window.

**Metrics and decision rules.** The efficiency metric is RE against F\*_mid with D as the effect size (Section 3.1). Robustness re-computes RE with F\*_lo and F\*_hi. Validity is the physical slip rate in direct replay. The four core decisions use a Bonferroni split of a 5 % family-wise level, one-sided 0.0125 each. All intervals CI\*\* are two-sided 97.5 % percentile intervals from 2,000 object-cluster bootstrap draws that resample calibration and test objects within family (all four instances of an object move together) and recompute λ̂ or q̂ per draw. The rules are:
- **H1** is confirmed iff the one-sided 98.75 % Clopper–Pearson upper limit of the non-monotone rate is ≤ 2 % (at most 7 of 800) and the H1-V physical-minus-label disagreement Δ has CI\*\* upper limit ≤ 0.02.
- **H2a (primary)** requires D ≥ 0.10 (the smallest effect size of interest, SESOI), a CI\*\* lower limit > 0, and both conditions again with F\*_lo and F\*_hi in place of F\*_mid.
- **H2b (co-primary)** compares CertGrip-full with CSF-μ̂ at σ = 0.2. It declares superiority on the H2a rule and equivalence if the CI\*\* lies inside ±0.10 (two one-sided tests, TOST).
- **H3** passes iff the CI\*\* upper limit of R_E = RE_window(OQT-CertGrip)/RE_window(Oracle-CertGrip) is < 1.10 for each of S1, S2 and S3, and the realised physical slip rates of the two arms in the window differ by ≤ 0.02.

Secondary analyses (pre-registered in 07 and operationalised in 08f–08h before computation) are unadjusted and labelled as such. We also report σ\*, the smallest σ at which the CI\*\* lower limit of D(H2a) falls below 0.10.

**Hyperparameters and reproducibility.**

| Item | Value |
|---|---|
| Preload / squeeze | F₀ = 32.7 N for 0.4 s; F₀ → 1.5 F₀ → F₀ over 0.3 s |
| Probe | F₀ → 0.005 F₀ log-linear over 0.25 s; return in 0.02 s, hold 0.1 s |
| Detector | 500 Hz; 6-frame smoothing; 8-frame rise < ½ stick rise, 2 consecutive frames; armed at r > 0.1 |
| Taxel noise | multiplicative lognormal 0.05; additive 0.002 N; channel gain lognormal 0.10 |
| Onset noise σ | {0, 0.1, 0.2, 0.4}; primary 0.2 |
| Labels | log bisection on [0.1, 100] N, 11 replays |
| Target level α | 0.10 (H1-V, H1c and H2-n also at other levels) |
| Calibration size | n = 500 per stratum (H2-n: 50) |
| CRC grid (08c) | q̂_sel + linspace(−0.4, 0.4, 20), pooled |
| CRC grid (08e, post hoc) | q̂_sel,d + linspace(−0.8, 0.8, 41), per stratum |
| Learner | gradient-boosted quantile trees, τ = 1 − α; 30-config random search, 4-fold object-grouped CV, identical for all feature sets; scikit-learn HistGradientBoostingRegressor (quantile loss); search space (code/certgrip/models.py): learning rate log-uniform on [0.02, 0.3], max_iter ∈ {100, 200, 400, 800}, max_leaf_nodes ∈ {7, 15, 31, 63}, min_samples_leaf ∈ {5, 10, 20, 40}, l2_regularization ∈ {0, 0.1, 1}; selected configurations are logged with each fit |
| OQT | η = 0.03412; anti-windup at F_max; one tracker per stratum |
| Seeds | predictor seed 0 primary, seeds 1–4 refit; onset ε per instance; stream orderings `default_rng([4242, shift, ordering])` |
| Inference | 2,000 object-cluster bootstrap draws; CI\*\* 97.5 %; SESOI 0.10 |

**Compute.** Simulation is CPU-only. A replay costs about 0.01 s and is bit-identical across repeats on the same machine. The main simulation therefore needs about 2–3 CPU-hours, run as sharded jobs on free GitHub Actions runners.

**Deviations from the pre-registration.**
1. The CRC route (08c) was written after the H1-M counts were seen and before any predictor existed.
2. The 08c λ-grid had a floor defect: λ̂ sat at grid index 0 in D1/D2 for CSF-μ̂ at σ ≤ 0.2, and at index 1 for CSF-1. A post hoc per-stratum 41-point grid (08e) was added. Under its pre-fixed reporting rule it can mark an 08c result as unreliable but cannot upgrade a decision.
3. The pre-registration lists the selection objects once as 200–249 (08b §3) and elsewhere as 150–199 (08b §5, 08c). The code and the logged selection used 150–199.
4. The probe arm's H3-B prediction was never specified and is untested. D-μ was computed on calibration plus test rather than on train objects. The H2-M mass-noise draw was fixed only in 08h.
5. The H3-L TOST was evaluated after the ρ − ρ_ID read-out had been seen.

## 5 Results

### 5.1 Main comparison (H2a, primary)

COMP selection returned CSF-1 (selection-split mean RE 0.7686, against 0.8294 for Mondrian-CSF and 0.8335 for CertGrip-P). Table 1 gives the pre-registered read-out. On the 2,800 test instances, CertGrip-full at σ = 0.2 has RE 0.4567 against 0.7832 for CSF-1, which gives D = 0.4168 with CI\*\* [0.3484, 0.4778]. The point estimate exceeds the SESOI of 0.10 and the lower limit is far above 0, so H2a is decided as superiority. The robustness requirement holds: with F\*_lo and F\*_hi in place of F\*_mid, D is 0.4150 and 0.4186. The physical test slip rate is 0.0829 for CertGrip-full and 0.1021 for CSF-1. The latter is marginally above α, which a guarantee on the expectation permits on a finite test set.

The superiority holds across every pre-registered robustness view, though not in the H2-R sub-pool discussed below. It holds on the label route (D 0.4292), under the post hoc 08e grids (0.4289), for refits with seeds 1–4 (08c 0.3932–0.4494; label route 0.4145–0.4442), against Mondrian-CSF (0.4381), and with only 50 calibration instances per stratum (0.4146 at α 0.10, 0.4654 at α 0.20). Across the 16 family × disturbance cells, the random-effects pooled D is 0.4388 (τ = 0.0511). The smallest cell is F1D3 at 0.2979, and every cell has a CI\*\* lower limit above 0.16, so no cell violates the safety guard. The tail does not pay for the mean: the ratio of 95th-percentile relative excess is T = 0.5918 [0.5540, 0.6564]. The probe arm closes 0.5172 [0.4489, 0.5762] of the gap between CSF-1 and the privileged oracle (label route; oracle RE 0.1271). The advantage shrinks with onset noise: at σ = 0, 0.1, 0.2 and 0.4, D(H2a) is 0.6789, 0.5825, 0.4168 and 0.1401. At σ = 0.4 the lower limit is 0.0832, below the SESOI, so σ\* = 0.4.

| Comparison (α 0.10, test) | Route | D | CI\*\* | Decision |
|---|---|---|---|---|
| **H2a: CertGrip-full σ0.2 vs CSF-1** | CRC 08c | **0.4168** | [0.3484, 0.4778] | superiority |
| H2a with F\*_lo / F\*_hi | CRC 08c | 0.4150 / 0.4186 | [0.3468, 0.4758] / [0.3501, 0.4798] | holds |
| H2a | label rule | 0.4292 | [0.3654, 0.4822] | superiority |
| H2a (post hoc grids) | CRC 08e | 0.4289 | [0.3577, 0.4770] | superiority |
| H2-C vs Mondrian-CSF | label rule | 0.4381 | [0.3733, 0.4872] | superiority |
| H2-H pooled over 16 cells | label rule | 0.4388 | τ = 0.0511 | no harmful cell |
| H2-T (P95 ratio T) | CRC 08c | 0.5918 | [0.5540, 0.6564] | pass (< 1.10) |
| **H2-R narrow-μ, mid-amplitude sub-pool** | label rule | **−0.2614** | [−0.5320, −0.0325] | method worse |

*Table 1. Main comparison and robustness. Arm RE (CRC 08c): CertGrip-full 0.4567 [0.4079, 0.5033], physical slip 0.0829; CSF-1 0.7832 [0.6968, 0.8583], physical slip 0.1021. Rows other than H2a are secondary and unadjusted.*

### 5.2 Where the saving comes from

Table 2 walks the feature chain on the label route (secondary). Static touch at the lifted preload adds nothing over proprioception: D(S vs P) = −0.0084 [−0.0360, 0.0128], equivalent within ±0.05. There is no evidence that the squeeze helps: D(full vs S) = −0.0263 [−0.0558, 0.0149], and equivalence within ±0.03 is not shown either. Adding the onset feature is where the change occurs, with D(CertGrip-full vs full) = 0.4739 [0.4148, 0.5229]. Conversely, the touch and squeeze features add nothing measurable to onset-only on the CRC route: onset-only reaches RE 0.4336 with physical slip 0.0857, and D(CertGrip-full vs onset-only) = −0.0534 [−0.1233, 0.0508] (H4e not confirmed; the label route gives −0.0417, recorded as equivalence). Shuffling the non-proprioceptive features across rows gives D = −0.0253 [−0.0526, 0.0085] against P (H4c inconclusive).

**H2b (co-primary) is not confirmed.** Against the physics plug-in CSF-μ̂, which uses the same noisy onset and has RE 0.4843 and physical slip 0.0657, the learned arm has D = 0.0569 [−0.0399, 0.1454]. The interval contains both 0 and the SESOI. The post hoc 08e grid gives D = 0.0240 with CI\*\* upper limit 0.1001, which lies just above the ±0.10 equivalence margin. The label route gives 0.0134 [−0.0850, 0.0814], inside ±0.10. We do **not** claim equivalence. We also do not claim that the learned model improves on the plug-in at σ = 0.2.

The comparison depends on σ (secondary). On the label route the plug-in is better at σ = 0 (D −0.2022) and σ = 0.1 (−0.0753), the two are equivalent at σ = 0.2, and the learned arm is better at σ = 0.4 (0.3275). The 08e grids agree in direction (σ 0: −0.1522; σ 0.4: 0.3315). The 08c CRC route instead reports H2b superiority at σ = 0 (0.2461) and σ = 0.1 (0.1072). Under the 08e reporting rule we treat these two 08c results as unreliable, because the plug-ins' λ̂ sits at the grid floor in D1/D2.

A friction-information diagnostic supports the attribution. D-μ, the cross-validated R² of log μ on each arm's log-force residual, is 0.7937 for P and 0.6034 for CSF-1, so the no-probe arms leave most of the friction variation unexplained. For CertGrip-full it is 0.0105, 0.0452, 0.2142 and 0.5655 at σ = 0, 0.1, 0.2 and 0.4, and for CSF-μ̂ at σ = 0.2 it is 0.0054. Touch also identifies family (touch-only family accuracy 0.7257 against chance 0.25), but giving both arms the family identity leaves the gain intact: D_FID = 0.4638 against D = 0.4555 without it (H4b, unadjusted secondary). H2-M is descriptive only, because the onset feature confounds m and μ. Without mass, D = 0.4598 (change 0.0042 [−0.0446, 0.0399]). With 10 % mass noise and COMP re-selected (again CSF-1, RE 0.7991), D = 0.4603.

| Ablation (label route unless stated) | D | CI\*\* | Decision |
|---|---|---|---|
| H4a: S vs P (±0.05) | −0.0084 | [−0.0360, 0.0128] | equivalence |
| H4a: full vs S (±0.03) | −0.0263 | [−0.0558, 0.0149] | not confirmed |
| H4a: CertGrip-full vs full (+onset) | 0.4739 | [0.4148, 0.5229] | report only |
| H4e: CertGrip-full vs onset-only (CRC 08c) | −0.0534 | [−0.1233, 0.0508] | not confirmed |
| **H2b: CertGrip-full vs CSF-μ̂, σ0.2 (CRC 08c)** | **0.0569** | [−0.0399, 0.1454] | **not confirmed** |
| H2b (CRC 08e, post hoc) | 0.0240 | [−0.0949, 0.1001] | not confirmed |
| H2b (label rule) | 0.0134 | [−0.0850, 0.0814] | equivalence (secondary) |
| H4c: shuffled vs P (±0.05) | −0.0253 | [−0.0526, 0.0085] | inconclusive |
| H4b: D_FID (both arms given family ID) | 0.4638 | [0.3940, 0.5135] | D_FID ≥ 0.5 D |
| H4d: D_F4 − D_F1 | 0.0342 | [−0.0424, 0.1138] | inconclusive |

*Table 2. Attribution ablations. All rows except H2b are secondary and unadjusted.*

### 5.3 Where it fails

H2-R recalibrates both methods inside the sub-pool with μ ∈ [0.5, 0.8] and disturbance amplitude in the middle 50 % of each type's range (n_cal 352, n_test 548). There the probe arm is worse than CSF-1: D = −0.2614 [−0.5320, −0.0325]. This is a secondary analysis that carried no registered prediction. A plausible reading is that a narrow friction range removes the variation the probe measures while the probe's noise remains. We did **not** test this explanation. The CoM mechanism test H4d is inconclusive (D_F4 − D_F1 = 0.0342 [−0.0424, 0.1138]).

### 5.4 Validity of the certificate

H1 is not confirmed. The monotonicity gate found 8 non-monotone instances of 800, giving a Clopper–Pearson upper limit of 0.02115 > 0.02. Seven of the eight occurred under D2 (shake). The violations are small: the largest slip force above F\*_hi exceeds it by a relative 0.00904. The physical audit H1-V passes for all four arm × α combinations. The label rule slightly over-counts slips, with Δ ranging from −0.00429 (CertGrip, α 0.10) to −0.00143 (CertGrip, α 0.05). The label-route split-conformal unit test UT3 passes 160 of 160 cells. Twenty of these (α 0.01, n 50) are degenerate, so the informative count is 140 of 140. Uncalibrated targeters over-slip. RAW-Q and RAW-G exceed α at every level (slip − α between 0.0096 and 0.0507, every CI\*\* above 0). At α = 0.05, however, their intervals ([0.020, 0.045] and [0.016, 0.042]) do not exclude the pre-registered +0.025 margin, so H1c is not confirmed.

### 5.5 Online calibration under shift

Table 3 summarises the streams. Frozen offline calibration breaks under the friction and amplitude shifts. Frozen-CertGrip's window slip reaches 0.3056 (S1) and 0.2461 (S3), and Frozen-COMP's reaches 0.5101 (S1). Neither frozen arm breaks under S2. OQT-CertGrip holds the window label-rule slip between 0.0999 and 0.1016 across shifts, and the direct-replay audit of ordering 0 gives physical rates of 0.103 (S1), 0.092 (S2) and 0.101 (S3). OQT-CertGrip also needs less force than OQT-COMP in every shift (S1 RE 0.4763 against 0.8087). Whether its log-ratio advantage over COMP is preserved under S1 was tested by ρ − ρ_ID = 0.0857 [−0.0444, 0.1859]. The interval does not lie inside the ±0.05 TOST margin, so H3-L is not confirmed.

**H3 is inconclusive** in all three shifts. R_E is 0.8778 [0.7404, 1.1204] in S1, 1.1739 [1.0234, 1.4283] in S2 and 0.9629 [0.8363, 1.1449] in S3. The realised CI\*\* half-widths, about 0.15–0.20, are wider than the projected ≈ 0.12. The matched-rate co-requirement fails in S1 (physical difference 0.032) and S2 (−0.035), and holds in S3 (0.009). The direction of R_E follows the slip mismatch: the oracle under-slips in S1 and over-slips in S2. R_E is therefore not a like-for-like efficiency comparison in S1 and S2. In S1m, R_E has an upper limit below 1.10 (0.8871 [0.7723, 1.0265]), but the window label-rule slip rates differ by 0.0248 > 0.02, so the full criterion is not met. Constant η beats decaying η in catch-up: the cumulative excess slips over the first 500 shifted steps are larger for the decaying schedule by ΔC = 58.15 [48.20, 70.20] in S1 and 42.40 [32.40, 49.35] in S3 (H3-S, unadjusted). No step was capped at F_max in any window.

| Shift | OQT-CertGrip slip / RE | OQT-COMP RE | Frozen-CertGrip / Frozen-COMP slip | Oracle-CertGrip slip / RE | R_E [CI\*\*] | H3 |
|---|---|---|---|---|---|---|
| S1 (μ × 0.6) | 0.1016 / 0.4763 | 0.8087 | 0.3056 / 0.5101 | 0.0751 / 0.5426 | 0.8778 [0.7404, 1.1204] | inconclusive |
| S2 (F5) | 0.0999 / 0.4262 | 0.7398 | 0.1017 / 0.1051 | 0.1346 / 0.3631 | 1.1739 [1.0234, 1.4283] | inconclusive |
| S3 (amp. × 1.5) | 0.1000 / 0.5067 | 0.8635 | 0.2461 / 0.1910 | 0.0863 / 0.5262 | 0.9629 [0.8363, 1.1449] | inconclusive |

*Table 3. Online calibration, window steps 1,001–2,000, label-rule slip averaged over 20 orderings, α = 0.10.*

## 6 Discussion

**What the evidence licenses.** The confirmed claim is narrow and, we think, useful. A friction-onset probe of a quarter second, read by a touch-only detector, carries enough friction information that a conformally certified grip force needs about 42 % less relative excess force than the best non-tactile conformal method. This holds at a physical slip rate that conformal risk control bounds in expectation. The ablations say where the saving comes from. Static touch and the squeeze carry essentially no friction information in our protocol, as the pilot had already suggested, while the onset feature carries almost all of it. The residual-friction diagnostic tells the same story: no-probe arms leave a cross-validated R² of 0.7937 (P) between log μ and their residual, against 0.0054 for the plug-in fed by the onset. At σ = 0.2, learning on top of the onset shows no demonstrated gain over the one-line physics formula that uses the same onset (H2b not confirmed). In the secondary, unadjusted σ sweep, the learned model is better at σ = 0.4 and worse at σ = 0. One reading is that a learner pays off only when the friction reading is noisy enough that other cues help to denoise it. Conformal calibration is what makes the saving *certifiable*, and the probe is what makes it *large*.

**Unexpected results.** Three outcomes departed from the plan. First, the monotonicity premise failed narrowly (8 of 800), mostly under shake. The violations sit within 1 % of F\*_hi, and the physical audit shows the label rule erring on the safe side. Still, the failure forced the switch to CRC on the physical loss, and it is why we present that route, not the label route, as primary. Second, the narrow-friction, mid-amplitude sub-pool reverses the main result. The probe is therefore not a free lunch. When friction varies little, a noisy friction reading can cost more than it gains, and practitioners should expect the advantage to scale with the friction spread of their object set. Third, the online efficiency comparison was underpowered and confounded by unequal realised slip rates between the tracker and the oracle, so H3 could not be decided in either direction.

**Relation to prior work.** Friction-estimating grip controllers \cite{khamis2021real, niu2026synchronized} and incipient-slip methods \cite{dong2019maintaining, boonstra2024estimate} use the same physical cue as our probe but leave the safety margin as a design parameter. Our results suggest that this cue, combined with a calibration step that requires no friction model, already provides most of the attainable saving relative to a friction-blind certified baseline. The learned components of tactile pipelines should therefore be compared against a calibrated physics plug-in on the same cue, not only against a friction-blind controller. On the conformal side, our online result is in line with the long-run guarantees of quantile tracking \cite{angelopoulos2023conformala} and with the known slow adaptation of decaying steps \cite{angelopoulos2024online}. The physical audit shows that these guarantees carry over to a contact outcome in simulation when the feedback is the slip itself.

**Practical implications.** A robot can run the probe on every grasp at a cost of under 0.4 s (descent, return and hold). The offline certificate requires F\* labels and replays, which only a simulator provides. The deployable route is the online tracker, warm-started from a simulation-calibrated offset and updated from observed slips. It commits the robot to about α T slips over T grasps plus a catch-up transient after a shift. It is therefore suited to objects that can be dropped safely.

## 7 Limitations

All results come from a single simulator (MuJoCo) with five object families and a modelled tactile detector. In simulation the detector recovers friction almost perfectly, so the operating point σ = 0.2 is an assumed noise level, not a measured property of any real sensor. The σ sweep shows that the main effect weakens quickly with noise, and its lower limit falls below the SESOI at σ = 0.4. The offline certificate needs F\* labels and per-instance replays on a 20-point force grid, which exist only in simulation. It is therefore not deployable as is, and online quantile tracking is the route to hardware. Validity rests on the CRC route adopted after the monotonicity gate failed, and the grid repair (08e) is post hoc. The 08c λ-grid floor defect makes the 08c H2b results at σ = 0 and 0.1 unreliable. H2b is unresolved at the primary σ. H3 was underpowered by design, its matched-rate requirement failed in two shifts, and the feedback in its 20 orderings is the label rule, with physical audits for one ordering only. The H2-R sub-pool is a regime in which the method loses, and its cause is untested. The concentration of non-monotone instances under D2 is unexplained. The certificate is marginal over grasps within a disturbance stratum and gives no per-object or per-family guarantee. All secondary analyses are unadjusted for multiplicity, and several (08e, the H3-L TOST) were specified after related read-outs had been seen. Mass is assumed to be measurable during the lift. The no-mass and noisy-mass conditions are descriptive only, because the onset confounds mass and friction.

## 8 Conclusion

We asked whether a tactile probe can make a certified minimal-force grasp substantially gentler, and which component is responsible. In MuJoCo simulation, a ramp-down friction-onset probe combined with conformal risk control on the physical binary slip loss reduces mean relative excess grip force by D = 0.4168 (97.5 % CI [0.3484, 0.4778]) relative to the strongest non-tactile conformal baseline, which was selected beforehand. The test physical slip rate is 0.0829 at α = 0.10. The saving comes from the probe. Static touch and the squeeze contribute nothing measurable, and at the primary onset noise a learned model shows no demonstrated gain over a physics plug-in using the same onset. The result has a stated scope limit: in a narrow-friction, mid-amplitude sub-pool the method is worse than the baseline (D = −0.2614). Under friction, amplitude and new-family shifts, online quantile tracking from binary slip feedback keeps the window slip rate near α where frozen calibration breaks. Whether it does so at a force cost within 10 % of label-based recalibration is inconclusive. Of four pre-registered core decisions, one was confirmed. Future work should measure onset noise on a physical gripper with a real tactile sensor, replace the simulated σ by that measurement, and run an online-only calibration study on hardware, where binary slip feedback is the only signal available.
