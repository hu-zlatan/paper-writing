# Stage 18 peer review (v3 draft, run 2): independent reviewer pair

**Paper:** *Probe, Then Calibrate: Conformal Slip-Risk Control of Grip Force from a Tactile Friction-Onset Probe (a Simulation Study)*
**Venue lens:** RSS program committee (the rubric in the prompt is NeurIPS/ICML-style 1–10; we use it as given)
**Reviewer role:** balanced, rigorous about methodology-evidence consistency
**Date:** 2026-11-10

---

## 0. Independent verification (shared by both reviewers)

Both reviewers wrote their own scripts under `/tmp/claude-0/rev2/`. The scripts read the raw replay files directly (`results/v1/crc/*.jsonl`, `results/v1/crc_v2/`, `results/v2/crc09{,e}/`, `results/v3/crc10{,e}/`, `results/v{2,3}/b3/`, `results/v1/labels/`). They did not use the authors' analysis JSONs. The scripts reimplement monotonised CRC per stratum ((n R̃ + 1)/(n + 1) ≤ α, first qualifying index, else the top of the grid), RE over avoidable instances, D, the object-cluster bootstrap, the sub-pools, the re-splits and the online window statistics.

| Claim in paper | Recomputed | Status |
|---|---|---|
| Learned probe arm RE 0.4567, slip 0.0829; CSF-1 RE 0.7832, slip 0.1021; **D = 0.4168** | 0.4567 / 0.0829; 0.7832 / 0.1021; D 0.41682 | exact |
| CI\*\* [0.3484, 0.4778] (2,000 draws, seed 2026) | [0.3519, 0.4736] (my 1,000 draws, other seed) | consistent within Monte Carlo error |
| H2b learned vs plug-in 0.0569 [−0.0399, 0.1454] | 0.05692; my CI [−0.0353, 0.1416] | consistent |
| σ curve D 0.6789 / 0.5825 / 0.4168 / 0.1401 | identical | exact |
| Seeds 1–4: 0.4343 / 0.4197 / 0.3932 / 0.4494; seed-4 slip 0.1018 | identical | exact |
| Mean (median) hold force 6.521 (4.473), 6.519 (4.423), 7.062 (4.556), 7.606 (5.476) N | identical | exact |
| Mean excess 1.623 vs 2.708 N; F\*_mid quantiles 0.9549 / 3.184 / 11.35 N, max 31.87 N, share > 32.7 N = 0 | identical | exact |
| Per-stratum slips, primary grid (learned, CSF-1, plug-in) and refined grid (learned, CSF-1) | identical | exact |
| Friction-quintile slip (learned 0.2161→0.003571; plug-in 0.08571→0.02857; CSF-1 0.4804→0) | identical | exact |
| Refined grid: D 0.4289; plug-in 0.4149; plug-in slip/RE 0.075 / 0.4551; learned vs plug-in 0.02397 | identical | exact |
| Plug-in λ̂ at index 0 in D1/D2 (primary) | idx [0, 0, 14, 12] | confirmed |
| Shrunk plug-in: 0.435 / 0.4522 / 0.4484; σ 0.4: 0.2454; learned vs shrunk −0.03216 / −0.06463 / −0.03532; σ 0.4 −0.1395, slips 0.08214 / 0.09286 | identical (−0.1396 at σ 0.4, a rounding difference) | exact |
| Unshrunk plug-in at σ 0.4 RE 0.9877; σ 0 / 0.1 learned-vs-plug-in 0.246 / 0.1072 / 0.3182; refined plug-in RE 0.208 / 0.2915 vs learned 0.2397 / 0.3212 | identical | exact |
| Friction prior σ_p 0.2 / 0.4 / 0.8: prior RE 0.4312 / 0.9213 / 2.7859; D −0.0299 / 0.5042 / 0.8361 | identical, **but see B-W6 for the "edge rule" label** | exact |
| Uniform margin κ = 1.0: slip 0.3350, RE 0.2341, strata 0.0414 / 0.0229 / 0.6571 / 0.6186 | identical | exact |
| Sub-pools on refined grid: −0.3152 / −0.1717 / +0.4929; plug-in −0.6804 / −0.3705; primary grid +0.3754 / +0.3387 / +0.5004; 352 cal / 548 test | identical | exact, **but see A-W2** |
| H2-R label route −0.2614 [−0.5320, −0.0325], Holm p 0.03 / 0.12; 52 rows, 40 rejected | matches `a3_holm.json` | confirmed |
| Re-splits (200): learned 0.08469 / 0.05 / 0.57; plug-in 0.07121 / 0.0 / 0.405; CSF-1 0.08514 / 0.12 / 0.41 | my 200 re-splits (seed 99): 0.0825 / 0.035 / 0.495; 0.0702 / 0.0 / 0.375; 0.0847 / 0.11 / 0.355 | consistent (seed variability) |
| Online physical feedback: every window slip and D_RE in Table 4, and the 95 % intervals | identical to 4 d.p. (20 orderings, v2 o0–4 + v3 o5–19 for S1/S3) | exact, **but see B-W4** |
| Fig. 1b frontier points (all 36) and D_match 0.4563 (linear interpolation) | identical | exact |
| Monotonicity gate: 8 / 800, 7 of 8 in D2, CP upper 0.02115 | `h1m_analysis.json`; my `beta.ppf(0.9875, 9, 792)` = 0.021147 | confirmed (the level is 98.75 %, one-sided, which the paper does not state) |
| Preload: max deviation 0.1597 N, no preload slip; onset found on 100 % of instances | 0.159697 N; 0 / 8,000; found rate 1.0 | confirmed |
| Break-even 13.22 s, probe-specific phases 14.3458 N·s, shared phases 27.4258 N·s | reproduced arithmetically, **but the accounting omits a probe-specific phase (A-W3)** | arithmetic correct, definition incomplete |
| Learner: 30-config random search, GroupKFold(4), hyper-parameter ranges; η = 0.1 × IQR = 0.03412 | `certgrip/models.py`, `h3_streams.py`, stream headers | confirmed |

