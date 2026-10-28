# Stage 8 · Pass 2 — Skeptic (fresh opus subagent, 2026-10-28)

> System: "You are a senior scientific skeptic. Your job is to find ways each proposed hypothesis could be UNFALSIFIABLE, vague, or trivially true. You are intentionally harsh — the goal is to make every hypothesis precise."
> Task: "For each hypothesis below, identify: precision of prediction; quantitative failure condition; multiple confirming mechanisms and the distinguishing measurement; trivial truth. Output markdown: per-hypothesis critique, then a verdict (KEEP / REVISE / REJECT)."
> `{proposer_output}` = full content of `docs/07a_proposer.md`.

---

## Cross-cutting problems (apply to several hypotheses)

**X1. The stated statistics cannot deliver the stated thresholds.**
- *Wilcoxon over 5 seeds cannot reach p < 0.05.* With n = 5 paired seeds the smallest attainable two-sided Wilcoxon signed-rank p is 2/2⁵ = 0.0625 (one-sided 0.031). H1(3) and H2(1) specify "Wilcoxon … over seeds/episodes". Over seeds, the two-sided test cannot pass. Over episodes, it is pseudoreplication: episodes within a seed are not independent draws of the training process. The unit of analysis has to be fixed in advance. Either use ≥ 10 seeds, or use a hierarchical / cluster bootstrap with seed as the cluster.
- *A 3 pp non-inferiority margin is underpowered at 500 episodes.* At success ≈ 0.5 and paired correlation ρ, SE(Δ) ≈ √(2·0.25·(1−ρ)/500) ≈ 3.2·√(1−ρ) pp. The 95% one-sided bound is then about ±5.2·√(1−ρ) pp. That falls below 3 pp only if ρ ≳ 0.67. Correlation between the two methods' per-episode outcomes is not reported and not guaranteed. The required sample size must be computed from a pilot ρ, or the margin widened.
- *Only H1 applies multiplicity correction.* H1–H4 make about 40 separate significance claims over 8 (set × T) cells. The family-wise correction (Holm per hypothesis, or one pre-registered primary endpoint per hypothesis) has to be stated.

**X2. The success metric is bounded and threshold-dependent, so floor and ceiling effects can produce or erase any gap.** "Identity ∧ < 5 mm ∧ < 5°" has no stated object scale, pose-prior bounds or noise σ. At T = 3 on S every method may sit near 0%, and at T = 10 near 100%. Then "gap vanishes with budget" (H2) and "ranking preserved" (H4) become artifacts of saturation. Fix: (i) state object size, prior bounds, σ_p and σ_n; (ii) report a pilot showing every method's success lies in [10%, 90%] for each cell used in a test; (iii) pre-register a non-saturating co-primary metric, such as the PF's log-probability of the true (k, x, y, θ) or the final posterior entropy, and require each directional claim to hold on it too.

**X3. The evaluation particle filter is unspecified.** Every method is scored with "the same PF (N particles)", but N_eval, the resampling scheme and roughening are not given. If N_eval is small, particle depletion caps achievable accuracy and compresses all differences toward zero. That favors the non-inferiority claims (H1(1), H4) for the wrong reason. Fix N_eval, and show that success is converged in N_eval (for example, under 1 pp change from N_eval to 4·N_eval).

**X4. The prediction and the failure condition are not exact complements in H1, H2, H3 and H4.** Each one leaves outcomes that neither confirm nor refute the hypothesis (details below). Every hypothesis needs a single decision rule: confirmed iff …, otherwise rejected.

---

## H1 — sPCE policy ≈ greedy EIG accuracy at ≥ 100× lower latency, beats task-reward RL

