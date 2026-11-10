```
FIGURE 1 PROMPT
Full-width, two-panel vector figure for a robotics paper (RSS style), white background, sans-serif labels,
colour-blind-safe palette (learned probe model = deep blue, onset-only learned model = light blue, probe plug-in = teal,
friction-blind conformal baseline CSF-1 = orange, alpha line = dashed grey). Title strip above the panels:
"Probe, then calibrate (simulation)". No inset in either panel.

(a) Protocol timeline with absolute forces (schematic shape, real numbers). x-axis: time within one grasp episode;
y-axis: grip force in N (log scale). Segments, left to right: "preload F0 = 32.7 N (same for every object)" as a flat
line held 0.4 s; "squeeze F0 -> 1.5 F0 -> F0" as a small half-sine bump over 0.3 s; "ramp-down probe" as a
log-linear descent from F0 towards 0.005 F0 over 0.25 s, cut short by a red marker labelled "incipient-slip onset
F_onset -> mu-hat = m g / (2 F_onset)", then a fast return to F0 (0.02 s, held 0.1 s); then "ramp to hold force
F = F_base(x) e^lambda-hat" followed by a shaded "disturbance window (0.6 s)". Shade the squeeze, probe, return and
re-hold segments in light blue and label the bracket "probe-specific phases: 17.96 N s". Over the hold segment draw a
horizontal band with two tick lines: "learned probe model, mean hold force 6.521 N" (blue) and "CSF-1, mean hold force
7.606 N" (orange), and a grey dotted line "median minimal force F*_mid 3.184 N". Side note at right: "break-even hold
time 16.56 s (hold saving vs probe-specific force-time)".

(b) Risk-efficiency frontier (real data, test set, onset noise sigma = 0.2). x-axis: test physical slip rate
(0 to 0.30); y-axis: mean relative excess hold force RE_mid. One solid polyline with markers per arm over
calibration-grid offsets k = -4 ... +4. Points (slip, RE), k = -4 ... +4:
  learned probe model (primary grid): (0.2661, 0.2309) (0.2007, 0.2839) (0.1539, 0.3391) (0.1200, 0.3967)
    (0.0829, 0.4567) (0.0568, 0.5194) (0.0339, 0.5847) (0.0225, 0.6529) (0.0136, 0.7239)
  onset-only learned model (primary grid): (0.2786, 0.2114) (0.2214, 0.2635) (0.1729, 0.3178) (0.1321, 0.3745)
    (0.0857, 0.4336) (0.0568, 0.4952) (0.0404, 0.5595) (0.0250, 0.6266) (0.0157, 0.6965)
  probe plug-in (refined grid, because its primary grid has a floor in D1/D2): (0.2414, 0.2399) (0.1943, 0.2905)
    (0.1446, 0.3432) (0.1032, 0.3980) (0.0750, 0.4551) (0.0582, 0.5144) (0.0404, 0.5763) (0.0296, 0.6406)
    (0.0229, 0.7075)
  CSF-1 (primary grid): (0.1711, 0.6037) (0.1536, 0.6375) (0.1432, 0.6728) (0.1293, 0.7097) (0.1021, 0.7832)
    (0.0743, 0.8599) (0.0436, 0.9398) (0.0168, 1.0233) (0.0100, 1.1103)
Vertical dashed grey line at alpha = 0.10. Mark the CRC operating point (k = 0) of each arm with a larger filled
marker. Vertical double arrow at slip 0.10 between the learned-probe-model curve and the CSF-1 curve, annotated
"D_match = 0.4563 (secondary, slip level read off the test set)". Do not annotate an ordering between the probe-fed
curves. Footer line under both panels: "MuJoCo, rigid contact, modelled touch detector, assumed onset noise
sigma = 0.2, friction log-uniform on [0.3, 1.0]; the offline bound is marginal per disturbance stratum, in
expectation, and needs simulator replays".

Draft caption: Probe, then calibrate (simulation). (a) Every grasp starts from the same 32.7 N preload, so only the
ramp-down probe's onset carries friction information; the method chooses the hold force (mean 6.521 N vs 7.606 N for
the friction-blind baseline), and the probe's own force-time (including the return and 0.1 s re-hold at F0) is
recovered only after a 16.56 s hold. (b) Test physical slip vs relative excess hold force across the calibration grid;
at matched slip 0.10 the probe-fed arms need less excess force than the friction-blind conformal baseline (D_match
0.4563, descriptive). CSF-1's primary-grid λ̂ sits at index 1 in D1/D2, so its lowest offsets are clipped there and the
lower end of the orange curve is flat; the refined grid, where CSF-1 is interior, gives a similar D (0.4289).
```

# Probe, Then Calibrate: Conformal Slip-Risk Control of Grip Force from a Tactile Friction-Onset Probe (a Simulation Study)

## Abstract

We choose a low grip *hold* force whose physical slip rate is at most α. Friction-blind conformal baselines can bound slip but must cover the whole friction range. After a fixed preload, a ramp-down probe lowers the grip until a touch-only detector reports incipient slip, giving a Coulomb friction estimate. A force rule fed with it (a one-line plug-in or a learned quantile model) is calibrated per disturbance stratum by conformal risk control (CRC) on the binary physical-slip loss. The resulting bound holds in simulation, marginally per stratum and in expectation, and needs counterfactual simulator replays. In MuJoCo at α = 0.10, with an assumed onset noise σ = 0.2 and friction drawn on [0.3, 1.0] independently of all other inputs, the one confirmed pre-registered result is that the learned probe model reduces relative excess hold force against the strongest non-tactile conformal baseline by D = 0.4168 (97.5 % CI [0.3484, 0.4778]); mean hold force is 6.521 vs 7.606 N. D falls to 0.1401 at σ = 0.4. Secondary, partly post hoc and grid-dependent analyses (unadjusted) attribute the saving to the probe: the learned model shows no demonstrated gain over a plug-in, and at σ = 0.4 a shrunk plug-in beats it. Where friction spread is narrow (μ ∈ [0.5, 0.8]) the baseline is better (D −0.2614, label route; −0.3152, refined CRC grid). Online, binary physical-feedback tracking returns to α after shift (late-window slip 0.1001–0.1018); efficiency against oracle recalibration is inconclusive.

## 1 Introduction

Many manipulation tasks need the smallest grip force that still keeps the object in the hand through the motions and loads of the task. Excess holding force loads the object and the actuator for the whole hold, and slip prevention at limited force is a recognised concern for prosthetic hands \cite{berman2025autonomous}. Too little force drops the object. Humans resolve this trade-off by scaling grip force to the friction they feel after a brief contact \cite{johansson1984roles} and by re-regulating when friction changes suddenly \cite{willemet2024grip}. Robotic tactile grip regulation pursues the same goal. Controllers monitor incipient slip and tighten the grasp \cite{dong2019maintaining, veiga2020grip, berman2025autonomous}, estimate friction online and add a safety margin \cite{khamis2021real, niu2026synchronized}, or learn a map from tactile signals to a gentle grasp force \cite{boonstra2024estimate}. None of them gives a quantitative, distribution-free statement of the form "this force rule slips on at most a fraction α of grasps". Their margins are set by hand or estimated, and the resulting slip rate is whatever the experiment shows.

Conformal methods provide exactly this kind of statement. Split conformal prediction \cite{lei2017distribution} and conformal risk control \cite{angelopoulos2022conformal} turn any predictor into a rule whose expected loss on an exchangeable test point is bounded by a target level. They need only a held-out calibration set. In grasping, the predictor proposes a force, and calibration inflates it until the slip risk on calibration grasps is at most α. The guarantee is cheap, but its price in force depends on what the predictor knows: a rule that cannot see friction must cover the whole friction range with one inflation factor, which is conservative for most objects. The relevant comparator for a tactile method is therefore not an uncalibrated controller but the *strongest non-tactile conformal baseline*: a rule that uses everything a robot knows without touch and is calibrated to the same α. We selected this comparator on a disjoint selection split before any calibration or test data were read. A friction-blind Coulomb rule, CSF-1 (selection-split mean relative excess 0.7686), beat a Mondrian variant given privileged object-family identity (0.8294) and a learned proprioceptive quantile model (0.8335).

The paper asks one question in three parts. First, can a short tactile probe make a certified physical slip rate of at most α cheaper in hold force? Here "certified" means in simulation, marginal per disturbance stratum and in expectation. Second, which component carries the saving: the probe itself, or a learned model on top of it? Third, does calibration survive distribution shift when the only feedback available on a robot is whether the object slipped?

Our answer combines one mechanism with one statistical tool. The mechanism is the probe. After a fixed preload F₀ = 32.7 N, which is identical for every object and therefore says nothing about mass or friction, the gripper lowers its force until a touch-only detector reports incipient slip. Under Coulomb friction the onset force gives μ̂ = m g/(2 F_onset). The tool is CRC on the binary physical slip loss, applied per disturbance stratum. We use the physical loss because the pre-registered monotonicity premise of the label rule failed in 8 of 800 instances. The offline calibration needs counterfactual replays of every calibration grasp at every grid force, which only a simulator provides; the deployable route is online tracking from one binary outcome per grasp.

