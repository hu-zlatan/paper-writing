#!/usr/bin/env python3
"""Stage 6 KNOWLEDGE_EXTRACT: build evidence cards from 04_shortlist.jsonl (abstracts only).

Per-cite_key fields were written by hand after reading each record's abstract.
Title, cite_key, card_id and citation are produced in code from the record.
Run from papers/p2:  python3 code/literature/build_cards_v1.py
"""
import json

NS = "not stated in abstract"
SRC = "docs/04_shortlist.jsonl"
OUT = "docs/05_knowledge_cards.json"

# (problem, method, data, metrics, findings, limitations)
F = {}

F["almohammed2022switched"] = (
    "Grasping unknown objects with a robot gripper without slip while applying minimal force.",
    "Switched adaptive controller with Lyapunov-based stability analysis; translational and rotational slip velocities are driven to the origin.",
    "Experiments on a novel sensorized gripper prototype with objects of different sizes, shapes and weights. Counts not stated in abstract.",
    "Slip velocity convergence (asymptotic stability), slippage prevention, applied force relative to the minimum needed, object deformation.",
    "Lyapunov analysis shows asymptotic stability with slip velocities converging to the origin; experiments show slippage prevention and minimal force without excessive deformation. No numbers reported in abstract.",
    "Control-theoretic (deterministic, Lyapunov) guarantee of slip-velocity convergence, not a probabilistic guarantee that P(slip) <= alpha (inferred). Reactive to measured slip velocity rather than a pre-grasp calibrated force choice (inferred). No distribution-free calibration or online adaptation from binary slip feedback under distribution shift (inferred). Abstract gives no quantitative results.")

F["dong2019maintaining"] = (
    "Detect incipient slip (predict slip) from a vision-based tactile sensor and use it to keep grasps within slipping bounds.",
    "GelSlim imprint motion compared with a 2D planar rigid transformation; the deviation gives a dense slip field monitored in real time at 24 Hz; slip feedback used to adjust gripping force.",
    "10 objects, 240 tests; closed-loop bottle-cap screwing/unscrewing experiment.",
    "Incipient-slip detection accuracy.",
    "86.25% detection accuracy over 240 tests on 10 objects; most failures on highly deformable objects; slip feedback adjusted grip force to avoid slip in a bottle-cap task.",
    "Detector gives a slip flag/field with an empirical accuracy, not a coverage-style guarantee that P(slip) <= alpha (inferred). Assumes mostly rigid objects and 2D rigid-body imprint motion. Force adjustment is a feedback response to detected slip, not a calibrated force selection (inferred). No online calibration under distribution shift (inferred).")

F["khamis2021real"] = (
    "Real-time friction and weight sensing for grip force control, to apply a near-optimal grip force and avoid drops.",
    "PapillArray tactile sensor on each finger of a two-finger gripper senses grip force, object weight, incipient slip and friction; closed-loop grip-force controller targets near-optimal force with an intentionally added 20% safety margin.",
    "Vertical lifting task with an object of varying weight and friction plus some common household items.",
    "Applied grip force relative to the force required to avoid slip.",
    "With a 20% safety margin on the target force, the actual grip force was only 9-30% greater than that required to avoid slip.",
    "Safety margin is a fixed heuristic (20%), not derived from a target slip probability; no probabilistic or distribution-free guarantee (inferred). Relies on a friction estimate from a specific sensor concept. Torque not yet included (future work). No adaptive calibration from binary slip feedback under distribution shift (inferred).")

F["kuo2025tracing"] = (
    "Regulate grasping force to reduce slippage during dynamic object interaction with unknown object properties and unreliable external sensing.",
    "Physics-informed energy abstraction (object as a virtual energy container); the mismatch between applied finger power and retained object energy is a slip-aware stability signal; model-based learning and planning for real-time grasp force optimization from tactile sensing.",
    "Simulation and hardware experiments across diverse motion-object pairs. Dataset sizes not stated in abstract.",
    "Slippage reduction and grasp duration; learning time (minutes).",
    "Learns grasping force control from scratch within minutes, reduces slippage and extends grasp duration, without external sensing or prior object knowledge. No numbers in abstract.",
    "Reduces slippage empirically; no formal bound on slip probability (inferred). Learned energy-dynamics model offers no distribution-free guarantee and no explicit recalibration under shift from binary slip labels (inferred). Quantitative results not stated in abstract.")

F["boonstra2024estimate"] = (
    "Gently grasp objects by anticipating slip, since force regulation otherwise needs the unknown friction coefficient and existing approaches only react after slip.",
    "CNN trained to estimate the grasp safety margin (extra lateral force before the frictional limit) from tactile images of a camera-based sensor tracking 82 colored markers in 3D; a simple proportional controller regulates force using the margin.",
    "High-density camera-based tactile sensor with 82 markers; training set size not stated in abstract.",
    "Safety margin estimate; regrasp reaction time; grasping force.",
    "Proportional controller on the learned margin robustly grasps a wide variety of objects, outperforms slip detection methods, reduces regrasp reaction times and decreases grasping forces to 1-3 N.",
    "Point estimate of the safety margin with no uncertainty interval or finite-sample guarantee on P(slip) (inferred); very close to our setting (force selection from tactile input, no friction prior) but lacks a coverage guarantee and online recalibration from binary slip feedback under distribution shift (inferred). Quantitative accuracy of the margin estimator not stated in abstract.")

