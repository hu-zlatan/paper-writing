# Stage 18 peer review, draft v3, run 1 (independent reviewer, fresh context)

Role: a balanced conference reviewer who checks closely that the methods match the evidence.
Inputs read: `prompts/stage18_v3_system.txt`, `prompts/stage18_v3_user.txt`. I read the whole paper draft and the Figure 1 prompt. I went through the evidence block (results_v1/v2/v3 JSON, the run-log excerpt, the stats grep and the pointer to the pre-registration) by block, and I searched it for every number the paper uses. I also opened `docs/08b_preregistration.md`, `code/certgrip/sim.py`, `code/analysis_v3_a.py`, `code/analysis_v3_d.py` and `code/tools_stage19_rows.py`, along with the raw replay, label and monotonicity files under `results/v1/`. No repository file was modified apart from this review.

---

## 0. Independent recomputation from raw data (what I checked myself)

I wrote my own scripts in a scratchpad, outside the repo. They load the raw direct-replay files (`results/v1/crc/*.jsonl`, 4,800 records = 2,000 calibration + 2,800 test, 1,200 objects) and the bisection labels (`results/v1/labels/id_F[1-4].jsonl`). They then rebuild the monotonised loss, the per-stratum CRC λ̂ with the (n+1) correction, the test slip, signed RE against F\*_mid, and D. The results:

| Quantity (paper) | Paper | Recomputed | Match |
|---|---|---|---|
| Records / cal / test / objects | 4,800 / 2,000 / 2,800 | 4,800 / 2,000 / 2,800 / 1,200 objects | yes |
| λ̂ index, learned arm D1–D4 (primary) | — | 10 / 10 / 11 / 10 | = 19_report_rows |
| λ̂ index, CSF-1 D1–D4 | — | 1 / 1 / 15 / 14 | = 19_report_rows |
| λ̂ index, plug-in σ 0.2 D1–D4 | "index 0 in D1/D2" | 0 / 0 / 14 / 12 | yes |
| RE learned / CSF-1 | 0.4567 / 0.7832 | 0.45673 / 0.78318 | yes |
| H2a D | 0.4168 | 0.416821 | yes |
| Test slip learned / CSF-1 | 0.0829 / 0.1021 | 0.082857 / 0.102143 | yes |
| Mean (median) hold force learned / onset-only / plug-in / CSF-1 | 6.521 (4.473) / 6.519 (4.423) / 7.062 (4.556) / 7.606 (5.476) N | 6.5215 (4.4728) / 6.5190 (4.4228) / 7.0620 (4.5558) / 7.6065 (5.4762) | yes |
| Mean excess over F\*_mid learned / CSF-1 | 1.623 / 2.708 N | 1.6233 / 2.7084 | yes |
| F\*_mid 10/50/90 % quantiles, max, share > 32.7 N | 0.9549 / 3.184 / 11.35, 31.87, 0.0 | 0.95495 / 3.1837 / 11.3547, 31.873, 0.0 | yes |
| σ curve D at σ 0 / 0.1 / 0.2 / 0.4 | 0.6789 / 0.5825 / 0.4168 / 0.1401 | 0.67893 / 0.58252 / 0.41682 / 0.14011 | yes |
| Seeds 1–4 D | 0.4343 / 0.4197 / 0.3932 / 0.4494 | 0.43430 / 0.41966 / 0.39322 / 0.44935 | yes |
| Seed-4 overall slip | 0.1018 | 0.10179 | yes |
| Plug-in vs CSF-1 (primary) / onset-only vs CSF-1 | 0.3816 / 0.4464 | 0.38162 / 0.44639 | yes |
| H2b learned vs plug-in | 0.0569 | 0.056918 | yes |
| Learned vs unshrunk plug-in σ 0 / 0.1 / 0.4 | 0.246 / 0.1072 / 0.3182 | 1−0.2515/0.3335 = 0.246; 0.1072; 0.3182 | yes |
| Unshrunk σ 0.4 plug-in RE; learned σ 0.4 slip / RE | 0.9877; 0.08214 / 0.6735 | 0.98768; 0.082143 / 0.67345 | yes |
| Comparator D1/D2 slips at σ 0 / 0.1 | 0.007143 / 0.002857, 0.01571 / 0.007143 | 0.0071 / 0.0029, 0.0157 / 0.0071 | yes |
| Per-stratum slip, learned / CSF-1 / plug-in (primary) | Table 3 | identical to 4 d.p. | yes |
| Friction-quintile slip, learned / plug-in / CSF-1 | Table 3 | 0.21607…0.00357 / 0.08571…0.02857 / 0.48036…0.0 | yes |
| Figure 1b frontier, all 36 (slip, RE) points, k = −4…+4 (learned, onset-only, CSF-1) | Fig. 1 prompt | identical to 4 d.p. | yes |
| D_match at slip 0.10 (linear interpolation on frontier) | 0.4563 | 0.456312 | yes |
| H2a CI\*\* [0.3484, 0.4778] | 97.5 %, 2,000 object-cluster draws | my own bootstrap (cal and test objects resampled within family, λ̂ refit in each draw, different RNG): [0.3529, 0.4758] | yes, within MC error |
| Refined grid: D learned / plug-in / onset-only vs CSF-1; learned vs plug-in | 0.4289 / 0.4149 / 0.4412; 0.02397 | 0.42892 / 0.41490 / 0.44119; 0.023965 | yes |
| Refined per-stratum slip learned / CSF-1 | 0.1043/0.1014/0.0729/0.0814; 0.09/0.0929/0.11/0.1057 | identical | yes |
| Refined plug-in slip / RE | 0.075 / 0.4551 | 0.075 / 0.45506 | yes |
| Refined arm RE, plug-in vs learned at σ 0 / 0.1 | 0.208 vs 0.2397; 0.2915 vs 0.3212 | 0.208 vs 0.2397; 0.2915 vs 0.3212 | yes |
| Monotonicity gate: 8 / 800 non-monotone, 7 under D2 | yes | raw `mono/id_F[1-4]`: 8 / 800, 7 in D2 (1 in F2 D1) | yes |
| Friction / mass ranges | log-U [0.3, 1.0]; [0.05, 1.0] kg | observed 0.3001–0.9998; 0.0500–0.9958 kg | yes |
| Disturbance amplitudes D1 / D2 / D3 / D4 | U[1,10] m/s², 5–20 mm, 0.5–2 mg, 0.2–1.0 m | observed 1.007–10, 0.005–0.02 m, 0.502–1.999, 0.2–1.0 | yes |

Numbers I checked against the JSON by key, not recomputed: H3 R_E 0.8778 / 1.1739 / 0.9629 and their CIs, matched-rate differences 0.032 / −0.035, oracle S2 slip 0.1346, the physical-feedback stream windows (0.1389, 0.1001–0.1018, and so on), H2-R −0.2614 [−0.5320, −0.0325] with n 352 / 548, the CRC sub-pools (−0.3152, −0.1717, +0.4929; primary +0.3754 / +0.3387 / +0.5004), the reactive-controller rows (0.765 / 0.4632 / 0.9921 / 0.9514), the re-split summaries (200 re-splits, seed 3031), Holm (52 rows, 40 rejected), the selection-split baseline choice (0.7686 / 0.8294 / 0.8335), shrinkage OLS coefficients, the a7 integrated-force file (27.4258 / 14.3458 N·s; break-even 13.2218 s), compute hours (14.4998), detector diagnostics (r 0.9480, bias 0.3186, SD 0.1103; onset displacement 0.1263 / 0.2543 / 1.9238 mm), static-touch check (0.1597 N, 0 preload slips) and H1-V Δ.