**Contributions.**
- **(C1) Probe protocol and calibrated plug-in.** We give a grasp protocol in which a friction-uninformative preload leaves a ramp-down onset probe as the only friction channel. Per-stratum CRC on the monotonised physical binary slip loss turns a one-line Coulomb plug-in on that onset, or any other probe-fed rule, into a rule with marginal expected slip ≤ α in simulation, given counterfactual replays at every grid force.
- **(C2) Pre-registered evaluation and force accounting.** Against the friction-blind conformal baseline, the learned probe model (the pre-registered probe arm) reduces relative excess hold force by D = 0.4168 [0.3484, 0.4778] and lowers mean hold force by 1.085 N on the primary test split. This is the only confirmed pre-registered decision, and its size is conditional on the assumed σ and the independent friction draw. We also count what the fixed protocol costs: the hold saving recovers the probe-specific force-time only after a 16.56 s hold.
- **(C3) Attribution and limits (secondary).** Secondary rows, several post hoc and grid-dependent, locate the saving in the probe rather than the learner: plug-in, shrunk plug-in, onset-only learner, feature chain, a non-tactile friction prior, and uniform and tuned margins. Two reactive slip-tightening controllers serve as a negative control, not as an attribution ablation. We check empirically how the certificate behaves across object re-splits, strata and friction levels, report a sub-pool in which the method loses, and run an online binary-feedback study under three shifts.

Of the four pre-registered core decisions, one is confirmed: the learned probe arm beats the baseline. The label-validity premise and the learned-versus-plug-in decision are not confirmed, and online efficiency is inconclusive (Section 7). Section 2 positions the work. Section 3 defines the problem and method, Section 4 the protocol and statistics, and Section 5 reports results. Sections 6–8 discuss them, state limitations and conclude.

## 2 Related Work

**Friction reading and tactile grip control.** Reading friction from incipient slip is an established idea. Rubber-based tactile sensors were used early on to detect incipient slip and control grip \cite{marconi1996incipient}. Surveys of tactile friction estimation and slip detection \cite{chen2018tactile, romeo2020methods} describe a mature literature in which incipient slip, the partial slip at the contact periphery that precedes gross sliding, is the key friction cue, and in which the frictional properties of the interface determine the minimum grip force. Human precision grip adapts force to surface friction \cite{johansson1984roles} and to sudden friction changes \cite{willemet2024grip}. On the robot side, slip detectors on multifingered hands \cite{james2020slip}, learned temporal detectors on barometric sensors \cite{grover2022detect} and reactive multifingered controllers that combine slip onset with internal-force optimisation \cite{ayral2026reactive} trigger corrective tightening. Closer to minimal-force grasping, \cite{dong2019maintaining} keep grasps within slipping bounds by monitoring incipient slip, \cite{khamis2021real} estimate friction in real time and add a margin to the target force, \cite{boonstra2024estimate} learn to estimate incipient slip for gentle grasping, and \cite{niu2026synchronized} couple online friction estimation with adaptive grasp control. Learned and reflex controllers extend this to dynamic interaction \cite{kuo2025tracing}, vision-tactile reflexes \cite{feng2026tactilereflex} and sim-to-real force policies \cite{lach2024zero}. Adaptive analytical controllers come with Lyapunov arguments \cite{almohammed2022switched}, independent finger controllers stabilise grasps \cite{veiga2020grip}, and vision-language models select pre-grasp forces from experience \cite{shang2026exp}. In all of these the margin is reactive, hand-set or estimated, and none states a distribution-free bound on the resulting slip rate. We evaluate two stand-ins for this family: a reactive slip-tightening controller and an estimate-plus-tuned-margin rule (Section 5.3).

**Robust grasping under uncertainty.** Model-based approaches bound the risk of losing a grasp through assumed uncertainty sets. Grasping-force optimisation has been examined under parameter uncertainty \cite{cloutier2018examining}. Control barrier functions enforce friction-cone constraints \cite{cortez2019control} and, combined with disturbance observers and tactile sensing, give adaptive safe grasping \cite{kim2024robust}. Friction-informed risk margins \cite{enwerem2026firmgrasp} and variational belief parameterisations \cite{enwerem2026variational} make grasp synthesis tolerant of multimodal uncertainty. These guarantees hold relative to a model and its uncertainty set. Ours holds relative to the data-generating distribution of grasps without a friction model, at the price of being marginal over grasps and of needing calibration data from that distribution.

**Conformal prediction and risk control.** Conformal prediction gives finite-sample, distribution-free guarantees under exchangeability \cite{vovk2005algorithmic, lei2017distribution, angelopoulos2023conformal}. Conformalized quantile regression adapts the guarantee to the input \cite{romano2019conformalized}, and training-conditional \cite{bian2023training} and class-conditional \cite{ding2023class} variants refine the marginal statement. Conformal risk control generalises coverage to bounded monotone losses \cite{angelopoulos2022conformal}, with extensions to non-monotone losses \cite{angelopoulos2026conformal} and non-exchangeable data \cite{farinhas2023non}. Learn-then-Test gives high-probability risk control by multiple testing \cite{angelopoulos2025learn}. Under shift, adaptive conformal inference \cite{gibbs2021adaptive, gibbs2022conformal}, conformal PID control and quantile tracking \cite{angelopoulos2023conformala}, decaying step sizes \cite{angelopoulos2024online} and semi-bandit feedback \cite{ge2024stochastic} keep long-run coverage near the target. In robotics, conformal tools certify decisions \cite{lekeufack2024conformal}, verification and control \cite{lindemann2025formal, lindemann2023conformal}, motion planning among dynamic agents \cite{dixit2022adaptive}, contact-aware state estimation \cite{marques2026particle}, LLM planners \cite{ren2023robots}, sensorimotor policies under shift \cite{huang2023conformal}, RL safety filters \cite{strawn2023conformal}, safe Bayesian optimisation \cite{zhang2024bayesian}, interactive imitation learning \cite{zhao2024conformalized} and perception-planning pipelines \cite{kumar2026learnable}. In these works the controlled quantity is a prediction set, a trajectory region or a decision loss. None of them calibrates a physical contact outcome as a binary loss over a family of grip forces.

**Novelty.** Reading friction from slip onset is not new, and CRC, Learn-then-Test and score-space quantile tracking are used here as published. The paper contributes three things. First, a protocol in which the onset is the *only* friction channel, so that its value can be isolated. Second, a per-stratum, marginal bound on the *physical* slip rate of the resulting hold force, valid in simulation. Third, an attribution study showing that the calibrated saving comes from the probe and not from the learned model.

## 3 Problem Formulation and Method

### 3.1 Problem

A grasp instance x comprises an object (family, geometry, mass m, friction coefficient μ, centre-of-mass offset), a grasp pose offset, and a disturbance of known type d ∈ {D1, D2, D3, D4} (lift acceleration, shake, lateral pull, payload added mid-hold) with a hidden amplitude. A parallel-jaw gripper commands a hold force F, and slip(F, x) ∈ {0, 1} is the physical outcome of a full episode. A slip is a tangential displacement of the object relative to the pad frame above 2 mm, a rotation about the grasp axis above 3°, or loss of pad contact. The minimal no-slip force F\*(x) is bracketed in simulation by log-space bisection on [F_min, F_max] = [0.1, 100] N, using one replay at F_max and 10 halvings (11 replays). This gives F\*_lo < F\*_hi and F\*_mid = √(F\*_lo F\*_hi). A force rule is scored by its mean relative excess and its physical slip rate,

$$\mathrm{RE}(F) = \mathbb{E}_x\big[(F(x) - F^*_{\mathrm{mid}}(x))/F^*_{\mathrm{mid}}(x)\big], \qquad \mathrm{SR}(F) = \mathbb{E}_x[\mathrm{slip}(F(x), x)].$$

RE is signed, includes slipped instances, and is computed over avoidable instances (F\*_hi ≤ F_max). The task is

$$\min_F \ \mathrm{RE}(F) \quad \text{s.t.} \quad \mathrm{SR}(F) \le \alpha,$$

with the constraint enforced without a contact model, from calibration instances drawn from the test distribution. Two rules A and B are compared on identical test instances by $D = 1 - \mathrm{RE}(A)/\mathrm{RE}(B)$, so D > 0 means that A needs less excess force. D is a reduction in relative excess, not a share of hold force. The F\* labels exist only in simulation.

### 3.2 Grasp protocol and the friction-onset probe