F["niu2026synchronized"] = (
    "Gentle grasping by coupling real-time friction estimation with adaptive grasp control.",
    "Particle-filter estimate of the friction coefficient from vision-based tactile sensors, fed into a reactive controller that modulates grasp force; estimation and control run synchronously in a closed loop.",
    "Robotic experiments; details not stated in abstract.",
    "not stated in abstract",
    "Framework validated through extensive robotic experiments; no numbers in abstract.",
    "Bayesian-style (particle filter) friction estimate has no distribution-free finite-sample guarantee on slip probability (inferred). Relies on an explicit friction coefficient model (inferred). Does not use binary slip feedback with conformal calibration. No quantitative results in abstract.")

F["feng2026tactilereflex"] = (
    "Force-sensitive manipulation of fragile deformable containers (e.g. liquid-filled plastic cups) within a narrow force margin between slip and deformation.",
    "Noise-statistics-driven calibration: sensor intrinsic noise (static-hold-and-unload protocol) sets all controller thresholds; three-channel reflex controller (shear intensity, contact intensity, center of pressure) from dual visuo-tactile sensors at about 12 Hz for slip suppression, weight-adaptive release and force protection.",
    "Ablation on container deformation (5 trials per configuration) and a dynamic pouring task (10 attempts, two water volumes).",
    "Success rates (container deformation prevention; pouring success).",
    "Full three-channel system 5/5 success versus at most 1/5 for partial configurations; pouring: fixed-effort baselines fail in all 10 attempts, TactileReflex 9/10 across two water volumes.",
    "Thresholds derived from sensor noise statistics are a heuristic calibration and carry no stated probability bound on slip (inferred). Reflex control reacts to proxies rather than choosing a force with a guaranteed slip risk (inferred). Small trial counts (5 and 10). No online adaptation from binary slip feedback under distribution shift (inferred).")

F["lach2024zero"] = (
    "Tactile-based continuous grasp force control that transfers from simulation to a real robot without fine-tuning.",
    "Model-free deep RL policy trained in a simulation environment producing realistic normal forces; inductive bias and domain randomization to support zero-shot sim-to-real transfer.",
    "Simulated training environment; real-robot evaluation details not stated in abstract.",
    "Policy performance versus a hand-crafted baseline.",
    "Learned policy performs similarly or better than a hand-crafted baseline; ablations show inductive bias and domain randomization facilitate sim-to-real transfer. No numbers in abstract.",
    "Learned policy has no probabilistic guarantee on slip (inferred); under distribution shift it relies on domain randomization rather than online calibration from slip feedback (inferred). Focus on limiting force; slip-probability target not addressed (inferred). Quantitative results not stated in abstract.")

F["veiga2020grip"] = (
    "Grip stabilization for multi-digit robotic hands without monolithic object and contact models.",
    "Modular biomimetic approach: independent per-finger tactile controllers prevent local slip, with slip predicted from BioTac / BioTac SP tactile signals; no central communication.",
    "BioTac and BioTac SP sensors on multi-digit robotic hands; wide variety of objects (counts not stated in abstract).",
    "Grasp stability and resistance to external perturbations.",
    "Stable grasps emerge with independent controllers, resistant to external perturbations across a wide variety of objects. No numbers in abstract.",
    "Slip predicted by a learned/heuristic detector with no probabilistic guarantee (inferred); local reactive control rather than a calibrated force selection (inferred). No distribution-free coverage or online recalibration under shift (inferred). Quantitative results not stated in abstract.")

F["shang2026exp"] = (
    "Select the pre-contact grasp force (minimum feasible force) before the adaptive controller starts.",
    "Experience-conditioned framework: retrieves a few similar prior grasp experiences and conditions a vision-language model for in-context prediction of minimum feasible force from a single RGB image.",
    "129 object instances; real-world tests on 30 unseen objects.",
    "MAE (N); appropriate force selection rate.",
    "Best-case MAE of 0.43 N, reducing error by 72% over zero-shot inference; appropriate force selection rate improved from 63% to 87% on 30 unseen objects.",
    "Vision-based pre-grasp point prediction, no tactile input and no uncertainty quantification or guarantee on slip probability (inferred). Appropriate-force rate of 87% is empirical, not a coverage guarantee. No online calibration from slip feedback (inferred). Compliant grippers; relevance to tactile conformal setting is as a pre-grasp baseline (inferred).")

F["chen2018tactile"] = (
    "Review of tactile sensing for friction estimation and incipient slip detection, needed to find the minimum grip force for secure grasping.",
    "Survey organized by sensor capability: gross slip detection, incipient slip detection, and friction measurement; recommends sensors that encourage incipient slip and measure displacement and deformation.",
    "Literature survey; no dataset.",
    "not stated in abstract",
    "Argues most research ignores sensing frictional properties of the sensor-object interface, which is essential for the minimum grip force; recommends sensor mechanics that allow partial slip and instrumentation measuring displacement/deformation. No numbers.",
    "Survey (2018), predates conformal approaches; does not discuss statistical guarantees on slip probability (inferred). Frames minimum grip force via friction sensing, i.e. assumes a friction-estimation route rather than distribution-free calibration (inferred).")

