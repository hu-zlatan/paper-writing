# Stage 8 · Pass 1 — Proposer (fresh opus subagent, 2026-10-28)

> System: "You formulate testable scientific hypotheses."
> Task: "Generate at least 2 falsifiable hypotheses from synthesis. Output markdown and for each hypothesis provide rationale, measurable prediction, failure condition."
> `{synthesis}` = full content of `docs/06_synthesis.md`. Constraints respected (from `docs/00_topic_init.md`): CPU-only (2 vCPU sandbox + GitHub Actions CPU runners), simulation only (vectorized numpy geometric probe model; MuJoCo physical fingertip contact), known object library of K rigid shapes, static object, planar SE(2) pose (x, y, θ) + identity first.

## Shared experimental setting (applies to all hypotheses)

- **World:** K known planar shapes (polygons); state s = (k, x, y, θ) drawn from a fixed prior (uniform identity, bounded uniform pose). Object is static.
- **Action:** a guarded probe line (start point, direction) on a fixed workspace boundary, parameterized continuously; candidate sets for baselines are discretized from the same space.
- **Observation:** contact point + surface normal with Gaussian noise (σ_p, σ_n), or a *no-contact* symbol.
- **Belief / evaluation estimator:** the same particle filter (N particles over identity × SE(2)) is used to score *every* method after T touches, so methods differ only in *which* touches they choose.
- **Object sets:** **A** = asymmetric, mutually dissimilar shapes; **S** = ambiguous set (shapes with rotational/reflective near-symmetries and pairs that share long identical edge segments).
- **Budgets:** T ∈ {3, 5, 8, 10}. **Seeds:** ≥ 5 training seeds; ≥ 500 evaluation episodes per condition with shared (paired) episode states across methods.
- **Success:** identity correct AND translation error < 5 mm AND rotation error < 5° (MAP estimate).
- **Methods:** random; coverage heuristic (max–min distance on MAP shape, after zheng2026bayesian); greedy PF-EIG (nested Monte Carlo over C candidates); task-reward RL (same architecture, success/negative-entropy reward); **sPCE-total** (ours: policy trained on sPCE bound of total EIG over T); **sPCE-1step** (same architecture, trained on one-step EIG increments only).

---

## H1 — An sPCE-trained amortized policy matches greedy EIG accuracy at ≥ 100× lower decision latency, and beats task-reward RL

**Rationale.** Gap 1 and Gap 3: information-driven touch selection (hebert2013next, javdani2012efficient, gordon2026active) optimizes EIG online, with cost ∝ particles × candidates × outcome samples; policy-based BED (foster2021deep, blau2022optimizing, vincent2022policy) amortizes that optimization into a forward pass but has never been tested on touch. Learned tactile exploration (riou2024reinforcement, xu2023tandem3d) uses hand-designed rewards whose relation to posterior uncertainty is indirect. If the sPCE bound is a good training signal, the policy should inherit EIG-level touch quality while costing one small-network forward pass on CPU.

**Measurable prediction.**
1. On both sets A and S, at every T ∈ {3, 5, 8, 10}, sPCE-total success rate is ≥ greedy PF-EIG minus 3 percentage points (non-inferiority margin, one-sided paired test over shared episodes, α = 0.05), using greedy PF-EIG with N = 2,000 particles and C = 64 candidates.
2. Median per-decision wall-clock latency (single CPU core, batch size 1, same machine) of sPCE-total is ≥ 100× lower than greedy PF-EIG at that configuration (expected order: < 1 ms vs > 100 ms).
3. sPCE-total achieves higher success than task-reward RL (same architecture, same training-sample budget) on ≥ 6 of the 8 (set × T) conditions, significant (Wilcoxon signed-rank over seeds/episodes, p < 0.05, Holm-corrected) in aggregate; and both beat random and coverage at T ≤ 5 (p < 0.05).