Every method runs the same protocol, so every method sees the same physical history up to the moment it chooses F. The gripper closes to a constant preload F₀ = 32.7 N (m g/μ with m_max = 1 kg and μ_min = 0.3) and holds it for 0.4 s. Because F₀ is the same for every instance, it encodes neither mass nor friction. A squeeze F₀ → 1.5 F₀ → F₀ follows over 0.3 s. Then comes the **ramp-down probe**: the force falls log-linearly from F₀ towards 0.005 F₀ over 0.25 s. A detector that reads only the pad touch grids computes the shear/normal ratio r = Σ_pads |shear| / Σ normal from noisy taxels and declares onset when the smoothed log r stops rising (constants in Table A1). At onset the force returns to F₀ within 0.02 s and holds for 0.1 s. The gripper then ramps to the chosen hold force F, settles, and runs the 0.6 s disturbance window. The slip reference is the pose before the probe, so a slip during the probe counts as a slip of the grasp.

The onset gives the Coulomb reading μ̂ = m g/(2 F_onset), clipped to [0.1, 3]. Simulated touch is cleaner than a real sensor, so we add onset noise in log units, $\tilde f = \log F_{\mathrm{onset}} + \sigma\varepsilon$ with $\varepsilon \sim \mathcal{N}(0,1)$ drawn once per instance and σ ∈ {0, 0.1, 0.2, 0.4}. All core decisions use **σ = 0.2**, an assumed level. The same noisy onset is passed to every arm that uses it.

The protocol is fixed. Preload and squeeze are protocol constants that exceed every test instance's F\*_mid (Section 5.1), and the probe induces micro-slip on every grasp by design. The method chooses only the hold force, and "minimal force" in this paper refers only to that force.

### 3.3 Force rules

Every rule has the form

$$F(x;\lambda) = \min\big(F_{\max},\, F_{\mathrm{base}}(x)\, e^{\lambda}\big),$$

where λ is a log-force offset set by calibration. The rules differ only in $F_{\mathrm{base}}$ and in what it may read. Mass is given to every method, on the stated assumption that a robot can weigh the object during the lift. External disturbance amplitudes (D3, D4) are hidden from all methods.

- **Probe plug-in** (the simplest instance of the method): $F_{\mathrm{base}} = m(g + a_{\mathrm{cmd}})/(2\hat\mu)$, with μ̂ from the noisy onset.
- **Shrunk probe plug-in:** the same formula with $\log\hat\mu_s = a + b\log\hat\mu$. The coefficients (a, b) come from an ordinary-least-squares fit of log μ on log μ̂ over the selection split only (800 instances). At σ = 0.2 this gives a = −0.3858, b = 0.7397; at σ = 0.4, a = −0.4738, b = 0.4044. The fit uses the true μ of the selection objects, so it is a simulator-only ingredient; on hardware it would need a reference set of known materials.
- **Learned probe model (optional):** a gradient-boosted quantile predictor ĝ(x) at level τ = 1 − α, trained on bisection F\* labels, which are also available only in simulation. Its feature sets are nested: P (proprioception: disturbance type, commanded acceleration, log mass, aperture at contact) ⊂ S (+ static touch) ⊂ full (+ squeeze features) ⊂ learned probe model (+ onset). The onset-only model is P plus the onset feature.
- **Non-tactile baselines:** CSF-1, $F_{\mathrm{base}} = m(g + a_{\mathrm{cmd}})/(2\bar\mu)$ for D1/D2 and $m g/(2\bar\mu)$ for D3/D4, with $\bar\mu$ the geometric mean of the friction range. Mondrian-CSF uses the same formula with one offset per family × disturbance cell \cite{ding2023class}, so it is given privileged family identity. A non-tactile friction prior replaces $\bar\mu$ by $\tilde\mu = \mathrm{clip}(\mu\, e^{\sigma_p \varepsilon_p}, 0.1, 3.0)$, σ_p ∈ {0.2, 0.4, 0.8}. This prior is an oracle-side construction that asks how good a friction prior from material or vision would have to be; it is not a deployable estimator. The friction-blind conformal baseline was chosen from CSF-1, Mondrian-CSF and the learned proprioceptive model on the selection split, before any calibration or test access.
- **Uncalibrated and tuned tactile alternatives.** (i) *Probe + one uniform margin:* F = (1 + κ)·F_base^μ̂ with κ ∈ {0, 0.25, 0.5, 1.0}. (ii) *Probe + empirically tuned per-stratum margin:* the smallest grid λ whose calibration physical slip is ≤ α, with no (n + 1) correction. (iii) *Reactive slip-tightening (negative control):* the hold starts at c times an uncalibrated nominal force, c ∈ {0.5, 0.75}. During the hold, the same noisy-taxel ratio is read every 10 ms and smoothed over 6 frames. On each detection of r̄ > r_safe on 2 consecutive frames, F ← min(F_max, 1.25 F), ramped over 20 ms, with at most 4 steps. The friction-blind variant (REACT-blind) uses r_safe = 0.8·μ_min and the CSF-1 nominal force. The probe-informed variant (REACT-probe) uses r_safe = 0.8·μ̂ and the plug-in force. A slip before tightening counts.

The noise models of the probe and the prior differ. Since μ̂ = m g/(2 F_onset), noise on the onset force is noise on the friction estimate: σ perturbs log F_onset, and hence log μ̂, on top of the detector's own bias and error. σ_p perturbs a clipped log-normal friction prior. Equal nominal values of σ and σ_p are therefore not claimed to mean equal estimate quality.

### 3.4 Calibration on the physical binary loss

For an arm with base force $F_{\mathrm{base}}$ and calibration instance i, define the physical loss and its monotonised version on a grid Λ,

