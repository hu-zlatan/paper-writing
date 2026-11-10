# Stage 18 (v3, pass 2, run 1): Simulated peer review

**Paper:** *Probe, Then Calibrate: Conformal Slip-Risk Control of Grip Force from a Tactile Friction-Onset Probe (a Simulation Study)*
**Reviewer stance:** balanced conference reviewer, strict on whether the methods match the evidence.
**Inputs read:** the system and user prompts in full: the draft (lines 30–407) and the evidence block (a) results_v1.json, (a2) results_v2.json, (a3) results_v3.json, (b) the run log and (c) the statistics grep. I also opened the raw replays and labels (`results/v1/crc/*.jsonl`, `results/v1/labels/id_F*.jsonl`), the analysis JSONs (`v1/crc_analysis*.json`, `v1/h3_analysis.json`, `v1/h1m_analysis.json`, `v1/sec08f_tail.json`, `v2/a_analysis.json`, `v3/a_analysis*.json`, `v3/a3_holm.json`, `v3/a7_integrated.json`, `v3/b2_analysis.json`, `v3/b3_analysis.json`), the pre-registration documents (`docs/07_hypotheses.md`, `docs/08b_preregistration.md`) and the code (`code/analysis_crc.py`, `code/certgrip/models.py`, `code/react_run.py`, `code/tools_stage19_rows.py`). All scratch scripts are in `/tmp/claude-0/rev3/`.

---

## 0. Independent recomputation (what I verified and how)

I rewrote the CRC pipeline myself rather than reusing the authors' analysis code (`/tmp/claude-0/rev3/recompute.py`, `frontier.py`, `boot.py`, `q.py`, `s.py`, `mu.py`). It reads the raw 4,800 calibration and test replays (20-point grid per arm) and the 8,000 F\* labels. Then it monotonises the loss, applies the (n+1) CRC rule per stratum, and scores test slip and RE over the avoidable instances.

| Quantity | Paper | Recomputed | Status |
|---|---|---|---|
| Split sizes: cal / test instances; cal / test objects | 2,000 / 2,800; objects 200–324 / 325–499 | 2,000 / 2,800; 500 / 700 objects; 200–324 / 325–499 | match |
| λ̂ index, learned (D1–D4) | — | 10/10/11/10 | consistent with JSON |
| λ̂ index, CSF-1 (D1/D2) | "index 1" | 1/1 (D3 15, D4 14) | match |
| λ̂ index, plug-in (D1/D2) | "index 0 (floor)" | 0/0 | match |
| RE learned / CSF-1 | 0.4567 / 0.7832 | 0.4567 / 0.7832 | match |
| **D (H2a)** | **0.4168** | **0.4168** | match |
| 97.5 % CI\*\* for D | [0.3484, 0.4778] (2,000 draws) | [0.348, 0.476] (my own object-cluster bootstrap, 400 draws, refitting λ̂) | match within Monte-Carlo error |
| Test slip learned / CSF-1 | 0.0829 / 0.1021 | 0.0829 / 0.1021 | match |
| Per-stratum slip, learned and CSF-1 (primary) | 0.0871/0.0714/0.0757/0.0971; 0.1157/0.0886/0.1057/0.0986 | identical | match |
| Mean (median) hold force: learned / onset-only / plug-in / CSF-1 | 6.521 (4.473) / 6.519 (4.423) / 7.062 (4.556) / 7.606 (5.476) N | identical | match |
| Mean excess over F\*_mid | 1.623 vs 2.708 N | 1.623 vs 2.708 | match |
| F\*_mid quantiles 10/50/90 %, max, share > F₀ | 0.9549 / 3.184 / 11.35, 31.87, 0.0 | identical | match |
| D across σ = 0 / 0.1 / 0.2 / 0.4 | 0.6789 / 0.5825 / 0.4168 / 0.1401 | identical | match |
| Seeds 1–4 D; seed-4 slip | 0.4343 / 0.4197 / 0.3932 / 0.4494; 0.1018 | identical | match |
| Onset-only D; plug-in D (primary) | 0.4464; 0.3816 | 0.4464; 0.3816 | match |
| H2b learned vs plug-in | 0.0569 | 0.0569 | match |
| Learned vs unshrunk plug-in, σ 0 / 0.1 / 0.4 | 0.246 / 0.1072 / 0.3182; comparator D1/D2 slips 0.007143/0.002857, 0.01571/0.007143; σ 0.4 plug-in RE 0.9877 | identical | match |
| σ 0.4 learned arm slip / RE (for the shrunk row) | 0.08214 / 0.6735 | 0.0821 / 0.6735 | match |
| Fig. 1b frontier, k = −4…+4: learned, onset-only, CSF-1 (27 points) | listed | all 27 identical | match |
| Matched-slip D at 0.10 | 0.4563 | 0.4562 (my own linear interpolation) | match |
| Slip by friction quintile: learned, CSF-1, plug-in | 0.2161…0.003571; 0.4804…0.0; 0.08571…0.02857 | identical | match |
| Friction range, independence | log-uniform [0.3, 1.0], independent | μ ∈ [0.3001, 0.9989]; corr(log μ, log m) = −0.009; geometric-mean μ by family 0.53–0.56 | match |
| Break-even 16.56 / 28.61 s; plug-in 32.99 s; onset-only 16.52 s | — | 17.96/1.085, 31.04/1.085, 17.96/0.544, 17.96/1.087 reproduce them | match (arithmetic) |
| Integrated force at T = 1/5/30 s | 37.57/63.65/226.7 and 38.65/69.08/259.2 | 31.04 + F̄·T reproduces all six | match |