F["romeo2020methods"] = (
    "Survey of sensors and methods for slip detection and prevention in robotic and prosthetic hands.",
    "Review from classical techniques to latest solutions tested on robotic systems; discusses strengths and weaknesses per technique and sensing technology.",
    "Literature survey; no dataset.",
    "not stated in abstract",
    "Summarizes the state of the art in slip detection and gives future directions; notes no impact on the industrial market has been achieved. No numbers.",
    "Survey (2020) without statistical guarantees for slip prevention (inferred); does not cover conformal or online calibration methods (inferred). Useful as background on slip detection, not as a method for force selection.")

F["james2020slip"] = (
    "Slip detection for grasp stabilization on a multifingered tactile hand.",
    "Support vector machines detect slip on the Tactile Model O (T-MO) hand; real-time response to slip onset tested in multiple scenarios.",
    "11 different objects in various grasps; two real-world scenarios (added weight, lifting at first attempt).",
    "Slip detection capability (numbers not stated in abstract).",
    "T-MO detects slipping, reacts to stabilize the grasp and works in real-world scenarios; no numbers in abstract.",
    "Binary slip classifier without calibrated error control or probabilistic slip guarantee (inferred). Reactive (detect then respond) rather than choosing a grip normal force with risk <= alpha (inferred). No online adaptation under distribution shift reported in abstract.")

F["berman2025autonomous"] = (
    "Autonomous slip-prevention grip force control for a robotic prosthetic hand, with shared control for prosthesis users.",
    "Optical flow sensor detects slip events, which trigger increases in desired grip force in a closed-loop force controller; integrated in shared control with myoelectric position control.",
    "Bench test platform, then human participants grasping, transferring and releasing various objects; comparison with myoelectric-only control in a task with a secondary cognitive task. Participant count not stated in abstract.",
    "Slip prevention, grasp stability, user cognitive effort, task success.",
    "Controller effectively prevented slips and improved grasp stability under various perturbations; shared control reduced cognitive effort and increased task success compared to myoelectric-only control. No numbers in abstract.",
    "Threshold-style reactive increments after detected slip, no guarantee on P(slip) (inferred). Prosthetic-hand application; no statistical calibration or adaptation to distribution shift (inferred). Quantitative results not stated in abstract.")

F["ayral2026reactive"] = (
    "Low-level reflex layer for multifinger grasp stabilization by halting in-hand slip.",
    "Hybrid: learned tactile slip detection (piezoelectric sensing for fast slip cues) plus model-based internal-force control, with piezoresistive arrays for contact localization; no prior object knowledge.",
    "Controlled trials on a multifingered hand under external perturbations; counts not stated in abstract.",
    "Slip onset detection time; grasp response latency; model update and force selection times.",
    "Slip onset detected after 20.4 +/- 6 ms; theoretical grasp response latency on the order of 30 ms; grasp-model updates under 5 ms; internal-force selection about 4 ms; supports sub-50 ms tactile-driven responses.",
    "Focus on latency of a reflex response, not on a probabilistic guarantee on slip (inferred). Learned detector without calibrated error rates (inferred). Internal-force optimization preserves wrench but does not choose force with a slip-probability bound; no online calibration under shift (inferred).")

F["grover2022detect"] = (
    "Detect slip from barometric tactile sensors.",
    "Temporal convolutional neural network trained for slip detection on barometric tactile data.",
    "Barometric tactile sensor data of varied slip speed and direction; two manipulation tasks with common objects. Sizes not stated in abstract.",
    "Detection accuracy (value not stated in abstract).",
    "High detection accuracies, robust to speed and direction of slip, generalizes to unseen real-world scenarios; no numbers in abstract.",
    "Slip detector with empirical accuracy, no distribution-free guarantee or calibration of error rate (inferred). Detection only; does not select grip force (inferred). No online adaptation under distribution shift. Quantitative results not stated in abstract.")

F["willemet2024grip"] = (
    "How humans adapt grip force to sudden changes in friction while holding an object.",
    "Human experiment with an object containing an ultrasonic friction modulation device suspended in a pulley system controlling load; friction changed alone and with load.",
    "Human participants (number not stated in abstract).",
    "Grip force response to friction and load changes.",
    "When load and friction changed simultaneously, grip force was regulated based on safety requirements; participants increased grip force when friction decreased but did not adjust when friction increased.",
    "Human physiology study, not a robotic method; no algorithm or guarantee (inferred). Provides motivation for adaptive grip under changing friction (distribution shift) but no probabilistic slip bound or conformal calibration (inferred).")

F["enwerem2026firmgrasp"] = (
    "Grasp quality metrics that account for friction uncertainty instead of one deterministic friction coefficient.",
    "FIRMGrasp: Conditional Value-at-Risk based risk-adjusted force-closure margin at confidence beta (inscribed-ball radius of the grasp wrench space); proven monotone in beta, differentiable; certifies force closure with probability at least beta for margin > 0.",
    "1,599 LEAP Hand and Allegro Hand grasps; shake and pick tests; MuJoCo trials with RealHand L6 and LEAP Hand.",
    "Probability that a successful grasp is ranked above a failed one; fraction of grasps withstanding lift and lateral pull; retention rate.",
    "53% of nominally force-closed grasps lose closure in the adverse friction tail; ranking probability 0.53 (shake) and 0.67 (pick) for nominal margin versus 0.63 and 0.78 for the risk margin; at adverse friction 0.2, 70% of grasps with positive margin withstand lift and pull versus 25% for nominal-positive but risk-margin nonpositive; 95% of grasps with contact and positive margin retain the object in MuJoCo with RealHand L6.",
    "Probabilistic force-closure certificate (probability at least beta) but it depends on a friction distribution/model assumed in the CVaR evaluation (inferred), so it is not distribution-free. Grasp synthesis for multifingered hands, not tactile grip normal force selection and not online recalibration from slip feedback (inferred). Largely simulation-based evaluation.")