$$L_i(\lambda) = \mathbb{1}\{\text{slip in a direct replay at } F(x_i;\lambda)\}, \qquad \tilde L_i(\lambda) = \max_{\lambda' \ge \lambda,\ \lambda' \in \Lambda} L_i(\lambda').$$

$\tilde L_i$ is non-increasing in λ and $\tilde L_i \ge L_i$, so a risk bound on $\tilde L$ implies the same bound on physical slip.

**CRC (primary).** Within each stratum, with n = 500 calibration instances and $\tilde R_n(\lambda) = \frac{1}{n}\sum_i \tilde L_i(\lambda)$,

$$\hat\lambda = \min\Big\{\lambda \in \Lambda : \frac{n \tilde R_n(\lambda) + 1}{n + 1} \le \alpha\Big\},$$

and λ̂ = max Λ if no grid point qualifies. By \cite{angelopoulos2022conformal}, a test instance exchangeable with the stratum's calibration instances satisfies E[slip at F(x; λ̂)] ≤ α. The bound is marginal over instances and friction values, holds per stratum, and holds in expectation over the calibration draw. It is not a guarantee for one calibration set, one object or one friction level.

**Learn-then-Test (secondary).** Per stratum, λ is scanned from the top of the grid downwards and kept while the one-sided Clopper–Pearson upper bound at δ = 0.1 on the calibration physical risk is at most α \cite{angelopoulos2025learn}. This gives P(risk ≤ α) ≥ 1 − δ per stratum over the calibration draw, the training-conditional view of \cite{bian2023training}. It is not family-wise across strata.

**Grids.** The primary grid has 20 points, Λ = q̂_sel + linspace(−0.4, 0.4, 20), centred on the arm's label-rule conformal quantile on the selection split and pooled over strata. A post hoc refined grid with 41 points per stratum, q̂_sel,d + linspace(−0.8, 0.8, 41), serves as a sensitivity route. A grid-edge rule re-runs an arm on the refined-grid recipe if a stratum's λ̂ lands on index 0 or 19. Because that choice depends on the calibration data, and the refined grid was adopted after the primary-grid floor was seen, edge-rule and refined-grid rows are not covered exactly by the CRC theorem as run; only primary-grid CRC rows are.

**Why the physical loss.** The pre-registered certificate was split conformal on bisection labels with the one-sided score $s = \log F^*_{\mathrm{hi}} - \log \hat g(x)$ \cite{romano2019conformalized}. It transfers to physical slip only if slip is monotone in F. The monotonicity gate tested this on 800 instances and failed: 8 instances were non-monotone, the one-sided 98.75 % Clopper–Pearson upper limit (the Bonferroni-split level) was 0.02115 > 0.02, and 7 of the 8 were under D2. CRC on the physical loss needs no monotonicity, so it became the primary route, and the label route is reported as secondary.

**Deployability.** The offline calibration needs a replay of each calibration grasp at every grid force, so it is a simulation procedure. The online tracker of Section 3.5 needs only one binary outcome per grasp.

```
Algorithm 1: probe, then calibrate (per arm, per disturbance stratum d)
input : base-force rule F_base (probe plug-in, shrunk plug-in or learned model), grid Lambda,
        calibration instances {x_i} in stratum d, level alpha
0  every instance: preload F0, squeeze, ramp-down probe -> F_onset (+ onset noise sigma); F_base(x) uses it
1  for i in calibration set, for lambda in Lambda:
2       L[i, lambda] <- slip of a direct replay at min(F_max, F_base(x_i) * exp(lambda))
3  Ltilde[i, lambda] <- max_{lambda' >= lambda} L[i, lambda']                       # monotonise
4  CRC: lambda_hat <- first lambda with (sum_i Ltilde[i, lambda] + 1)/(n + 1) <= alpha, else max(Lambda) (flag)
5  LTT: scan lambda downwards from max(Lambda); keep while CP_upper(risk at lambda; delta) <= alpha
6  deploy: preload, squeeze, probe -> F_onset; command F = min(F_max, F_base(x) * exp(lambda_hat))
```

**Complexity.** Calibration needs |Λ| replays per instance and O(|Λ| n) work per stratum; because every instance is replayed on the full grid, the bootstrap refits λ̂ without new simulation. Deployment costs one probe and a closed-form force.

### 3.5 Online calibration from binary feedback

On hardware, F\* labels and replays are unavailable, but whether the object slipped is observed after every grasp. Score-space online quantile tracking \cite{angelopoulos2023conformala} updates one log-force offset per stratum,

$$q_{t+1} = q_t + \eta\,(\mathrm{slip}_t - \alpha), \qquad F_t = \min\big(F_{\max},\, F_{\mathrm{base}}(x_t)\, e^{q_t}\big),$$

with η = 0.1 × IQR of the in-distribution calibration scores (η = 0.03412, frozen) and anti-windup that skips the update when F_t is capped at F_max. We track in score space rather than with the level update of adaptive conformal inference \cite{gibbs2021adaptive}, because a friction drop can move scores beyond the support of the calibration scores. The reference arms are a decaying step size \cite{angelopoulos2024online}, frozen offline calibration, and an oracle that recalibrates on labelled instances from the shifted distribution (label route). We study two feedback variants. The pre-registered variant uses label-rule feedback with the label-route warm start. The secondary variant uses physical direct-replay feedback with the CRC λ̂ warm start, which is the route a robot would use. With this update the long-run average slip over uncapped steps approaches α whatever the shift. The experiments therefore measure the transient, the force the tracker needs, and the comparison with frozen and oracle calibration, not whether the tracker reaches α in the long run.

## 4 Experimental Setup

**Simulator and objects.** All experiments run in MuJoCo 4.0.0 (timestep 0.002 s, elliptic friction cone, impratio 10, condim 6). The parallel-jaw gripper has a force-controlled closing axis and one touch grid per pad. Fast tactile simulators exist \cite{wang2022tacto, akinola2025tacsl, leins2025hydroelastictouch}, and sensor configuration matters for learned manipulation \cite{luu2025manifeel, birtalan2026impact}. We use MuJoCo's pad grids with the explicit noise model of Section 3.2. The in-distribution families are F1 boxes, F2 cylinders, F3 capsules and F4 off-CoM composites. F5 thin plates are held out for the new-family shift. Friction is log-uniform on [0.3, 1.0], drawn independently of family, geometry, mass, CoM offset and disturbance, so no non-tactile input carries friction information. Mass is log-uniform on [0.05, 1.0] kg. The strata are D1 lift acceleration U[1, 10] m/s², D2 shake (amplitude U[5, 20] mm at U[2, 5] Hz), D3 lateral pull U[0.5, 2]·m g and D4 payload U[0.2, 1.0]·m. A static-touch check is consistent with the preload carrying no friction information: the summed pad normal reading differs from F₀ by at most 0.1597 N, and no instance slipped during the preload. Touch is not uninformative about shape: touch-only features identify the object family with accuracy 0.726 (95 % CI [0.7014, 0.7514]; chance 0.25). Because friction is drawn independently of family, this carries no friction information by construction.

**Splits.** Splits are by object within family: train objects 0–149, selection 150–199, calibration 200–324, test 325–499. Calibration has n = 500 instances per stratum (2,000 in total), and test has 2,800 (700 per stratum). The selection split is used only to choose the baseline, to centre the grids and to fit the shrinkage coefficients.

**Shifts and streams.** S1 lowers friction (μ × 0.6), S2 introduces family F5, and S3 scales every disturbance amplitude by 1.5. S1m (μ × 0.9) is reported but is not a primary shift. The pre-registered streams have T = 2,000 steps, with the shift from step 501, evaluation window 1,001–2,000, 20 orderings and label-rule feedback. The physical-feedback streams cover S1–S3 with 20 orderings each and report windows 1–500 (pre-shift), 501–1,000 (transient), 1,001–2,000 and 1,501–2,000, with 95 % intervals over orderings only. The orderings largely reuse the same instances (in S2 all orderings permute one identical post-shift set), so these intervals measure order effects on a nearly fixed sample, not the sampling variability of slip under shift.

**Statistics.** Efficiency is RE against F\*_mid with D as the effect size. Validity is the physical slip rate in direct replay. The four core decisions share a Bonferroni split of a 5 % family-wise level (one-sided 0.0125 each). CI\*\* denotes a two-sided 97.5 % percentile interval from 2,000 object-cluster bootstrap draws, which resample calibration and test objects within family and refit λ̂ in every draw. The main comparison requires D ≥ 0.10 (the smallest effect size of interest, SESOI), a CI\*\* lower limit above 0, and both again with F\*_lo and F\*_hi in place of F\*_mid. The learned-versus-plug-in contrast uses the same superiority rule plus a registered TOST equivalence test within ±0.10 (0.0125 per side), read off the 97.5 % CI\*\*. Matched-slip RE uses one target slip (0.10), found by interpolation between grid offsets inside every bootstrap draw. Because that slip level is read off the test set, matched-slip contrasts are descriptive. For the v1 secondaries, Holm's correction is applied within the registered secondary families. Second- and third-round rows are unadjusted and labelled; their decision labels are superiority (lower limit > 0), inferiority (upper limit < 0) or "not shown". The refined grid can mark a primary-grid result as unreliable but cannot upgrade it.

**Pre-registered decisions.** There are four: the learned probe arm against the baseline (H2a), decided as superiority; the learned model against the plug-in (H2b), not confirmed; label validity (H1), not confirmed; and online efficiency (H3), inconclusive.

**Deviations from the pre-registration.**
(1) The CRC route was written after the monotonicity counts were seen, but before any predictor existed.
(2) On the primary grid, the plug-in's λ̂ sat at index 0 in D1/D2 (a grid floor). This was handled by the post hoc refined grid.
(3) The pre-registration gives the selection objects once as 200–249 and elsewhere as 150–199; the code uses 150–199.
(4) The probe arm's shift prediction was never specified and is untested. A friction diagnostic was computed on calibration plus test objects. The noisy-mass draw was fixed in a later addendum (result in Section 5.1). One equivalence test under S1 was evaluated after its read-out.
(5) The second- and third-round analyses were registered after the first- and second-round read-outs and reviews, and they cannot change a first-round decision.
(6) The reactive-controller detector was fixed after the third-round analyses of existing replays and the shrunk plug-in read-out, but before any reactive-controller code. A 3-object timing pilot printed 12 calibration-instance outcomes; no parameter was changed afterwards, and the optional CRC variant of the controller was dropped.
(7) The registered physical-replay online oracle was not produced.
(8) The tuned per-stratum margin is tuned on the calibration split, as registered.
Constants and learner settings are in Table A1, and compute is in Appendix B.

## 5 Results

All numbers are from simulation, at α = 0.10, on the 2,800 in-distribution test instances, with CRC on the primary grid unless stated otherwise. "Certified" refers throughout to the marginal, per-stratum, in-expectation bound of Section 3.4, in simulation.

### 5.1 Main comparison and force in newtons

**At α = 0.10 the learned probe model has a lower relative excess hold force than the friction-blind conformal baseline (pre-registered, confirmed).** The learned probe model has RE 0.4567 [0.4079, 0.5033] against 0.7832 [0.6968, 0.8583] for CSF-1. This gives D = 0.4168 with CI\*\* [0.3484, 0.4778], decided as superiority. With F\*_lo and F\*_hi in place of F\*_mid, D is 0.4150 and 0.4186. Test physical slip is 0.0829 for the learned probe model and 0.1021 for CSF-1, so the probe arm is compared at lower slip. CSF-1's primary-grid λ̂ lies at index 1 in D1/D2, close to the grid floor; on the refined grid, where it is interior, D is 0.4289 (below), so the headline is not an artefact of this. The size of D is conditional on the assumed σ = 0.2 and on friction being independent of every non-tactile input (Section 7).

**Route robustness and replication (secondary, Table 1).** The saving holds at matched slip 0.10, under Learn-then-Test, on the refined grid and with an empirically tuned per-stratum margin. These routes re-analyse the seed-0 replays, so they show route robustness, not replication; predictor refits with seeds 1–4 replicate it (all superiority). Mass is given to every method; with 10 % multiplicative mass noise per object (pre-registered, label route), D is 0.4603 [0.4106, 0.5050] against 0.4292 without noise, a change of 0.031 [−0.008, 0.071]. All of these are pool-level statements; Section 5.4 reports a sub-pool where the sign reverses.

**Force in newtons (secondary, descriptive, point values).** Over the 2,800 test instances, F\*_mid has 10 / 50 / 90 % quantiles of 0.9549 / 3.184 / 11.35 N and a maximum of 31.87 N. The share of instances above the 32.7 N preload is 0.0. Mean (median) hold force is 6.521 (4.473) N for the learned probe model, 6.519 (4.423) N for the onset-only model, 7.062 (4.556) N for the plug-in and 7.606 (5.476) N for CSF-1, and mean excess over F\*_mid is 1.623 against 2.708 N: the learned model holds 1.085 N less than CSF-1 (single split, no interval).

**What the protocol costs.** The phases shared by every arm (preload, squeeze, ramp-down, the 0.02 s return to F₀ and the 0.1 s re-hold at F₀) integrate to 31.04 N·s. Of this, the probe-specific squeeze, ramp-down, return and re-hold account for 17.96 N·s. Integrated force at hold times T = 1 / 5 / 30 s is 37.57 / 63.65 / 226.7 N·s for the learned model and 38.65 / 69.08 / 259.2 N·s for CSF-1. Compared with a friction-blind grasp that skips the probe-specific phases, the break-even hold time is 16.56 s for the learned model, 16.52 s for the onset-only model and 32.99 s for the plug-in at σ 0.2. Counting all shared phases as probe cost (an upper bound), it is 28.61 s for the learned model. For holds shorter than about 16.6 s, the probe's own force-time outweighs the hold saving, which rules out the benefit for many short pick-and-place holds. In every arm, the fixed 32.7 N preload dominates force-time.

| Row (α 0.10, test) | Grid / route | Value [CI\*\*] | Decision |
|---|---|---|---|
| Friction-blind conformal baseline (CSF-1) | CRC, primary | RE 0.7832 [0.6968, 0.8583]; slip 0.1021; hold F 7.606 N (median 5.476) | — |
| Learned probe model (σ 0.2) | CRC, primary | RE 0.4567 [0.4079, 0.5033]; slip 0.0829; hold F 6.521 N (4.473); excess 1.623 N | — |
| **Probe arm vs baseline (pre-registered, H2a)** | CRC, primary | **D 0.4168 [0.3484, 0.4778]**; F\*_lo / F\*_hi 0.4150 / 0.4186 | **superiority** |
| At matched slip 0.10 (test-selected) | CRC, primary / refined | D 0.4563 [0.4096, 0.4896] / 0.4475 [0.4111, 0.4880] | superiority |
| High-probability bound (Learn-then-Test, δ 0.1) | CRC, primary | D 0.4043 [0.3362, 0.4561]; learned slip 0.0696, RE 0.4895; CSF-1 0.0907 / 0.8216 | superiority |
| Refined grid (post hoc) | CRC, refined | D 0.4289 [0.3577, 0.4770] | superiority |
| Empirical per-stratum margin (no (n+1)) | primary / refined | D 0.4168 [0.3514, 0.4817] / 0.4289 [0.3606, 0.4787] | superiority |
| Seeds 1–4 (replication) | CRC, primary | 0.4343 / 0.4197 / 0.3932 / 0.4494 | all superiority |
| Mass noise 10 % (label route) | label | D 0.4603 [0.4106, 0.5050] vs 0.4292; change 0.031 [−0.008, 0.071] | secondary |
| Integrated force, T 1 / 5 / 30 s | CRC, primary | learned 37.57 / 63.65 / 226.7 N·s; CSF-1 38.65 / 69.08 / 259.2 N·s | descriptive |
| Break-even hold time vs CSF-1 (probe phases / all phases) | CRC, primary | learned 16.56 / 28.61 s; onset-only 16.52 / 28.55 s; plug-in 32.99 / 57.02 s | descriptive |

*Table 1. Main comparison, route robustness and force. Only the bold row is decision-bearing. All other rows are secondary; the route rows re-analyse the seed-0 replays, refined-grid and edge-rule rows are outside the exact CRC theorem (Section 3.4), and the force rows are point values on one test split. Shared protocol phases, including the post-onset return and re-hold, integrate to 31.04 N·s, of which 17.96 N·s are probe-specific.*

### 5.2 Where the saving comes from

**A one-line plug-in on the same onset already captures the saving. The learned model shows no demonstrated gain at σ = 0.2, and at σ = 0.4 a shrunk plug-in is better (secondary unless stated).**

*Probe-fed rules against CSF-1 (Table 2).* The probe plug-in reaches D = 0.4149 [0.3322, 0.4890] on the refined grid; its primary-grid 0.3816 is biased by the grid floor. The shrunk plug-in reaches 0.435 on the primary grid (also at the floor in D1–D2), 0.4522 under the edge rule and 0.4484 on a common refined-recipe grid, and 0.2454 at σ = 0.4. The onset-only model reaches 0.4464. All are superiority, but none is a pre-registered decision, and the cleaner plug-in values come from the post hoc refined grid or the data-dependent edge rule. With that qualification, the probe, a simple force rule and CRC suffice for a large saving over the friction-blind baseline.

*Learned model against plug-in at σ = 0.2.* The registered contrast is D = 0.0569 [−0.0399, 0.1454], not confirmed. The registered TOST equivalence test (±0.10), read off the 97.5 % CI\*\*, was not met (upper limit 0.1454; 0.1001 on the refined grid). The label-route estimate, 0.0134 [−0.0850, 0.0814], lies within ±0.10 but is not decision-bearing. None of the 8 further direct contrasts in Table 2 is shown; their points range from −0.06463 to 0.05379, and 6 of the 8 lie below the registered point estimate. At σ = 0.2 the learned model shows no demonstrated gain over a plug-in on the same onset.

*Across σ.* At σ = 0.4 the shrunk plug-in beats the learned arm: D(learned vs shrunk) = −0.1395 [−0.1832, −0.01264], inferiority, the opposite of the registered prediction. Slip is not matched in this row (0.08214 for the learned arm, 0.09286 for the shrunk plug-in), and no matched-slip version exists. The earlier result that the learned model beats the unshrunk plug-in at σ 0 / 0.1 / 0.4 (Table 2) is qualified, not overturned: the unshrunk σ = 0.4 plug-in is worse than CSF-1 itself (RE 0.9877 vs 0.7832), and at σ 0 and 0.1 the comparator sat at the primary-grid floor in D1–D2, whereas on the refined grid its arm-level RE is below the learned arm's. This suggests, untested, that those superiorities depend on the grid.

*Feature chain (label route unless stated).* Static touch is equivalent to proprioception within ±0.05 (D −0.0084). There is no evidence that the squeeze helps (D −0.0263). Adding the onset gives D 0.4739. The full pipeline and the onset-only model are not distinguishable (D −0.0534 [−0.1233, 0.0508], CRC).

*Non-tactile friction prior.* The learned model's D against the prior falls from 0.8361 (σ_p 0.8) to 0.5042 (σ_p 0.4) to −0.0299 [−0.1903, 0.0816] (σ_p 0.2, both arms on the same refined-recipe grid). Against a prior of log-noise 0.2 no advantage is shown (no equivalence test was registered); the σ_p 0.4 / 0.8 rows compare against unshrunk priors worse than CSF-1 (Table 2) and carry little weight.

*σ dependence (Fig. 2).* The main D is 0.6789 / 0.5825 / 0.4168 / 0.1401 at σ = 0 / 0.1 / 0.2 / 0.4, and its lower limit falls below the SESOI at σ = 0.4. Where a real sensor sits on this curve is unknown (Section 7).

| Row (σ 0.2 unless stated) | Grid / route | D [CI\*\*] | Decision |
|---|---|---|---|
| Probe plug-in vs CSF-1 | CRC, refined / primary | 0.4149 [0.3322, 0.4890] / 0.3816 [0.2965, 0.4505] (grid floor) | superiority |
| Shrunk plug-in vs CSF-1 | CRC, primary / edge rule / same grid | 0.435 [0.3594, 0.4720] / 0.4522 [0.4013, 0.5162] / 0.4484 [0.4015, 0.5146] | superiority |
| Shrunk plug-in vs CSF-1, σ 0.4 | CRC, primary | 0.2454 [0.1679, 0.2989] | superiority |
| Onset-only learned vs CSF-1 | CRC, primary / refined | 0.4464 [0.3776, 0.4906] / 0.4412 [0.3846, 0.4942] | superiority |
| **Learned vs plug-in (pre-registered, H2b)** | CRC, primary | **0.0569 [−0.0399, 0.1454]**; TOST ±0.10 not met | **not confirmed** |
| Learned vs plug-in | CRC, refined / label route | 0.02397 [−0.09487, 0.1001] / 0.0134 [−0.0850, 0.0814] | not shown / within ±0.10 (secondary, not decision-bearing) |
| Learned vs plug-in, Learn-then-Test | primary / refined | 0.05379 [−0.0568, 0.1222] / −0.004233 [−0.08602, 0.1069] | not shown |
| Learned vs plug-in, matched slip | primary / refined | −0.02384 [−0.08446, 0.01937] / −0.06104 [−0.1104, 0.01228] | not shown |
| Learned vs shrunk plug-in | primary / edge rule / same grid | −0.03216 [−0.09825, 0.07434] / −0.06463 [−0.1851, 0.008734] / −0.03532 [−0.1688, 0.01035] | not shown |
| **Learned vs shrunk plug-in, σ 0.4** | CRC, primary | **−0.1395 [−0.1832, −0.01264]**; slip 0.08214 vs 0.09286; RE 0.6735 vs 0.591 | inferiority |
| Learned vs unshrunk plug-in, σ 0 / 0.1 / 0.4 | CRC, primary | 0.246 / 0.1072 / 0.3182; comparator λ̂ index 0 in D1–D2 at σ 0 / 0.1; refined arm RE plug-in 0.208 / 0.2915 vs learned 0.2397 / 0.3212 | qualified |
| Feature chain: S vs P / full vs S / + onset | label route | −0.0084 [−0.0360, 0.0128] / −0.0263 [−0.0558, 0.0149] / 0.4739 [0.4148, 0.5229] | equivalence / not confirmed / report only |
| Full learned vs onset-only | CRC, primary | −0.0534 [−0.1233, 0.0508] | not confirmed |
| Learned vs friction prior σ_p 0.2 / 0.4 / 0.8 | same grid / primary / primary | −0.0299 [−0.1903, 0.0816] / 0.5042 [0.4362, 0.5635] / 0.8361 [0.8137, 0.8573]; prior RE 0.4312 / 0.9213 / 2.7859 | not shown / superiority / superiority |

*Table 2. Where the saving comes from. Bold rows: the registered learned-versus-plug-in decision and the σ 0.4 shrunk-plug-in result. Only the H2b row is decision-bearing; all other rows are secondary and unadjusted. In the σ 0 / 0.1 unshrunk rows, the comparator's D1 / D2 test slips are 0.007143 / 0.002857 and 0.01571 / 0.007143.*

**Figure 2.** *Dependence on assumed onset noise. D (learned probe model vs CSF-1, CRC primary grid) at σ = 0 / 0.1 / 0.2 / 0.4: 0.6789 / 0.5825 / 0.4168 / 0.1401 with CI\*\*, and the SESOI 0.10 as a dashed line. Open markers show the shrunk plug-in against CSF-1 at σ 0.2 / 0.4 (0.435 / 0.2454).*

### 5.3 Tactile competitors and calibration alternatives

**Without calibration, a single margin cannot reach α in every stratum. A margin tuned per stratum on the calibration data lands where CRC does on this split. The registered reactive controllers miss α by a wide margin.**

*Probe + one uniform margin (second round, descriptive).* With κ ≤ 0.5 the rule under-grips (slip ≥ 0.6182); at κ = 1.0 D1 and D2 are over-protected while D3 and D4 slip at 0.6571 / 0.6186. The plug-in force for D3/D4 cannot see the hidden external load, so no uniform margin fits both types of stratum.

*Probe + empirically tuned per-stratum margin (third round).* On the primary grid this rule reproduces the CRC test points for the learned model, the plug-in and CSF-1, and on the refined grid for the learned model and CSF-1. Only the refined-grid plug-in moves (slip 0.07964, RE 0.4409, against 0.075 / 0.4551 under CRC), so there the (n + 1) correction costs 0.0142 RE. At 500 calibration grasps per stratum, CRC adds a finite-sample guarantee rather than a different operating point.

*Reactive slip-tightening (third round, descriptive, negative control).* Both reactive arms start the hold at 0.5–0.75 times an uncalibrated nominal force, so they test a registered design, not where the saving comes from. REACT-blind with c = 0.5 / 0.75 slips at 0.765 / 0.4632, with mean 2.501 / 3.099 tightening steps. REACT-probe slips at 0.9921 / 0.9514 and takes about half a step per instance (Table 3). Every arm and stratum slips at ≥ 0.3086. This registered design fails under a criterion where slip before tightening counts. Detection timing is not reported, so we claim no reason for the failure and make no claim against reactive control in general; a reactive hybrid that starts at the CRC-calibrated force was not run (Section 7).

| Row (σ 0.2, test) | Value | Status |
|---|---|---|
| Probe + uniform margin κ 0 / 0.25 / 0.5 / 1.0 | slip 0.9582 / 0.8257 / 0.6182 / 0.3350; RE −0.3829 / −0.2287 / −0.0744 / 0.2341; κ 1.0 strata 0.0414 / 0.0229 / 0.6571 / 0.6186 | descriptive |
| Plug-in + tuned per-stratum margin | primary slip 0.06571, RE 0.4843 (= CRC); refined 0.07964 / 0.4409 (CRC 0.075 / 0.4551); D vs CSF-1 0.3816 [0.3014, 0.4517] / 0.4331 [0.3344, 0.4956] | secondary |
| REACT-blind, c 0.5 / 0.75 | slip 0.765 / 0.4632; RE −0.1731 / 0.4185; steps 2.501 / 3.099; at cap 0.2446 / 0.5425; c 0.75 strata 0.3414 / 0.3086 / 0.6057 / 0.5971 | descriptive |
| REACT-probe, c 0.5 / 0.75 | slip 0.9921 / 0.9514; RE −0.6358 / −0.4534; steps 0.4964 / 0.5079 | descriptive |
| Re-splits (200), CRC: mean slip / share > α / share any stratum > α (primary; refined) | learned 0.08469 / 0.05 / 0.57 (0.08516 / 0.09 / 0.69); plug-in 0.07121 / 0.0 / 0.405 (0.08466 / 0.035 / 0.475); CSF-1 0.08514 / 0.12 / 0.41 (0.08646 / 0.075 / 0.615) | descriptive |
| Re-splits, Learn-then-Test: mean slip / share any stratum > α | learned 0.06826 / 0.07 (0.07045 / 0.105); plug-in 0.06199 / 0.075 (0.07102 / 0.13); CSF-1 0.0685 / 0.105 (0.0673 / 0.06) | descriptive |
| Per-stratum slip D1–D4 (primary; refined) | learned 0.0871 / 0.0714 / 0.0757 / 0.0971 (0.1043 / 0.1014 / 0.0729 / 0.0814); CSF-1 0.1157 / 0.0886 / 0.1057 / 0.0986 (0.09 / 0.0929 / 0.11 / 0.1057); plug-in 0.0586 / 0.0386 / 0.08 / 0.0857 | descriptive |
| Slip by friction quintile (low → high μ) | learned 0.2161 / 0.1179 / 0.05893 / 0.01786 / 0.003571; plug-in 0.08571 / 0.0875 / 0.07321 / 0.05357 / 0.02857; CSF-1 0.4804 / 0.02857 / 0.001786 / 0.0 / 0.0 | descriptive |
| **Mid-friction sub-pool, label route (H2-R)** | **D −0.2614 [−0.5320, −0.0325]**; 352 cal / 548 test; Holm p 0.03 (family) / 0.12 (all 52) | secondary |
| Sub-pools, CRC refined: μ ∧ amp / μ only / amp only | −0.3152 [−0.5231, −0.0172] / −0.1717 [−0.4275, −0.01539] / 0.4929 [0.4251, 0.5537]; plug-in −0.6804 / −0.3705 / 0.4869; μ ∧ amp CSF-1 slip 0.1004, RE 0.2633 vs learned 0.08394 / 0.3463; μ only CSF-1 slip 0.08208, RE 0.3281 vs learned 0.08585 / 0.3844 | inferiority / inferiority / superiority |
| Sub-pools, CRC primary: μ ∧ amp / μ only / amp only | 0.3754 [0.2648, 0.4823] / 0.3387 [0.2423, 0.4278] / 0.5004 [0.4237, 0.5516]; CSF-1 at the grid floor in D1/D2, slip 0.03285 (μ ∧ amp) / 0.03396 (μ only) | unreliable (grid floor) / unreliable / superiority |

*Table 3. Competitors, certificate behaviour and where the method loses. Upper block: Section 5.3; lower block: Section 5.4. Re-splits re-partition the same 4,800 instances (split-to-split variability, not new objects). "μ ∧ amp" is μ ∈ [0.5, 0.8] with mid-half disturbance amplitude. All rows are secondary; only the H2-R row carries a Holm-adjusted p.*

### 5.4 How the certificate behaves, and where the method loses

**Across 200 object re-splits, the mean test slip stays below α for every rule, arm and grid. The bound is marginal, though: single strata and low-friction objects exceed α often.**

*Re-splits (descriptive; split-to-split variability, not new objects).* Under CRC, mean slip is 0.07121–0.08646 and the share of splits with overall slip above α is 0.0–0.12; under Learn-then-Test, mean slip is 0.06199–0.07102. For the learned model at least one stratum exceeds α in 0.57 (primary) / 0.69 (refined) of splits, for CSF-1 in 0.41 / 0.615.

*Single-split tables (Table 3).* On the primary grid every stratum of the learned model is at or below α, while CSF-1 exceeds α in D1 and D3; on the refined grid the learned model exceeds α in D1 and D2, and CSF-1 in D3 and D4. The seed-4 refit has overall slip 0.1018. By friction quintile, slip falls from 0.2161 to 0.003571 for the learned model and from 0.4804 to 0.0 for CSF-1; the plug-in is flatter (0.08571 to 0.02857), so the low-friction objects carry most of the miscoverage.

*Validity of labels.* The label monotonicity gate failed (8 / 800; in the gate set the largest slip force above F\*_hi exceeds it by a relative 0.00225, and 0.00904 over all recorded violations including the shift pools). The check of labels against physical slip passes for all four arm × α combinations (physical minus label Δ between −0.00429 and −0.00143).

*Where the method loses.* On the label route, in the sub-pool μ ∈ [0.5, 0.8] with mid-range disturbance amplitude (352 calibration / 548 test instances), D = −0.2614 [−0.5320, −0.0325]. Its Holm-adjusted p is 0.03 within its family and 0.12 over all 52 first-round secondaries. On the refined CRC grid D is −0.3152 [−0.5231, −0.0172] (inferiority); with the μ restriction alone it is −0.1717 [−0.4275, −0.01539], whose interval contains −0.3152; with the amplitude restriction alone it is +0.4929 (superiority). The primary grid gives +0.3754 / +0.3387 / +0.5004, but in the two μ-restricted sub-pools CSF-1's λ̂ sits at the primary-grid floor in D1/D2, so it runs far below α (slip 0.03285 and 0.03396). By our rule that the refined grid can mark a primary-grid result as unreliable, these two superiorities are marked unreliable. Slip does not explain the reversal: in the μ ∧ amp cell CSF-1 slips more than the learned model on the refined grid (0.1004 vs 0.08394), but in the μ-only sub-pool it slips less (0.08208 vs 0.08585) and still needs less excess force (RE 0.3281 vs 0.3844). The reversal comes with the μ restriction, not the amplitude restriction, and the plug-in shows the same pattern. Our untested reading is that the method loses where the friction spread is narrow relative to the probe's error: the log-width of [0.5, 0.8] is of the order of the onset's log-unit error (assumed σ = 0.2 on top of the detector's bias 0.3186 and SD 0.1103), so a friction-blind rule pays little for covering the range while the probe arm still pays for its estimation error.