Numbers I matched to the analysis JSONs but did not recompute from raw files:
- matched-slip, LTT and refined-grid D (`v2/a_analysis*.json`, `v1/crc_analysis_v2.json`);
- the shrunk plug-in rows (`v3/b1_analysis*.json`);
- the sub-pool rows (`v1/sec08g.json`, `v3/a_analysis*.json` A4–A6);
- the re-splits (`v3/a_analysis.json` A1: R = 200, seed 3031);
- Holm (`v3/a3_holm.json`: 52 rows, 40 rejected; H2-R p 0.01 → Holm 0.03 within its family, 0.12 over all rows);
- the monotonicity gate (`v1/h1m_analysis.json`: 8/800, 7 in D2, CP 0.02115);
- the reactive arms (`v3/b2_analysis.json`), the H3 streams (`v1/h3_analysis.json`), physical-feedback B3 (`v3/b3_analysis.json`), the tail ratio (`v1/sec08f_tail.json` crc_08c 0.5918 [0.5540, 0.6564]), the compute figures and the static-touch check.

I also checked the learner settings against `certgrip/models.py`: HistGradientBoostingRegressor with quantile loss, the stated random-search ranges and GroupKFold(4). They match. The reactive constants in `react_run.py` (0.8, 1.25, 4 steps, 6 frames, 2 consecutive frames, 30 ms) also match Table A1. All ≈ 50 citation keys exist in the project's literature store.

**Trial count / fabrication check.** The paper claims no "N independent trials". Every replication count it states is correct:
- one primary predictor seed plus four refits;
- 2,000 bootstrap draws (`crc_analysis.json: draws 2000`);
- 200 re-splits;
- 20 stream orderings;
- n = 500 calibration instances per stratum and 2,800 test instances.

It describes the orderings correctly as largely re-using the same instances. **No CRITICAL fabrication was found.**

---

## 1. Topic adherence

The paper stays on topic: a ramp-down onset probe, CRC on the physical binary slip loss, comparison against a pre-selected friction-blind conformal baseline, attribution to the probe rather than the learner, and online binary-feedback tracking under shift. Environment issues appear only as limitations or deviations, never as contributions. Examples are the simulator-only replays, the grid floor and the unlogged CPU-hours. One small drift: the Figure 1 prompt says "RSS style" while the stated target is NeurIPS/ICML.

