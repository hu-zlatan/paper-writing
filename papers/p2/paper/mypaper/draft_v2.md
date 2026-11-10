```
FIGURE 1 PROMPT
Full-width, three-panel vector figure for a robotics paper (RSS style), white background, sans-serif labels,
colour-blind-safe palette (CertGrip-full = deep blue, onset-only = light blue, physics plug-in CSF-mu-hat = teal,
non-tactile baseline CSF-1 = orange, alpha line = dashed grey). Title strip above the panels: "Probe, then certify".
Panels (b) and (c) are drawn from data; only panel (a) is a schematic.

(a) Protocol timeline (schematic). x-axis: time within one grasp episode; y-axis: grip force (log scale). Segments,
left to right: "preload F0 = 32.7 N (same for every object)" as a flat line held 0.4 s; "squeeze F0 -> 1.5 F0 -> F0"
as a small triangular bump (0.3 s); "ramp-down probe" as a log-linear descent from F0 towards 0.005 F0 over 0.25 s,
cut short by a red marker labelled "incipient-slip onset F_onset", followed by a fast return to F0; then
"ramp to F = F_base(x) e^lambda-hat" and a shaded "disturbance window (0.6 s)" with four small icons D1 lift
acceleration, D2 shake, D3 lateral pull, D4 payload. Shade only the probe segment in light blue and label it
"only friction channel". Inset next to the onset marker: pad shear/normal ratio vs time, rising during stick and
flattening at onset, annotated "8-frame rise < 1/2 stick rise, 2 consecutive frames". Under the onset marker:
"mu-hat = m g / (2 F_onset)".

(b) Risk-efficiency frontier (real data, test set, sigma = 0.2). x-axis: test physical slip rate (0 to 0.30);
y-axis: mean relative excess force RE_mid. One polyline with markers per arm over calibration-grid offsets
k = -4 ... +4 (left to right in k means decreasing slip). Points (slip, RE), k = -4 ... +4:
  CertGrip-full (primary grid): (0.2661, 0.2309) (0.2007, 0.2839) (0.1539, 0.3391) (0.1200, 0.3967) (0.0829, 0.4567)
    (0.0568, 0.5194) (0.0339, 0.5847) (0.0225, 0.6529) (0.0136, 0.7239)
  onset-only (primary grid): (0.2786, 0.2114) (0.2214, 0.2635) (0.1729, 0.3178) (0.1321, 0.3745) (0.0857, 0.4336)
    (0.0568, 0.4952) (0.0404, 0.5595) (0.0250, 0.6266) (0.0157, 0.6965)
  CSF-mu-hat (refined grid, dashed teal line, legend note "refined grid"): (0.2414, 0.2399) (0.1943, 0.2905)
    (0.1446, 0.3432) (0.1032, 0.3980) (0.0750, 0.4551) (0.0582, 0.5144) (0.0404, 0.5763) (0.0296, 0.6406)
    (0.0229, 0.7075)
  CSF-1 (primary grid): (0.1711, 0.6037) (0.1536, 0.6375) (0.1432, 0.6728) (0.1293, 0.7097) (0.1021, 0.7832)
    (0.0743, 0.8599) (0.0436, 0.9398) (0.0168, 1.023) (0.0100, 1.110)
Vertical dashed grey line at alpha = 0.10. Mark the CRC operating point (k = 0) of each arm with a larger filled
marker. Vertical double arrow at slip 0.10 between the CertGrip-full curve (RE 0.4290) and the CSF-1 curve
(RE 0.7891), annotated "matched slip 0.10: D_match = 0.4563 [0.4096, 0.4896] (secondary)".

(c) Result bars (conformal risk control, primary grid, test set, alpha = 0.10). Four bars of RE_mid with 97.5 %
object-cluster bootstrap error bars: CSF-1 0.7832 [0.6968, 0.8583]; CSF-mu-hat (sigma 0.2) 0.4843 [0.4435, 0.5219];
CertGrip-full (sigma 0.2) 0.4567 [0.4079, 0.5033]; onset-only (sigma 0.2) 0.4336 [0.3983, 0.4833]. On a secondary
right axis, one dot per bar for the test physical slip rate: 0.1021, 0.0657, 0.0829, 0.0857, against a dashed
alpha = 0.10 line. Bracket between the CSF-1 and CertGrip-full bars annotated "D = 0.4168 [0.3484, 0.4778],
pre-registered". Hatch the CSF-mu-hat bar lightly with a dagger and the note "dagger: lambda-hat at the primary-grid
floor in D1/D2, so this arm is over-protected; refined grid: RE 0.4551, slip 0.0750; learned vs plug-in not
confirmed". Small grey footnote marker at bottom right: "narrow-friction, mid-amplitude sub-pool: D = -0.2614
(method worse)".

Footer line under all panels: "Simulation (MuJoCo, rigid contact), modelled tactile detector, added onset noise
sigma = 0.2 (assumed); CRC bound holds in expectation over calibration draws, per disturbance stratum".

Draft caption: Probe, then certify. (a) Every grasp starts from the same 32.7 N preload, so only the ramp-down
probe's incipient-slip onset carries friction information. (b) Test physical slip against relative excess force
over the calibration grid: at matched slip 0.10 the probe-fed arms need far less excess force than the strongest
non-tactile conformal baseline CSF-1 (D_match 0.4563, secondary). (c) Conformal risk control at alpha = 0.10:
D = 0.4168, CI** [0.3484, 0.4778], test physical slip 0.0829. A physics plug-in on the same onset (CSF-mu-hat) is
not distinguishable from the learned model (learned-vs-plug-in contrast not confirmed). In a narrow-friction,
mid-amplitude sub-pool the probe arm is worse (D -0.2614). Simulation (MuJoCo), modelled detector, onset noise
sigma = 0.2.
```

# Probe, Then Certify: A Tactile Friction-Onset Probe with Conformal Risk Control for Certified-Slip Minimal-Force Grasping

## Abstract

A minimal-force grasp should state how often it slips. Non-tactile conformal baselines can, but they are friction-blind, so their calibrated force must cover the whole friction range. After a fixed preload that carries no friction information, our gripper ramps its force down until a touch-only detector reports incipient slip, giving a Coulomb friction estimate. Any force rule fed with it (a physics plug-in or a learned quantile model) is calibrated by conformal risk control (CRC) on the monotonised binary *physical* slip loss, per disturbance stratum, so that expected physical slip is at most α. In MuJoCo at α = 0.10, the pre-registered comparison against the strongest non-tactile conformal baseline, selected beforehand, gives D = 0.4168 (97.5 % CI [0.3484, 0.4778]) less relative excess force, with test physical slip 0.0829 against 0.1021. In secondary analyses the saving persists at matched slip (D 0.4563) and under a high-probability Learn-then-Test certificate (D 0.4043). It comes from the probe: the plug-in on the same onset reaches D 0.4149 (refined grid), and at onset noise σ = 0.2 the learned model shows no demonstrated gain over it. Against a non-tactile friction prior of log-noise 0.2, no advantage is shown. In a narrow-friction (μ ∈ [0.5, 0.8]), mid-amplitude sub-pool the method is worse: D = −0.2614 [−0.5320, −0.0325]. Under shift, binary-feedback quantile tracking keeps window slip near α where frozen calibration breaks; efficiency against oracle recalibration is inconclusive. Simulation only, with a modelled detector and assumed onset noise.

## 1 Introduction

Grasping fragile, compliant or valuable objects calls for the smallest grip force that still holds the object through the motions and loads of the task. Excess force damages soft or brittle objects, and slip prevention with limited force is a central concern for prosthetic hands \cite{berman2025autonomous}; too little force drops the object. Humans solve this trade-off by adapting grip force to the friction of the surface they touch \cite{johansson1984roles} and by re-regulating it when friction changes suddenly \cite{willemet2024grip}. Robotic tactile grip regulation has made steady progress on the same trade-off. Controllers detect incipient slip and tighten the grasp \cite{dong2019maintaining, veiga2020grip}, estimate friction online and add a safety margin \cite{khamis2021real, niu2026synchronized}, or learn a map from tactile signals to a gentle grasp force \cite{boonstra2024estimate}. What these controllers do not provide is a quantitative, distribution-free statement of the form "this force rule slips on at most a fraction α of grasps". Margins are set by hand, and their slip rate is whatever the experiment happens to show.