F["kim2024robust"] = (
    "Safe robotic grasping that avoids both damaging and dropping objects, with formal safety guarantees.",
    "Control Barrier Function safety filters enforcing contact force and force-closure constraints with finger force control; technique to estimate contact point, force and torque from tactile sensors at each finger; disturbance-observer-based CBFs compared with other filters.",
    "Numerical simulation of two-finger grasping; real robotic setup with multiple objects including fragile lab glassware.",
    "Safety violation and conservatism.",
    "Disturbance observer-based CBFs gave superior performance for safety guarantees with minimum conservatism; safe grasping achieved in real experiments. No numbers in abstract.",
    "Guarantee is deterministic (control barrier function, set invariance) under a model, not a probabilistic distribution-free guarantee P(slip) <= alpha (inferred). Requires force-closure/friction model assumptions (inferred). No online conformal calibration from binary slip feedback under shift.")

F["cortez2019control"] = (
    "Control barrier functions for sampled-data mechanical systems with model uncertainty, applied to robotic grasping.",
    "Novel robust control barrier functions for sampled-data systems allowing actuator constraints; grasp constraint-satisfying controller ensuring no slip, no overextension and no rolling off the fingertips.",
    "Simulation and experimental results on a robotic hand; details not stated in abstract.",
    "Constraint satisfaction.",
    "Simulation and experiments validate the control for the robotic hand; no numbers in abstract.",
    "Deterministic guarantee under a bounded-uncertainty model, no probabilistic slip guarantee and no statistical calibration (inferred). Slip constraint presumably depends on a friction model (inferred). Does not use tactile input per the abstract; no online adaptation from binary slip feedback.")

F["enwerem2026variational"] = (
    "Robust dexterous grasp acquisition under contact variability, sensing uncertainty and disturbances, optimizing tail risk.",
    "Variational inference of latent contact parameters and object pose with a differentiable Gaussian mixture belief; Gumbel-Softmax and reparameterization for pathwise gradients through a differentiable CVaR surrogate.",
    "Simulation, real serial-chain arm with a multifingered hand (grasp-and-lift under pose uncertainty), and a dataset of 243 force-closed grasps.",
    "Robust grasp success, planning time, tactile grasp-quality proxy, mean absolute calibration error.",
    "Mean absolute calibration error below 0.14 across simulation regimes versus 0.58 for a Cross-Entropy Method planner; roughly an order of magnitude less planning time than particle-filter MPC; both methods succeed on tested real perturbations but the proposed controller uses fewer steps and less time.",
    "Calibration is of a learned belief (model-based) and is not a finite-sample distribution-free guarantee (inferred). Grasp acquisition (pose/contact), not tactile normal-force selection (inferred). No online recalibration from binary slip feedback.")

F["cloutier2018examining"] = (
    "Robustness of grasping force optimization (GFO) methods to uncertainty in contact locations and friction coefficients.",
    "Monte Carlo simulation to estimate probability of failure and sensitivity for three GFO methods (linear, nonlinear, LMI-based).",
    "Two numerical examples representing common human-hand grasps.",
    "Probability of failure; sensitivity.",
    "Nonlinear and LMI methods give acceptable results while the linear method gives unacceptably high failure probabilities; nonlinear method remains acceptable when force direction changes and is considered robust.",
    "Failure probability is estimated by Monte Carlo under an assumed distribution of friction and contact location, not a distribution-free guarantee (inferred). Numerical examples only, no tactile feedback or online adaptation (inferred). Evaluates rather than provides a method with a guaranteed bound.")

F["vovk2005algorithmic"] = (
    "No abstract in record; from title/venue only: foundational treatment of algorithmic learning and conformal prediction (inferred from title; venue Springer eBooks, 2005).",
    "not stated in abstract (no abstract in record)",
    "not stated in abstract (no abstract in record)",
    "not stated in abstract (no abstract in record)",
    "not stated in abstract (no abstract in record)",
    "Abstract missing; from title/venue only. As a foundational reference it is expected to supply the exchangeability-based validity of conformal prediction (inferred from title), but this card cannot state specific results. Online-adaptive calibration under shift and grip application cannot be assessed from the record.")

F["lei2017distribution"] = (
    "Distribution-free predictive inference for regression.",
    "Conformal inference framework producing prediction bands from any regression estimator; compares full conformal, split conformal and jackknife; rank-one-out conformal inference; locally varying length bands; LOCO variable importance.",
    "Empirical results regenerated with the R package conformalInference; datasets not stated in abstract.",
    "Finite-sample marginal coverage; interval length; computational efficiency.",
    "Guarantees finite-sample marginal coverage even when assumptions do not hold; split conformal vs full conformal trade off accuracy and computation. No numbers in abstract.",
    "Regression intervals under exchangeability (inferred); marginal not conditional coverage. Not about binary slip events, grip force or distribution shift (inferred). Provides the split-conformal machinery, not an online adaptive scheme.")