## 2. Methodology–evidence consistency: discrepancies found

None of these is a fabrication. Most are presentation-level.

1. **Table 4 omits the S3 matched-rate co-requirement.** The row reads "—" for S3. `v1/h3_analysis.json` → `audit/S3|matched_physical` has diff 0.009 and matched = true, so S3 passed. Report it as "0.009 (pass)". The table should also say that these differences come from a single direct-replay audit (n = 500/1,000 steps), not from the 20-ordering average.
2. **The Figure 1 caption overstates the clipping effect.** It says "the lower end of the orange curve is flat". In the recomputed CSF-1 frontier, RE runs 0.6037 → 0.7097 and slip 0.1711 → 0.1293 over k = −4…−1. The curve is compressed, because only D1/D2 are clipped and D3/D4 still move, but it is not flat. Reword.
3. **The H2-R mid-friction reversal is framed more firmly than its multiplicity status allows.**
   - The abstract states as fact that "the baseline is better". The conclusion calls it "a Holm-adjusted secondary".
   - It survives Holm only within its family (0.03). Over all 52 first-round secondaries it does not (0.12; `a3_holm.json` reject_all = False).
   - The refined-CRC confirmations are unadjusted and have upper limits of −0.0172 and −0.01539.
   - Section 5.4 and Limitation 9 are accurate. The abstract and conclusion should also say "family-wise Holm only; not significant over all secondaries".
4. **The break-even comparison uses a counterfactual that was never simulated.** "Compared with a friction-blind grasp that skips the probe-specific phases" assumes that CSF-1 would keep the same calibrated hold force (7.606 N) without the probe. But CSF-1 was calibrated and tested *with* the probe in its protocol, and probe slips count as slips. Whether the probe changes CSF-1's slip, and hence its λ̂, is unknown. The 16.56 s figure is arithmetic on that assumption (17.96 N·s / 1.085 N) and should be labelled as such. A CSF-1 arm without the probe is cheap to run in this simulator.
5. **The integrated force-time is a constant-phase approximation.** `a7_integrated.json` uses one shared-phase integral, 31.04 N·s, for every instance and arm, plus F̄·T. The probe actually ends at an instance-specific onset, and the ramp-to-hold and settle transients are ignored. This is acceptable for a descriptive row, but the text should say so.
6. **The paper says it cannot explain the reactive-controller failure, but the evidence it reports already does.** Section 5.3 says "we claim no reason for the failure". The paper's own detector statistics show that log μ̂ − log μ has mean +0.3186 (`tools_stage19_rows.py`: x = log μ̂, y = log μ), so the raw μ̂ overestimates μ by about 1.37×. REACT-probe therefore:
   - uses r_safe = 0.8 μ̂ ≈ 1.1 μ, a shear/normal threshold at or above the true friction limit, so it can hardly detect slip before gross slip;
   - starts at c ∈ {0.5, 0.75} times an *uncalibrated*, biased plug-in force.

   Its 0.99/0.95 slip and ~0.5 steps per instance are the expected result. As built, the "negative control" is mis-specified. It should be dropped, rebuilt on the bias-corrected (shrunk) μ̂, or have this mechanism stated. Section 2 should not present it as a "stand-in for this family".
7. **The "pre-registered" label on H2a is accurate but needs one clause.** The CRC route was a *conditional* fallback in `07_hypotheses.md` (H1-M failure condition). It was concretised after the gate failed (Deviation 1), and the grids were centred and selected later. The decision-bearing D is on the primary CRC grid, which is covered by the theorem as run. Good, but the abstract should note that the route was the pre-registered fallback, not the originally planned primary.

I found nothing that misreports the experimental setup, the statistical tests (Clopper–Pearson, percentile bootstrap, Holm and TOST are all present in `code/`), the hyperparameters or the baselines.

## 3. Length