I also extracted every decimal number from the paper text and the Figure 1 prompt and looked for each one in the v1/v2/v3 result values. Every number was found, apart from section numbers, the constant 32.7, "97.5 %" and the derived 0.0142 (= 0.4551 − 0.4409, which is correct). This check is weak for 4-decimal numbers in [0, 1], so the recomputations above carry the real weight.

**Bottom line of the audit:** I found **no fabricated number, trial count or statistical test**. Two factual problems turned up (sections 2.1 and 2.2 below): an omission in the force-time accounting that biases the break-even figure, and one statistic attributed to the wrong pool.

---

## 1. Checklist items from the prompt

### 1.1 Topic adherence
The paper stays on topic: a ramp-down friction-onset probe, per-stratum CRC on the binary physical slip loss, comparison against the selected strongest non-tactile conformal baseline (CSF-1), attribution ablations (plug-in, shrunk plug-in, onset-only, feature chain, friction prior, margins, reactive controllers) and an online binary-feedback study under three shifts. No section drifts. No environment issue is presented as a contribution: Appendix B mentions the sandbox and unlogged CPU-hours only as a reporting caveat, and the 8/800 monotonicity failure is presented as the reason for switching to the physical loss, not as a contribution. One mild drift: the "Practical implications" paragraph and Appendix C ("master draft only") carry descriptive material that a 9-page version does not need.

### 1.2 Methodology–evidence consistency
- **Trials / seeds / orderings / draws.** The paper claims n = 500 per stratum for calibration and 2,800 test instances, five predictor seeds (0 primary, 1–4 refits), 2,000 object-cluster bootstrap draws, 200 re-splits, 20 stream orderings and T = 2,000 steps. All of these match the evidence (`crc_analysis.json` draws 2000; `h3_analysis.json` "20 orderings"; `A1_resplits` R = 200; arm keys `full_rd@0.2#0…#4`; the raw files hold 2,000 + 2,800 records).
- **Statistical tests.** Clopper–Pearson (`analysis_h1m.py`, `analysis_v2_a.py`), the object-cluster bootstrap (`analysis_v3_a.py`, `h3_streams.py`) and Holm (`analysis_v3_c.py`) are all present in code. The registered TOST for H2b is reported only through the CI: the stored H2b record has a `decision` field but no separate TOST statistic. Because CI\*\* is 97.5 %, the paper's reading (upper limit 0.1454 > 0.10, so not equivalent) is equivalent to a TOST at 0.0125 per side. Acceptable, but the paper should say explicitly that the TOST was read off the 97.5 % CI.
- **Hyperparameters.** The detector constants in Table A1 match the run headers (`rd_detector`: T 0.25, floor 0.005, w 6, k 8, consec 2, slope_frac 0.5, r_arm 0.1, t_up 0.02; taxel noise 0.05 / 0.002 / 0.10). η = 0.03412 matches. The shrinkage coefficients match.
- **Baselines.** The selection-split choice of CSF-1 matches `comp_selection.json`. The pre-registration gives the selection objects as "200–249" while the code uses 150–199. The paper discloses this as deviation (3).
- **Discrepancies found:** see 2.1 (force-time accounting) and 2.2 (monotonicity statistic). Two smaller points: the Fig. 1a prompt describes the squeeze as a "triangular bump", but `sim.py` uses a half-sine (`F0·(1 + 0.5 sin πs)`); and the robustness result for the "mass is given" assumption exists but is not reported (2.5).

### 1.3 Trial count
**No CRITICAL fabrication.** Every count the paper states matches the evidence and the raw files. The paper never claims "N independent trials" beyond what was run. It is also careful to call route re-analyses of the seed-0 replays "route robustness, not replication", and re-splits "split-to-split variability, not new objects".

### 1.4 Length
Word counts include tables:

| Section | Words | Threshold |
|---|---|---|
| Abstract | 238 | ≥ 150, OK |
| Introduction | 828 | ≥ 700, OK |
| Related work | 615 | ≥ 500, OK |
| Method (§3) | 1,926 | ≥ 800, OK |
| Experimental setup (§4) | 760 | ≥ 600, OK |
| Results (§5) | 3,656 | ≥ 500, OK |
| Discussion / Limitations / Conclusion | 532 / 381 / 223 | — |
| Appendix | 616 | — |
| **Total** | **≈ 9,800** | ≥ 4,000, OK |