### 5.5 Online calibration under shift

**Frozen calibration breaks under friction and amplitude shift. Binary-feedback tracking returns to α after a transient, and the probe arm keeps its force advantage. Efficiency against oracle recalibration stays inconclusive.**

*Pre-registered streams (label feedback, Table 4).* The frozen probe arm's window slip reaches 0.3056 (S1) and 0.2461 (S3), and the frozen baseline's 0.5101 (S1); neither breaks under S2. The tracking probe arm holds window label slip between 0.0999 and 0.1016 in every shift. H3 is inconclusive in all three shifts (realised half-widths 0.15–0.20 against a projected ≈ 0.12), and the matched-rate co-requirement fails in S1 and S2.

*Physical feedback (third round).* In the transient window 501–1,000 the probe arm overshoots to 0.1389 (S1) and 0.1368 (S3), less than CSF-1 in S1 (0.2087). In the late window 1,501–2,000 its slip is 0.1001 / 0.1008 / 0.1018, and every interval contains α, consistent with convergence. Because the orderings largely share instances (identical post-shift sets in S2), the intervals reflect order effects, not sampling variability under shift. D_RE against CSF-1 is 0.3107–0.4432 across shifts and windows, and 0.4152–0.4432 outside the S1 transient.

*Oracle.* No physical-replay oracle was produced. The label-route oracle itself slips at 0.1346 in S2, so R_E is not updated.

