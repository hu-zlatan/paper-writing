# Stage 18 peer review (v2 draft, pass 2, run 1)

**Paper:** "Probe, Then Certify: A Tactile Friction-Onset Probe with Conformal Risk Control for Certified-Slip Minimal-Force Grasping in Simulation"

## Evidence actually inspected

Files opened and numbers recomputed with read-only Python:

- `results/v1/crc_analysis.json`: primary CRC grid. All 14 arms (slip, RE, CI, λ̂ indices) and all 19 contrasts (H2a, H2b, H4e, σ curve, seeds 1–4).
- `results/v1/crc_analysis_v2.json`: refined grid. All arms and contrasts.
- `results/v2/a_analysis.json` and `a_analysis_08e.json`: frontier points (all 4 arms × 9 offsets × 2 grids), LTT λ̂/slip/RE, matched-slip RE and D, and every CI\*\*.
- `results/v2/b_analysis.json` and `b_analysis_edge.json`: H5 at σ_p 0.2/0.4/0.8 with the edge rule, CSF-proxy arms, B2 margins (cal and test, per stratum).
- `results/v2/b3_analysis.json`: every window mean, every per-ordering value and D_RE. `results/v2/compute_v2.json`.
- `results/v1/h3_analysis.json`: all shifts and arms, R_E with CI, matched diffs, ordering-0 physical audit. Also `sec08h_h3s.json` and `sec08f_h3b.json`.
- `results/v1/sec08g.json` (Mondrian, oracle gap, H4d, H2-R, H2-H with all 16 cells, H2-n, D-loc), `sec08f_tail.json`, `sec08f_label.json`, `sec08f_dmu.json`, `sec08f_ut3.json`, `sec08h_dfid.json`, `sec08h_h4b.json`, `sec08h_massnoise.json`, `sec08h_h1c.json`.
- `results/v1/h1m_analysis.json`, `h1v_analysis.json`, `h2_label_rule.json`, `h4a_label_rule.json`, `comp_selection.json`, `19_report_rows.json`.
- Raw labels `results/v1/labels/id_F1..F4.jsonl` (8,000 rows). I recomputed the F\*_mid distribution of the 2,800 test instances, the unavoidable count, the onset-found rate, and the static-touch record format.
- Code: `code/analysis_crc.py` (CRC rule, monotonisation, bootstrap, decision rules), `code/analysis_v2_a.py` (frontier, matched-slip interpolation, LTT with Clopper–Pearson), `code/certgrip/models.py` (learner search space, GroupKFold), `code/certgrip/sim.py` (F₀, MuJoCo options, detector constants), `code/requirements.txt`.
- Pre-registration and amendments: `docs/08b_preregistration.md` §4–5, `docs/09_amendment_v2.md` (full), and parts of `docs/07_hypotheses.md` (Holm, H2-H, H2-R, H2-n), `docs/08f/08g/08h` (Holm not applied, H2-R definition).

I did not open any 18_\*, 20_\*, results/14_\*, results/15_\*, PROGRESS.md or OWNER_TODO.md file, and I did not look at git history.

## Fabrication audit

**CRITICAL_FABRICATION: NO.**

I spot-checked about 190 numbers in the paper against the raw result files. They cover the abstract, Fig. 1 (all 36 refined-grid frontier points, the bars, the slip dots and the σ inset), Tables 1, 2, 3, D1, F1 and F2, the primary-grid frontier in App. D, App. C compute and App. E diagnostics.

- Every checked number matches the repository output to the reported precision. Ratio-derived values also match when recomputed from the arm REs, for example seed D values, A3 D values and onset-only vs CSF-1.
- Trial and instance counts are consistent with the code and outputs:
  - n_cal = 2,000 (500 per stratum) and n_test = 2,800.
  - The selection split has 800 instances.
  - Bootstrap uses 2,000 object-cluster draws with λ̂ refitted in every draw, as `analysis_crc.py` confirms.
  - Predictor seeds 0–4.
  - 20 label-feedback orderings and 5 physical-feedback orderings.
  - Each instance is simulated deterministically; the paper never claims "N independent trials" beyond this.