Nothing is under length. The real risk is the opposite: with four dense tables, two figures and about 8,600 words of main text, the paper will not fit 9 NeurIPS/ICML pages. Section 5 reads as a list of secondary rows. In addition, Figure 1 is still a generation prompt and Figure 2 exists only as a caption, so no figure is rendered.

---

## 2. Issues found in the evidence audit (shared by both reviewers)

### 2.1 Force-time accounting leaves out probe-specific force-time (substantive, fix required)
`analysis_v3_a.py::a7_force` counts the shared phases as preload (F₀ × 0.4 s), squeeze (mean recorded normal force × 0.3 s) and ramp-down (analytic log-linear integral up to onset). In `sim.py::_rd_touch_probe`, the probe then **returns to F₀ over t_up = 0.02 s and holds F₀ for 0.1 s** (`self._step(int(0.1 / DT))`) before the ramp to the hold force. The paper itself describes these segments (Sec. 3.2, Fig. 1a), but they are missing from the 14.3458 N·s "probe-specific" and the 27.4258 N·s "shared" figures. From the 2,800 test label records, the omitted force-time averages **3.62 N·s per grasp**: 0.1 × 32.7 = 3.27 N·s plus about 0.35 N·s for the return. Corrected at the same 1.085 N hold saving:
- probe-phase break-even: (14.3458 + 3.619) / 1.085 ≈ **16.6 s**, not 13.22 s;
- all-phase break-even: (27.4258 + 3.619) / 1.085 ≈ **28.6 s**, not 25.28 s;
- the integrated force-time at T = 1 / 5 / 30 s moves up by the same constant for every arm.

The 13.22 s figure appears in the Fig. 1 prompt and caption, C2, Sec. 5.1, Table 1, the Discussion and the Conclusion. Either include the return-and-hold segment, or state explicitly that it is excluded and why: it is protocol-specific to the probe, so excluding it is hard to justify. The qualitative conclusion ("short holds do not pay back the probe") gets stronger, not weaker.

### 2.2 Monotonicity statistic attributed to the wrong pool (minor, factual)
Sec. 5.4 says: "The label monotonicity gate failed (8 / 800; the largest slip force above F\*_hi exceeds it by a relative 0.00904)". `h1m_analysis.json` computes `max_rel_above_F_hi` = 0.00904 over all 10 recorded violations. In `19_report_rows.json → h1m_violations_split`, the **800-instance gate set has a maximum of 0.00225**; the 0.00904 comes from the shift pools (S2/S3, outside the gate). Report 0.00225 for the gate. You can add that two more non-monotone instances appeared in the 300 shift-pool checks (maximum 0.00904).

### 2.3 Headline method vs confirmatory arm (framing)
The paper says the method is "probe + simple force rule + CRC" with the learner optional (abstract, §6, §8; C1 names the plug-in). Yet the only confirmatory decision (H2a) is about the **learned** arm `full_rd@0.2`. The plug-in's own comparison with CSF-1 is secondary and post hoc. On the primary grid it sits on the grid floor in D1/D2 (λ̂ index 0, D 0.3816), and the claim rests on the post hoc refined grid (0.4149) and on the third-round shrunk plug-in, whose primary λ̂ is also at index 0 in D1/D2. This is honestly labelled, but the abstract's "the saving comes from the probe" is a secondary-evidence claim. Either lead with the learned-arm result as the confirmed one and present plug-in sufficiency as a secondary finding, or say plainly in the abstract that the plug-in claim is not pre-registered.