F["romano2019conformalized"] = (
    "Conformal prediction intervals can be conservative since they have constant or weakly varying length across inputs.",
    "Conformalized quantile regression: combines conformal prediction with quantile regression to adapt to heteroscedasticity.",
    "Popular regression datasets (not named in abstract).",
    "Coverage validity; interval length.",
    "Theoretical valid-coverage guarantee; shorter intervals than other conformal methods in experiments. No numbers in abstract.",
    "Regression setting under exchangeability (inferred); no online recalibration or binary feedback. Not applied to grip force or slip (inferred).")

F["angelopoulos2023conformal"] = (
    "Gentle introduction to conformal prediction and distribution-free uncertainty quantification for black-box models.",
    "Tutorial covering practical theory and examples, with extensions to structured outputs, distribution shift, time series, outliers and abstaining models; Python code and Jupyter notebooks.",
    "Real-data example notebooks (not specified in abstract).",
    "Coverage with user-specified probability (e.g. 90%).",
    "Conformal sets have explicit non-asymptotic distribution-free guarantees with any pre-trained model. No numbers beyond the 90% example.",
    "Tutorial; does not itself address grip force, binary slip feedback or tactile data (inferred). Distribution-shift coverage is discussed as an extension; specifics not stated in abstract.")

F["angelopoulos2022conformal"] = (
    "Control the expected value of any monotone loss with conformal-style guarantees (beyond miscoverage).",
    "Conformal risk control generalizing split conformal; tight up to O(1/n); extensions to distribution shift, quantile risk control, multiple and adversarial risk control, and U-statistics.",
    "Worked examples from computer vision and NLP: false negative rate, graph distance, token-level F1.",
    "Expected loss (risk) bound.",
    "Algorithm generalizes split conformal prediction with its coverage guarantee and is tight up to an O(1/n) factor. No numbers beyond that.",
    "Guarantee is on expected risk for monotone losses under exchangeability (distribution shift handled only as extension) (inferred). Not demonstrated on grasp or tactile slip. Slip indicator loss monotone in grip force is a plausible fit, which is an inference, not stated in abstract.")

F["angelopoulos2026conformal"] = (
    "Risk control guarantees for non-monotonic losses with multi-dimensional parameters.",
    "Guarantees for generic algorithms (e.g. empirical risk minimization) applied to possibly non-monotonic losses; guarantee depends on algorithm stability.",
    "Applications: selective image classification, FDR and IoU control of tumour segmentations, multi-group debiasing of recidivism predictions.",
    "Risk control (FDR, IoU, etc.); specific metrics not stated in abstract.",
    "Unstable algorithms have looser guarantees; no numbers in abstract.",
    "Extends risk control beyond monotone losses at the price of stability-dependent, looser guarantees (inferred). Not tied to robotics, tactile data or online binary feedback (inferred). Relevant only if the slip loss is non-monotone in force (inferred).")

F["farinhas2023non"] = (
    "Conformal risk control for non-exchangeable data, e.g. change points, time series or drift.",
    "Non-exchangeable conformal risk control: controls expected value of any monotone loss with data weighted by relevance to a test example.",
    "Synthetic and real-world data (not named in abstract).",
    "Expected risk bound; tightness.",
    "Flexible framework with few assumptions; careful weights can give tighter bounds; experiments show usefulness. No numbers in abstract.",
    "Requires choosing weights and is a batch weighted approach; no explicit online update from per-step binary feedback in the abstract (inferred). Not applied to robotics or tactile data. Guarantee degrades with weight choice and drift magnitude (inferred).")

F["gibbs2021adaptive"] = (
    "Prediction sets in an online setting where the data distribution varies over time in an unknown fashion.",
    "Adaptive conformal inference (ACI): wrapper around any point or quantile predictor; models distribution shift as a learning problem in a single parameter (the miscoverage level) re-estimated continuously.",
    "Two real-world datasets (not named in abstract).",
    "Long-run coverage frequency.",
    "Provably achieves desired coverage frequency over long-time intervals irrespective of the data generating process; predictions robust to visible and significant distribution shifts on two datasets. No numbers in abstract.",
    "Guarantee is long-run average coverage, not per-step or conditional (inferred). Requires observing the true label each step (inferred), whereas slip feedback is binary and about an action outcome. Not applied to grip force; step-size must be chosen, trading off with shift rate (inferred).")

F["gibbs2022conformal"] = (
    "Online conformal prediction where earlier ACI over-weights historical data and needs knowledge of the shift rate.",
    "Modifies ACI with an additional step tuning the gradient-descent step size over time; provably small regret over all local intervals of a given width.",
    "Two real-world datasets: stock market volatility and COVID-19 case counts.",
    "Local regret; coverage.",
    "Provably small regret over all local time intervals of given width; robust and adaptive on real-world shifts. No numbers in abstract.",
    "Developed for time-series prediction sets, not robotics or grip force (inferred). Needs observed labels each round (inferred). Guarantee concerns local coverage frequency, not a single-shot slip probability bound for a chosen force (inferred).")