| Section | Words | Threshold | OK? |
|---|---|---|---|
| Abstract | 243 | ≥ 150 | yes |
| Introduction | 854 | ≥ 700 | yes |
| Related Work | 615 | ≥ 500 | yes |
| Method (§3) | 1,992 | ≥ 800 | yes |
| Experimental Setup (§4) | 842 | ≥ 600 | yes |
| Results (§5) | 3,768 | ≥ 500 | yes |
| Discussion + Limitations + Conclusion | 582 + 571 + 250 | — | yes |
| Total (incl. appendix) | ≈ 10,300 | ≥ 4,000 | yes |

No section is under-length. The opposite risk applies: about 9,700 words of main text plus four dense tables, an algorithm box and two figures will not fit 9 NeurIPS/ICML pages. Results alone is about 3,800 words. Move Table 3's lower block, the Learn-then-Test and edge-rule rows and most of §5.5's table to the appendix.

---

## Reviewer A (robotics / tactile manipulation)

**Summary.** After a fixed 32.7 N preload and a squeeze, a ramp-down probe finds incipient-slip onset with a modelled touch detector and gives a Coulomb μ̂. A force rule fed with μ̂ is calibrated per disturbance stratum by CRC on the physical slip loss. In MuJoCo at α = 0.10 and an assumed onset noise σ = 0.2, the learned probe model needs 41.7 % less relative excess hold force than a friction-blind conformal Coulomb rule (1.085 N lower mean hold force). Most of the saving is already captured by a one-line plug-in.

**Strengths**
- S1. The exposition is exceptionally honest and quantitative. Every number I recomputed from raw replays matched to the reported precision (Section 0 above). The paper reports where it loses (μ ∈ [0.5, 0.8]), where the learner is beaten (σ = 0.4, shrunk plug-in), and what the protocol costs (16.56 s break-even).
- S2. The protocol is well designed for attribution. A friction-uninformative preload, plus friction drawn independently of every non-tactile input, makes the onset the only friction channel. The feature chain P ⊂ S ⊂ full ⊂ full+onset shows cleanly that static touch and the squeeze add nothing.
- S3. Force is reported in newtons and in force-time, not only as relative excess. This is rare and useful.
- S4. The probe's physical footprint is quantified: median onset displacement 0.126 mm, max 1.92 mm, no instance ≥ 2 mm.

**Weaknesses**
- W1. **Simulation only, and the effect size is set by an assumed parameter.** D runs from 0.68 to 0.14 as σ goes from 0 to 0.4, and σ is not grounded in any sensor. The detector's own error (SD 0.11 log, bias +0.32) is a property of MuJoCo touch grids, not of a real tactile sensor. A NeurIPS/ICML robotics reader will ask where GelSight, BioTac or barometric sensors sit on Fig. 2. Without that, the headline is one point on a hypothetical curve, as the paper itself says.
- W2. **The baseline is weak by construction.** With μ independent of everything a robot sees without touch, any friction-blind rule must cover a 3.3× friction range. The 0.4168 is then largely the gain of knowing friction under Coulomb physics, which is expected. The informative experiment, a pool where friction correlates with family or appearance and a deployable vision or category prior, is missing. The oracle-side prior at σ_p = 0.2 already erases the advantage (D −0.0299).
- W3. **The fixed protocol dominates the force budget.** A 32.7 N preload and a 49 N squeeze on every object, when the median F\*_mid is 3.2 N, defeats the "minimal-force" motivation (prosthetics, fragile objects). The hold saving pays back only after 16.6 s. The paper is candid about this, but it limits practical relevance. An adaptive or low preload is the obvious missing arm.
- W4. **Tactile competitors are thin.** The reactive negative control is mis-specified (Section 2, item 6): its threshold uses the uncorrected, upward-biased μ̂, so it cannot detect slip before gross slip. The tuned margin is the authors' own construction, so no published friction-estimating controller is reproduced. The "relation to prior work" therefore rests on no real competitor.
- W5. **Conditional safety on dangerous objects.** The lowest-friction quintile slips at 0.2161 under the learned model and 0.4804 under CSF-1, at a nominal α = 0.10. For a slip-certification paper this is the key practical caveat. It is reported but not addressed, even though stratifying on μ̂ bins (a deployable Mondrian split on the probe output) would be easy to test.