Conformal methods supply exactly this kind of statement. Split conformal prediction \cite{lei2017distribution} and conformal risk control \cite{angelopoulos2022conformal} turn any predictor into a rule whose expected loss on an exchangeable test point is bounded by a target level, using a held-out calibration set and no distributional assumptions. In grasping, the predictor proposes a force and calibration inflates it until the empirical slip risk on calibration grasps is at most α. The guarantee is cheap, but its price in force depends on what the predictor knows. A rule that cannot see friction must cover the whole friction range with one inflation factor, and with μ spanning a factor of more than three, the calibrated force is conservative for most objects. The relevant comparison for a tactile method is therefore not an uncalibrated controller but the *strongest non-tactile conformal baseline*: a method that uses everything a robot knows without touch (mass, commanded motion, aperture, even privileged object-family identity) and is calibrated to the same α. We selected this comparator on a disjoint selection split before any calibration or test data were read. The physics plug-in CSF-1 (selection-split mean relative excess 0.7686) beat Mondrian-CSF with privileged family identity (0.8294) and a learned proprioceptive predictor CertGrip-P (0.8335).

This framing raises three questions. Can a ramp-down probe supply enough friction information to cut excess grip force at a certified physical slip rate of at most α? Which component carries the saving: static touch, a probing squeeze, the friction-onset probe, or a learned model on top? And does calibration survive distribution shift when the only feedback available on a robot is whether the object slipped?

Our answer combines one mechanism with one statistical tool. The mechanism is the probe. After a fixed preload F₀ = 32.7 N, identical for every object and therefore uninformative about mass and friction, the gripper lowers its force until a touch-only detector reports incipient slip; under Coulomb friction the onset force gives μ̂ = m g/(2 F_onset). The tool is CRC on the binary physical slip loss, applied per disturbance stratum. Its guarantee, which we call "certified" throughout, is marginal and in expectation: within a stratum, the slip rate is at most α in expectation over the calibration draw and the test grasp. We report a high-probability Learn-then-Test variant \cite{angelopoulos2025learn} next to it. CRC on the physical loss, rather than split conformal on simulator labels, is needed because the pre-registered monotonicity gate failed: in 8 of 800 instances the label rule was not monotone in force.

**Contributions.**
- **(C1) Method: probe, then a simple force rule, then a certificate.** A grasp protocol in which a friction-free preload makes a ramp-down onset probe the only friction channel, and CRC on the monotonised physical slip loss turns any probe-fed force rule into one whose expected slip is at most α per stratum. The simplest instance is a one-line Coulomb plug-in on the onset; the learned quantile model is optional.
- **(C2) Pre-registered evaluation against the best non-tactile conformal comparator.** At α = 0.10 the probe arm reduces mean relative excess force by D = 0.4168 (CI\*\* [0.3484, 0.4778]) relative to CSF-1. Secondary analyses compare the arms at matched slip and under a high-probability certificate.
- **(C3) Attribution.** Ablations and stronger baselines locate the saving in the probe. The plug-in on the same onset already captures it; static touch, the squeeze and the learned model add no demonstrated gain at the primary noise level; a sufficiently good non-tactile friction prior leaves no shown advantage; and there is a sub-pool in which the method loses.
- **(C4) Online calibration under shift from binary feedback.** Frozen calibration breaks under friction and amplitude shifts, while quantile tracking keeps slip near α, also with physical feedback (descriptive). Efficiency against oracle recalibration is inconclusive.

We state the confirmatory record plainly. Of four pre-registered core decisions one is confirmed (the main comparison); the validity premise and the learned-versus-plug-in contrast are not confirmed, and the online efficiency decision is inconclusive (Table 0). Section 2 positions the work, Section 3 defines the problem and method, Section 4 gives the protocol and every deviation from the pre-registration, Section 5 reports results, and Sections 6 to 8 discuss, state limitations and conclude.

| Code | Question | Status | Outcome |
|---|---|---|---|
| H1 (H1-M, H1-V) | Is the simulator's slip label monotone in force and faithful to physics? | primary | not confirmed (monotonicity gate failed) |
| H2a | Probe arm vs strongest non-tactile conformal baseline (efficiency at α) | primary | superiority |
| H2b | Learned model vs physics plug-in on the same onset (σ 0.2) | co-primary | not confirmed |
| H3 | Online tracking vs oracle recalibration under shift (ratio R_E) | primary | inconclusive (S1, S2, S3) |
| H4a / H4e / H4c | Feature chain; touch on top of onset; shuffled touch | secondary | Table 2 |
| H5 | Probe arm vs non-tactile friction prior of noise σ_p | secondary (second round) | held as predicted |
| H2-R | H2a contrast in a narrow-friction, mid-amplitude sub-pool | secondary, no prediction | reversal |
| H1c | Do uncalibrated targeters miss α? | secondary | not confirmed (inconclusive) |
| A1 / A2 / B2 / B3 | Matched-slip frontier / Learn-then-Test / probe + fixed margin / online physical feedback | secondary (second round); B2, B3 descriptive | Tables 1–3 |

*Table 0. Hypothesis glossary. The text uses descriptive names; codes appear in this table and in table rows. "Second round" marks analyses registered after the first read-out; all of them are secondary.*

## 2 Related Work

**Tactile slip, friction reading and grip control.** Reading friction from incipient slip is an established idea. Rubber-based tactile sensors were used early on to detect incipient slip and control grip \cite{marconi1996incipient}, and surveys of tactile friction estimation and slip detection \cite{chen2018tactile, romeo2020methods} describe a mature literature in which incipient slip, the partial slip at the contact periphery that precedes gross sliding, is the key friction cue. Human precision grip adapts force to surface friction \cite{johansson1984roles} and to sudden friction changes \cite{willemet2024grip}. On the robot side, slip detectors on multifingered hands \cite{james2020slip}, learned temporal detectors on barometric sensors \cite{grover2022detect} and reactive multifingered controllers that combine slip onset with internal-force optimisation \cite{ayral2026reactive} trigger corrective tightening. Closer to minimal-force grasping, \cite{dong2019maintaining} keep grasps within slipping bounds by monitoring incipient slip, \cite{khamis2021real} estimate friction in real time and add a margin to the target force, \cite{boonstra2024estimate} learn to estimate incipient slip for gentle grasping, and \cite{niu2026synchronized} couple online friction estimation with adaptive grasp control. Learned and reflex controllers extend this to dynamic interaction \cite{kuo2025tracing}, vision-tactile reflexes \cite{feng2026tactilereflex} and sim-to-real force policies \cite{lach2024zero}; adaptive analytical controllers come with Lyapunov arguments \cite{almohammed2022switched}, independent finger controllers stabilise grasps \cite{veiga2020grip}, and vision-language models select pre-grasp forces from experience \cite{shang2026exp}. In all of these the margin is reactive, hand-set or estimated, and none states a distribution-free bound on the resulting slip rate.

**Robust and safe grasping under uncertainty.** Model-based approaches bound the risk of losing a grasp through assumed uncertainty sets. Grasping-force optimisation has been examined under parameter uncertainty \cite{cloutier2018examining}; control barrier functions enforce friction-cone constraints \cite{cortez2019control} and, with disturbance observers and tactile sensing, give adaptive safe grasping \cite{kim2024robust}; friction-informed risk margins \cite{enwerem2026firmgrasp} and variational belief parameterisations \cite{enwerem2026variational} make grasp synthesis tolerant of multimodal uncertainty. These guarantees hold relative to a model and its uncertainty set. Our certificate holds relative to the data-generating distribution of grasps, without a friction model, at the price of being marginal over grasps and needing calibration data from that distribution.