F["angelopoulos2023conformala"] = (
    "Uncertainty quantification for time series with formal guarantees under systematic errors, trends and distribution shift.",
    "Conformal PID control: combines conformal prediction with control theory (quantile tracking, error integration, scorecasting) to model conformal scores online.",
    "COVID-19 deaths 4-week-ahead forecasting; electricity demand, market returns, temperature with autoregressive, Theta, Prophet and Transformer models.",
    "Coverage.",
    "Improvement in coverage over the ensemble forecaster used in official CDC communications; theory simplifies and strengthens existing online conformal analyses. No numbers in abstract.",
    "Targets real-valued time-series forecasts, not binary slip outcomes or force selection (inferred). Needs ground-truth labels each step. Controller gains add tuning parameters (inferred).")

F["angelopoulos2024online"] = (
    "Online conformal prediction where the coverage is only retrospective and the population quantile is not estimated.",
    "Online conformal prediction with decaying step sizes; retrospective coverage guarantee for arbitrary sequences while estimating a population quantile when it exists.",
    "Theory and experiments (datasets not stated in abstract).",
    "Coverage at each time point and on average.",
    "When the distribution is stable, coverage is close to the desired level for every time point, not just on average. No numbers in abstract.",
    "Decaying step sizes reduce responsiveness to abrupt shift (inferred), which conflicts with the project's distribution-shift requirement unless the schedule is adapted (inferred). Not applied to tactile or grip data.")

F["ge2024stochastic"] = (
    "Online conformal prediction when the true label is only observed if it is in the prediction set (semi-bandit feedback).",
    "Novel online conformal algorithm with sublinear regret against the optimal conformal predictor.",
    "Retrieval task, image classification task and auction price-setting task.",
    "Regret; performance against baselines.",
    "Proves sublinear regret versus the optimal conformal predictor; good empirical performance versus baselines. No numbers in abstract.",
    "Partial-feedback (censored) setting resembles our binary slip feedback structure (inferred), but the guarantee is regret, not a coverage bound on P(slip) (inferred). Stochastic i.i.d.-style assumption (stochastic online) (inferred). Not tested on tactile or grip control.")

F["bian2023training"] = (
    "Stronger training-conditional coverage guarantees for distribution-free predictive inference.",
    "Analysis of training-conditional coverage of several distribution-free methods beyond split conformal.",
    "Theoretical analysis; no dataset stated in abstract.",
    "Training-conditional coverage.",
    "Split conformal achieves training-conditional coverage; some other methods achieve it while it is impossible to guarantee for others without further assumptions.",
    "Theory for batch regression intervals under exchangeability (inferred); relevant to how many calibration samples suffice (inferred) but not to online shift or binary slip feedback. No robotics application.")

F["ding2023class"] = (
    "Class-conditional coverage with many classes and little labeled data per class.",
    "Clustered conformal prediction: cluster classes with similar conformal scores and calibrate at cluster level.",
    "Four image data sets with up to 1000 classes.",
    "Class-conditional coverage; set size.",
    "Clustered conformal typically outperforms existing methods in class-conditional coverage and set size. No numbers in abstract.",
    "Classification with many classes; not a regression/threshold problem such as force selection (inferred). Group-conditional idea may inform per-object conditional coverage (inferred), but the abstract states no shift or online setting.")

F["lekeufack2024conformal"] = (
    "Safe autonomous decisions despite imperfect ML predictions.",
    "Conformal Decision Theory: calibrate decisions directly without constructing prediction sets; provable low-risk guarantees without world-model assumptions, allowing non-IID or adversarial observations.",
    "Robot motion planning around humans and robot manufacturing experiments (details not stated in abstract).",
    "Risk of the decisions; specific metrics not stated in abstract.",
    "Provable statistical guarantees of low risk without assumptions on the world model; experiments demonstrate utility in motion planning around humans and manufacturing. No numbers in abstract.",
    "Closest methodological precedent (calibrating a decision parameter online with risk guarantee), yet not applied to grip normal force or tactile slip (inferred). Guarantee is a long-run average risk, not per-grasp (inferred). Feedback model needed for slip is not described in abstract.")

F["lindemann2025formal"] = (
    "Practical safety guarantees for learning-enabled autonomous systems via conformal prediction.",
    "Overview of conformal prediction-based formal verification and control for autonomous systems; the record's abstract is only an introductory passage.",
    "not stated in abstract",
    "not stated in abstract",
    "not stated in abstract (the abstract text is an introduction, with no results).",
    "Magazine-style overview with no specific method for grasping or slip (inferred). Abstract is truncated/introductory so claims cannot be extracted. Possible motivation for conformal safety in control (inferred).")

F["dixit2022adaptive"] = (
    "Safe motion planning among dynamic agents with unknown motion distributions.",
    "Adaptive conformal prediction on an online data stream to obtain uncertainty sets for multistep-ahead predictions using delayed observations, used inside model predictive control.",
    "Simulation case study: a drone avoiding a flying frisbee.",
    "Probabilistic coverage of prediction sets; safety.",
    "Distribution-free adaptive uncertainty sets with probabilistic coverage that capture changes in prediction quality and agent motion; evaluated in simulation. No numbers in abstract.",
    "Simulation-only; navigation prediction, not grasping or tactile (inferred). Needs observed trajectories to be revealed (inferred). Does not map to binary slip feedback.")