**Precision.** This is a conjunction of three claims (non-inferiority, latency, superiority over RL) bundled as one hypothesis. A single experiment can test it, but a refutation does not say *which* claim failed. Split it into H1a (accuracy vs greedy), H1b (matched-accuracy latency) and H1c (objective vs task reward). Vague points:
- **The greedy PF-EIG baseline is under-specified.** It has N = 2,000 and C = 64, but the number of outcome samples per candidate (M) in the nested Monte Carlo is not given, nor whether candidates are resampled each step, nor how far the code is vectorized. Latency scales linearly with M, so the 100× ratio can be tuned freely.
- **"Task-reward RL (success / negative-entropy reward)" is two different baselines.** A dense negative-PF-entropy-reduction reward telescopes to the total entropy reduction, which is essentially a Monte Carlo estimate of the same total-EIG objective sPCE bounds. Against that variant, H1c tests *estimator variance* (sPCE contrastive bound vs PF-entropy REINFORCE), not "information objective vs task objective". Against sparse success reward, it tests dense vs sparse reward. Pick one, or keep both and predict each separately.
- **"Same training-sample budget"** needs a unit: environment episodes, simulator calls, or gradient steps. sPCE consumes L contrastive samples per episode, and whether those count toward the budget is not stated.

**Quantitative failure condition.**
- **Failure (a) is in the wrong direction for a non-inferiority claim.** The prediction requires non-inferiority (the upper confidence bound of the deficit is < 3 pp) in *all* 8 cells. Failure (a) triggers only if sPCE is *significantly worse by > 3 pp* in ≥ 2 cells. An underpowered study (see X1) therefore can never trigger failure. Absence of evidence is being counted as confirmation. In the same way, "≥ 2 of 8" tolerates one clear failure that the prediction forbids. Fix: confirmed iff the one-sided 95% upper bound of [greedy − sPCE] is < 3 pp in ≥ 7 of 8 cells (pre-registered), and rejected otherwise.
- **The non-inferiority comparison is missing a precondition.** Greedy must itself beat random by a stated margin (for example, ≥ 10 pp at T ≤ 5). Otherwise "within 3 pp of greedy" is uninformative.
- Failure (c) "not significantly worse in aggregate" has no aggregate test defined. Name the test, the unit and the effect-size floor.

**Competing mechanisms.**
- *The latency claim is close to trivially true.* A small MLP or DeepSets forward pass on CPU takes about 10–100 µs. Nested Monte Carlo over 2,000 × 64 × M cannot be done in under a few ms. A ≥ 100× ratio at the stated configuration is therefore guaranteed by construction and should not be headline evidence. The only non-trivial version is clause (b), *matched accuracy*. Promote (b) to the primary latency claim: sweep greedy (N, C, M) to its Pareto front of accuracy vs latency, then compare the policy against the cheapest greedy point within 3 pp of full-size greedy accuracy.
- *Amortization cost is excluded.* A fair comparison of compute reports the break-even episode count: training CPU-hours ÷ per-episode savings. Without it, "100× cheaper" leaves out the most expensive phase.
- *Why sPCE might beat RL.* Possible reasons are (i) the information objective, (ii) a denser or lower-variance gradient, (iii) better hyperparameter tuning. To separate them: report the learning curves (success vs training samples) of both methods, the gradient variance at a fixed checkpoint, and an equal-budget hyperparameter search for each method.

**Trivially true?** Partly, in the latency claim. Not in the accuracy claims.

**Verdict: REVISE.** Split the claims. Make matched-accuracy latency primary and the fixed-configuration ratio secondary. Correct the non-inferiority decision rule. Specify M and the RL reward. Fix the statistical unit and the power analysis.

---

## H2 — Non-myopic advantage concentrated at small budgets on ambiguous sets