### 2.4 The CSF-1 comparator is also close to its grid floor
CSF-1's primary λ̂ is index **1** in D1/D2 (recomputed). Its frontier points at k = −4…−2 are therefore clipped in those strata, which explains the flat lower end of the orange curve in Fig. 1b. Mention this in the Fig. 1 caption and in §5.1. The refined-grid D (0.4289), where CSF-1 sits at indices 20–21 of 41, shows that the headline is not an artefact of this.

### 2.5 An existing robustness result is not reported
Mass is given to every method (§3.3), which is a central assumption. `sec08h_massnoise.json` contains a pre-registered 10 % mass-noise check: D 0.4603 [0.4106, 0.5050] against 0.4292 without noise (label route), change 0.031 [−0.008, 0.071]. The paper mentions only that "the noisy-mass draw was fixed in a later addendum". Report the result: it supports the paper. Likewise `sec08h_dfid.json` shows that touch-only features identify object family at 72.6 % (chance 25 %). This is consistent with the preload carrying no *friction* information, because friction is drawn independently of family, but it should be stated to pre-empt the obvious objection.

### 2.6 Oracle-side ingredients that are not labelled as such
The shrunk plug-in's OLS uses the **true μ** of the selection objects, and the learned model trains on bisection F\* labels. Both are simulator-only. The friction prior is flagged as oracle-side; the shrinkage fit should be flagged the same way, or a deployable route given (for example, a lab calibration set of known materials).

---

## Reviewer A (conformal prediction / statistical ML perspective)

**Summary.** The paper calibrates the hold force of a parallel-jaw grasp with split CRC on a monotonised binary physical-slip loss, per disturbance stratum. The base force comes from a Coulomb reading of a ramp-down incipient-slip onset. Against a friction-blind CRC-calibrated Coulomb rule selected beforehand, relative excess hold force drops by D = 0.4168 at α = 0.10 in MuJoCo. Ablations attribute the saving to the onset reading, not to the learned quantile model. An online quantile tracker with binary feedback returns to α after three shifts.

**Strengths.**
1. Very good statistical hygiene: pre-registration, Bonferroni-split core decisions, SESOI, TOST, object-cluster bootstrap with λ̂ refit inside every draw, a stated multiplicity scope (Holm for round 1, unadjusted and labelled later rounds), and a numbered list of deviations. I recomputed the main D, its CI (to MC error), the σ curve, the seeds, per-stratum and per-quintile slips and all 36 frontier points from raw replays, and everything matched.
2. The guarantee is stated carefully throughout (marginal, per stratum, in expectation, in simulation, needs replays), and the empirical re-split and per-stratum and quintile tables show exactly what a marginal guarantee does and does not deliver.
3. The comparator is the right one: a non-tactile rule calibrated to the same α, not an uncalibrated controller. Negative and inconvenient results are reported: H1 failed, H2b was not confirmed, H3 was inconclusive, the mid-friction sub-pool reverses, and the shrunk plug-in beats the learner at σ 0.4.
4. The tuned-margin result (CRC and a per-stratum empirical margin land on the same point at n = 500) is honest. It clarifies that CRC adds a finite-sample guarantee, not force efficiency.

**Weaknesses.**
1. **Limited methodological novelty for an ML venue.** CRC, LTT and quantile tracking are used as published. The monotonisation `max_{λ'≥λ} L(λ')` is the standard trick. Reading friction from incipient slip is established. The contribution is a careful empirical application and an attribution study, which is closer to a strong robotics-workshop or RA-L-style paper than to a NeurIPS/ICML methods paper.
2. **The effect size is set by the simulation design.** D depends on two assumed quantities: friction drawn log-uniform on [0.3, 1.0], independently of every non-tactile input, and onset noise σ = 0.2. The paper shows that D falls to 0.1401 at σ = 0.4 and reverses in the μ ∈ [0.5, 0.8] band. Without a measured σ, the headline is one point on a curve whose location is unknown. The paper concedes this, but that does not make the number informative.
3. **The guarantee is not deployable as implemented.** Offline CRC needs a replay at every grid force for every calibration grasp. The deployable online route has long-run (not finite-sample) validity, transient overshoot to 0.139 under S1, no physical-replay oracle, and an inconclusive pre-registered efficiency decision.
4. **Framing mismatch (§2.3).** The confirmed arm is the learned model, but the advertised method is the plug-in. The plug-in evidence is post hoc and depends on the grid.
5. **The force-time break-even is understated by about 25 % (§2.1).**
6. **Unmatched slip in key secondary contrasts.** H2a compares learned slip 0.0829 against CSF-1 slip 0.1021, which is conservative for the probe arm. The σ = 0.4 learned-vs-shrunk inferiority (0.0821 vs 0.0929) and the mid-friction reversal are also at unmatched slip. The signed RE rewards an arm for slipping more, so these contrasts mix efficiency with risk. A matched-slip version of the σ = 0.4 shrunk row should be computed, which is cheap because all grids are replayed.
7. Presentation: roughly 9,800 words, four large tables and unrendered figures. Section 5 would gain from moving most secondary rows to the appendix.