- The statistical procedures described are the ones in the code:
  - CRC with the (nR + 1)/(n + 1) rule on a monotonised loss.
  - Fixed-sequence LTT with a one-sided Clopper–Pearson bound at δ = 0.1.
  - Percentile bootstrap at 1.25/98.75 (CI\*\* 97.5 %).
  - DerSimonian–Laird pooling for H2-H.

The problems I found are mis-descriptions of the pre-registration and of decision labels, not invented numbers. One of them is factually wrong and must be fixed (P1 below).

## Topic adherence and length

- **On topic.** The paper stays on the stated topic throughout: probe + CRC certified slip, comparison against the strongest non-tactile conformal baseline, attribution ablations, and online binary-feedback calibration under shift. Environment and infrastructure issues are not presented as contributions. Appendix C (compute) is appropriately brief.
- **Length.** No section falls below the minimum thresholds. Word counts:

  | Section | Words |
  |---|---|
  | Abstract | 252 |
  | Introduction | 1,197 |
  | Related Work | 693 |
  | Method (§3) | ≈ 2,240 |
  | Setup (§4) | 1,155 |
  | Results (§5) | ≈ 2,880 |
  | Discussion | 1,019 |
  | Limitations | 551 |
  | Conclusion | 306 |
  | Total including appendix | ≈ 12,200 |

- **The paper is over-length.** The main body (Abstract to Conclusion) is about 10,300 words plus five tables, a three-panel figure and an algorithm box, well beyond 9 NeurIPS/ICML pages. The Discussion repeats §5 nearly sentence by sentence, and §5.2 repeats the H2b numbers three times. A 30–40 % cut is needed.

---

## Reviewer A (robotics / tactile manipulation perspective)

**Scores:** Soundness 3/4 · Presentation 2/4 · Contribution 2/4 · **Overall 4/10 (borderline reject)** · Confidence 4/5

### Strengths
1. **Unusually honest, pre-registered evaluation.**
   - The confirmatory record is stated plainly: 1 of 4 core decisions confirmed.
   - The failed monotonicity gate is reported and drives the method change.
   - Deviations are listed (App. B), and every secondary number names its route and grid.
   - I found no number that the outputs do not support.
2. **The attribution is clean and useful.** The probe is designed so that the onset is the only friction channel:
   - fixed preload F₀ = 32.7 N;
   - static touch verified to carry no friction information (`19_report_rows.json` static_touch_check);
   - nested feature sets.

   The result that a one-line Coulomb plug-in on the onset captures essentially all of the saving is valuable and counter-hype (CSF-μ̂ vs CSF-1: D = 0.4149 on the refined grid, against 0.4289 for the learned arm). So is the finding that onset-only is never worse than the full pipeline (six route × grid rows).
3. **Conditions are put up front.** The σ curve (0.6789 → 0.1401), the narrow-friction reversal (−0.2614) and the CSF-proxy result at σ_p = 0.2 are in the abstract, not buried.

### Weaknesses
1. **The "minimal-force" framing is weak relative to the protocol.** I recomputed from the raw labels (`results/v1/labels/id_F*.jsonl`, 2,800 test instances):
   - F\*_mid has median 3.18 N, mean 4.90 N, 95th percentile 14.5 N and maximum 31.9 N.
   - Every object first receives a 32.7 N preload for 0.4 s, a 49 N squeeze peak, and a forced incipient slip.
   - So every grasp is pressed at roughly 10× its median minimal force before the hold. Since max F\* < F₀, simply holding at F₀ would never slip on this pool.
   - The saving the paper certifies is about 0.33 in relative excess hold force, on the order of 1–2 N absolute for a typical object.

   The paper acknowledges that peak force is not reduced (§1, §7). It does not quantify the hold-vs-protocol force ratio, the hold duration needed for the saving to dominate the integrated force, or whom the result serves. Fragile objects are excluded, and robust objects tolerate excess force.