**Precision.** This is the most scientifically interesting hypothesis and also the most loosely specified.
- **The control "sPCE-1step" may not be myopic.** By the chain rule of mutual information, total EIG equals the *sum* of expected one-step conditional EIG increments. A policy trained on "one-step EIG increments" with credit flowing from later increments back to earlier actions (for example, return = Σ increments, γ = 1) optimizes the *same* objective as sPCE-total, and Δ should then be ≈ 0 for a trivial reason. The control is myopic only if each action is optimized against its own immediate increment, with no credit assignment across steps (γ = 0, or stop-gradient through the history). This must be stated exactly, with the loss written out.
- **The two objectives have different bound tightness.** A sum of T per-step sPCE bounds and one T-step sPCE bound have different bias at the same L. A nonzero Δ could therefore come from bound looseness, not myopia. Report the high-N nested-MC estimate of the *true* total EIG of both trained policies, and require the Δ in true EIG to have the same sign as Δ in success.
- **Set S is defined qualitatively.** It contains shapes "with near-symmetries" and pairs "sharing long identical edges". The ambiguity property must be stated quantitatively, because it is the independent variable. Example: for S, the mean over beliefs of max-over-actions one-step EIG is ≤ X% of A's, while two-step EIG is comparable. Without this, S is simply "harder", and any method gap there is unexplained.
- Only T = 3 and T = 10 enter the "monotone shrinkage" test. T = 5 and T = 8 are dropped, so "monotone" is untested.
- Prediction (1) says greedy PF-EIG "shows the same sign of deficit". This needs a threshold and a test.
- **Prediction (4), the mechanistic signature, has no thresholds and is confounded.** Higher entropy after touch 1 also follows from a *worse* first move. Required instead: on the *same* belief states, the sPCE-total first touch has lower oracle one-step EIG but higher oracle two-step EIG (greedy second touch) than the sPCE-1step first touch, with paired p < 0.05 and a stated minimum difference (for example, ≥ 0.1 nats).

**Quantitative failure condition.**
- **"Δ(10, S) not significantly different from 0" treats a non-significant result as proof of equality.** With 5 seeds almost anything is non-significant. Use an equivalence test (TOST) with a stated margin, for example |Δ(10, S)| < 2 pp.
- **Shrinkage at T = 10 is likely trivially true because of the ceiling (X2).** If both policies reach ~100% at T = 10, Δ → 0 regardless of mechanism. The shrinkage claim must be shown on the non-saturating metric, or only over cells with success < 90%.
- "Interaction absent (Δ on A as large as on S)" has no threshold. State the interaction test (for example, a set × objective term in a mixed model with seed as a random effect) and the minimum interaction size.
- The prediction requires Δ ≥ 5 pp, but the failure condition requires only "not significantly > 0". A result of Δ = 2 pp with p < 0.05 neither confirms nor refutes the hypothesis.

**Competing mechanisms.** Possible causes of Δ > 0 on S: (i) genuine set-up moves; (ii) differences in bound tightness or gradient variance; (iii) the 1-step control under-training on hard sets; (iv) floor effects on A making |Δ(A)| small (giving a spurious interaction). Distinguishing measurements: the oracle two-step EIG analysis above (i); true-EIG estimates of both policies (ii); training curves until plateau, with identical hyperparameter search (iii); a non-saturating metric (iv). The strongest test is a constructed **positive control**: an object pair where the optimal 2-touch plan is known analytically to require a zero-immediate-EIG first touch. Then check whether sPCE-total discovers it and sPCE-1step does not.

**Trivially true?** The shrinkage part, possibly, because of saturation. The core claim is not trivial.

**Verdict: REVISE.** Define the myopic control's loss exactly. Quantify "ambiguous". Replace "not significant" with equivalence tests. Use a non-saturating metric. Replace the entropy-after-touch-1 signature with paired oracle one-step vs two-step EIG. Add the analytic positive control.

---

## H3 — Planning for no-contact outcomes improves touch selection

**Precision.**
- **The No-NC-objective ablation is not a well-defined likelihood.** The outcome space is {contact with (p, n)} ∪ {no-contact}. For each hypothesis h, P(no-contact | h) = 1 − P(contact | h). Setting the no-contact likelihood constant across h, while the contact likelihood still depends on h, gives an unnormalized and inconsistent model. The sPCE bound computed on it is no longer a bound on anything. The policy may then degrade because its training gradient is *biased*, not because it lost the ability to "plan misses". The ablation must be specified as a normalized alternative model. Example: the policy is trained on a model where outcomes are only "contact (p, n)" observed conditioned on contact, and no-contact episodes are dropped from the contrastive term. The bias that this introduces must also be stated.
- The direction of the effect is ambiguous a priori. A policy that ignores no-contact information may simply learn to *avoid* misses, since they waste budget. That could match or beat Full when contact probes are already very informative. The hypothesis should say why the miss-including strategy dominates on S, quantitatively: what fraction of S's belief states have a best action with predicted P(NC) ∈ [0.2, 0.8].
- Prediction (3), "NC fraction higher on S than on A", is confounded by geometry. If S shapes are thinner or smaller, or have concavities, misses are more frequent under *any* policy. Report the comparison relative to random's NC fraction on the same set.
- The 0.1 nats threshold is quantitative but has no reference point. Compare it with (a) the realized IG of random policy misses and (b) the realized IG of Full's contact probes.