**Trial count / fabrication check.** The paper's counts all match the code and raw files: n = 500 calibration and 700 test instances per stratum, predictor seeds 0–4, 2,000 bootstrap draws, 200 re-splits, 20 orderings × 3 shifts × 2,000 steps, 52 Holm rows. The simulator is deterministic, so "seeds" means predictor refits; the paper says so. Every inferential procedure the paper names (object-cluster percentile bootstrap, Clopper–Pearson, Holm, TOST via CI, Bonferroni split) is present in `code/`. **We found no fabricated number and no mismatch in trial counts.** The problems we found are about interpretation and accounting, not invented results.

**Topic adherence.** The draft stays on the stated topic: probe, CRC on the physical binary loss, the strongest non-tactile conformal baseline, attribution ablations and online binary feedback. It does not present environment problems as contributions. The deviations list and the compute appendix are procedural, not contributions.

**Length.** By our count: Abstract 236 words, Introduction 825, Related Work 611, Method 1,920, Setup 756, Results 3,653, Discussion 529, Limitations 378, Conclusion 220, Appendix 614; about 9,760 words in total. Every section clears the minimum. The risk is the opposite: with four dense tables, the paper is well over a 9-page (or RSS 8-page) budget, and the Results section reads like an audit log (see A-W5).

---

## Reviewer A: robotics / tactile manipulation

### Summary
The paper proposes a fixed grasp protocol: a 32.7 N preload, a squeeze, then a log-linear ramp-down that stops at touch-detected incipient slip. The onset force gives μ̂ = m g/(2 F_onset). A hold-force rule fed with μ̂ is calibrated per disturbance stratum by CRC on the binary physical-slip loss. In MuJoCo at α = 0.10, it uses 41.7 % less relative excess force than a friction-blind conformal Coulomb rule. Ablations show that a one-line plug-in on the onset captures most of the saving. A binary-feedback online tracker returns to α after three shifts.

### Strengths
1. **Honest framing.** The paper states plainly that the result is simulation-only, that the bound is marginal per stratum and in expectation, that offline calibration needs simulator replays, and that three of four pre-registered decisions are not confirmed or inconclusive. RSS reviewers rarely see this degree of candour.
2. **The right comparator.** Comparing against a *calibrated* friction-blind rule chosen beforehand on a disjoint split, rather than against an uncalibrated controller, is the correct design for asking what touch buys under a slip guarantee.
3. **The attribution result is useful to the community.** The learned model shows no demonstrated gain over a Coulomb plug-in on the same onset, and a shrunk plug-in beats it at σ = 0.4. That is a sobering, practically relevant message for learned tactile grip control.
4. **Force in newtons and force-time.** Reporting absolute hold forces, the preload's dominance and a break-even hold time is the kind of accounting robotics papers usually skip.
5. **Fully reproducible numbers.** Every headline and table value we recomputed from raw replays matched (Section 0).