2. **The comparator is weak by construction.** Friction is drawn log-uniformly over a 3.3× range and independently of every non-tactile input, so any friction-blind rule must pay for the whole range.
   - "Strongest non-tactile conformal baseline" means the best of three pre-chosen friction-blind rules.
   - The one informative stronger baseline, a friction prior at σ_p = 0.2, erases the advantage: D = −0.0299 [−0.1903, 0.0816].
   - The natural tactile competitors were not run: reactive slip-tightening, a friction-estimate controller with a tuned per-stratum margin, and a correlated-μ pool. The paper says so (§2, §7). As a result, the paper cannot claim practical relevance for tactile grip control.
3. **Simulation only, with an idealised sensor.**
   - The static touch record equals the commanded normal force and m g/2 exactly in the raw files (e.g. `touch_preload = [32.7, −0.8908, …]`).
   - Onset noise σ is assumed, and the headline is very sensitive to it.
   - The detector's intrinsic noise-free error (SD 0.11 log units, 0.20 for capsules) is already of the same order as the assumed σ.
   - No hardware anchoring of σ is attempted, not even from published onset-detection errors (which 09 §C planned to search for).
4. **The narrow-friction reversal undercuts generality and is under-analysed.** A back-of-envelope calculation explains it:
   - In the sub-pool μ ∈ [0.5, 0.8], the log-μ spread has SD ≈ 0.136.
   - The probe's effective log-noise is ≈ √(0.2² + 0.11²) ≈ 0.23, larger than the friction spread itself.
   - So the reversal is expected, not anomalous, and practitioners need this rule of thumb.

   The analysis also has gaps:
   - It is on the label route, whose premise failed.
   - Only about 88 calibration instances per stratum are available.
   - No arm-level RE or slip is reported.
   - It confounds narrow μ with mid amplitude.
5. **Presentation.**
   - The text is dense with route and grid qualifiers, hypothesis codes and repeated caveats.
   - The Discussion largely restates §5.
   - Fig. 1 has three panels with numerous annotations, which will not be readable at column width.

### Actionable revisions (Reviewer A)
- Report absolute forces:
  - the F\*_mid distribution against F₀ and 1.5 F₀;
  - absolute mean hold force per arm;
  - the integrated force over protocol + hold for representative hold durations.

  State the hold duration at which the hold saving dominates.
- Add the rule-of-thumb reading of the σ curve and the sub-pool reversal: effective onset noise versus friction log-spread.
- Cut the main text to 9 pages. Move the label-route rows, the σ-ordering paragraph and most of §5.5 to the appendix, and drop the restatement in §6.

---

## Reviewer B (conformal inference / methodology perspective)

**Scores:** Soundness 3/4 · Presentation 2/4 · Contribution 2/4 · **Overall 5/10 (borderline)** · Confidence 4/5

### Strengths
1. **Correct CRC use, with properties checked in code.**
   - Monotonisation L̃ = running max from the top, a valid upper bound on L.
   - The (nR̃ + 1)/(n + 1) ≤ α rule.
   - A fallback that is flagged.
   - Grids are built from the selection split only, so even the "post hoc" refined grid does not touch the calibration or test data.
   - The bootstrap refits λ̂ in every draw, so the intervals include calibration variability (`analysis_crc.py` lines 45–53 and 90–140).
2. **The LTT variant is implemented correctly** as fixed-sequence testing on a monotone risk with a one-sided Clopper–Pearson bound (`analysis_v2_a.py`). The paper correctly states the per-stratum guarantee and the 4δ union bound.
3. **The paper is honest that the offline certificate is simulation-only** (§3.4 "Where the certificates apply"). It is also honest that the OQT long-run slip ≈ α follows from an accounting identity and is not a finding (§3.5).

