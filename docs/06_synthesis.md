# Stage 7 · SYNTHESIS (v1)

> Prompt: `pipeline/references/stage_prompts/synthesis.md` (system: "You are a synthesis specialist for literature reviews."),
> `{topic}` = RESTRICTS.yaml project.topic, `{cards_context}` = `docs/05_knowledge_cards.json` (56 cards).
> Additional full-text check (WebFetch, 2026-10-28) of the closest precursor, Zheng et al. 2026 (arXiv:2603.21410v1).
> Generated 2026-10-28 by the session model.

## Cluster Overview

| # | Cluster | Cards (cite_keys) | One-line takeaway |
|---|---|---|---|
| 1 | Information-driven touch selection for localization / recognition | javdani2012efficient, hebert2013next, petrovskaya2011global, vien2015touch, chen2015submodular, gordon2026active, murali2022active, murali2024shared, ottenhaus2018active, yang2019multifidelity, sipos2023multiscope | Touches are chosen online by one-step (greedy) information criteria or surrogates evaluated on a belief at decision time. |
| 2 | Heuristic / belief-guided active tactile recognition and pose | zheng2026bayesian, zheng2024bayesian, kuster2026belief, pai2023tactofind, bonzini2022leveraging, saleem2026manipulation | Rich Bayesian beliefs (incl. free-space evidence) but next-touch rules are geometric heuristics, not information objectives. |
| 3 | Learned tactile exploration policies (RL / attention) | riou2024reinforcement, riou2021seeing, niemann2024when, fleer2020efficient, xu2023tandem3d, kamtikar2026tactful, shahidzadeh2023actexplore, schneider2025tactile | Policies are fast at run time but trained on task / coverage / classification rewards; no information-theoretic objective, little joint pose+identity belief. |
| 4 | Touch-based pose estimation and filtering (no action selection) | koval2015pose, drigalski2020contact, manuelli2016localizing, bauza2023tac2pose, kelestemur2020bayes, zirui2026tacloc, ye2026you, liang2020hand, rostel2022state, sodhi2021tactile, suresh2021tactile, suresh2024neuralfeels, gandler2020object | Mature estimators; contact/no-contact likelihoods exist (manifold PF); they assume the touches are given. |
| 5 | Policy-based / amortized Bayesian experimental design | foster2021deep, ivanova2021implicit, blau2022optimizing, vincent2022policy, hedman2025step, rainforth2024modern, kleinegesse2020sequential, iqbal2024nesting, iqbal2024recursive, huang2026aline, asano2022sequential, shen2023reinforcement | sPCE / InfoNCE-style bounds let a design policy be trained offline and run in milliseconds; demonstrated on scientific toy models (source location, hyperbolic discounting, SIR), not on tactile robotics. |
| 6 | Theory of adaptive information gathering | javdani2012efficient, chen2015submodular, esfandiari2019adaptivity | Under adaptive submodularity greedy is near-optimal; when hypotheses are hard to separate (non-submodular regimes) myopic selection can be poor. |
| 7 | Context: touch in dexterous manipulation, surveys, simulators | seminara2019active, navarroguerrero2023visuo, calandra2018more, qi2023general, lin2022tactile | Motivation and tooling. |

## Cluster 1 — Information-driven touch selection

Greedy information gain has a long history in touch localization: Hebert et al. (hebert2013next) pick the next best touch by expected information; Javdani et al. (javdani2012efficient) connect touch selection to (adaptive) submodularity, giving guarantees for greedy hypothesis pruning; Chen et al. (chen2015submodular, DiRECt) note that myopic value-of-information approximations "are known to perform poorly" and propose a non-myopic submodular surrogate — still optimized online at every step. Recent work keeps the online, local flavour: Gordon et al. (gordon2026active) compute EIG from Fisher information around an MLE and refine candidate actions with cross-entropy search, and state that EIG is local and fails when the MLE is a bad local minimum. Murali et al. (murali2022active, murali2024shared) select viewpoints/touches by information gain in visuo-tactile pipelines. Common pattern: per-decision optimization over candidates on the current belief → cost grows with particles × candidates × outcome samples; selection is one-step.

## Cluster 2 — Heuristic belief-guided active tactile recognition

Zheng et al. (zheng2026bayesian) maintain a joint belief over object class and 6D pose with a customized particle filter that fuses contact, GelSight patches and **free-space (no-contact) evidence** — the full text shows the next touch is chosen by a max–min distance rule on the MAP shape (farthest from explored and unreachable points), one-step, no expected-value computation, decision time not reported; computation grows with the number of object priors. Zheng et al. 2024 (zheng2024bayesian) use a global-shape heuristic to guide exploration. These works show joint identity+pose beliefs with negative information are practical, but leave the *selection rule* uninformed by expected information.

## Cluster 3 — Learned tactile exploration

Riou et al. (riou2024reinforcement, riou2021seeing) train RL agents with classification, exploration and pose rewards; Niemann et al. (niemann2024when) and Fleer et al. (fleer2020efficient) learn haptic attention for classification and when to stop; TANDEM3D (xu2023tandem3d) co-trains exploration with recognition; TACTFUL (kamtikar2026tactful) trains on hardware with a dynamic reward schedule; AcTExplore (shahidzadeh2023actexplore) rewards shape coverage. Tactile MNIST (schneider2025tactile) provides a benchmark for active tactile localization/classification. None trains on an information bound; rewards are hand-designed mixtures whose relation to posterior uncertainty is indirect.