F["marques2026particle"] = (
    "Calibrated uncertainty for robot motion in contact-rich settings with multimodal futures.",
    "CaPTURe: geometry-aware conformal prediction using particle-based models and a calibration dataset of transitions to locally calibrate motion uncertainty and produce probabilistically valid prediction regions.",
    "Two simulated planning tasks: marble in a labyrinth and tight-tolerance peg-in-hole insertion.",
    "Coverage; task success rate.",
    "Achieves the user-specified coverage requirement in and out of contact and up to 30% absolute improvement in task success rate over the best baseline.",
    "Simulation-only; configuration prediction regions rather than grip force or slip (inferred). Calibration dataset is offline (batch), not online under shift (inferred). Contact-aware calibration is topical but not tactile grip.")

F["lindemann2023conformal"] = (
    "Predict failures of cyber-physical systems at runtime with respect to signal temporal logic specifications.",
    "Two predictive runtime verification algorithms using conformal prediction regions for the satisfaction measure or future states; applicable to RNN/LSTM trajectory predictors.",
    "Numerical experiments with an F-16 aircraft and a self-driving car.",
    "Probability of specification violation; prediction region validity.",
    "First formal guarantees (to the authors' knowledge) for predictive runtime verification with widely used trajectory predictors, computationally simple and distribution-free. No numbers in abstract.",
    "Trajectory/STL verification setting; not grasp control or binary slip (inferred). Calibration assumes exchangeable calibration/test trajectories (inferred). Simulation-based examples only.")

F["ren2023robots"] = (
    "LLM planners hallucinate; robots need to know when to ask for help.",
    "KnowNo: conformal prediction to measure and align LLM planner uncertainty, with statistical guarantees on task completion while minimizing human help.",
    "Simulated and real robot setups with different ambiguity modes (counts not stated in abstract).",
    "Task completion guarantee; help requests; efficiency and autonomy.",
    "Performs favorably against ensembles and prompt-tuning baselines in efficiency and autonomy while providing formal assurances. No numbers in abstract.",
    "High-level planning with discrete option sets; not low-level force control or tactile (inferred). Calibration assumes exchangeability with calibration data (inferred); no online adaptation from binary feedback under shift (inferred).")

F["huang2023conformal"] = (
    "Detect and react to distribution shifts in a sensorimotor controller's observables.",
    "Conformal policy learning: switching policies that take conformal quantiles as input, or policies augmented with a quantile and trained by RL.",
    "Simulated autonomous driving and active perception with a physical quadruped.",
    "Detection of shift with formal guarantees; performance versus five baselines.",
    "Formal convergence guarantees in finite time; outperforms five baselines and is simplest besides one ablation. No numbers in abstract.",
    "Uses conformal quantiles to detect shift and switch policies, not to choose a force with a slip-probability bound (inferred). Not grasping or tactile (inferred). Guarantee is about detection/convergence rather than calibrated action selection.")

F["strawn2023conformal"] = (
    "Safe RL controllers among uncertain dynamic agents (pedestrian navigation).",
    "Conformal predictive safety filters: predict agent trajectories, conformal uncertainty intervals, learn a safety filter that follows the RL controller while avoiding the intervals.",
    "Collision avoidance gym environment in simulation.",
    "Number of collisions; conservativeness.",
    "Outperforms existing controllers in simulation and minimizes collisions without overly conservative predictions. No numbers in abstract.",
    "Simulation-only navigation; no tactile or grip force (inferred). Assumes exchangeable calibration for intervals (inferred); no online recalibration from binary feedback stated.")

F["zhang2024bayesian"] = (
    "Black-box Bayesian optimization with a controllable rate of unsafe trials, regardless of constraint function properties.",
    "Safe-Bocp: Bayesian optimization built on online conformal prediction, for noiseless or noisy safety feedback.",
    "Synthetic and real-world data (not named in abstract).",
    "Rate of safety violation.",
    "Satisfies safety requirements irrespective of constraint function properties, at the cost of an arbitrary controllable non-zero violation rate. No numbers in abstract.",
    "Violation-rate guarantee is long-run, with non-zero violations allowed (inferred), so individual grasps can slip. Closest to using binary safety feedback with online conformal calibration (inferred) but no tactile features or grip force application.")

F["zhao2024conformalized"] = (
    "Interactive imitation learning where human feedback is intermittent and the expert shifts.",
    "Intermittent quantile tracking (IQT): online conformal calibration with a probabilistic model of intermittent labels; ConformalDAgger uses IQT intervals to query the expert.",
    "Simulated and hardware deployments on a 7DOF manipulator.",
    "Coverage; number of interventions.",
    "Maintains asymptotic coverage guarantees and empirically achieves desired coverage; ConformalDAgger detects high uncertainty when the expert shifts and increases interventions compared to baselines. No numbers in abstract.",
    "Asymptotic coverage guarantee, not finite-sample (inferred). Feedback is expert labels, not binary slip outcomes (inferred). Not grip force or tactile.")