**Conformal prediction and risk control.** Conformal prediction gives finite-sample, distribution-free guarantees under exchangeability \cite{vovk2005algorithmic, lei2017distribution, angelopoulos2023conformal}. Conformalized quantile regression adapts to the input \cite{romano2019conformalized}; training-conditional \cite{bian2023training} and class-conditional or clustered \cite{ding2023class} variants refine the marginal statement. Conformal risk control generalises coverage to bounded monotone losses \cite{angelopoulos2022conformal}, with extensions to non-monotone losses \cite{angelopoulos2026conformal} and non-exchangeable data \cite{farinhas2023non}; Learn-then-Test gives high-probability risk control by multiple testing \cite{angelopoulos2025learn}. Under shift, adaptive conformal inference \cite{gibbs2021adaptive, gibbs2022conformal}, conformal PID control and quantile tracking \cite{angelopoulos2023conformala}, decaying step sizes \cite{angelopoulos2024online} and semi-bandit feedback \cite{ge2024stochastic} keep long-run coverage near target. In robotics, conformal tools certify decisions \cite{lekeufack2024conformal}, verification and control \cite{lindemann2025formal, lindemann2023conformal}, motion planning among dynamic agents \cite{dixit2022adaptive}, contact-aware state estimation \cite{marques2026particle}, LLM planners \cite{ren2023robots}, sensorimotor policies under shift \cite{huang2023conformal}, RL safety filters \cite{strawn2023conformal}, safe Bayesian optimisation \cite{zhang2024bayesian}, interactive imitation learning \cite{zhao2024conformalized} and perception-planning pipelines \cite{kumar2026learnable}. The controlled quantity there is a prediction set, a trajectory region or a decision loss; none certifies a physical contact outcome as a binary loss over a family of grip forces.

**Novelty.** Lowering the force until slip to read friction is not new. What is new is (i) a protocol in which the onset is the *only* friction channel, so its value can be isolated; (ii) a distribution-free, per-stratum bound on the *physical* slip rate of the resulting minimal force; and (iii) evidence that the calibrated saving comes from the probe, not from the learned model.

## 3 Problem Formulation and Method

### 3.1 Certified minimal-force grasping

A grasp instance x comprises an object (family, geometry, mass m, friction coefficient μ, centre-of-mass offset), a grasp pose offset, and a disturbance of known type d ∈ {D1, D2, D3, D4} (lift acceleration, shake, lateral pull, payload added mid-hold) with an amplitude. A parallel-jaw gripper commands a grip force F, and slip(F, x) ∈ {0, 1} is the physical outcome of a full episode: a slip is a tangential displacement of the object relative to the pad frame above 2 mm, a rotation about the grasp axis above 3°, or loss of pad contact. The minimal no-slip force F\*(x) is bracketed in simulation by log-space bisection on [F_min, F_max] = [0.1, 100] N with one replay at F_max and 10 halvings (11 replays), giving F\*_lo < F\*_hi and F\*_mid = √(F\*_lo F\*_hi). A force rule is scored by its mean relative excess and its physical slip rate,

$$\mathrm{RE}(F) = \mathbb{E}_x\big[(F(x) - F^*_{\mathrm{mid}}(x))/F^*_{\mathrm{mid}}(x)\big], \qquad \mathrm{SR}(F) = \mathbb{E}_x[\mathrm{slip}(F(x), x)],$$

where RE is signed and includes slipped instances. The task is

$$\min_F \ \mathrm{RE}(F) \quad \text{s.t.} \quad \mathrm{SR}(F) \le \alpha,$$

with the constraint enforced without a contact model, from calibration instances drawn from the test distribution. Two rules A and B are compared on identical test instances by $D = 1 - \mathrm{RE}(A)/\mathrm{RE}(B)$, so D > 0 means that A needs less excess force. The labels F\* exist only in simulation; this is why the certificate below is defined on the physical outcome and why Section 3.5 gives a label-free online route.

### 3.2 Grasp protocol and the friction-onset probe

Every method runs the same protocol, so every method sees the same physical history up to the moment it chooses F. The gripper closes to a constant preload F₀ = 32.7 N (m g/μ with m_max = 1 kg and μ_min = 0.3) and holds it for 0.4 s; because F₀ is the same for every instance, it encodes neither mass nor friction. A probe squeeze F₀ → 1.5 F₀ → F₀ follows over 0.3 s. Then comes the **ramp-down probe**: the force falls log-linearly from F₀ towards 0.005 F₀ over 0.25 s. A detector that reads only the pad touch grids computes the shear/normal ratio r = Σ_pads |shear| / Σ normal from noisy taxels and declares onset when the smoothed log r stops rising (constants in Table 5); a total normal reading below 1 mN declares onset directly. At onset the force returns to F₀ within 0.02 s and holds for 0.1 s; the gripper then ramps to the chosen F, settles, and runs the 0.6 s disturbance window. The slip reference is the pose before the probe, so a slip during the probe counts as a slip of the grasp.

The onset gives the Coulomb reading μ̂ = m g/(2 F_onset), clipped to [0.1, 3]. Because simulated touch is cleaner than a real sensor, we add onset noise in log units, $\tilde f = \log F_{\mathrm{onset}} + \sigma\varepsilon$ with $\varepsilon \sim \mathcal{N}(0,1)$ drawn once per instance and σ ∈ {0, 0.1, 0.2, 0.4}. All core decisions use **σ = 0.2**, an assumed level; σ = 0 is an upper bound on what the probe can deliver. The same noisy onset is passed to every arm that uses it. Static touch at the preload hold and the squeeze features are recorded from noise-free grids, which favours the arms that use them and makes the attribution conservative.

### 3.3 Force rules

Every rule has the form $F(x;\lambda) = \min\big(F_{\max},\, F_{\mathrm{base}}(x)\, e^{\lambda}\big)$, where λ is a log-force offset set by calibration. They differ only in $F_{\mathrm{base}}$ and in what it may read (Table 4).

- **Probe-fed plug-in CSF-μ̂:** $F_{\mathrm{base}} = m(g + a_{\mathrm{cmd}})/(2\hat\mu)$, with μ̂ from the noisy onset. This is the simplest instance of the method.
- **Probe-fed learned model:** a gradient-boosted quantile predictor ĝ(x) at level τ = 1 − α. Its nested feature sets are P (proprioception: disturbance type, commanded acceleration, log mass, aperture at contact) ⊂ S (+ static touch and a preload-slip flag) ⊂ full (+ squeeze features) ⊂ CertGrip-full (+ onset feature $(\tilde f, \text{found})$); onset-only is P plus the onset feature.
- **Non-tactile baselines:** CSF-1, $F_{\mathrm{base}} = m(g + a_{\mathrm{cmd}})/(2\bar\mu)$ for D1/D2 and $m g/(2\bar\mu)$ for D3/D4, with $\bar\mu$ the geometric mean of the μ range; Mondrian-CSF, the same formula with one offset per family × disturbance cell (16 cells) \cite{ding2023class}, given privileged family identity; and CertGrip-P. The comparator COMP is the best of these three by mean label-rule RE at α = 0.10 on the selection split, committed before any calibration or test file was read.
- **CSF-proxy (second round):** the CSF-1 formula with $\bar\mu$ replaced by a non-tactile friction prior $\tilde\mu = \mathrm{clip}(\mu\, e^{\sigma_p \varepsilon_p}, 0.1, 3.0)$, $\varepsilon_p \sim \mathcal{N}(0,1)$ per instance and independent of ε, σ_p ∈ {0.2, 0.4, 0.8}. It is an oracle-side construction that asks how good a friction prior from material or vision would have to be; it is not a deployable estimator. σ_p is log-noise on a friction prior and σ is log-noise on an onset force; the two are different noise models and are never placed on one scale.
- **Probe + fixed margin (second round, uncalibrated):** $F = (1 + \kappa)\, F_{\mathrm{base}}^{\hat\mu}$, the uncalibrated CSF-μ̂ force with one hand-set margin κ ∈ {0, 0.25, 0.5, 1.0}.

Mass is given to every method on the stated assumption that a robot can weigh the object during the lift; external disturbance amplitudes (D3, D4) are hidden from all methods.

| Arm | mass, a_cmd | static touch | squeeze | onset | family ID | friction prior |
|---|---|---|---|---|---|---|
| CSF-1, CertGrip-P | ✓ | | | | | |
| Mondrian-CSF | ✓ | | | | ✓ | |
| CSF-proxy (σ_p) | ✓ | | | | | ✓ (oracle-side) |
| CSF-μ̂, probe + fixed margin | ✓ | | | ✓ | | |
| onset-only | ✓ | | | ✓ | | |
| CertGrip-full | ✓ | ✓ | ✓ | ✓ | | |

*Table 4. Inputs per arm. All arms run the same physical protocol.*