### Weaknesses
**A-W1. The headline effect is close to true by construction (major).** Friction is drawn log-uniform on [0.3, 1.0] *independently of every non-tactile input*. So no non-tactile rule can carry friction information, and CSF-1 is nearly the Bayes-optimal friction-blind rule. D = 0.42 therefore mainly measures how wide the friction prior is relative to the probe's noise; it does not measure a property of tactile grip regulation. The paper says so in Section 6, which we appreciate. But the abstract and contributions still present D = 0.4168 as the result. The two oracle-side checks (friction prior σ_p = 0.2 gives D ≈ −0.03; the sub-pool μ ∈ [0.5, 0.8] reverses the sign) show that the effect vanishes when friction is either predictable or narrow. A realistic object set, with friction correlated with family, material or appearance, is needed before the 0.42 means anything for a robot.

**A-W2. The "where it loses" analysis is framed too generously to the method (major; must fix).** We recomputed the sub-pools.
- **The primary-grid superiority in the sub-pool is a grid-floor artefact.** Inside the μ ∧ amp sub-pool, CSF-1's λ̂ is at **index 0 in D1 and D2** (also for μ only). That is why CSF-1 runs at slip 0.0328, far below α, with RE 0.566. On the refined grid, CSF-1's λ̂ is at index 10 in every stratum, and its slip is 0.1004. The paper's own rule says "the refined grid can mark a primary-grid result as unreliable but cannot upgrade it", and the grid-edge rule (re-run if λ̂ is at index 0) should apply. Both point the same way: the primary-grid +0.3754 / +0.3387 should be marked unreliable, not presented as equal evidence ("the picture depends on the grid"; Limitation 7, "but not on the primary grid").
- **"Slip is not matched" does not explain the μ-only reversal.** On the refined grid with the μ restriction alone, CSF-1 slips *less* than the learned model (0.0821 vs 0.0858) and still needs less excess force (RE 0.3281 vs 0.3844; D = −0.1717). The unmatched-slip caveat applies only to the μ ∧ amp cell.
- **There is an obvious candidate mechanism.** The paper says none is established. But the log-width of [0.5, 0.8] is ln 1.6 ≈ 0.47, comparable to the onset's error in log units (σ = 0.2 added noise plus detector SD 0.11 and bias 0.32). A friction-blind rule wins when the friction spread is not much larger than the probe's error. This can be tested directly with the existing replays (D against the μ-band width at fixed σ) and would turn a "loss" into a usable decision rule for practitioners.

**A-W3. The probe's force-time is under-counted, so the break-even time is understated (major; must fix).** `code/analysis_v3_a.py::a7_force` integrates preload, squeeze and ramp-down only. `certgrip/sim.py::_rd_touch_probe` then returns to F₀ over 0.02 s **and holds F₀ for 0.1 s**. That phase exists only because of the probe; a no-probe grasp would go straight from preload to the hold ramp. On the test split it adds about **3.62 N·s** (mean F_onset is 2.20 N). With it included, the probe-specific cost is about 17.96 N·s, not 14.35 N·s, and the break-even rises from 13.22 s to **≈ 16.6 s** for the learned model. The all-phase bound rises from 25.28 s to ≈ 28.6 s, and the plug-in's from 26.35 s to ≈ 33.0 s. The figure appears in the abstract chain (C2), Fig. 1a, Table 1, Section 6 and the Conclusion. Correct it, or define the phases explicitly and justify the exclusion.

**A-W4. The reactive competitors are straw men (major for C3).** In `code/react_run.py`, both REACT arms start the hold at c ∈ {0.5, 0.75} × the **uncalibrated** nominal force (CSF-1's or the plug-in's `log_g`, with no λ̂ offset), and any > 2 mm slip before tightening counts. Starting at roughly half the estimated minimal force, with a detector that needs two 10 ms frames plus a 20 ms ramp, almost guarantees slip (REACT-probe 0.99 / 0.95). The paper hedges ("no claim against reactive control in general"). But C3 still lists "reactive slip-tightening controllers" among the ablations that "locate the saving in the probe". As run, they locate nothing. Either add a reactive variant that starts at the CRC-calibrated force and tightens on detection (the natural hybrid), or remove the reactive rows from the attribution claim and label them a negative control.