### Weaknesses
1. **The pre-registration is mis-described for H2b (factual error).** The paper says "no equivalence test was registered" for the learned-vs-plug-in contrast in at least five places:
   - C3 (§1);
   - §5.2, twice;
   - the Table 2 caption;
   - §6 and §8 ("no equivalence is claimed").

   This is false:
   - `docs/08b_preregistration.md` §4 item 3 registers "TOST equivalence within ±0.10 at 0.0125 per side".
   - The docstring of `code/analysis_crc.py` says "H2b likewise (TOST ±0.10)", and `decide()` implements it.
   - The paper's own §4 says "The learned-versus-plug-in contrast declares superiority by the same rule and equivalence if the CI\*\* lies inside ±0.10".

   So the paper contradicts itself. The correct statement is that the registered TOST failed:
   - primary-grid CI\*\* [−0.0399, 0.1454];
   - refined-grid upper limit 0.1001, just outside the margin;
   - on the secondary label route the code labels the result "equivalence" ([−0.0850, 0.0814]).

   This is a correction in favour of transparency, not of the method. It still has to be fixed, because the current wording claims that a registered test did not exist.
2. **The H1c ledger entry is inaccurate.** Table A1 says "not confirmed (RAW-Qv within α at every level)", but the outputs differ:
   - RAW-Qv's point slip is *above* α at every level (+0.0029, +0.0161, +0.0125, +0.0396).
   - Only its CI\*\* contains 0.
   - The file's decision is "partly confirmed / not confirmed": RAW-Q and RAW-G over-slip with every CI above 0, but do not exceed the registered margin at α = 0.05.

   Also, "a practitioner's validation-tuned shift already lands near α" (§5.5, §6) is generous. The point estimate at α = 0.20 is 0.2396, the CI\*\* half-width at α = 0.10 is about 0.04, and the comparison uses label slip, while CRC slip is physical.
3. **H2-H is called "pass" despite significant heterogeneity.** Q = 31.04 on 15 df gives p ≈ 0.009, with τ = 0.051. "Pass" refers only to the no-harmful-cell guard. The paper should say that heterogeneity is significant and that D3 cells are consistently weakest (0.30–0.39). The guard's lower limit of 0.1602 for F3D3 is close to its threshold.
4. **Realised slip above α is under-reported.**
   - Seed 4 of CertGrip-full has overall test slip 0.1018 > α (`crc_analysis.json`, `full_rd@0.2#4`). The seed row reports only D.
   - CSF-1 exceeds α in D1 (0.1157) and D3 (0.1057).
   - The label-route rules slip physically at 0.1014 (CertGrip) and 0.1114 (CSF-1). The audit "passes" only in the sense |Δ| ≤ 0.02.

   These are compatible with an in-expectation bound, but they should be tabulated per seed and per stratum. No conditional or per-cell slip is reported at all (acknowledged in §7).
5. **The grid design flaw biases a decision-bearing contrast.** The primary grid is pooled over strata and ±0.4 wide, while per-stratum λ̂ for the plug-ins spans indices 0–15. CSF-μ̂ therefore sits at the floor in D1/D2, which biases H2b towards the learned arm. The paper handles this transparently (App. B(2), the refined grid). Still, the decision-bearing H2b estimate is the biased one, and the paper should say plainly that H2b is uninformative as registered.
6. **Matched-slip D_match is test-selected.** It is labelled descriptive, which is correct. The text in §6 nonetheless uses it to "address" the unequal-slip objection. A calibration-side matched comparison would be the valid version: select the offset per arm such that calibration risk equals a common target, then evaluate on test.
7. **Multiplicity.** Holm was registered (07 §4) and dropped. The H2-R reversal's upper limit is −0.0325, so it would likely not survive correction. This is acknowledged, but the abstract presents the reversal without that caveat.