**Actionable revisions (A)**
1. Rebuild REACT-probe with the shrunk, bias-corrected μ̂ and add a reactive hybrid that starts at the CRC-calibrated force. Otherwise drop the arm and stop calling it a stand-in for the reactive family.
2. Simulate CSF-1 without the probe-specific phases to ground the break-even number.
3. Add one correlated-friction pool, e.g. μ depending on family with residual spread, with a non-tactile Mondrian-by-family baseline under CRC.
4. Add μ̂-binned (Mondrian) CRC and report the per-quintile slip. This targets the low-friction miscoverage directly.
5. Ground σ: cite published onset-detection or friction-estimation errors and place them on Fig. 2. Even a rough mapping would help.
6. Trim to 9 pages; move the online B3 table and the re-split rows to the appendix.

**Score: 4 / 10 (borderline reject).** The study is careful and fully reproducible. However, the central effect is conditional on an assumed noise level and on a friction distribution that makes the baseline weak by design, there is no hardware, and there is no faithful tactile competitor. Presented as it is now, it is not a NeurIPS/ICML robotics contribution. It would fit a workshop or a robotics venue once hardware σ is measured.

---

## Reviewer B (statistics / conformal methodology)

**Summary.** The paper applies split CRC with a monotonised binary loss per stratum, Learn-then-Test as a high-probability variant, and score-space quantile tracking online. The decisions are pre-registered with a Bonferroni split, and the post hoc and secondary analyses are labelled throughout.

**Strengths**
- S1. **Inferential hygiene is excellent.**
  - Four core decisions at 0.0125 one-sided each, with a SESOI and TOST equivalence registered for H2b.
  - Holm applied within the registered families; second- and third-round rows clearly marked unadjusted.
  - Deviations enumerated, each with its consequence.
  - A rule that the refined grid can only downgrade a primary-grid result, never upgrade it.
- S2. **The guarantee is stated correctly and narrowly.** It is marginal per stratum, in expectation over the calibration draw, and requires counterfactual replays. The monotonisation argument (L̃ ≥ L, L̃ non-increasing) is right, and the primary grid is centred on a disjoint selection split, so the CRC theorem applies to the primary rows as run. The paper correctly excludes the edge-rule and refined-grid rows.
- S3. **The bootstrap refits λ̂ inside every draw with object clustering.** My independent re-implementation reproduces the CI (Section 0).
- S4. **The empirical certificate checks are informative:**
  - 200 re-splits;
  - per-stratum and per-quintile slip;
  - the tuned-margin row, which shows that the (n+1) correction changes nothing at n = 500. The paper correctly concludes that CRC adds a guarantee, not a different operating point.

**Weaknesses**
- W1. **The methodological novelty is limited.** CRC, LTT and quantile tracking are used as published. The paper says so (§2 "Novelty"), but then the contribution must rest on the robotics finding, which Reviewer A finds conditional.
- W2. **The certificate is not deployable, and the deployable route has no finite-sample guarantee.** Offline CRC needs replays of every calibration grasp at all 20 (or 41) grid forces, which only a simulator can provide. The online tracker has only a long-run-average guarantee. The physical-replay oracle was not produced, so H3 is inconclusive in all shifts, and the S2 R_E CI [1.023, 1.428] lies entirely above 1. The paper's answer to its own third question is therefore weak. Interval-censored calibration from one outcome per grasp is named as the open problem. It was the skeptic's rejected option in `07_hypotheses.md`, and it is the natural methodological contribution this paper could have made.
- W3. **Grid design is a recurring confound.**
  - The ±0.4-log primary grid pooled over strata floors the plug-in (index 0) and almost floors CSF-1 (index 1) in D1/D2.
  - This biases H2b towards the learner and H2a slightly against the method.
  - It makes the two μ-restricted sub-pool superiorities unreliable, and it forces a post hoc refined grid.
  - As a result, most of the attribution narrative (C3) rests on post hoc or data-dependent grids. The H2b decision itself was taken on a grid known to over-protect the plug-in (slip 0.0586/0.0386 in D1/D2).