**Quantitative failure condition.**
- **"Neither ablation reduces success significantly" means one ablation is enough to confirm.** That is much weaker than predictions (1) and (2), which require both. The 5 pp effect size from prediction (1) also disappears from the failure condition (X4).
- "Indistinguishable realized information gain" needs an equivalence margin, not a non-significant test.

**Competing mechanisms.** Full > No-NC-objective could reflect (i) deliberate informative misses, (ii) a better-calibrated training objective in general (the ablation's bias hurts contact probes too), or (iii) the history encoder benefiting from the extra signal. **Discriminating measurement:** the *pre-touch predictive no-contact probability* of each chosen probe under the current belief. Planned misses should have P(NC) near the outcome-entropy maximum, roughly 0.3–0.7. Incidental misses would have P(NC) near 0. Also measure the share of each probe's pre-touch EIG that comes from the NC branch, versus the contact branch, under the full model. Prediction: on S, Full selects probes with a higher NC-branch EIG share than No-NC-objective (paired, stated margin). To isolate (ii), compare *contact-only* probes between the two policies. If those probes also have lower EIG under No-NC-objective, the effect is objective bias, not planning.

**Trivially true?** No, but it is at risk of being confirmed for the wrong reason, through the ablation bias.

**Verdict: REVISE.** Define a coherent, normalized ablation likelihood. Require both ablations, with the 5 pp effect size, in the failure rule. Add the P(NC)-at-selection and NC-branch-EIG-share measurements. Normalize the NC fraction against random.

---

## H4 — Rankings survive the geometric → MuJoCo fidelity shift

**Precision.**
- **The fidelity shift is uncontrolled, so the hypothesis can be confirmed by construction.** Whether ranking survives depends almost entirely on fingertip radius, contact stiffness and guard threshold. With a tiny rigid fingertip, MuJoCo nearly reproduces ray casting and H4 is trivially true. Pre-register the MuJoCo parameters, and *measure* the shift: the contact-point bias and normal-error distributions vs the training σ_p and σ_n. Require the shift to be non-trivial (for example, a median point error ≥ 2 σ_p, or a stated fingertip radius ≥ x% of the smallest object feature). Better, sweep fingertip radius at 2–3 levels and predict where ranking breaks.
- **Kendall τ ≥ 0.8 over 5 methods allows exactly one discordant pair out of 10.** Methods that are statistically tied (for example, random and coverage at T = 10, or sPCE vs greedy by H1's own claim of near-equality) produce random rank swaps. Two expected ties together give a substantial probability of τ < 0.8 from noise alone. Compute τ only over pairs separated in geometric fidelity, or test pairwise sign preservation for the pre-registered separated pairs.
- "Conditions where methods are separable (non-overlapping 95% CIs)" — the rule is unclear on *all* pairs vs *any* pair. Non-overlapping CIs is also an overly strict and non-standard test of difference.

**Quantitative failure condition.**
- **The prediction includes an absolute transfer gap ≤ 10 pp, but the failure condition omits it.** Only the relative "greedy + 5 pp" criterion remains (X4).
- 200 scenes give SE ≈ 3.5 pp per method. The difference of two transfer gaps (a four-way contrast) has SE ≈ 5–7 pp. That cannot resolve a 5 pp criterion. Increase to ≥ 1,000 scenes, or widen the margin explicitly.

**Competing mechanisms.** If ranking is preserved, possible reasons are (i) the policy is robust to the mismatch, (ii) the mismatch is tiny, or (iii) all methods degrade toward the PF floor together, which compresses differences. Distinguishing measurements: the measured shift (ii); the absolute MuJoCo success of each method vs random (iii). The gap to random must remain ≥ y pp, not merely be "significant".

**Trivially true?** Possibly, depending on simulator parameters, as written.

**Verdict: REVISE.** Pre-register and measure the size of the fidelity shift, or sweep it. Restrict ranking claims to pre-separated pairs. Restore the 10 pp absolute criterion in the failure rule. Increase scenes or justify the power.

---

## H5 (secondary) — Policy latency flat; greedy latency ∝ N·C

**Precision.** The prediction is precise. The thresholds (b ∈ [0.8, 1.2], R² ≥ 0.9, < 2×, ≥ 100×) are quantitative.

**Trivially true?** **Yes.** Greedy nested-MC EIG does work proportional to N·C·M *by construction*. A fixed-size network's forward pass is independent of N and C *by construction*, and independent of K unless the output head depends on K. The only ways H5 can fail are implementation artifacts: fixed overhead dominating at small N·C (b < 0.8), or BLAS threading on 2 vCPUs. Those failures describe the code, not the science. This is an engineering benchmark, not a hypothesis. Its part (3) duplicates H1(b).

**Non-trivial question that is missing.** The open empirical issue is not latency but *accuracy scaling*. As K grows (4 → 8 → 16), does the amortized policy's success degrade faster than greedy's, given fixed network capacity and training budget? That is the real cost of amortization, and it could fail.

**Verdict: REJECT as a hypothesis.** Keep the latency sweep as a reported measurement supporting H1b. Optionally replace it with "H5′: at fixed network size and training budget, sPCE-total's deficit to greedy PF-EIG on success grows by ≤ x pp per doubling of K", with an explicit failure threshold.

---

## Verdict summary

| Hypothesis | Verdict | Blocking issue |
|---|---|---|
| H1 | **REVISE** | Non-inferiority failure rule is in the wrong direction, so an underpowered study passes. The headline latency ratio is guaranteed by construction. The "task-reward RL" baseline is ambiguous (the dense entropy reward ≈ same objective). |
| H2 | **REVISE** | The 1-step control equals the total objective unless credit assignment is cut (chain rule of MI). "Ambiguous" is not quantified. Shrinkage is confounded by the success ceiling, and a non-significant result is treated as zero. |
| H3 | **REVISE** | The No-NC-objective likelihood is unnormalized, so degradation may reflect gradient bias, not lost planning. The failure rule needs only one ablation and has no effect size. |
| H4 | **REVISE** | The size of the fidelity shift is uncontrolled, so the hypothesis can be confirmed with a tiny fingertip. τ ≥ 0.8 over 5 methods with expected ties is noise-dominated. The 10 pp criterion is dropped from the failure rule. |
| H5 | **REJECT** | True by construction. Keep it as a benchmark under H1b, or replace it with a K-scaling accuracy hypothesis. |

## Three most serious problems

1. **The H2 myopic control may be the same objective as the treatment.** Total EIG equals the sum of one-step conditional EIGs. If sPCE-1step propagates credit across steps, Δ ≈ 0 by construction. If it is mis-specified the other way, Δ may reflect bound tightness rather than non-myopia. The paper's central "non-myopic" claim depends on writing this loss out exactly and adding oracle two-step-EIG and analytic positive-control checks.
2. **The statistical design cannot meet its own thresholds, and failure rules let underpowered results pass.** Wilcoxon over 5 seeds cannot reach two-sided p < 0.05. 500 episodes do not resolve a 3 pp non-inferiority margin unless paired correlation is ≳ 0.67. H1(a), H2 and H3 are phrased so that "not significant" counts in favor of the hypothesis. Fix the statistical unit and run a power analysis, use TOST for equivalence claims, and make each failure condition the exact complement of its prediction.
3. **Bounded, threshold-dependent success plus an unspecified evaluation PF can create or erase every gap.** The 5 mm / 5° threshold has no object scale. With floor or ceiling effects and particle depletion at unknown N_eval, "gap vanishes at large T" (H2), "ranking preserved" (H4) and "within 3 pp of greedy" (H1) can all be produced by saturation. Pre-register a non-saturating co-primary metric (log-probability of the true state or posterior entropy), require success in [10%, 90%] for tested cells, and show N_eval convergence.