### Actionable revisions (Reviewer B)
- Correct every "no equivalence test was registered" statement for H2b (see P1).
- Fix the Table A1 H1c entry and the RAW-Qv wording.
- Report the H2-H heterogeneity test, per-seed slips and per-stratum slips for all arms.
- Add the abstract-level caveat that the sub-pool reversal is unadjusted, from a label route, and n_cal ≈ 88 per stratum.

---

## Consolidated must-fix list

### Paper-level fixes (no new experiments)
1. **(P1, factual) H2b equivalence was registered.**
   - Replace every "no equivalence test was registered (for H2b)" with "the registered TOST equivalence at ±0.10 (0.0125 per side) was not met", in C3, §5.2 (two places), the Table 2 caption, §6 and §8.
   - This also removes the conflict with §4.
   - Keep "no equivalence test" only for H5 and H4e, where it is true (09 registered superiority / not-shown labels only).
2. **(P2) Correct the Table A1 H1c entry** to "partly confirmed / not confirmed; RAW-Qv point slip above α at every level, CI\*\* contains 0", and soften "lands near α" in §5.5 and §6.
3. **(P3) Report H2-H heterogeneity:** Q = 31.04, df 15, p ≈ 0.009. State that "pass" refers to the no-harmful-cell guard only.
4. **(P4) Report per-seed test slip** (seed 4: 0.1018 > α) and per-stratum slip for every primary-grid arm, alongside D.
5. **(P5) Quantify force accounting:** F\*_mid distribution (median 3.18 N, mean 4.90 N, max 31.9 N) against F₀ = 32.7 N and the 49 N peak; absolute mean hold force per arm. State explicitly that holding at F₀ alone would not slip on this pool.
6. **(P6) Abstract caveat:** the narrow-friction reversal is a label-route, unadjusted, small-n secondary. Add the noise-versus-spread reading.
7. **(P7) Length:**
   - Cut the main text to 9 pages.
   - Remove the §6 restatement of §5.
   - Move label-route rows, the σ-ordering paragraph and the RAW-Q/G details to the appendix.
   - Simplify Fig. 1.
8. **(P8)** State that the decision-bearing H2b estimate is biased by the grid floor, so H2b as registered is uninformative rather than merely "not confirmed".

### Evidence-level items (new experiments or analyses)
1. **(E1) Practical baselines on the same probe:**
   - a per-stratum tuned margin, i.e. a per-stratum validation shift (cheap, no new simulation beyond replays already available);
   - a reactive slip-tightening controller;
   - a friction-estimate controller with tuned margins.

   Compare at matched (calibration-selected) slip.
2. **(E2) Correlated-μ pool or deployable friction prior** (e.g. family- or material-correlated μ), so that the comparator is not friction-blind by construction.
3. **(E3) Re-run H2-R on the CRC route and decompose it:** narrow-μ only versus mid-amplitude only, with arm-level slip and RE.
4. **(E4) A calibration-selected matched-slip comparison** to replace the test-selected D_match.
5. **(E5) Ground σ** from published incipient-slip-detection error on real tactile sensors (registered in 09 §C but not done), or run a small hardware measurement.
6. **(E6) Adaptive-preload variant**, or report integrated force over protocol + hold, to test whether the "minimal force" claim survives full-episode force accounting.
7. **(E7) Physical-feedback online study with intervals:** more orderings, S2 included, an oracle reference that meets α, and a bootstrap interval for R_E.

## Recommendation
This is a careful, transparent and numerically faithful simulation study. Its main contribution is attribution: the friction information is in the probe, and a calibrated Coulomb plug-in suffices. Its weaknesses limit significance:
- a friction-blind comparator in a world built so that friction is unpredictable;
- an assumed sensor noise to which the effect is very sensitive;
- a "minimal-force" saving of a few newtons after a 33–49 N protocol;
- 3 of 4 core decisions not confirmed;
- no tactile competitor evaluated.

As it stands it is a borderline-to-weak-reject at NeurIPS/ICML (A: 4, B: 5). It would fit a robotics venue or workshop better after P1–P8 and at least E1/E3.