- W4. **Some contrasts compare at unmatched slip.** These are the σ 0.4 shrunk-plug-in inferiority (0.082 vs 0.093) and the H2a headline (0.0829 vs 0.1021). The H2a mismatch favours the baseline, so it is conservative. The σ 0.4 result has no matched version, and its upper limit is −0.0126, so it is fragile.
- W5. **Multiplicity framing in the summary texts** (Section 2, item 3). The abstract's "the baseline is better" for μ ∈ [0.5, 0.8] rests on a Holm-family p = 0.03 that fails Holm over all secondaries (0.12), plus unadjusted refined-grid rows with upper limits near 0.
- W6. **Online intervals.** These are over orderings of a nearly fixed instance set, which the paper acknowledges. "Consistent with convergence" is fine, but "returns to α" in the abstract reads stronger than an order-effect interval supports.

**Actionable revisions (B)**
1. In the abstract and conclusion, qualify the mid-friction reversal as "Holm-significant within its family only (0.03; 0.12 over all 52 secondaries)", and the online result as "late-window slip 0.100–0.102 over 20 orderings of largely shared instances".
2. Report the S3 matched-rate co-requirement (0.009, pass) in Table 4 and say that the co-requirement comes from a single audit.
3. Re-run H2b on a per-stratum grid wide enough that no arm floors, or state prominently, in §5.2's lead sentence, that the registered H2b test was taken on a grid that floors the plug-in.
4. Add a matched-slip version of the σ 0.4 shrunk-plug-in row. The replays exist, so this is cheap.
5. Provide at least a sketch of a calibration from binary outcomes only, for example an interval-censored or one-replay-per-grasp CRC that randomises a single grid force per calibration grasp and gives an unbiased risk estimate. Even a simulation demonstration would turn the paper's open problem into a contribution.
6. Fix the Figure 1 caption ("flat" → "compressed") and label the break-even figure as assuming that the no-probe CSF-1 keeps its calibrated force.

**Score: 5 / 10 (borderline).** The paper is a model of transparent, reproducible reporting, and every checked number holds up against raw data. But the conformal machinery is off-the-shelf, the certificate is simulator-only, the deployable online route is inconclusive on efficiency, and the attribution claims lean on post hoc grids. These are significant weaknesses for NeurIPS/ICML.

---

## Consolidated verdict

- **Scores:** Reviewer A 4, Reviewer B 5 (mean 4.5, borderline reject / borderline).
- **CRITICAL_FABRICATION:** no. Trial, seed, bootstrap, re-split and ordering counts all match the evidence. All core numbers reproduce from raw replays.
- **Must-fix items, ranked:**
  1. Fix or remove the REACT-probe "negative control". Its r_safe = 0.8 μ̂ uses a μ̂ that overestimates friction by about 1.37× (detector bias +0.3186 log), so its failure is a design artefact. Do not present it as a stand-in for the reactive or prior-work family.
  2. Qualify the multiplicity and online claims in the abstract and conclusion: H2-R is significant under Holm within its family only (0.12 over all rows), and the online intervals cover orderings only. Also correct the Table 4 S3 co-requirement (0.009, pass) and the Fig. 1 "flat" caption.
  3. Ground the force-cost and comparator claims. Simulate CSF-1 without the probe phases (the break-even counterfactual), and, if possible, add a correlated-friction pool or a μ̂-binned CRC so the headline is not purely a function of the friction-independence design and the assumed σ. Trim the main text to 9 pages.
