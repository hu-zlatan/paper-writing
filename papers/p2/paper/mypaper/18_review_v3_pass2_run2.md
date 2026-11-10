# Stage 18 (v3, pass 2, run 2): Independent Review

**Paper:** *Probe, Then Calibrate: Conformal Slip-Risk Control of Grip Force from a Tactile Friction-Onset Probe (a Simulation Study)*
**Reviewer role:** a balanced RSS program-committee pair (A: tactile manipulation / grasp control; B: conformal inference / statistical methodology) who are strict about whether the methodology matches the evidence.
**Inputs:** `prompts/stage18_v3_pass2_system.txt`, `prompts/stage18_v3_pass2_user.txt` (I read the paper draft in full, then the evidence block's structure and its sections (b)–(d)), plus raw replay files under `results/`, code under `code/` and pre-registration documents under `docs/`.
**Scratch scripts:** `/tmp/claude-0/rev4/` (`crc_recompute.py`, `more.py`, `boot.py`, `sub.py`, `b3.py`). I modified no repository file.

---

## 0. Independent verification (what I recomputed from raw files)

I wrote my own scripts. They read the raw per-instance replay records (`results/v1/crc/*.jsonl`, `results/v1/crc_v2/*.jsonl`, `results/v3/crc10/*.jsonl`, `results/v{2,3}/b3/*.jsonl`) and the bisection labels (`results/v1/labels/*.jsonl`). From these I re-implemented monotonised per-stratum CRC (the (n+1) rule), Learn-then-Test, RE, D, matched-slip interpolation, sub-pools and the online windows. I did not reuse the project's analysis code.

| Quantity (paper) | Paper | My recomputation | Match |
|---|---|---|---|
| Data sizes: cal / test | 2,000 / 2,800 (500 / 700 per stratum) | 2,000 / 2,800; 0 unavoidable test instances | yes |
| λ̂ indices, CSF-1 (primary grid) | index 1 in D1/D2 | {D1:1, D2:1, D3:15, D4:14} | yes |
| λ̂ indices, plug-in σ 0 / 0.1 / 0.2 | grid floor (0) in D1/D2 | 0 in D1/D2 for all three | yes |
| RE learned / CSF-1 | 0.4567 / 0.7832 | 0.45673 / 0.78318 | yes |
| **H2a D** | **0.4168** | **0.416821** | yes |
| H2a CI\*\* | [0.3484, 0.4778] | [0.3474, 0.4739] (my object-cluster bootstrap, 600 draws, different seed) | yes, within MC error |
| Test slip learned / CSF-1 | 0.0829 / 0.1021 | 0.08286 / 0.10214 | yes |
| Mean (median) hold force: learned, onset-only, plug-in, CSF-1 | 6.521 (4.473), 6.519 (4.423), 7.062 (4.556), 7.606 (5.476) | 6.5215 (4.4728), 6.5190 (4.4228), 7.0620 (4.5558), 7.6065 (5.4762) | yes |
| Mean excess learned / CSF-1 | 1.623 / 2.708 N | 1.6233 / 2.7084 | yes |
| D at σ 0 / 0.1 / 0.2 / 0.4 | 0.6789 / 0.5825 / 0.4168 / 0.1401 | 0.67893 / 0.58252 / 0.41682 / 0.14011 | yes |
| H2b learned vs plug-in | 0.0569 | 0.056918 | yes |
| Onset-only vs CSF-1; full vs onset-only | 0.4464; −0.0534 | 0.44639; −0.05341 | yes |
| Plug-in vs CSF-1 (primary) | 0.3816 | 0.38162 | yes |
| Seeds 1–4 | 0.4343 / 0.4197 / 0.3932 / 0.4494 | 0.43430 / 0.41966 / 0.39322 / 0.44935 | yes |
| Seed-4 overall slip | 0.1018 | 0.10179 | yes |
| Refined grid: learned vs CSF-1; learned vs plug-in; plug-in vs CSF-1; onset-only vs CSF-1 | 0.4289; 0.02397; 0.4149; 0.4412 | 0.42892; 0.023965; 0.41490; 0.44119 | yes |
| Refined plug-in slip / RE | 0.075 / 0.4551 | 0.0750 / 0.45506 | yes |
| LTT (δ 0.1): D; learned slip / RE; CSF-1 slip / RE | 0.4043; 0.0696 / 0.4895; 0.0907 / 0.8216 | 0.40428; 0.06964 / 0.48945; 0.09071 / 0.82162 | yes |
| Matched slip 0.10 D (primary) | 0.4563 | 0.45631 | yes |
| Fig. 1(b) frontier, all 9 points of learned, onset-only and CSF-1 | listed | every point reproduced to 4 d.p. | yes |
| Per-stratum slip D1–D4: learned, CSF-1, plug-in | listed in Table 3 | identical | yes |
| Friction-quintile slip: learned, CSF-1 | 0.2161 … 0.003571; 0.4804 … 0.0 | 0.21607 … 0.00357; 0.48036 … 0.0 | yes |
| F\*_mid quantiles 10 / 50 / 90 %, max, share > 32.7 N | 0.9549 / 3.184 / 11.35, 31.87, 0.0 | 0.95495 / 3.18370 / 11.3547, 31.873, 0.0 | yes |
| Shrunk plug-in vs CSF-1 at σ 0.2 / 0.4; learned vs shrunk at σ 0.2 / 0.4 | 0.435 / 0.2454; −0.03216 / −0.1395 | 0.4350 / 0.2454; −0.0321 / −0.1395 (shrunk slip at σ 0.4: 0.09286) | yes |
| Sub-pools, primary grid: μ∧amp / μ only / amp only (sizes 352 / 548 for μ∧amp) | 0.3754 / 0.3387 / 0.5004; CSF-1 slip 0.03285 / 0.03396 | 0.37538 / 0.33874 / 0.50036; 0.03285 / 0.03396; 352 / 548 | yes |
| Online physical feedback, every window, both arms, S1–S3 (slip and RE) | Table 4 | all reproduced (e.g. S1 501–1,000: 0.1389 vs 0.2087; 1,501–2,000: 0.1001 / 0.1008 / 0.1018) | yes |
| D_RE S1, windows 1–500 / 501–1,000 | 0.4432 / 0.3107 | 1 − 0.4190/0.7524 = 0.443; 1 − 0.3936/0.5710 = 0.311 | yes |
| Break-even 16.56 s / 28.61 s | 17.96 / 1.085 and 31.04 / 1.085 | 16.56 / 28.61 | yes (arithmetic) |

**Cross-checked against result JSONs and code, not recomputed from raw data:** Holm counts (52 rows, 40 rejected; `v3/a3_holm.json`); monotonicity gate (8 / 800, CP 0.02115; `v1/h1m_analysis.json`); comparator selection (0.7686 / 0.8294 / 0.8335; `v1/comp_selection.json`); touch-family accuracy 0.726 [0.7014, 0.7514] (`sec08h_dfid.json`); static-touch deviation 0.1597 N; detector r 0.948, bias 0.3186, SD 0.1103; onset displacement median / p95 / max 0.126 / 0.254 / 1.92 mm; mass-noise D 0.4603; H3 R_E 0.8778 / 1.1739 / 0.9629; label oracle S2 slip 0.1346; S1m R_E 0.8871, slip difference 0.0248; ΔC 58.15 / 42.40; tail ratio 0.5918; friction-residual cvR² values; reactive-controller rows (`v3/b2_analysis.json`); compute (14.50 and 2.357 CPU-h). In code I confirmed: MuJoCo 4.0.0 in every replay header; `timestep 0.002`, `cone="elliptic"`, `impratio="10"`, `condim="6"` in `certgrip/sim.py`; a 30-configuration random search with `GroupKFold(n_splits=4)` and the exact hyper-parameter ranges of Table A1 in `certgrip/models.py`; 2,000 bootstrap draws (seed 2026) in `crc_analysis.json` and `analysis_v3_a.py`; Clopper–Pearson via `scipy.stats.beta`; Holm in `analysis_v3_c.py`. The 20 online orderings per shift exist (S1 and S3 orderings 0–4 are reused from `results/v2/b3/`, as stated in `b3v3_online.py`).

**Trial count.** The paper's run counts match the evidence:
- one seed-0 predictor set, with seeds 1–4 as refits;
- one deterministic replay set: 4,800 cal + test instances, with replays bit-identical across repeats;
- 2,000 bootstrap draws;
- 200 re-splits of the same instances;
- 20 stream orderings per shift.

The paper never claims independent repeated trials beyond these, and it explicitly calls re-splits and orderings non-independent. The split sizes match the amended pre-registration (`docs/08b_preregistration.md` l. 66: 150–199 / 200–324 / 325–499, 2,800 test). The original `07_hypotheses.md` 250/125/125 split was superseded there.

**CRITICAL_FABRICATION: no.** I found no number or procedure claimed without support. The only factual slip I found is in a figure caption (W-B6).

---

## 1. Topic adherence

The paper stays on topic throughout. It covers the probe, per-stratum CRC on the physical binary loss, the strongest non-tactile conformal baseline chosen on a selection split, attribution ablations (plug-in, shrunk plug-in, onset-only learner, feature chain, friction prior, margins), and online binary-feedback calibration under three shifts. Environment issues (an empty `platform.processor()` and unlogged CPU-hours) appear only in Appendix B as disclosures, not as contributions. Two items are related but peripheral: the force-time accounting and the reactive negative control. Both are framed as limits, which is appropriate.

## 2. Length check

The prompt asks for a NeurIPS/ICML check; I also apply RSS norms. Word counts for the main text, excluding the Figure 1 generation prompt:

| Section | Words | Threshold | Status |
|---|---|---|---|
| Abstract | 241 | ≥ 150 | ok |
| Introduction | 851 | ≥ 700 | ok |
| Related Work | 611 | ≥ 500 | ok |
| Method (§3) | 1,986 | ≥ 800 | ok |
| Experimental Setup (§4) | 838 | ≥ 600 | ok |
| Results (§5) | 3,765 | ≥ 500 | ok |
| Discussion / Limitations / Conclusion | 579 / 568 / 247 | — | ok |
| Total (incl. appendix) | ≈ 10,100 | ≥ 4,000 | ok, but long |

No section is under-length. The opposite risk is real. At ≈ 9,500 main-text words with four dense tables, the paper will very likely exceed an 8-page RSS limit (or a 9-page NeurIPS limit). §5 reads as a ledger of four-decimal numbers rather than an argument.

---

## Reviewer A (tactile manipulation / grasp control)

**Score: 4 / 10 (Borderline, leaning reject for RSS).** Confidence 4/5.

### Strengths
- **A-S1. Unusually honest and verifiable.**
  - Every headline and secondary number I checked reproduces exactly from the raw replays.
  - Only one of four pre-registered decisions is called confirmed.
  - The authors report a sub-pool in which their method loses.
  - They deflate their own learned model: a shrunk plug-in beats it at σ = 0.4.

  This level of claim hygiene is rare and valuable.
- **A-S2. The protocol isolates the probe.** A friction-uninformative preload, independent friction draws, and a check that static touch carries shape but not friction information together make the attribution question well-posed. The result that "a one-line Coulomb plug-in on the onset + CRC captures the saving" is a useful negative result for learned tactile pipelines.
- **A-S3. Physically meaningful force accounting.** The paper reports newtons, integrated N·s and a break-even hold time (16.56 s) instead of only relative excess. The admission that short pick-and-place holds do not benefit is a mature and practically important statement.
- **A-S4. A physical-slip loss rather than label surrogates.** It is the right choice for a certificate about dropping objects, and it is motivated by a pre-registered gate that failed (8 / 800 non-monotone).

### Weaknesses
- **A-W1. The effect is largely produced by the design.**
  - Friction is log-uniform on [0.3, 1.0] (a 3.3× range) and drawn independently of everything a non-tactile rule can see. Any friction-blind rule must therefore pay for the full range.
  - The paper concedes this (Lim. 6: "D largely measures the width of the friction range relative to the probe's error"). The concession, however, takes most of the scientific content out of the headline D = 0.4168.
  - When the range shrinks to [0.5, 0.8], the sign flips (−0.26 label route, −0.32 refined CRC).
  - There is no pool with realistic friction–category correlation and no deployable vision or material prior. A reader therefore cannot tell whether the probe beats what a real robot would have.
- **A-W2. "Minimal-force grasping" with a 32.7 N preload and a 49 N squeeze.**
  - The median minimal force is 3.18 N, and the 10 % quantile is 0.95 N.
  - Every object is therefore squeezed at roughly 15× its median minimal hold force (and at 50× for the lightest decile) before the method saves about 1.1 N during the hold.
  - The motivation cites fragile objects and prosthetic slip prevention, and the protocol contradicts it.
  - No low or adaptive preload was run, although such a preload is what would make the probe relevant to fragile objects.
  - Section 6 also says the probe drives every object to incipient slip on every grasp.
- **A-W3. Simulation only, with an assumed noise level that sets the result.**
  - D ranges from 0.68 to 0.14 as σ goes from 0 to 0.4, and σ = 0.2 is assumed, with no hardware or published grounding.
  - Rigid MuJoCo contact with soft-constraint parameters (`solref 0.004 1`, `solimp 0.95 0.99 0.001`) determines when incipient slip appears relative to gross slip. On real elastomer pads this lead time is the whole point of incipient-slip sensing, and here it is a simulator artefact.
  - There is no sensitivity study over contact parameters, and no second simulator or tactile model (TACTO, TacSL and hydroelastic touch are cited but not used).
- **A-W4. No competitive tactile baseline at matched slip.**
  - The reactive slip-tightening controllers slip at 0.46–0.99, which makes them a strawman. The paper labels them a "negative control", which is honest, but it leaves the key comparison (probe + CRC vs. the friction-estimate-plus-margin controllers of Khamis et al. / Niu et al.) unanswered.
  - The tuned per-stratum margin reproduces CRC's operating point exactly. So for the robotics reader the method's practical content is "read friction from an onset and tune a margin on 500 grasps per stratum", which is not new.
  - The reactive hybrid that starts at the calibrated force, which is the natural competitor, was not run.
- **A-W5. The certificate does not reach a robot.**
  - The offline bound needs counterfactual replays of every calibration grasp at all 20 grid forces, which is impossible on hardware.
  - The deployable route (online binary feedback) has only a long-run-average guarantee.
  - Its pre-registered efficiency test (H3) is inconclusive, and the physical-replay oracle was never produced.
  - For RSS, the "certified slip" in the title therefore applies to a simulation-only artefact.
- **A-W6. The guarantee is weakest where it matters physically.**
  - The lowest-friction quintile slips at 0.216 under the learned model; CSF-1 slips at 0.48 there.
  - In 57–69 % of re-splits at least one stratum exceeds α.
  - Slippery objects are the ones that get dropped, so a marginal guarantee that hides this is of limited practical value. The paper reports it honestly, but no friction-conditional (e.g., Mondrian-by-μ̂-bin) calibration is attempted, although it is the obvious fix.

### Actionable revisions (A)
1. Add at least one pool with correlated friction (e.g., μ tied to family / material with residual spread) and a deployable non-tactile prior (category → μ), and report D as a function of within-category friction spread. That turns the conditional headline into a curve a reader can place a real robot on.
2. Run a low / adaptive preload variant, for example starting at 3–5 N and stepping up on slip during lift, and report squeeze and peak forces per object. Otherwise, drop "minimal-force grasp" from the framing and state plainly that only the hold force is minimised after a high-force probe.
3. Add a contact-parameter sensitivity study (solref / solimp, pad compliance) for the onset-to-gross-slip lead time and for D, or a second tactile simulator.
4. Implement the natural competitor: a probe-estimated friction with a margin tuned per stratum plus reactive tightening starting at that force. Compare at matched slip.
5. Try friction-conditional CRC (strata by μ̂ bin) to address the low-friction miscoverage.
6. Even a small hardware pilot, aimed at measuring σ for one sensor, would change the paper's significance substantially.

---

## Reviewer B (conformal inference / statistics)

**Score: 5 / 10 (Borderline).** Confidence 4/5.

### Strengths
- **B-S1. A correct and carefully scoped use of CRC.**
  - The monotonisation L̃ = max over λ' ≥ λ is valid, and L̃ ≥ L gives the physical-slip bound.
  - The (n+1) rule and the fallback to max Λ are standard.
  - The paper states precisely that the bound is marginal, per stratum and in expectation over the calibration draw, and that edge-rule and refined-grid rows fall outside the theorem as run. This is correct and commendably precise.
- **B-S2. Pre-registration with a deviation log.** There are four core decisions on a Bonferroni split, a SESOI, a TOST registered for the learned-versus-plug-in contrast, Holm within registered families, and post hoc rows labelled as unadjusted. My bootstrap reproduces the CI\*\* of the headline.
- **B-S3. An appropriate comparator.** The comparator is the strongest non-tactile *conformal* baseline, chosen on a disjoint split (`comp_selection.json`), not an uncalibrated controller.
- **B-S4. The online study is reported with the right caveats.** Orderings share instances, so the intervals measure order effects; H3 is inconclusive; the oracle is missing.

### Weaknesses
- **B-W1. The method is published tools applied as published.**
  - CRC, Learn-then-Test and score-space quantile tracking are used unchanged, and the paper says so.
  - The statistical novelty is the choice of loss (physical binary slip over a force family) and the per-stratum application. That is a sensible engineering choice, not a methodological contribution.
  - The novelty therefore rests on the robotics side, which is weakened by A-W1–A-W5.
- **B-W2. The primary grid is badly centred, and the attribution rests on post hoc rows.**
  - On the primary grid, λ̂ sits at index 0 in D1/D2 for the plug-in at every σ (0 / 0.1 / 0.2), at index 0 for the shrunk plug-in at σ 0.2, and at index 1 for CSF-1 and the shrunk plug-in at σ 0.4 (all verified).
  - The cause is that the grid is pooled over strata, centred on a label-rule quantile, with a half-width of only ±0.4 in log, while the D1/D2 base forces include m·a_cmd and are over-protective.
  - The paper's central secondary message ("probe + simple rule suffices") therefore relies on the post hoc refined grid or the data-dependent edge rule, which the paper itself places outside the CRC theorem.
  - The comparator CSF-1 is also near the floor in the headline. The refined grid's D = 0.4289 reassures here, but the design flaw should be fixed rather than worked around.
- **B-W3. Asymmetric reliability rule in the losing sub-pool.**
  - The rule says "the refined grid can mark a primary-grid result as unreliable but cannot upgrade it". In the μ ∈ [0.5, 0.8] sub-pools the primary grid gives +0.375 / +0.339, and these are declared unreliable because CSF-1 is at the floor (slip 0.033).
  - The refined-grid inferiority (−0.3152, upper limit −0.0172) is then reported as the finding. Its upper bounds are within 0.02 of zero, it is unadjusted, and it is one of many post hoc sub-pool rows.
  - Reporting against one's own interest is laudable, but the sub-pool result should be described as fragile, not as "the baseline is better". The abstract's "the baseline is better" is stronger than the evidence warrants.
- **B-W4. Multiplicity across rounds.**
  - The paper contains well over 100 numeric contrasts across three analysis rounds; only 52 first-round rows are Holm-adjusted.
  - Three "inferiority" rows have upper limits within 0.02 of zero.
  - The prose (Abstract, Discussion) draws directional conclusions from unadjusted second- and third-round rows (σ 0.4 shrunk plug-in, sub-pool reversal). These should be consistently labelled exploratory in the Abstract and Conclusion, not only in the tables.
- **B-W5. The comparisons are not at matched slip.**
  - D compares the learned arm at slip 0.083 with CSF-1 at 0.102. This favours CSF-1 in RE terms, so it is conservative for the headline, which is fine.
  - The σ = 0.4 inferiority row (0.082 vs 0.093) and the sub-pool rows have no matched-slip version. Since RE and slip trade off steeply (frontier slope ≈ −2.5 RE per unit slip near α), an unmatched slip difference of 0.01 corresponds to about 0.025 RE, which is non-trivial against D differences of 0.03–0.06. A matched-slip or frontier-area metric should accompany every attribution contrast.
- **B-W6. Small factual and presentational issues.**
  - **(a) Fig. 1 caption.** It says CSF-1's "lowest offsets are clipped … and the lower end of the orange curve is flat". This is false by the caption's own data: the k = −4…−1 points move from (0.1711, 0.6037) to (0.1293, 0.7097), with a slope similar to that of the interior. Only the D1/D2 contribution is clipped, and D3/D4 still move. Reword the caption.
  - **(b) Undefined diagnostic.** The "friction residual R²" (App. C) is not defined in the text. Per `sec08f_dmu.json` it is a grouped-CV R² of a log μ → residual regression, computed on cal + test objects (deviation 4). Define it or drop it.
  - **(c) Hidden selection.** The comparator selection used the label rule, at unequal selection-split slip (CSF-1 0.095 vs Mondrian 0.0725). State this.
  - **(d) Inconsistent tests.** The H2b TOST is "read off the 97.5 % CI\*\*", whereas a ±0.10 TOST at 0.0125 per side corresponds to the same interval. That is consistent, but say once that a single 97.5 % interval serves both tests.
- **B-W7. Re-splits and orderings are not independent replications.** The paper says so. The only independent replication is the seed 1–4 refit of the predictor, which varies the learner but not the objects, the friction draws or the noise ε. A fresh-object replication (new object IDs, new ε) of H2a would be cheap in simulation and would turn the single confirmed decision into a replicated one.

### Actionable revisions (B)
1. Pre-specify a per-stratum grid wide enough (e.g., ±1.2 log) that no arm hits an edge, and re-run H2a and the plug-in contrasts as a *confirmatory replication on fresh objects and fresh ε*. Demote the current refined and edge-rule rows to supplementary.
2. Report every attribution and sub-pool contrast at matched slip, or as the area between frontiers over a slip band. At minimum, add the matched-slip version of the σ 0.4 and sub-pool rows.
3. Soften the sub-pool claim in the Abstract and Conclusion to "evidence (unadjusted, post hoc) that the advantage vanishes or reverses when the friction spread is narrow". Pair it with a pre-specified friction-width sweep (several nested μ ranges) so that "narrow spread relative to probe error" becomes a tested statement.
4. For deployability, add a replay-free calibration variant: for example, LTT or a sequential test on one binary outcome per calibration grasp at a pre-chosen λ sequence (a "fixed-sequence testing" design), which needs no counterfactual replays. This directly attacks what the paper calls "the central open problem".
5. Fix the Fig. 1 caption, define the friction-residual R², and cut §5 to the decision-relevant rows, moving the rest to the appendix to fit the page limit.

---

## Consolidated assessment

| Check | Verdict |
|---|---|
| On topic | Yes |
| Method–evidence consistency | High. Every checked number reproduces from raw replays. One caption misstatement (Fig. 1, "flat"). |
| Trial count | Consistent. No inflated or fabricated trial counts. |
| CRITICAL_FABRICATION | **No** |
| Length | All sections above thresholds; the paper is over-long for an 8–9-page venue. |
| Novelty | Incremental. The probe idea and the conformal tools are known; the contribution is the protocol plus the attribution study. |
| Baselines | The non-tactile conformal baseline is appropriate but weak by construction (independent friction). The tactile competitors are a strawman (reactive) or equivalent to CRC (tuned margin). |
| Ablations | Present, extensive and meaningful (plug-in / shrunk / onset-only / feature chain / prior). Several rest on post hoc grids. |
| Limitations | Exceptionally candid. |
| Recommendation | Borderline. Not ready for RSS without a less constructed friction distribution, a low-preload variant or reframing, and a cleanly gridded fresh-object replication. A hardware σ measurement would most improve the paper. |

**Scores:** Reviewer A **4/10**, Reviewer B **5/10**.

**Top 3 must-fix items**
1. **The headline is constructed by design.** Independent log-uniform friction on [0.3, 1.0] makes friction-blind rules weak, and the sign flips on [0.5, 0.8]. Add a correlated-friction or deployable-prior pool and a pre-specified friction-width sweep, and present D as a curve, not a point.
2. **The protocol contradicts "minimal force", and the certificate is not deployable.** The 32.7 N preload and 49 N squeeze sit against a median F\* of 3.2 N, the break-even hold is 16.6 s, and the offline bound needs counterfactual replays. Run a low or adaptive preload and a replay-free (one-outcome-per-grasp) calibration variant, or narrow the claims accordingly.
3. **The grid design and the post hoc attribution.** The primary grid floors the plug-in and CSF-1 in D1/D2, and the "plug-in suffices" message and the sub-pool reversal rest on post hoc, unadjusted, unmatched-slip rows. Pre-specify a wide per-stratum grid, replicate H2a on fresh objects and noise, report the attribution at matched slip, and fix the Fig. 1 caption ("flat" is false).