**Actionable revisions.**
- Fix the force-time accounting to include the 0.02 s return and the 0.1 s F₀ hold. Update 13.22 → ≈16.6 s and 25.28 → ≈28.6 s, plus the integrated values (Fig. 1, C2, §5.1, Table 1, §6, §8).
- Correct the monotonicity statistic to 0.00225 for the 800-instance gate.
- Make the abstract's attribution claim explicitly secondary, or restructure so the confirmed result (learned arm vs CSF-1) and the secondary result (plug-in sufficiency) are clearly separated.
- Add matched-slip versions of the σ 0.4 learned-vs-shrunk row and the mid-friction sub-pool row.
- Report the existing mass-noise robustness result (D 0.4603) and the D-FID result.
- State that the H2b TOST was evaluated through the 97.5 % CI\*\*.
- Cut §5 to the decision-bearing rows plus the sufficiency and attribution story, and move the remaining rows to the appendix. Render the figures.
- Ground σ: even an estimate of onset-force scatter from published incipient-slip detector studies would place the headline on the curve.

**Score: 5 / 10 (borderline).** Rigorous, honest and fully reproducible from the raw data. The ML novelty is small, the effect size depends on assumed simulation parameters, and the certificate is simulation-only.

---

## Reviewer B (robotic grasping / tactile manipulation perspective)

**Summary.** A simulation study of minimal-hold-force grasping. A fixed 32.7 N preload and a squeeze are followed by a ramp-down probe that stops at a touch-detected incipient slip, giving μ̂. A Coulomb plug-in or a learned quantile model sets the hold force, which is inflated per disturbance type by conformal risk control so that the physical slip rate is at most α in expectation.

**Strengths.**
1. A clean experimental design for *isolating* the value of the friction cue. The friction-uninformative preload and the iid friction draw make the onset the only friction channel, and the feature chain confirms that static touch and the squeeze add nothing.
2. The paper reports absolute newtons and force-time, not just relative excess, and admits that the fixed 32.7 N preload dominates the force budget, so the "minimal force" claim applies to the hold force only.
3. Credible tactile competitors are attempted: a uniform margin, a tuned per-stratum margin and two reactive slip-tightening controllers. Their failures are reported without overclaiming ("we make no claim against reactive control in general").
4. Honest practical caveats: the probe slips every object by a median 0.126 mm, and the protocol excludes fragile or slip-intolerant objects.