F["kumar2026learnable"] = (
    "Fixed nonconformity scores in conformal prediction ignore context, giving conservative or unsafe intervals in robotics.",
    "Learnable Conformal Prediction: lightweight neural nonconformity score s_theta(x) using geometric, semantic and model cues, trained for coverage, efficiency and calibration; preserves finite-sample guarantees.",
    "MRPB navigation benchmark; COCO, BDD100K, Cityscapes; CIFAR-100, HAM10000, ImageNet.",
    "Navigation success, path inflation, interval width at 90% coverage, set size.",
    "Navigation success 91.5% vs 87.8% for Standard CP; path inflation 4.5% vs 12.2%; interval width reduced 46-54% at 90% coverage; sets shrunk 4.7-9.9%; real-time on edge hardware.",
    "Offline split/batch calibration with finite-sample guarantee under exchangeability (inferred); no online adaptation under distribution shift in abstract. Not tactile or grip force.")

F["wang2022tacto"] = (
    "Fast simulation of high-resolution vision-based tactile sensors.",
    "TACTO simulator rendering touch readings at hundreds of frames per second, configurable for DIGIT and OmniTact.",
    "Grasp stability prediction from 1 million grasps; marble manipulation control task; sim2real proof of concept.",
    "Rendering speed; grasp stability prediction (values not stated in abstract).",
    "Renders at hundreds of frames per second; demonstrated on grasp stability prediction using 1 million grasps and a sim2real proof of concept.",
    "Simulator; no guarantee or control method (inferred). Possible data source for slip-distribution experiments (inferred), but friction/slip fidelity is not stated in abstract.")

F["akinola2025tacsl"] = (
    "GPU-based visuotactile simulation and learning to generate signals and learn tactile policies.",
    "TacSL library in Isaac simulator with a learning toolkit and a new asymmetric actor-critic distillation RL algorithm for sim-to-real tactile policies.",
    "Contact-intensive training environments in simulation; sim-to-real transfer evaluation.",
    "Simulation speed; policy benefits from distillation and multimodal sensing.",
    "Simulates visuotactile images and extracts contact-force distributions over 200x faster than the prior state-of-the-art.",
    "Simulation tooling; no uncertainty quantification or slip-probability guarantee (inferred). Sim fidelity for slip under shift is not stated.")

F["leins2025hydroelastictouch"] = (
    "Accurate yet efficient simulation of pressure-based tactile sensors.",
    "Hydroelastic contact model producing smooth contact forces for soft-to-soft and soft-to-rigid contacts, integrated in a MuJoCo-based open-source simulator.",
    "Zero-shot sim-to-real transfer of an object state estimation model.",
    "Not stated in abstract.",
    "Validates capacity to synthesize real-world tactile data via zero-shot sim-to-real transfer; no numbers in abstract.",
    "Simulator; no control or statistical guarantee (inferred). Slip behavior fidelity not stated in abstract.")

F["luu2025manifeel"] = (
    "Benchmark for visuotactile manipulation policy learning.",
    "ManiFeel simulation benchmark with contact-rich tasks, modular evaluation across sensing modalities, tactile representations and policy architectures, plus real-world validation.",
    "Simulated tasks; codebase, datasets and checkpoints to be released (sizes not stated in abstract).",
    "Policy performance across tasks and modalities (not specific in abstract).",
    "Tactile sensing enhances policy performance across scenarios; task-dependent strengths of tactile modalities; no numbers in abstract.",
    "Benchmark of supervised policies, not grip force or slip guarantee (inferred). Likely tangential to the conformal contribution (inferred).")

F["birtalan2026impact"] = (
    "Effect of tactile sensor density and layout on grasp learning efficiency.",
    "Simulation comparison of 6 tactile sensor configurations on RL performance using two setups.",
    "Six sensorized simulations in two setups.",
    "RL learning performance (specific metrics not stated in abstract).",
    "Setup-specific and generalized effects across 6 configurations; one configuration consistently best across both setups.",
    "Simulation-only sensor layout study with no guarantee or calibration (inferred). Tangential to the conformal contribution (inferred).")

assert all(len(v) == 6 for v in F.values())
KEYS = ["problem", "method", "data", "metrics", "findings", "limitations"]


def first_surname(authors):
    a = authors[0] if authors else ""
    if isinstance(a, dict):
        a = a.get("name") or a.get("display_name") or ""
    parts = a.split()
    return parts[-1] if parts else "Unknown"


def main():
    recs = [json.loads(l) for l in open(SRC, encoding="utf-8") if l.strip()]
    rk = [r["cite_key"] for r in recs]
    assert len(rk) == len(set(rk)), "duplicate cite_keys"
    missing = [k for k in rk if k not in F]
    extra = [k for k in F if k not in rk]
    assert not missing, f"no card for {missing}"
    assert not extra, f"extra keys {extra}"
    cards = []
    for i, r in enumerate(recs, 1):
        a = r.get("authors") or []
        etal = " et al." if len(a) > 1 else ""
        cite = f"{first_surname(a)}{etal}, {r['title']}, {r.get('venue')}, {r.get('year')}"
        c = {"card_id": "p2c%02d" % i, "title": r["title"], "cite_key": r["cite_key"]}
        c.update(dict(zip(KEYS, F[r["cite_key"]])))
        c["citation"] = cite
        cards.append(c)
    out = {"prompt": "pipeline/references/stage_prompts/knowledge_extract.md",
           "source": "docs/04_shortlist.jsonl (abstracts only)", "cards": cards}
    with open(OUT, "w", encoding="utf-8") as f:
        json.dump(out, f, indent=1, ensure_ascii=False)
    print("wrote", OUT, len(cards), "cards")


if __name__ == "__main__":
    main()