**A-W5. The "minimal force" is only the hold force; peak and preload forces are fixed and large.** Every object, including 50 g ones, sees 32.7 N for 0.4 s and 49 N at the squeeze peak, and is driven to incipient slip (median 0.13 mm, max 1.92 mm). For the motivating applications (fragile objects, prostheses, actuator load), peak force usually matters at least as much as hold force. The paper states this in Limitation 5. The Introduction's motivation ("excess holding force loads the object…") should be narrowed to match. An adaptive-preload experiment would make the paper much stronger for RSS.

**A-W6. Sensor realism.** σ = 0.2 is assumed and sets the effect size (D from 0.68 to 0.14 over σ = 0 to 0.4). No grounding from published incipient-slip detector error is attempted, although some of the cited works (Khamis 2021; Boonstra 2024; Dong 2019) report friction-estimate errors that could at least place σ on the curve. A literature-based bracket would cost one paragraph.

**A-W7. Mass is assumed known.** μ̂ = m g/(2 F_onset) and every force rule use the true mass. The justification ("weigh during the lift") is not in the protocol, which runs the probe before the hold. There is a 10 % mass-noise secondary in `results/v1/sec08h_massnoise.json` (D 0.4603 [0.4106, 0.5050], label route), which supports robustness. It is mentioned only as a deviation. Report it in the main text.

**A-W8. Presentation.** The Results section mixes three amendment rounds, two grids, three calibration routes and label vs physical routes, with numbers to 4–5 significant figures. An RSS reader cannot easily tell what is established. Move most secondary rows to an appendix, and keep one table with H2a, the σ curve, plug-in vs learned and the sub-pool.

### Questions for the authors
1. Does the D-against-μ-band-width curve (from existing replays) show a crossover, and where is it relative to σ?
2. How do the CRC-calibrated hold force plus the reactive tightening hybrid perform?
3. Why is the 0.1 s re-hold at F₀ needed after onset? Could the probe return directly to the hold force (which would also shorten the break-even time)?

### Actionable revisions (Reviewer A)
1. Rewrite Section 5.4, Table 3 and Limitation 7: mark the primary-grid sub-pool superiority unreliable (CSF-1 at the grid floor); state that the μ-only reversal occurs at matched or lower CSF-1 slip; add the friction-spread vs probe-error analysis.
2. Recompute force-time with the post-onset return and 0.1 s hold, and update 13.22 / 25.28 / 26.35 s everywhere (abstract chain, C2, Fig. 1a, Tables 1, Sections 6 and 8).
3. Either add a calibrated-start reactive hybrid, or remove reactive controllers from the C3 attribution claim.
4. Add a correlated-friction pool (for example friction partly predictable from family) or a deployable category prior, so that "strongest non-tactile baseline" is not trivially friction-blind.
5. Move the mass-noise result into Section 5.1, and bracket σ with literature values.
6. Cut Results to the decision-bearing and mechanism-relevant rows; round to 2–3 significant figures in the main text.

**Score (Reviewer A): 4 / 10 (borderline reject).** Careful, honest and reproducible. But the main effect is largely set by a design choice (friction independent of all non-tactile inputs, with assumed σ), the force-time accounting has a real omission, the reactive comparison is uninformative, and there is no hardware. For RSS we would want either hardware onset-noise grounding or a non-trivial non-tactile baseline.

---

## Reviewer B: conformal prediction / statistical methodology

### Summary
The paper applies split CRC on a monotonised binary physical-slip loss, per disturbance stratum, over a log-force offset grid. The base force comes from a tactile friction estimate. It compares this, with pre-registered decisions, a Bonferroni split, object-cluster bootstrap CIs and many labelled secondaries, against a calibrated friction-blind rule. It also studies score-space online quantile tracking with binary feedback.

### Strengths
1. **Correct use of CRC.** Monotonising the loss on the grid (L̃ ≥ L, non-increasing) and evaluating physical L at λ̂ gives a valid bound E[L] ≤ E[L̃] ≤ α. The (n + 1) correction, the fallback to max Λ and the per-stratum exchangeability (each object appears once per stratum) are all correct. We checked the implementation independently.
2. **Statistical hygiene above the field norm.** There is pre-registration, a disjoint selection split for the comparator and grid centring, an object-cluster bootstrap that refits λ̂ in every draw, Bonferroni for the four core decisions, Holm for the first-round secondaries, explicit "unadjusted" labels, and a TOST that is run and reported as not met.
3. **Clear scope of the guarantee.** Marginal per stratum, in expectation over the calibration draw, not per object or per friction level. This is backed by re-splits (mean slip below α; single-stratum exceedance in 0.57 of splits), quintile tables and a Learn-then-Test high-probability variant. This is how conformal claims should be presented.
4. **Useful empirical finding on finite-sample cost.** At n = 500 per stratum, the empirically tuned margin lands on the same grid point as CRC on the primary grid. So the guarantee is nearly free on this grid. This is consistent with the (1 − α)/n ≈ 0.0018 correction being below the grid spacing.