### 3.4 Certificates on the physical binary loss

For an arm with base force $F_{\mathrm{base}}$ and calibration instance i, define the physical loss and its monotonised version on a grid Λ,

$$L_i(\lambda) = \mathbb{1}\{\text{slip in a direct replay at } F(x_i;\lambda)\}, \qquad \tilde L_i(\lambda) = \max_{\lambda' \ge \lambda,\ \lambda' \in \Lambda} L_i(\lambda').$$

The loss is the outcome of a fresh simulated episode, not the bisection label. $\tilde L_i$ is non-increasing in λ and $\tilde L_i \ge L_i$, so a risk bound on $\tilde L$ implies the same bound on physical slip.

**In-expectation certificate (CRC, primary).** Within each stratum, with n = 500 calibration instances and $\tilde R_n(\lambda) = \frac{1}{n}\sum_i \tilde L_i(\lambda)$,

$$\hat\lambda = \min\Big\{\lambda \in \Lambda : \frac{n \tilde R_n(\lambda) + 1}{n + 1} \le \alpha\Big\},$$

and λ̂ = max Λ if no grid point qualifies, a fallback that voids the bound and is reported. By \cite{angelopoulos2022conformal}, a test instance exchangeable with the stratum's calibration instances satisfies E[slip at F(x; λ̂)] ≤ α. The expectation runs over the calibration set and the test instance together: the bound is marginal and per stratum, not a guarantee for one deployment, one object or one family.

**High-probability certificate (Learn-then-Test, secondary).** Per stratum, λ is scanned from the top of the grid downwards and kept while the one-sided Clopper–Pearson upper bound at δ = 0.1 of the calibration physical risk at λ is at most α; λ̂_LTT is the last kept value (max Λ, flagged, if none) \cite{angelopoulos2025learn}. This gives P(risk ≤ α) ≥ 1 − δ per stratum over the calibration draw, the training-conditional view of \cite{bian2023training}. It holds per stratum at δ = 0.1, not family-wise across strata.

**Grids.** The primary CRC grid is fixed per arm before calibration: Λ = q̂_sel + linspace(−0.4, 0.4, 20), with q̂_sel the label-rule conformal quantile of the arm's scores on the selection split, pooled over strata. A post hoc refined grid, q̂_sel,d + linspace(−0.8, 0.8, 41) per stratum, is a sensitivity route; under its pre-fixed reporting rule it can mark a primary-grid result as unreliable but cannot upgrade a decision. For the second-round CSF-proxy arms a grid-edge rule was registered: if a stratum's λ̂ lands on index 0 or 19, the arm is re-run on the refined-grid recipe.

```
Algorithm 1: probe-then-certify (per arm, per disturbance stratum d)
input : base-force rule F_base (CSF-mu-hat plug-in or learned model), grid Lambda,
        calibration instances {x_i} in stratum d, level alpha
0  every instance: preload F0, squeeze, ramp-down probe -> F_onset (+ onset noise sigma); F_base(x) uses it
1  for i in calibration set, for lambda in Lambda:
2       L[i, lambda] <- slip of a direct replay at min(F_max, F_base(x_i) * exp(lambda))
3  Ltilde[i, lambda] <- max_{lambda' >= lambda} L[i, lambda']                       # monotonise
4  CRC: lambda_hat <- first lambda with (sum_i Ltilde[i, lambda] + 1)/(n + 1) <= alpha, else max(Lambda) (flag)
5  LTT: scan lambda downwards from max(Lambda); keep while CP_upper(risk at lambda; delta) <= alpha
6  deploy: preload, squeeze, probe -> F_onset; command F = min(F_max, F_base(x) * exp(lambda_hat))
```

**Design rationale.** The pre-registered certificate was split conformal on bisection labels with the one-sided score $s = \log F^*_{\mathrm{hi}} - \log \hat g(x)$ \cite{romano2019conformalized}. It certifies the label event F < F\*_hi, which transfers to physical slip only if slip is monotone in F. The monotonicity gate tested this on 800 instances and failed (8 non-monotone, one-sided Clopper–Pearson upper limit 0.02115 > 0.02; 7 of 8 under D2). Following the registered failure branch, the primary route became CRC on the physical loss, which needs no monotonicity; the label route is reported as secondary. The monotonised loss costs slight conservatism wherever the raw loss flickers. LTT is added because CRC's in-expectation bound permits realised slip above α on a given calibration set.

**Complexity.** Calibration needs |Λ| direct replays per instance (20 on the primary grid), choosing λ̂ is O(|Λ| n) per stratum, and LTT adds one Clopper–Pearson bound per grid point. Because every calibration and test instance is replayed on the full grid, the bootstrap recomputes λ̂ in each draw without new simulation. At deployment the method costs one probe of under 0.4 s and a closed-form force.

### 3.5 Online calibration from binary feedback

On hardware, F\* labels and replays are unavailable, but whether the object slipped is observed after every grasp. Score-space online quantile tracking (OQT) \cite{angelopoulos2023conformala} updates one log-force offset per stratum,

$$q_{t+1} = q_t + \eta\,(\mathrm{slip}_t - \alpha), \qquad F_t = \min\big(F_{\max},\, F_{\mathrm{base}}(x_t)\, e^{q_t}\big),$$

with η = 0.1 × IQR of the in-distribution calibration scores (η = 0.03412, frozen) and anti-windup that skips the update when F_t was capped at F_max. We track in score space rather than with the level update of adaptive conformal inference \cite{gibbs2021adaptive}, because a friction drop can move scores beyond the support of the calibration scores, where a level-indexed tracker saturates. Reference arms are decaying-step OQT \cite{angelopoulos2024online}, frozen offline calibration, and an oracle that recalibrates on labelled instances from the shifted distribution. Two feedback variants are studied. The pre-registered study uses label-rule feedback slip_t = 1{F_t < F\*_hi,t} with the label-route offset as warm start. The second-round study feeds the physical slip of a replay at F_t and warm-starts from the CRC λ̂, which is the route a robot would use.

## 4 Experimental Setup

**Simulator and objects.** All experiments run in MuJoCo 4.0.0 (timestep 0.002 s, elliptic friction cone, impratio 10, condim 6), with physics parameters identical for every family and shift. The parallel-jaw gripper has a force-controlled closing axis and one touch grid per pad. Fast tactile simulators exist \cite{wang2022tacto, akinola2025tacsl, leins2025hydroelastictouch}, and sensor configuration matters for learned manipulation \cite{luu2025manifeel, birtalan2026impact}; we use MuJoCo's pad grids with the explicit noise model of Section 3.2. In-distribution families are F1 boxes, F2 cylinders, F3 capsules and F4 off-CoM composites; F5 thin plates are held out as a new-family shift. Friction is log-uniform on [0.3, 1.0] and mass log-uniform on [0.05, 1.0] kg. Friction is drawn independently of family, geometry, mass, CoM offset and disturbance, so no non-tactile input carries friction information by construction. Disturbances are applied with the hand held still: D1 lift acceleration U[1, 10] m/s² and D2 shake (amplitude U[5, 20] mm at U[2, 5] Hz) enter as inertial pseudo-forces, D3 lateral pull U[0.5, 2]·m g and D4 payload U[0.2, 1.0]·m as forces on the object. Every object receives one instance per disturbance type. A report-only check confirms that static touch carries no friction information in this contact model: the summed pad normal reading differs from F₀ by at most 0.1597 N, and no instance slipped during the preload.

**Splits.** Splits are by object within family: train objects 0–149, selection 150–199, calibration 200–324, test 325–499. Calibration has n = 500 instances per stratum (2,000 in total) and test has 2,800 (700 per stratum). The selection split (800 instances from 200 objects) is used only to choose COMP and to centre the grids. Pilot objects, used to set the detector constants, are disjoint from all of these.

**Shifts and streams.** S1 lowers friction (μ × 0.6), S1m lowers it mildly (μ × 0.9, not a primary shift), S3 scales every disturbance amplitude by 1.5, and S2 introduces family F5. The pre-registered streams have T = 2,000 steps: steps 1–500 in-distribution, the shift from step 501, evaluation window 1,001–2,000, 20 orderings, label-rule feedback, with physical outcomes audited by direct replay on ordering 0. The second-round physical-feedback streams use the same pools and orderings 0–4 for S1 and S3 only, with CertGrip-full and CSF-1, 500 in-distribution steps followed by 1,500 shifted steps, and windows 1–500 (pre-shift), 1,001–2,000 and 1,501–2,000.

**Metrics and decision rules.** Efficiency is RE against F\*_mid with D as the effect size; validity is the physical slip rate in direct replay. The four core decisions share a Bonferroni split of a 5 % family-wise level (one-sided 0.0125 each). CI\*\* denotes a two-sided 97.5 % percentile interval from 2,000 object-cluster bootstrap draws that resample calibration and test objects within family and recompute λ̂ (or q̂) in every draw. The main comparison requires D ≥ 0.10 (the smallest effect size of interest, SESOI), a CI\*\* lower limit above 0, and both again with F\*_lo and F\*_hi in place of F\*_mid. The learned-versus-plug-in contrast declares superiority by the same rule and equivalence if the CI\*\* lies inside ±0.10. The online decision passes iff the CI\*\* upper limit of R_E = RE_window(OQT-CertGrip)/RE_window(Oracle-CertGrip) is below 1.10 in S1, S2 and S3 and the two arms' window physical slip rates differ by at most 0.02. σ\* is the smallest σ at which the CI\*\* lower limit of the main D falls below 0.10. Secondary analyses, including all second-round rows, are unadjusted and labelled; second-round decisions are superiority if the CI\*\* lower limit is above 0, inferiority if the upper limit is below 0, and "not shown" otherwise. Matched-slip RE uses one target slip (0.10), found by linear interpolation between adjacent grid offsets k ∈ {−4, …, +4} and repeated inside every bootstrap draw; all matched-slip intervals have 2,000 of 2,000 valid draws. A few diagnostics use other intervals (95 % with 500 draws for the friction-residual diagnostic; a 95 % random-effects interval for the pooled cell analysis; Clopper–Pearson for the monotonicity gate), and we say so where they appear.

| Item | Value |
|---|---|
| Preload / squeeze | F₀ = 32.7 N for 0.4 s; F₀ → 1.5 F₀ → F₀ over 0.3 s |
| Probe | F₀ → 0.005 F₀ log-linear over 0.25 s; return in 0.02 s, hold 0.1 s |
| Detector | 500 Hz; 6-frame smoothing; 8-frame rise < ½ stick rise, 2 consecutive frames; armed at r > 0.1 |
| Taxel noise | multiplicative lognormal 0.05; additive 0.002 N; channel gain lognormal 0.10 |
| Onset noise σ | {0, 0.1, 0.2, 0.4}; primary 0.2 (assumed) |
| Friction-prior noise σ_p (CSF-proxy) | {0.2, 0.4, 0.8} |
| Fixed margins κ (probe + fixed margin) | {0, 0.25, 0.5, 1.0} |
| Labels | log bisection on [0.1, 100] N, 11 replays |
| Target level α; LTT δ | 0.10; 0.1 |
| Calibration size | n = 500 per stratum (small-calibration check: 50) |
| Primary CRC grid | q̂_sel + linspace(−0.4, 0.4, 20), pooled |
| Refined grid (post hoc) | q̂_sel,d + linspace(−0.8, 0.8, 41), per stratum |
| Learner | gradient-boosted quantile trees (scikit-learn HistGradientBoostingRegressor, quantile loss), τ = 1 − α; 30-configuration random search with 4-fold object-grouped CV, identical for all feature sets; learning rate log-uniform on [0.02, 0.3], max_iter ∈ {100, 200, 400, 800}, max_leaf_nodes ∈ {7, 15, 31, 63}, min_samples_leaf ∈ {5, 10, 20, 40}, l2_regularization ∈ {0, 0.1, 1} |
| OQT | η = 0.03412; anti-windup at F_max; one tracker per stratum |
| Seeds | predictor seed 0 primary, seeds 1–4 refit; onset ε and proxy ε_p fixed per instance; stream orderings `default_rng([4242, shift, ordering])`; bootstrap seed 2026 (second round) |
| Inference | 2,000 object-cluster bootstrap draws; CI\*\* 97.5 %; SESOI 0.10 |

*Table 5. Hyperparameters and protocol constants.*

**Compute.** Simulation is CPU-only; a replay is bit-identical across repeats on the same machine. The logged compute for the first-round study is 14.50 CPU-hours, of which the grid replays dominate (5.72 for the primary grid, 8.03 for the refined grid), because every calibration and test instance is replayed on the full grid for every arm. The second-round analyses A1–A3 reuse these replays; the new arms were budgeted at about 8 CPU-hours in total and used 2.357 logged CPU-hours (1.347 for the friction-proxy and fixed-margin replays, 0.868 for the refined-grid friction-proxy replays, 0.142 for the 20 physical-feedback streams, whose pilot rule allowed 6). The CPU model was not recorded by the job logs.

**Deviations from the pre-registration (stated once).** (1) The CRC route was written after the monotonicity counts were seen and before any predictor existed. (2) The primary grid had a floor defect: λ̂ sat at index 0 in D1/D2 for CSF-μ̂ at σ ≤ 0.2 and at index 1 for CSF-1, so the plug-ins are over-protected there and the primary-grid learned-versus-plug-in estimate is biased towards the learned arm; the refined grid was added post hoc. (3) The pre-registration gives the selection objects once as 200–249 and elsewhere as 150–199; the code and the logged selection use 150–199. (4) The probe arm's location-model prediction under shift was never specified and is untested; the friction-residual diagnostic was computed on calibration plus test objects; the noisy-mass draw was fixed only in a later addendum; the TOST for preservation of the log-ratio advantage under S1 was evaluated after its read-out. (5) The pre-registration specified Holm's correction within secondary families; the operational addenda replaced it with unadjusted intervals. (6) The probe arm, CSF-μ̂ and the split of the touch claim into a main and a learned-versus-plug-in contrast come from a pilot amendment written before any main-pool data existed; it replaced a pre-registered arm built on static touch and the squeeze only. (7) All second-round analyses (frontier, Learn-then-Test, extra contrasts, CSF-proxy, probe + fixed margin, physical-feedback streams) were registered after the first read-out and its review; they are secondary and cannot change a first-round decision. CSF-proxy at σ_p = 0.2 hit the grid edge and was re-run under the registered edge rule.

## 5 Results

### 5.1 Main comparison and certificate variants

**The probe arm needs about 42 % less relative excess force than the strongest non-tactile conformal baseline (pre-registered, confirmed).** COMP selection returned CSF-1. On the 2,800 test instances, CertGrip-full at σ = 0.2 has RE 0.4567 [0.4079, 0.5033] against 0.7832 [0.6968, 0.8583] for CSF-1, so D = 0.4168 with CI\*\* [0.3484, 0.4778]. The point estimate exceeds the SESOI and the lower limit is far above 0, and with F\*_lo and F\*_hi in place of F\*_mid D is 0.4150 and 0.4186; the main comparison is decided as superiority at the Bonferroni-adjusted level. Test physical slip is 0.0829 for CertGrip-full and 0.1021 for CSF-1. Per stratum (report-only, 700 test instances each), CertGrip-full slips at 0.0871, 0.0714, 0.0757 and 0.0971 in D1–D4, all at or below α. CSF-1 slips at 0.1157, 0.0886, 0.1057 and 0.0986, above α in D1 and D3. This is compatible with an in-expectation bound evaluated on one calibration set and finite test strata, and it is why we add a high-probability certificate below.

**At matched slip the saving remains (secondary).** The risk–efficiency frontier (Fig. 1b) removes the unequal realised slip from the comparison. At matched test slip 0.10, RE is 0.4290 [0.4099, 0.4560] for CertGrip-full and 0.7891 [0.7329, 0.8422] for CSF-1, so D_match = 0.4563 [0.4096, 0.4896] (refined grid 0.4475 [0.4111, 0.4880]), superiority. At equal slip the saving is the same size as, or larger than, at the CRC operating points.

**Under a high-probability certificate the saving remains (secondary).** Learn-then-Test (δ = 0.1) raises CertGrip-full's λ̂ indices from 10/10/11/10 to 10/10/12/11, lowering test slip from 0.0829 to 0.0696 and raising RE from 0.4567 to 0.4895; CSF-1 moves to slip 0.0907 and RE 0.8216. D_ltt = 0.4043 [0.3362, 0.4561] (refined 0.4015 [0.3391, 0.4594]), superiority. No Learn-then-Test fallback flag fired in any stratum.

**Route robustness and replication.** Across the CRC, matched-slip and Learn-then-Test routes on both grids, D(CertGrip-full vs CSF-1) ranges from 0.4015 to 0.4563, every CI\*\* lower limit above 0 (smallest 0.3362). These routes re-analyse the seed-0 replays, so they show route robustness, not replication. Replication evidence comes from the predictor refits: seeds 1–4 give 0.4343, 0.4197, 0.3932 and 0.4494 on the primary grid and 0.4145–0.4442 on the label route, all superiority. The effect also holds on the label route, on the refined grid and against Mondrian-CSF (Table 1), and with only 50 calibration instances per stratum (0.4146 at α 0.10, 0.4654 at α 0.20). Over the 16 family × disturbance cells the random-effects pooled D is 0.4388 (95 % [0.4036, 0.4741], τ = 0.0511, Q = 31.04 on 15 degrees of freedom); the lateral-pull cells are the weakest in every family (0.2979, 0.3868, 0.3115 and 0.3348 for F1–F4), and every cell's CI\*\* lower limit is at least 0.16. The tail does not pay for the mean: the ratio of 95th-percentile relative excess is T = 0.5918 [0.5540, 0.6564]. The probe arm closes 0.5172 [0.4489, 0.5762] of the gap between CSF-1 and a privileged oracle. The effect shrinks with onset noise (Section 5.2) and reverses in one sub-pool (Section 5.4).

| Comparison (α 0.10, test) | Route | D | CI\*\* | Decision |
|---|---|---|---|---|
| **H2a: CertGrip-full σ 0.2 vs CSF-1** | CRC, primary grid | **0.4168** | [0.3484, 0.4778] | superiority |
| H2a with F\*_lo / F\*_hi | CRC, primary grid | 0.4150 / 0.4186 | [0.3468, 0.4758] / [0.3501, 0.4798] | holds |
| A1: matched slip 0.10 | frontier, primary / refined | 0.4563 / 0.4475 | [0.4096, 0.4896] / [0.4111, 0.4880] | superiority |
| A2: Learn-then-Test, δ 0.1 | primary / refined | 0.4043 / 0.4015 | [0.3362, 0.4561] / [0.3391, 0.4594] | superiority |
| H2a | CRC, refined grid (post hoc) | 0.4289 | [0.3577, 0.4770] | superiority |
| H2a | label route | 0.4292 | [0.3654, 0.4822] | superiority |
| H2a seeds 1–4 | CRC, primary grid | 0.3932–0.4494 | all lower limits > 0 | superiority |
| H2-C vs Mondrian-CSF | label route | 0.4381 | [0.3733, 0.4872] | superiority |
| H2-T (P95 ratio T) | CRC, primary grid | 0.5918 | [0.5540, 0.6564] | pass |
| **H2-R narrow-μ, mid-amplitude sub-pool** | label route | **−0.2614** | [−0.5320, −0.0325] | method worse |

*Table 1. Main comparison, certificate variants and robustness. Arm values on the primary CRC route: CertGrip-full RE 0.4567, physical slip 0.0829; CSF-1 RE 0.7832, slip 0.1021. Under Learn-then-Test: 0.4895 / 0.0696 and 0.8216 / 0.0907. Rows other than the first two are secondary and unadjusted.*

### 5.2 Where the saving comes from

**A plain plug-in on the onset already captures the saving (secondary).** On the CRC route against CSF-1, the physics plug-in CSF-μ̂ on the same noisy onset reaches D = 0.4149 [0.3322, 0.4890] on the refined grid (primary grid 0.3816 [0.2965, 0.4505], biased against CSF-μ̂ by the grid floor), and onset-only reaches 0.4464 [0.3776, 0.4906] (refined 0.4412 [0.3846, 0.4942]); all are superiority. Probe, a simple force rule and CRC are enough.

**The learned model shows no demonstrated gain over the plug-in at σ = 0.2 (co-primary, not confirmed).** The pre-registered read-out is D(CertGrip-full vs CSF-μ̂) = 0.0569 [−0.0399, 0.1454], whose interval contains both 0 and the SESOI. On the refined grid D is 0.0240 [−0.0949, 0.1001], whose upper limit lies just above the ±0.10 equivalence margin; on the label route it is 0.0134 [−0.0850, 0.0814], within ±0.10 (secondary, not decision-bearing). Equivalence is not claimed. The primary-grid point estimate mixes slip levels (0.0829 against 0.0657 for the over-protected plug-in). At matched slip on the refined grid, CSF-μ̂'s RE (0.4045 [0.3892, 0.4369]) is below CertGrip-full's (0.4292 [0.4074, 0.4522]) with overlapping intervals, consistent with "not confirmed". Against CSF-1, CSF-μ̂'s D is larger than CertGrip-full's at matched slip (0.4690 / 0.4793 against 0.4563 / 0.4475, primary / refined grid) but smaller under Learn-then-Test (0.3704 / 0.4040 against 0.4043 / 0.4015) and CRC (0.3816 / 0.4149 against 0.4168 / 0.4289). No direct contrast was computed on these routes, so the ordering of the two is unresolved.

**Static touch, the squeeze and touch on top of the onset add no demonstrated gain.** Along the nested chain (label route, secondary), static touch is equivalent to proprioception within ±0.05 (D −0.0084 [−0.0360, 0.0128]), which in this rigid-contact model is a consistency check of the simulator: static touch reads F₀ and m g/2. There is no evidence that the squeeze helps (D −0.0263 [−0.0558, 0.0149]; equivalence within ±0.03 not shown). Adding the onset gives D = 0.4739 [0.4148, 0.5229]. The full pipeline shows no advantage over onset-only (D −0.0534 [−0.1233, 0.0508], not confirmed; refined −0.0219; label route −0.0417, secondary), and onset-only's D against CSF-1 is the larger of the two on all six route × grid rows (e.g. D_match 0.4736 against 0.4563). Shuffled touch is inconclusive (D −0.0253 [−0.0526, 0.0085]).

**Onset noise sets the size of the saving.** The main D is 0.6789, 0.5825, 0.4168 and 0.1401 at σ = 0, 0.1, 0.2 and 0.4; at σ = 0.4 its lower limit (0.0832) falls below the SESOI, so σ\* = 0.4. At σ = 0.2, a learned model shows no demonstrated gain over a plug-in using the same onset estimate. In secondary, unadjusted analyses it is better at σ 0.4 and worse at σ 0: on the label route the plug-in is better at σ 0 (D −0.2022) and σ 0.1 (−0.0753) and the learned model at σ 0.4 (0.3275), and the refined grid agrees in direction (−0.1522 at σ 0, 0.3315 at σ 0.4). The primary-grid superiority rows at σ 0 and 0.1 are unreliable because of the grid floor.

**Friction-information diagnostics.** The cross-validated R² of log μ on each arm's log-force residual is 0.7937 for P and 0.6034 for CSF-1, against 0.0105, 0.0452, 0.2142 and 0.5655 for CertGrip-full at σ = 0, 0.1, 0.2 and 0.4 and 0.0054 for CSF-μ̂ at σ = 0.2 (95 %, 500 draws); the diagnostic is blind to friction-independent noise, so it shows absence of systematic friction dependence, not precision. Without added noise the detector's reading correlates with log μ at 0.9480 (bias +0.3186, SD 0.1103 in log units), and its error correlates with log μ (r = −0.2529) and is largest for capsules (SD 0.1965). Giving both arms the family identity leaves the gain over P intact (D 0.4638 against 0.4555, unadjusted). No-mass and noisy-mass conditions are descriptive only, because the onset confounds m and μ (D 0.4598 and 0.4603).

### 5.3 Stronger baselines

**A good enough non-tactile friction prior leaves no shown advantage (held as predicted, secondary).** As registered, D(CertGrip-full vs CSF-proxy) is 0.8361 [0.8137, 0.8573] at σ_p = 0.8 and 0.5042 [0.4362, 0.5635] at σ_p = 0.4, and at σ_p = 0.2 it is −0.0299 [−0.1903, 0.0816] on the edge-rule grid (primary-grid row 0.0514 [−0.0673, 0.1660], superseded because λ̂ sat at index 0 in D1/D2). The interval first includes 0 at σ_p = 0.2: against a non-tactile prior of log-noise 0.2, CertGrip shows no efficiency advantage, and no equivalence test was registered. The proxy arms' RE is 2.786 [2.527, 3.070] at σ_p 0.8 and 0.9213 [0.8423, 1.002] at σ_p 0.4, against 0.7832 for CSF-1, and 0.4312 [0.3906, 0.4759] at σ_p 0.2 (slip 0.0825) against CertGrip-full's 0.4442 [0.4064, 0.4973] (slip 0.0900) on the same edge-rule grid. Proxy-versus-CSF-1 comparisons were not registered.

**A hand-set margin cannot replace calibration (descriptive).** With one uniform margin on the uncalibrated CSF-μ̂ force, κ ≤ 0.5 under-grips (test RE −0.3829, −0.2287 and −0.0744; overall slip 0.9582, 0.8257 and 0.6182). At κ = 1.0 overall slip is 0.3350 (RE 0.2341), with D1 and D2 over-protected (0.0414, 0.0229) while D3 and D4 stay at 0.6571 and 0.6186. Within this probe-plus-fixed-margin study, no single uniform margin brings every stratum near α; the calibrated arm reaches overall test slip 0.0829 (CRC) and 0.0696 (Learn-then-Test) because calibration sets stratum-specific offsets.

| Comparison | Route | D | CI\*\* | Decision |
|---|---|---|---|---|
| A3: CSF-μ̂ σ 0.2 vs CSF-1 | CRC, refined / primary | 0.4149 / 0.3816 | [0.3322, 0.4890] / [0.2965, 0.4505] | superiority |
| A3: onset-only σ 0.2 vs CSF-1 | CRC, primary / refined | 0.4464 / 0.4412 | [0.3776, 0.4906] / [0.3846, 0.4942] | superiority |
| H4a: S vs P (±0.05) | label route | −0.0084 | [−0.0360, 0.0128] | equivalence |
| H4a: full vs S (±0.03) | label route | −0.0263 | [−0.0558, 0.0149] | not confirmed |
| H4a: CertGrip-full vs full (+ onset) | label route | 0.4739 | [0.4148, 0.5229] | report only |
| H4e: CertGrip-full vs onset-only | CRC, primary grid | −0.0534 | [−0.1233, 0.0508] | not confirmed |
| **H2b: CertGrip-full vs CSF-μ̂, σ 0.2** | CRC, primary grid | **0.0569** | [−0.0399, 0.1454] | **not confirmed** |
| H2b | CRC, refined grid (post hoc) | 0.0240 | [−0.0949, 0.1001] | not confirmed |
| H2b | label route | 0.0134 | [−0.0850, 0.0814] | within ±0.10, secondary, not decision-bearing |
| H4c: shuffled touch vs P | label route | −0.0253 | [−0.0526, 0.0085] | inconclusive |
| **H5: CertGrip-full vs CSF-proxy σ_p 0.2** | CRC, edge-rule grid | **−0.0299** | [−0.1903, 0.0816] | not shown |
| H5: vs CSF-proxy σ_p 0.4 / 0.8 | CRC, primary grid | 0.5042 / 0.8361 | [0.4362, 0.5635] / [0.8137, 0.8573] | superiority |
| B2: probe + margin κ 0 / 0.25 / 0.5 / 1.0 | none | test slip 0.9582 / 0.8257 / 0.6182 / 0.3350 | — | descriptive |

*Table 2. Attribution and stronger baselines. Only the bold H2b row is decision-bearing; the primary-grid H2b row is biased towards CertGrip-full by the comparator's grid floor. The reference arm differs by row. σ (onset noise) and σ_p (friction-prior noise) are different noise models.*

### 5.4 Where it fails

In a sub-pool with μ ∈ [0.5, 0.8] and disturbance amplitudes in the middle half of each type's range (n_cal 352, n_test 548), recalibrated inside the sub-pool, the probe arm is worse than CSF-1: D = −0.2614 [−0.5320, −0.0325]. This secondary analysis carried no registered prediction. A plausible reading is that a narrow friction range removes the variation the probe measures while its noise remains; whether the narrow range causes the reversal is not tested (Section 7). The centre-of-mass mechanism test is inconclusive (D_F4 − D_F1 = 0.0342 [−0.0424, 0.1138]).

### 5.5 Validity of the certificate

The validity premise is not confirmed. The monotonicity gate found 8 non-monotone instances of 800 (Clopper–Pearson upper limit 0.02115 > 0.02), 7 of them under shake; the violations are small, the largest slip force above F\*_hi exceeding it by a relative 0.00225 in distribution and 0.00904 in the shift pools. The physical audit of the label route passes for all four arm × α combinations: the label rule slightly over-counts slips (physical minus label Δ between −0.00429 and −0.00143), and direct-replay physical slip of the label-route rules at α 0.10 is 0.1014 [0.0864, 0.1168] for CertGrip-full and 0.1114 [0.0911, 0.1336] for CSF-1. The split-conformal unit test passes 160 of 160 cells (140 of 140 informative). Uncalibrated targeters over-slip at every level (0.0096–0.0507 above α, every CI\*\* above 0), but at α 0.05 their intervals ([0.020, 0.045] and [0.016, 0.042]) do not exclude the registered +0.025 margin, so the corresponding secondary hypothesis is not confirmed (inconclusive).

### 5.6 Online calibration under shift

**Pre-registered streams (label-rule feedback, 20 orderings).** Frozen calibration breaks under the friction and amplitude shifts: Frozen-CertGrip's window slip reaches 0.3056 (S1) and 0.2461 (S3), and Frozen-COMP's 0.5101 (S1). Neither frozen arm breaks under S2. OQT-CertGrip holds window label slip between 0.0999 and 0.1016 in all shifts, with physical rates on the audited ordering of 0.103, 0.092 and 0.101 (S1, S2, S3), and needs less force than OQT-COMP in every shift (S1 RE 0.4763 against 0.8087). **The online efficiency decision is inconclusive** in S1, S2 and S3: R_E = 0.8778, 1.174 and 0.9629, with realised half-widths of 0.15–0.20 against a projected ≈ 0.12. The matched-rate co-requirement fails in S1 (physical difference 0.032) and S2 (−0.035), and the direction of R_E follows the slip mismatch, so R_E is not like-for-like there. In S1m the R_E upper limit is below 1.10 (0.8871 [0.7723, 1.026]) but the label slip difference is 0.0248 > 0.02. Preservation of the log-ratio advantage over COMP under S1 is not confirmed (ρ − ρ_ID = 0.0857 [−0.0444, 0.1859]). Constant η catches up faster than decaying η (cumulative excess-slip difference 58.15 [48.20, 70.20] in S1 and 42.40 [32.40, 49.35] in S3, unadjusted). No step was capped at F_max.

**Physical feedback with CRC warm start (second round; descriptive, 5 orderings, no interval).** In the shifted windows 1,001–2,000 and 1,501–2,000, mean physical slip over the 5 orderings lies between 0.0936 and 0.1032 for both CertGrip-full and CSF-1 on S1 and S3 (per-ordering range 0.082–0.112), and D_RE(CertGrip vs CSF-1) is 0.4115–0.4216 in those windows. Physical- and label-feedback trackers give close window means (S1 CertGrip, 1,001–2,000: slip 0.1002 against 0.1008, RE 0.4633 against 0.4729). No interval was registered; this is the online analogue of the main comparison, not a test of the online efficiency decision.

| Shift | OQT-CertGrip slip / RE | OQT-COMP RE | Frozen-CertGrip / Frozen-COMP slip | Oracle-CertGrip slip / RE | R_E [CI\*\*] | H3 |
|---|---|---|---|---|---|---|
| S1 (μ × 0.6) | 0.1016 / 0.4763 | 0.8087 | 0.3056 / 0.5101 | 0.0751 / 0.5426 | 0.8778 [0.7404, 1.120] | inconclusive |
| S2 (F5) | 0.0999 / 0.4262 | 0.7398 | 0.1016 / 0.1051 | 0.1346 / 0.3631 | 1.174 [1.023, 1.428] | inconclusive |
| S3 (amp. × 1.5) | 0.1000 / 0.5067 | 0.8635 | 0.2461 / 0.1910 | 0.0863 / 0.5262 | 0.9629 [0.8363, 1.145] | inconclusive |

| B3 (physical feedback, 5 orderings) | CertGrip slip / RE | CSF-1 slip / RE | D_RE |
|---|---|---|---|
| S1, steps 1–500 (pre-shift) | 0.0984 / 0.4274 | 0.1052 / 0.7615 | 0.4387 |
| S1, steps 1,001–2,000 | 0.1002 / 0.4633 | 0.1016 / 0.7915 | 0.4146 |
| S1, steps 1,501–2,000 | 0.1032 / 0.4626 | 0.0988 / 0.7998 | 0.4216 |
| S3, steps 1–500 (pre-shift) | 0.0976 / 0.4192 | 0.1032 / 0.7537 | 0.4438 |
| S3, steps 1,001–2,000 | 0.1010 / 0.5127 | 0.1010 / 0.8719 | 0.4120 |
| S3, steps 1,501–2,000 | 0.0992 / 0.5135 | 0.0936 / 0.8726 | 0.4115 |

*Table 3. Online calibration, α = 0.10. Upper block: pre-registered streams, window 1,001–2,000, label-rule slip averaged over 20 orderings; trackers and frozen arms start from the label-route offset. Lower block: second-round physical-feedback streams with CRC warm start, physical slip averaged over 5 orderings; descriptive, no interval.*

## 6 Discussion

**What the evidence licenses.** The friction information comes from the probe, and CRC makes the resulting saving certifiable. A quarter-second ramp-down, read by a touch-only detector and fed into a one-line Coulomb formula, already captures the saving against the strongest non-tactile conformal baseline (D 0.4149 on the refined grid, against the pre-registered 0.4168 for the learned arm). At σ = 0.2 a learned model shows no demonstrated gain over that plug-in; in secondary, unadjusted analyses it is better at σ 0.4 and worse at σ 0. One exploratory reading is that a learner pays off only when the friction reading is noisy enough that other cues help to denoise it. The operative method is therefore *probe + simple force rule + CRC*, with the learner as an option whose value depends on the sensor. Conformal calibration is what makes the saving certifiable, and the probe is what makes it large.

**What the second-round analyses add.** Two objections to the first-round result were that the arms realised different slip rates and that the certificate held only in expectation. The frontier answers the first: at equal slip 0.10 the saving is at least as large as at the CRC operating points. The Learn-then-Test variant answers the second: a per-stratum, high-probability bound at δ = 0.1 costs both arms some force and leaves D near 0.40. Both re-analyse the same replays, so they show that the conclusion does not hinge on the choice of certificate, not that it replicates. The probe-plus-fixed-margin study shows what calibration contributes beyond the probe: at κ = 1.0 a practitioner's single margin over-protects the inertial strata and under-protects the external-force strata at the same time. One likely reason, not tested, is that the D3 and D4 amplitudes are hidden, so their load multiplier can be absorbed only by a stratum-specific calibrated offset.

**How good must a non-tactile prior be?** The CSF-proxy sweep held as predicted: the advantage shrinks as the friction prior improves, and at a log-noise of 0.2 no advantage is shown. We read this as a statement about the probe's value, not as a defeat: the probe delivers a friction estimate of roughly that quality from touch alone, on every grasp, without any prior knowledge of the object's material. Where vision or object category already predicts friction that well, the probe's marginal value would be small; we did not evaluate a deployable prior of this kind.

**Unexpected results and prior work.** The monotonicity premise failed narrowly, mostly under shake, which forced the physical-loss route. The narrow-friction sub-pool reverses the result, so practitioners should expect the advantage to scale with the friction spread of their object set. Lateral-pull cells were consistently the weakest, a pattern we have not explained. Relative to friction-estimating controllers \cite{khamis2021real, niu2026synchronized} and incipient-slip methods \cite{dong2019maintaining, boonstra2024estimate}, which leave the margin as a design parameter, our results suggest that the same cue plus a model-free calibration step provides most of the saving, and that learned tactile components should be compared against a calibrated plug-in on the same cue. The online results are in line with quantile-tracking theory \cite{angelopoulos2023conformala} and the slower adaptation of decaying steps \cite{angelopoulos2024online}.

**Practical implications.** The probe costs under 0.4 s per grasp. In simulation it found an onset on every in-distribution instance and displaced the object by a median 0.126 mm at onset, with no instance reaching the 2 mm slip threshold during the probe, so objects for which even sub-millimetre slip is unacceptable are outside its scope. Because the offline certificate needs labels and replays that only a simulator provides, the deployable route is the online tracker warm-started from a simulation-calibrated offset and updated from observed slips; it commits the robot to about α T slips over T grasps plus a catch-up transient after a shift.

## 7 Limitations

*Simulation and sensing.* All results come from one simulator (MuJoCo) with rigid contact, rigid primitives and five object families, and a modelled tactile detector. σ = 0.2 is an assumed noise level added on top of the detector's intrinsic error, not a measured property of a real sensor; the main effect weakens quickly with noise, and its lower limit falls below the SESOI at σ = 0.4 (D 0.1401). Hardware grounding of σ was not done. Static touch and the squeeze carry no friction information by construction in this contact model, so that part of the attribution is a simulator consistency check, not a finding about elastomer sensors.

*Instance distribution and baselines.* Friction is drawn independently of all non-tactile inputs, so the ≈ 42 % figure is tied to this distribution. CSF-proxy is an oracle-side construction; no correlated-μ pool, deployable vision or category prior, or reactive slip-tightening controller was evaluated.

*Certificate.* F\* labels exist only in simulation, so the offline certificate is not deployable as is; online tracking with physical feedback is the hardware route, and it was studied on 5 orderings, S1 and S3 only, without intervals. The validity premise failed; validity rests on the CRC route adopted after that failure, and the grid fix is post hoc. Certificates are marginal per stratum; Learn-then-Test holds per stratum at δ = 0.1, not family-wise, and nothing is guaranteed per object, per family or on hardware.

*Unresolved contrasts.* The learned-versus-plug-in contrast is unresolved, and no direct CertGrip-full versus CSF-μ̂ contrast exists at matched slip or under Learn-then-Test. The online efficiency decision was underpowered, and its 20-ordering feedback is the label rule with a label-route warm start. The narrow-friction sub-pool is a regime in which the method loses; its cause, the concentration of non-monotone instances under shake and the weak lateral-pull cells are untested, and the exploratory stratifications of the sub-pool loss by detector error and family and of the lateral-pull margins by hidden amplitude were not run. All secondary analyses, including every second-round row, are unadjusted for multiplicity.

## 8 Conclusion

We asked whether a short tactile probe can make a certified minimal-force grasp substantially gentler, and which component is responsible. In MuJoCo simulation, a ramp-down friction-onset probe combined with conformal risk control on the physical binary slip loss reduces mean relative excess grip force by D = 0.4168 (97.5 % CI [0.3484, 0.4778]) relative to the strongest non-tactile conformal baseline, selected beforehand, at a test physical slip rate of 0.0829 for α = 0.10, under a bound that holds in expectation per disturbance stratum. In secondary analyses the saving remains at matched slip and under a high-probability Learn-then-Test certificate. The saving comes from the probe: a one-line Coulomb plug-in on the onset already captures it, and at the primary onset noise a learned model shows no demonstrated gain over that plug-in, so the method is the probe, a simple force rule and the certificate, with the learner optional. The result has a stated scope limit: in a narrow-friction, mid-amplitude sub-pool the method is worse than the baseline (D = −0.2614), and a non-tactile friction prior of log-noise 0.2 leaves no shown advantage. Under friction and amplitude shifts, frozen calibration breaks while binary-feedback quantile tracking keeps window slip near α, also with physical feedback in a descriptive study; whether it does so within 10 % of the force of oracle recalibration is inconclusive. Of four pre-registered core decisions, one was confirmed. Future work should measure onset noise on a physical gripper with a real tactile sensor, compare against a deployable friction prior and reactive slip tightening, and run the online physical-feedback calibration on hardware, where binary slip is the only signal available.