| Row | S1 (μ × 0.6) | S2 (F5) | S3 (amp. × 1.5) |
|---|---|---|---|
| Frozen probe arm / frozen baseline, label slip | 0.3056 / 0.5101 | 0.1017 / 0.1051 | 0.2461 / 0.1910 |
| Tracking probe arm, label feedback: slip / RE | 0.1016 / 0.4763 | 0.0999 / 0.4262 | 0.1000 / 0.5067 |
| **Online efficiency R_E [CI\*\*] (pre-registered, H3)** | 0.8778 [0.7404, 1.1204] | 1.1739 [1.0234, 1.4283] | 0.9629 [0.8363, 1.1449] |
| Matched-rate co-requirement (physical difference) | 0.032 (fail) | −0.035 (fail) | — |
| Label-route oracle slip (reference) | 0.0751 | 0.1346 | 0.0863 |
| Physical feedback, 501–1,000: probe arm [CI95] / CSF-1 slip | 0.1389 [0.1365, 0.1413] / 0.2087 | 0.0981 / 0.0938 | 0.1368 [0.1337, 0.14] / 0.126 |
| Physical feedback, 1,501–2,000: probe arm slip [CI95] / RE | 0.1001 [0.0969, 0.1033] / 0.4746 | 0.1008 [0.0974, 0.1043] / 0.4144 | 0.1018 [0.098, 0.1055] / 0.4999 |
| Physical feedback, 1,501–2,000: CSF-1 slip | 0.0993 | 0.1025 | 0.0999 |
| D_RE probe arm vs CSF-1 (1–500 / 501–1,000 / 1,001–2,000 / 1,501–2,000) | 0.4432 / 0.3107 / 0.4154 / 0.4152 | 0.4408 / 0.4247 / 0.4292 / 0.4342 | 0.441 / 0.4373 / 0.4171 / 0.4243 |