### Weaknesses
**B-W1. The certificate is not obtainable on a robot as implemented (major).** Offline CRC needs, for each calibration grasp, the counterfactual slip outcome at **every** grid force (20 or 41 replays of the identical instance). On hardware you observe one outcome per grasp. The paper says so. But it then calls the deployable route (online tracking) the "natural route to hardware", and that route carries only a long-run-average guarantee with no per-stratum finite-sample statement. Its efficiency (H3) is inconclusive and its physical-replay oracle was not produced. So the paper's distinctive claim ("certified-slip") holds only where the simulator can replay. RSS reviewers will ask for a one-outcome-per-grasp calibration scheme. Possible routes: randomise λ per calibration grasp and use an inverse-propensity-weighted or monotone-interval CRC (one Bernoulli per grasp, monotonicity in F used to bound L̃); or a Learn-then-Test variant on randomised forces. At minimum, discuss this as the central open problem, not as a deployability footnote.

**B-W2. Data-dependent grid choices weaken the exactness of the guarantee (moderate).** The grid-edge rule re-runs an arm on a different grid *if λ̂ lands on index 0 or 19*. That decision is a function of the calibration data, so the reported λ̂ is the output of an adaptive procedure for which the CRC bound does not hold exactly. The refined grid was also adopted post hoc after the primary-grid floor was seen. The effect is probably small, but the text calls the edge-rule rows certified on the same footing. Either (i) state that edge-rule and refined-grid rows are not covered by the CRC theorem as run, or (ii) define the grid choice from the selection split only (for example, widen until the selection-split q̂ is interior), which keeps exchangeability.