## Cluster 4 — Touch-based estimation

Koval et al. (koval2015pose) model the contact/no-contact dichotomy in a manifold particle filter; Manuelli & Tedrake (manuelli2016localizing) localize contacts with a particle filter; Tac2Pose (bauza2023tac2pose) estimates pose of known objects from the first touch; learned filters (kelestemur2020bayes, rostel2022state, sodhi2021tactile) and tactile SLAM (suresh2021tactile, suresh2024neuralfeels) track pose and shape. These supply our belief/likelihood machinery; they do not decide where to touch.

## Cluster 5 — Policy-based BED

DAD (foster2021deep) trains a design network on the sPCE lower bound of total EIG so that designs are produced "in milliseconds"; iDAD (ivanova2021implicit) removes the likelihood requirement; Blau et al. (blau2022optimizing) cast sequential BED as an MDP with sPCE-increment rewards solved by RL — permitting non-differentiable simulators; RL-DAD (vincent2022policy) does the same with likelihood-free bounds and mentions robotics as a motivating domain; Step-DAD (hedman2025step) adds test-time refinement; Rainforth et al. (rainforth2024modern) review bounds and estimators. Evaluations in these abstracts are scientific models (location finding, CES, SIR), not touch.

## Cluster 6 — Theory

Adaptive submodularity makes greedy competitive (javdani2012efficient); adaptivity gaps and semi-adaptive policies (esfandiari2019adaptivity) quantify how much adaptivity matters. Implication for us: the non-myopic advantage, if any, should appear where hypotheses are hard to separate in one step (symmetric / similar shapes, small budgets) and shrink as the budget grows.

## Cluster 7 — Context

Touch is necessary for dexterous manipulation under occlusion (calandra2018more, qi2023general); surveys (seminara2019active, navarroguerrero2023visuo) list active haptic perception as open; simulators exist (lin2022tactile) but tactile-image rendering is GPU-heavy, which supports our choice to model contact outcomes rather than tactile images.

## Gap 1 — No amortized, information-bound-trained touch policy for localization
No card trains a touch-selection policy on a bound of expected information gain about pose/identity; information-based methods (Cluster 1) optimize online and one-step, learned policies (Cluster 3) use task rewards. *Falsifiable:* a policy trained on the sPCE bound either reaches lower posterior pose error at a fixed budget than task-reward RL and greedy EIG on the same simulator, or it does not.

## Gap 2 — Myopic vs non-myopic touch selection has not been measured
No card reports the gap between one-step greedy EIG and a non-myopic policy for touch localization as a function of budget and object ambiguity. *Falsifiable:* measure success rate / pose error vs budget T ∈ {3,5,8,10} for greedy-EIG and non-myopic policy on symmetric vs asymmetric object sets; the gap is either significantly > 0 for small T on ambiguous sets, or not.

## Gap 3 — Decision latency of touch selection is unreported
No tactile touch-selection card reports per-decision compute; BED cards claim millisecond designs only on toy models. *Falsifiable:* measure wall-clock per decision for greedy EIG (as a function of particles × candidates) vs a policy forward pass at matched accuracy on the same CPU.

## Gap 4 — Negative (no-contact) information inside a *learned selection policy*
Free-space evidence is used in beliefs (zheng2026bayesian, koval2015pose) but no work tests whether a selection policy that conditions on and plans for no-contact outcomes selects better touches than one that ignores them. *Falsifiable:* ablate no-contact outcomes in the policy input/objective; success either drops significantly (especially on ambiguous sets) or does not.

## Gap 5 — Simulator-fidelity transfer of information-optimal touch policies
Policy-based BED has not been checked under a fidelity shift (geometric probe model → physical contact simulation). *Falsifiable:* evaluate the same policy under both fidelities on identical scenes; the ranking vs baselines is preserved or not.

## Prioritized Opportunities

| Rank | Gap | Feasibility (CPU, 5 months) | Novelty likelihood | Fit with SMART goal | Verdict |
|---|---|---|---|---|---|
| 1 | Gap 1 + Gap 2 (amortized non-myopic policy and the myopic–non-myopic measurement) | High: numpy simulator, small network | High (no card combines them; closest precursor uses a heuristic rule) | Core | Core novelty #1 |
| 2 | Gap 3 (latency) | Very high | Medium (DAD claims it generically) | Supports #1 | Required evidence for #1 |
| 3 | Gap 4 (negative information in the policy) | High | Medium (beliefs with free space exist; policy-level use untested) | Core novelty #2 reframed | Keep as secondary contribution, defended by ablation |
| 4 | Gap 5 (fidelity transfer) | Medium (MuJoCo CPU) | Medium | Defence against sim-only critique | Experiment, not a claimed novelty |

**Reframing decided here (recorded for stage 8):** core novelty #2 is no longer "using negative information" (prior art: koval2015pose, zheng2026bayesian) but "a selection policy that is trained to *plan for* no-contact outcomes under multimodal identity×pose beliefs", measured by ablation. Related-work positioning must credit Zheng et al. 2026 and Koval et al. 2015 for no-contact evidence in beliefs, Javdani/Hebert/Chen for greedy information-gain touch selection, and DAD / RL-BED / RL-DAD for the policy-based BED machinery.