**Failure condition.** H1 is rejected if any of: (a) sPCE-total is significantly worse than greedy PF-EIG by more than the 3-pp margin on ≥ 2 of the 8 conditions; (b) the latency ratio is < 100× (or greedy PF-EIG can be shrunk to N, C values that are within 100× of the policy's latency while staying within 3 pp of its own full-size accuracy — i.e. the speed-up is not real at matched accuracy); (c) task-reward RL is not significantly worse than sPCE-total in aggregate, or sPCE-total does not beat random/coverage at T ≤ 5.

---

## H2 — The non-myopic advantage is concentrated at small budgets on ambiguous object sets and vanishes as the budget grows

**Rationale.** Gap 2 and Cluster 6: under adaptive submodularity greedy hypothesis pruning is near-optimal (javdani2012efficient), whereas when hypotheses cannot be separated in one step, myopic value-of-information performs poorly (chen2015submodular, esfandiari2019adaptivity). With a symmetric/similar set S, a single touch often yields near-zero immediate EIG for identity or orientation, but a touch that sets up a disambiguating second touch has high two-step value. A total-EIG objective can learn such set-up moves; a one-step objective cannot. With a large budget, both eventually collapse the posterior, so the gap should shrink.

**Measurable prediction.** Define Δ(T, set) = success(sPCE-total) − success(sPCE-1step), same architecture and training compute, paired episodes.
1. On set S: Δ(3, S) and Δ(5, S) are > 0 with p < 0.05 (paired bootstrap / Wilcoxon over seeds), with Δ(3 or 5, S) ≥ 5 pp; and greedy PF-EIG shows the same sign of deficit against sPCE-total at T ≤ 5 on S.
2. Monotone shrinkage: Δ(10, S) < Δ(3, S), and Δ(10, S) is not significantly different from 0.
3. On set A: |Δ(T, A)| < Δ(T, S) for T ∈ {3, 5} (ambiguity × objective interaction positive in a two-way analysis over set × objective at T ≤ 5).
4. Mechanistic signature: the posterior entropy after touch 1 is *higher* for sPCE-total than for sPCE-1step on S (it "sacrifices" first-step information), yet lower after the final touch.

**Failure condition.** H2 is rejected if Δ(T, S) is not significantly > 0 at both T = 3 and T = 5, or if the set × objective interaction is absent (Δ on A is as large as on S), or if Δ does not shrink with T (Δ(10, S) ≥ Δ(3, S)). Per Success Criterion 2, a null result is reported as such, not hidden; a partial result (gap on S but no shrinkage) refutes the "concentrated at small budgets" part.

---

## H3 — Planning for no-contact outcomes, not merely filtering them, improves touch selection on multimodal beliefs

**Rationale.** Gap 4 and the stage-7 reframing: no-contact evidence is already used in beliefs (koval2015pose, zheng2026bayesian), so the claim to test is at the policy level. On multimodal identity × pose beliefs a probe aimed into space that is occupied under some hypotheses and free under others is informative *whichever* outcome occurs; a policy whose objective treats no-contact as uninformative (or whose input drops those history entries) should under-use such probes. Effects should be strongest on S and at small T, where hypotheses differ by which regions are occupied.

**Measurable prediction.** Three variants, same architecture/training budget; all evaluated with the *full* particle filter that uses no-contact likelihoods (so only selection changes):
- **Full:** policy input includes no-contact events; sPCE likelihood includes no-contact probability.
- **No-NC-input:** no-contact steps are masked from the history encoder.
- **No-NC-objective:** in the training likelihood, no-contact outcomes are treated as uninformative (constant likelihood across hypotheses).
Predictions: (1) Full beats No-NC-objective by ≥ 5 pp success on S at T ∈ {3, 5} (p < 0.05, paired); (2) Full beats No-NC-input on S at T ≤ 5 (p < 0.05); (3) the Full policy's fraction of probes that end in no-contact is higher on S than on A, and the per-touch realized information gain (entropy drop of the PF) of its no-contact probes is > 0.1 nats on average on S; (4) effects on A are smaller than on S.

**Failure condition.** H3 is rejected if neither ablation reduces success on S at T ≤ 5 by a statistically significant margin, or if the Full policy's no-contact probes yield realized information gain indistinguishable from the no-contact probes of the No-NC-objective policy (i.e. the policy does not *plan* informative misses — misses are incidental). If only No-NC-input matters but not No-NC-objective, the result is reported as "history conditioning", not "planning for no-contact".

---

## H4 — Rankings and most of the advantage survive the fidelity shift from geometric probe to MuJoCo physical contact

**Rationale.** Gap 5: policy-based BED has not been tested under simulator mismatch. The geometric model idealizes contact as ray–shape intersection with Gaussian noise; MuJoCo adds fingertip radius, finite step/guard thresholds, contact-point bias and normal noise from soft contact. Since the policy only consumes (point, normal | no-contact) observations, and the PF likelihood is shared, mismatch should mostly perturb observation noise rather than the information structure — so relative ranking should be preserved, with a moderate absolute drop.

**Measurable prediction.** Policies trained only on the geometric model (no fine-tuning) and all baselines are run on ≥ 200 identical (k, x, y, θ) scenes per condition in MuJoCo (static object, fingertip moved along the probe line until the contact sensor fires or the line ends), on sets A and S at T ∈ {3, 5, 10}.
1. Method ranking by success rate (sPCE-total, greedy PF-EIG, task-RL, coverage, random) has Kendall τ ≥ 0.8 between fidelities in every condition.
2. sPCE-total keeps a significant advantage over random and coverage at T ≤ 5 in MuJoCo (p < 0.05).
3. Transfer gap (geometric − MuJoCo success of sPCE-total) ≤ 10 pp, and ≤ the gap of greedy PF-EIG + 5 pp (i.e. the amortized policy is not disproportionately brittle).

**Failure condition.** H4 is rejected if Kendall τ < 0.8 in any condition where methods are separable (non-overlapping 95% CIs in geometric fidelity), or if sPCE-total loses its significance over random/coverage in MuJoCo at T ≤ 5, or if its transfer gap exceeds that of greedy PF-EIG by more than 5 pp. In that case the paper reports the gap and, as a diagnosis, the measured MuJoCo contact-point/normal error distribution versus the training noise model.

---

## H5 (secondary) — Amortized latency is flat in belief complexity while greedy-EIG latency scales with particles × candidates

**Rationale.** Gap 3 and Cluster 1: greedy EIG cost grows with N × C × outcome samples, and with K (zheng2026bayesian notes cost grows with the number of priors); a policy forward pass depends only on history length and network size. This is the mechanistic basis of the H1 latency claim and tests whether it holds as the problem grows (more objects, finer beliefs).

**Measurable prediction.** On the same CPU (single core, batch 1, 20 warm repeats), sweeping K ∈ {4, 8, 16}, N ∈ {500, 2,000, 8,000}, C ∈ {16, 64, 256}: (1) greedy PF-EIG median latency fits log-latency ≈ a + b·log(N·C) with b ∈ [0.8, 1.2] (R² ≥ 0.9); (2) policy latency varies < 2× across all K and T ≤ 10; (3) at the smallest greedy configuration whose success on S at T = 5 is within 3 pp of its largest configuration, the policy is still ≥ 100× faster.

**Failure condition.** Rejected if greedy latency is sub-linear in N·C (b < 0.8, e.g. because vectorization saturates the 2 vCPUs differently than expected) such that a cheap greedy configuration reaches matched accuracy within 100× of the policy, or if policy latency grows > 2× with K or T.

---

## Mapping to gaps, success criteria, and compute

| Hypothesis | Synthesis gap | Success criterion (00_topic_init) | Primary fidelity | CPU feasibility note |
|---|---|---|---|---|
| H1 | Gap 1, Gap 3 | SC1 | geometric | PF-EIG baseline is the costliest piece; evaluate it on a subset (≥ 500 paired episodes) on GitHub Actions runners |
| H2 | Gap 2 | SC2, SC3 (non-myopic ablation) | geometric | Two training runs per seed (total vs 1-step); small MLP/DeepSets |
| H3 | Gap 4 | SC3 (no-contact ablation) | geometric | Two extra ablation trainings per seed |
| H4 | Gap 5 | SC4 | MuJoCo | Evaluation only (no training in MuJoCo); ≥ 200 scenes per condition |
| H5 | Gap 3 | SC1 (latency) | geometric | Pure timing sweep, minutes |

Ablation of L (number of contrastive samples) and of the history encoder (SC3) are design ablations, not hypotheses; they are expected to be reported alongside H1–H3.