**B-W3. The registered H2b contrast was biased against the plug-in, and the bias is only partly fixed (moderate).** On the primary grid the plug-in's λ̂ is at index 0 in D1/D2 (stratum slips 0.0586 / 0.0386 at σ = 0.2; 0.0071 / 0.0029 at σ = 0). The registered H2b point estimate 0.0569 is therefore inflated in favour of the learned model. The paper reports this and gives refined-grid rows. But the abstract's "no demonstrated gain" wording is, if anything, generous to the learner. The σ 0 / 0.1 refined-grid numbers (plug-in RE below the learned model's) suggest the plug-in may be *better* there. A refined-grid bootstrap contrast at σ 0 / 0.1 (Limitation 8 says it is missing) costs no new simulation and should be added.

**B-W4. The intervals in the online study have little meaning because the orderings share instances (moderate).** We checked the stream files. In S2, all 20 orderings use the **identical 1,500 post-shift instances**, permuted. In S1/S3, two orderings share about 1,080–1,094 of 1,500 post-shift instances (the union over orderings is 2,096). The "95 % intervals over orderings" therefore measure order effects on a nearly fixed sample, not sampling variability of slip under shift. They should not be read as CIs for the late-window slip rate. The text says "intervals over orderings only". It should also say that the instances are shared, and an object-cluster bootstrap should be added for the physical-feedback rows (the H3 rows already have one).

**B-W5. Conditional miscoverage is large and concentrated, and the obvious remedy is not tried (moderate).** The lowest friction quintile slips at 0.216 for the learned model, more than twice α. The plug-in's profile is much flatter (0.086 → 0.029), and CSF-1's is extreme (0.48 → 0). For grasping, the low-friction objects are the ones that matter. Mondrian or group-conditional CRC on μ̂ bins (deployable, since μ̂ is observed) would give per-bin guarantees at little cost and can be evaluated on the existing replays. The flat plug-in profile is also a further, unreported argument for the plug-in over the learner. Mention it in Section 5.2.

**B-W6. Labelling inconsistencies (minor).** In Table 2 the friction-prior σ_p 0.2 row is labelled "edge rule". But −0.0299 is the learned arm **on the refined grid** against the prior on the refined grid (`results/v2/b_analysis_edge.json`: learned RE 0.4442), which is what the shrunk-plug-in rows call "same grid". Under the shrunk rows' "edge rule" convention (learned on the primary grid), the value would be 1 − 0.4567/0.4312 = **−0.059**. Use one convention throughout. Also state that the Clopper–Pearson upper limit 0.02115 is one-sided at 98.75 % (the Bonferroni-split level). A reader computing the usual 95 % limit gets 0.0180 < 0.02 and would conclude that the gate passed.

**B-W7. Multiplicity across rounds (minor).** Three amendment rounds were registered after earlier read-outs. Most second- and third-round rows are unadjusted, and three inferiority rows have upper bounds within 0.02 of zero. The paper flags all of this, which is good. The abstract nonetheless quotes two of them (the σ 0.4 shrunk result and the −0.3152 refined sub-pool) next to the confirmatory D, without the "unadjusted, post hoc" label. Add it.

**B-W8. Effect-size metric (minor).** D is a ratio of mean signed RE. Slipped instances contribute negative excess, so an arm that slips more gets a smaller RE. In H2a the probe arm slips *less* (0.083 vs 0.102), so this is conservative for the paper's claim, which is good. But for contrasts where the method slips more (μ ∧ amp refined; σ 0.4 shrunk), D is not comparable. Matched-slip D, or RE restricted to non-slipped instances, should accompany those rows.

### Questions for the authors
1. Can a one-outcome-per-grasp CRC be evaluated on the existing replays by subsampling one random grid force per calibration instance? This would directly show what the certificate costs on hardware.
2. What do group-conditional CRC on μ̂ tertiles and its lowest-quintile slip look like?
3. Does the online tracker's late-window slip CI change when instances are resampled by object rather than by ordering?

### Actionable revisions (Reviewer B)
1. Add a single-outcome calibration variant (or a clear theorem-level discussion), and temper "certified" in the title and abstract to "simulation-certified".
2. State that edge-rule and refined-grid rows are outside the exact CRC theorem, or move the grid choice to the selection split.
3. Add refined-grid bootstrap contrasts for learned vs plug-in at σ 0 / 0.1, and a group-conditional CRC (μ̂ bins) row with quintile slip.
4. Disclose instance sharing across orderings, and add an object-cluster bootstrap to the physical-feedback rows.
5. Fix the σ_p 0.2 "edge rule" label (−0.0299 vs −0.059), and state the CP level (98.75 %, one-sided).
6. Label the abstract's secondary numbers as unadjusted, post hoc secondaries.

**Score (Reviewer B): 5 / 10 (borderline).** Statistically sound and unusually transparent. Every number we checked reproduces, and the attribution result (the plug-in is enough) is valuable. It falls short because the guarantee that gives the paper its name needs counterfactual simulator replays, the deployable online route carries no per-stratum finite-sample statement, and the effect size is set by assumed σ and a constructed friction distribution.

---

## Consolidated must-fix list (both reviewers)

1. **Sub-pool framing (A-W2).** The primary-grid sub-pool "superiority" comes from CSF-1 sitting at the grid floor (λ̂ index 0 in D1/D2, slip 0.033). The μ-only refined reversal (D −0.1717) occurs at matched or lower CSF-1 slip (0.0821 vs 0.0858). Revise Section 5.4, Table 3, Limitation 7, the abstract and the conclusion: the method loses when the friction spread is narrow relative to the probe's error.
2. **Force-time accounting (A-W3).** Include the post-onset 0.02 s return and the 0.1 s re-hold at F₀ (≈ 3.62 N·s). Break-even becomes ≈ 16.6 s (not 13.22), the all-phase bound ≈ 28.6 s and the plug-in ≈ 33.0 s. Update C2, Fig. 1a, Table 1, Section 6 and Section 8.
3. **Scope of "certified" and of the competitors (B-W1, A-W4, A-W1).** The offline bound needs counterfactual replays. The reactive controllers start at 0.5–0.75 × the uncalibrated nominal force, so they are a negative control, not an attribution ablation. Friction independent of every non-tactile input makes the friction-blind baseline weak by construction. Temper the claims, or add a calibrated-start reactive hybrid, a correlated-friction pool and a one-outcome-per-grasp calibration variant.

Also fix: instance sharing across online orderings (B-W4); data-dependent grid choice (B-W2); the σ_p "edge rule" label and the CP level (B-W6); unadjusted labels in the abstract (B-W7); and length/readability (A-W8).

**CRITICAL_FABRICATION: no.** Trial counts, seeds, draws, orderings and statistical procedures all match the code and raw results. Every recomputed headline and table value reproduces.