**Weaknesses.**
1. **Simulation only, with an idealised touch model.** The recorded preload normal reading equals the commanded 32.7 N to within 0.16 N. MuJoCo rigid contact with an elliptic cone and condim 6 is far from real pad mechanics, which have viscoelasticity, a contact area that grows with force, and rate-dependent friction. The detector's noise-free friction reading already has a large bias (0.3186 in log units) and varies across families (SD 0.045–0.196). Real sensor behaviour is replaced by the assumed σ.
2. **The protocol dominates the energy budget.** The method saves about 1.085 N of hold force but spends a 1.5 F₀ squeeze and a probe. With the omitted return-and-hold segment included (§2.1), the break-even hold time is about 16.6 s against the probe phases and about 28.6 s against all shared phases. For many pick-and-place holds this means the protocol costs more than it saves. The paper should state this more prominently and, ideally, run the adaptive or low-preload variant it proposes as future work.
3. **The reactive baselines are not competitive.** REACT-probe slips on 95–99 % of grasps, which points to a detector or design failure, not a fair representative of reactive grip control. Without detection-timing data, and without a well-tuned reactive controller (for example a slip-margin controller in the style of Khamis et al. or Dong et al.), the claim that calibration is needed over classical tactile control is unsupported. The paper wisely does not make that claim, but the comparison then adds little.
4. **The friction distribution decides the outcome.** In a realistic setting, a vision or material category prior would correlate with μ. The paper's own oracle prior at σ_p = 0.2 already erases the advantage (D −0.0299). The mid-friction band reverses the sign on the label route and the refined CRC grid. The practical value therefore hinges on an untested correlation structure.
5. **The calibration needs simulator replays at every grid force,** so the offline certificate cannot be produced on hardware. The online tracker is the only deployable route, and it carries only long-run guarantees.
6. Minor: the Fig. 1a prompt calls the squeeze a "triangular bump", but the code uses a half-sine. The slip criterion (2 mm / 3°) is reasonable but should be justified against task needs. D2 hosts 7 of the 8 non-monotone instances, which deserves a sentence on the mechanism (stick-slip under shake?).

**Actionable revisions.**
- Correct the force-time accounting (§2.1). Promote the break-even analysis to the main contribution statement, and add a run with an adaptive or lower preload (for example a preload set from the weighed mass and μ_min), which the protocol allows.
- Replace or supplement REACT with a tuned reactive controller (grid-search r_safe and the step size on the calibration split, as was done for the tuned margin) and report detection latency.
- Add a pool with correlated friction (for example family-dependent μ ranges) and a deployable category prior. This is the most important missing competitor.
- Ground σ with a measured onset-force scatter on any real sensor, or at least from published detector repeatability.
- Report the mass-noise result and the D-FID result (§2.5), and flag the shrinkage OLS as needing ground-truth μ (§2.6).
- Render Figures 1–2, delete the "master draft only" appendix label, and cut §5 to fit 9 pages.

**Score: 4 / 10 (borderline, leaning reject for NeurIPS/ICML).** Careful and transparent, but simulation-only with an assumed noise level. The protocol costs more force-time than it saves on short holds, and the competitive baselines a robotics audience expects (tuned reactive control, correlated priors) are missing or weak.

---

## Overall assessment

| | Reviewer A | Reviewer B |
|---|---|---|
| Score | 5 | 4 |
| Recommendation | Borderline | Borderline / weak reject |

- **CRITICAL_FABRICATION: no.** Trial, seed, ordering, draw and split counts all match the evidence. The main numbers, CI, frontier, σ curve, seeds, refined-grid rows, strata and quintiles were recomputed from raw replays and matched.
- **Must-fix before submission:**
  1. Include the probe's 0.02 s return and 0.1 s F₀ hold in the force-time accounting. Break-even becomes ≈ 16.6 s (probe phases) and ≈ 28.6 s (all phases); update Fig. 1, C2, §5.1, Table 1, §6 and §8.
  2. Align the framing with the evidence. The confirmed result (H2a) is for the learned arm; "the saving comes from the probe / plug-in suffices" rests on secondary, post hoc, grid-dependent rows. Say so in the abstract and contributions, add matched-slip versions of the σ 0.4 shrunk row and the sub-pool row, and keep the conditionality on the assumed σ and the iid friction range in the headline.
  3. Compress to 9 pages and render the figures (≈ 9,800 words now, the figures are still prompts). Also correct the monotonicity statistic (0.00225 for the gate, not 0.00904), and report the existing mass-noise (D 0.4603) and D-FID results.