*Table 4. Online calibration under shift, α = 0.10. Upper rows: pre-registered streams, window 1,001–2,000, label-rule slip averaged over 20 orderings; H3 is inconclusive in every shift. Lower rows: third-round physical-feedback streams with the CRC warm start, 20 orderings that largely reuse the same instances, 95 % intervals over orderings only (descriptive).*

## 6 Discussion

**What the evidence licenses.** The confirmed, pre-registered result is that the learned probe model beats the friction-blind conformal baseline. Per-stratum CRC makes the saving certifiable in a marginal, per-stratum, in-expectation sense, in simulation and given counterfactual replays. Secondary rows, several post hoc and grid-dependent, add that a one-line plug-in on the onset, shrunk or not, captures the saving, and that the learned model shows no demonstrated gain over it. On that secondary evidence the operative method is *probe + simple force rule + CRC*, with the learner as an option whose value is not established. The saving amounts to about 1.085 N of mean hold force at α = 0.10, and it pays back the probe's own force-time only for holds longer than about 16.6 s. A per-stratum margin tuned on calibration data lands at the same operating point on this split. What CRC adds is the finite-sample guarantee, not a different force.

**The headline is conditional.** Two ingredients set the size of D: how much friction varies across the objects a robot meets, and how precisely its sensor reads the onset. In our pool, friction varies over [0.3, 1.0] independently of every non-tactile input, which forces any friction-blind rule to pay for the whole range. The onset noise is assumed. When the friction range is narrowed to [0.5, 0.8], the advantage disappears on the label route and on the refined CRC grid, even where CSF-1 slips less than the probe arm; a narrow spread relative to the probe's error is our untested reading. When the onset noise doubles to σ = 0.4, D falls to 0.1401. The figure is one point on a curve, not a property of tactile grip regulation.

**Why the learner does not help here.** At σ = 0.2 the learned model and the plug-in read the same noisy onset; no direct contrast separates them and the equivalence test is not met, so we claim neither a gain nor equivalence. At σ = 0.4 the learner's advantage over the raw plug-in disappears once the plug-in is shrunk, and the shrunk plug-in becomes the better rule (unadjusted, at unmatched slip). A learned component may still pay off with richer tactile signals, which is not tested here.

**Relation to prior work.** Friction-estimating controllers \cite{khamis2021real, niu2026synchronized} and incipient-slip methods \cite{dong2019maintaining, boonstra2024estimate} leave the safety margin as a design parameter. Our results suggest that the same cue plus a model-free calibration step yields a large saving over friction-blind rules, and that learned tactile components should be compared against a calibrated plug-in on the same cue. Whether probe plus CRC beats such controllers at equal slip is not shown: our reactive stand-in is one registered design that starts below the nominal force and serves only as a negative control, and the tuned margin is our own construction. The online results agree with quantile-tracking theory \cite{angelopoulos2023conformala}. The tracker needs only the binary outcome that a robot observes, but it carries only a long-run-average guarantee, with no per-stratum finite-sample statement. A calibration that certifies from one outcome per grasp is the central open problem for hardware.

**Practical implications.** The probe adds well under a second per grasp, but it drives every object to incipient slip on every grasp. In simulation it found an onset on every in-distribution instance and displaced the object by a median 0.126 mm at onset (95th percentile 0.2543 mm, maximum 1.92 mm). Objects for which sub-millimetre slip or the 1.5 F₀ squeeze is unacceptable are outside its scope.

## 7 Limitations

Each caveat is stated here once in full and referenced elsewhere.

1. *Simulation only; σ assumed.* The study uses one simulator with rigid contact, five object families and a modelled detector. σ = 0.2 sets the effect size: D runs from 0.6789 to 0.1401 as σ goes from 0 to 0.4. We did not ground σ on hardware or in published detector error, so where a real sensor sits on the curve is unknown.
2. *Deployability.* Offline CRC needs counterfactual replays of each calibration grasp at every grid force, so the certificate exists only where a simulator can replay. The deployable route is online physical-feedback tracking, with a long-run guarantee only. It was studied in simulation on 3 shifts × 20 orderings that largely share instances (identical post-shift sets in S2), with intervals over orderings only, and it shows transient overshoot to 0.1389 / 0.1368 in S1 / S3. No physical-replay oracle exists, and no one-outcome-per-grasp calibration was run.
3. *Marginal guarantee.* The bound holds per stratum and in expectation. For the learned model, single strata exceed α in a majority of re-splits (0.57 / 0.69), and the lowest-friction quintile slips at 0.2161. Learn-then-Test holds per stratum at δ = 0.1, not family-wise.
4. *Validity premise and grid choice.* The label monotonicity premise failed, and the CRC route and the refined grid were adopted after that failure. The edge rule and the refined grid depend on the data, so their rows are not covered exactly by the CRC theorem as run.
5. *Fixed protocol.* The 32.7 N preload and the squeeze exceed every test instance's F\*_mid, and the probe induces micro-slip on every grasp. The minimal-force claim applies to the hold force only, the probe's force-time is recovered only after a 16.56 s hold, and no adaptive or low preload was run.
6. *Friction distribution and competitors.* μ is drawn independently of all non-tactile inputs, which makes the friction-blind baseline weak by construction: no non-tactile rule can carry friction information, so D largely measures the width of the friction range relative to the probe's error. We ran no pool with correlated friction and no deployable vision or category prior; the non-tactile friction prior is oracle-side. We evaluated one registered reactive design, a negative control without detection-timing data, and no reactive hybrid that starts at the calibrated force.
7. *Where it loses.* For μ ∈ [0.5, 0.8], the friction-blind baseline is better on the label route and on the refined CRC grid. The opposite primary-grid result is unreliable because CSF-1 sits at the grid floor there. In the μ-only sub-pool the reversal holds although CSF-1 slips less, so unmatched slip does not explain it; that a narrow friction spread relative to the probe's error is the cause is a reading, not a tested result.
8. *Learned model and simulator-only ingredients.* There is no matched-slip version of the σ 0.4 shrunk-plug-in row or of the sub-pool rows, and the σ 0 / 0.1 learned-versus-plug-in rows have no refined-grid contrast. The shrinkage fit uses the true μ of the selection objects, and the learned model trains on bisection labels; both exist only in simulation.
9. *Multiplicity.* Holm covers only the first-round secondaries (52 rows, 40 rejected; no first-round verdict changes). Second- and third-round rows are unadjusted. Three third-round inferiority rows have upper bounds within 0.02 of 0 (−0.0172, −0.01539, −0.01264). A bootstrap p of 0.0 means p < 0.001, not 0.

## 8 Conclusion

We asked whether a short tactile probe can make a slip-bounded grasp cheaper in hold force, and which component carries the saving. In MuJoCo simulation, a ramp-down friction-onset probe combined with per-stratum conformal risk control on the physical binary slip loss reduces relative excess hold force by D = 0.4168 (97.5 % CI [0.3484, 0.4778]) against the strongest non-tactile conformal baseline, selected beforehand; this confirmed result is for the learned probe model. The bound is marginal per stratum and in expectation, and needs counterfactual replays. On the primary test split, mean hold force is 1.085 N lower, and the probe's own force-time is recovered only after a 16.56 s hold. Secondary, partly post hoc evidence indicates that the probe, a one-line (optionally shrunk) Coulomb plug-in and CRC suffice, and that a learned model shows no demonstrated gain. The result is conditional on an assumed onset noise and a wide friction range that no non-tactile input predicts, and in a mid-friction band μ ∈ [0.5, 0.8], where the friction spread is narrow, the baseline is better (D −0.2614 on the label route, a Holm-adjusted secondary). Under shift, binary-feedback tracking is consistent with convergence to α, while its efficiency against oracle recalibration is inconclusive. Three next steps follow. First, measure onset noise on a physical gripper with a real tactile sensor. Second, add an adaptive preload so that the protocol's force-time no longer dominates. Third, run online physical-feedback calibration on hardware, where binary slip is the only signal available.

## Appendix

### A Protocol constants and learner settings

| Item | Value |
|---|---|
| Preload / squeeze | F₀ = 32.7 N for 0.4 s; F₀ → 1.5 F₀ → F₀ over 0.3 s |
| Probe | F₀ → 0.005 F₀ log-linear over 0.25 s; return in 0.02 s, hold 0.1 s |
| Detector | 500 Hz; 6-frame smoothing; 8-frame rise < ½ stick rise, 2 consecutive frames; armed at r > 0.1 |
| Taxel noise | multiplicative lognormal 0.05; additive 0.002 N; channel gain lognormal 0.10 |
| Onset noise σ | {0, 0.1, 0.2, 0.4}; primary 0.2 (assumed) |
| Friction-prior noise σ_p | {0.2, 0.4, 0.8} |
| Uniform margins κ | {0, 0.25, 0.5, 1.0} |
| Reactive controllers | c ∈ {0.5, 0.75}; r_safe 0.8 μ_min (blind) or 0.8 μ̂ (probe); step × 1.25 over 20 ms, ≤ 4 steps; 10 ms read-out, 6-frame smoothing, 2 consecutive frames, 30 ms refractory |
| Labels | log bisection on [0.1, 100] N, 11 replays |
| Target level α; Learn-then-Test δ | 0.10; 0.1 |
| Calibration size | n = 500 per stratum |
| Primary CRC grid | q̂_sel + linspace(−0.4, 0.4, 20), pooled |
| Refined grid (post hoc) | q̂_sel,d + linspace(−0.8, 0.8, 41), per stratum |
| Learner | gradient-boosted quantile trees (scikit-learn HistGradientBoostingRegressor, quantile loss), τ = 1 − α; 30-configuration random search with 4-fold object-grouped CV, identical for all feature sets; learning rate log-uniform on [0.02, 0.3], max_iter ∈ {100, 200, 400, 800}, max_leaf_nodes ∈ {7, 15, 31, 63}, min_samples_leaf ∈ {5, 10, 20, 40}, l2_regularization ∈ {0, 0.1, 1} |
| Online tracker | η = 0.03412; anti-windup at F_max; one tracker per stratum |
| Seeds | predictor seed 0 primary, seeds 1–4 refit; onset ε and prior ε_p fixed per instance; stream orderings `default_rng([4242, shift, ordering])`; bootstrap seed 2026 (second and third rounds); re-split seed 3031 |
| Inference | 2,000 object-cluster bootstrap draws; CI\*\* 97.5 %; SESOI 0.10 |

*Table A1. Protocol constants and learner settings.*

### B Compute

Simulation is CPU-only, and a replay is bit-identical across repeats on the same machine. The first round used 14.50 logged CPU-hours of replay jobs (CRC grids 5.72 primary and 8.03 refined, bisection labels 0.60, monotonicity 0.15), and the second round 2.357. Third-round analyses of existing replays need no new simulation; the CPU-hours of the third-round shrunk-plug-in, reactive-controller and online replays, and the CPU model, were not logged.

### C Further secondary rows

On the label route, the main comparison against Mondrian-CSF with privileged family identity gives D 0.4381 [0.3733, 0.4872]. Pooled over the 16 family × disturbance cells it gives 0.4388, with no cell worse by more than 10 % but heterogeneous cell effects (Q 31.04). The tail ratio of 95th-percentile excess is 0.5918 [0.5540, 0.6564] (CRC, primary grid). The friction residual R² is 0.7937 for P, 0.6034 for CSF-1, 0.2142 for the learned model at σ 0.2 and 0.0054 for the plug-in at σ 0.2. Without added noise, the detector's reading correlates with log μ at 0.9480 (bias 0.3186, SD 0.1103 in log units). Online, S1m gives R_E 0.8871 [0.7723, 1.0265] with a label slip difference of 0.0248 > 0.02. A constant step catches up faster than a decaying step (cumulative excess-slip difference 58.15 in S1 and 42.40 in S3), and no step was capped at F_max.
