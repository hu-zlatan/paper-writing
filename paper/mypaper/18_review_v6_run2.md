# Stage 18 PEER_REVIEW [v6], run 2

Reviewed draft: Stage 17 PAPER_DRAFT [v6] (2026-11-13), as embedded in `paper/mypaper/prompts/stage18_v6_user.txt`.
Reviewers: two robot-learning reviewers of the RSS / CoRL kind (novelty, significance for robotics, whether the evidence
supports each claim). The instructions name NeurIPS/ICML (9 pages); both venue lenses are applied below.

Evidence checked: `results/v6/14_v6_analysis.json`, `results/v6/15_derived_v6.json`, `results/v5/results_v5.json`
(E6 latency, E7 look-ahead, D5 thresholds, `16_report_rows` regret), `docs/07c_amendment_v6_0.md` (with addendum v6.1),
`docs/07c_amendment_v5_1.md`, `code/analysis_v6.py`, `code/touchbed/stats.py`, and the raw jsonl under
`results/v5/test5/` and `results/v6/test5/`.

---

## 0. Verification summary (shared by both reviewers)

### 0.1 CRITICAL FABRICATION: none found

- **Trial / episode counts match.** All five cells are `complete: true` and `gt_complete: true` on both windows. Every
  method has 500 episodes on 0–499 and 200 on 300–499. There are 27 policy instances in S2/S12 and 22 elsewhere, as the
  paper says. E12 has 100 episodes per method in every cell. The bootstrap uses B = 10,000 (`N_BOOT`), with 5 student
  seeds, 5 BC seeds, 5 RL seeds, 2 G\* runs and 1 run per reduced planner. This matches `n_seeds` in the JSON.
- **Statistical tests claimed vs present.** The paper claims a crossed episode × seed bootstrap, TOST and Holm. All three
  are in `code/analysis_v6.py` (`two_sided`, `tost`, `holm`) and `code/touchbed/stats.py`. The paper claims no other
  test (no ANOVA or t-test).
- **Pre-registration.** The hypotheses H6a/H6b/H6c, δ = 0.04, the Holm families (5, 5, 10), the two windows, E12 being
  report-only, and the 733 CPU-h TIME_ESTIMATE ≤ 800 with no reduction all match `docs/07c_amendment_v6_0.md` and v6.1.
  *Not verifiable from this clone:* the repository is a shallow clone (`git rev-parse --is-shallow-repository` = true,
  73 commits), so the claim "the read-out script was committed before the first new record was read" cannot be checked
  against commit order.

### 0.2 Headline numbers recomputed from raw jsonl (independent loader, `python -I`)

I reproduced the episode loading of `analysis_v6.py` (v5 records for 0–299, v6 for 300–499). I then recomputed with my
own bootstrap implementation and a different RNG seed (12345 rather than the registered 0):

| Contrast (0–499) | Paper / JSON | Recomputed (seed 12345) |
|---|---|---|
| H6a S4, student − G\*(r1+r2) | −0.0374 [−0.0784, 0.0024]; ci90 [−0.0716, −0.0036]; p_TOST 0.4559 | −0.0374 [−0.0792, 0.0016]; ci90 [−0.0720, −0.0044]; p_lo 0.4549 |
| H6a A16-2 | −0.0028 [−0.0496, 0.0436]; p_TOST 0.0548 | −0.0028 [−0.0488, 0.0444]; p_lo 0.0527, p_hi 0.039 |
| H6b A16-2 − R-125 | +0.1532 [0.102, 0.204], p < 1e-4 | +0.1532 [0.100, 0.206], p = 0 |
| H6b A16-2 − R-500 | +0.1092 [0.058, 0.159] | +0.1092 [0.059, 0.160] |
| H6b S4 − R-125 / − R-500 | +0.0556 (p 0.0072) / +0.0676 (p 0.0016) | +0.0556 (p 0.0108) / +0.0676 (p 0.0024) |
| H6c S4 / A16-2 | +0.0084 / −0.0052 | +0.0084 / −0.0052 |
| G\* first-action agreement S4 / A16-2 | 0.402 / 0.314 | 0.402 / 0.314 |

The point estimates reproduce exactly. The intervals and p-values agree up to bootstrap Monte Carlo error.

**New finding: the H6b Holm count sits close to the bootstrap-seed boundary.** I re-ran all 10 H6b contrasts with
bootstrap seeds 1–10. Holm rejects 7/10 in nine of the ten seeds. With seed 10 it rejects 5/10: S4 − R-125 and
S12 − R-125 drop out. Across seeds the S4 − R-125 p-value ranges 0.0072–0.0124 (mean 0.0104), and the registered
seed 0 gives the lowest value. The fresh-window count (2/10) is stable in all ten seeds. The registered seed is the
legitimate result, but "7 of 10" depends on two contrasts that sit on the Holm threshold. The paper calls these two
"marginal" only because the reduced-planner variance is missing. It should also say that they are within bootstrap
Monte Carlo error of the threshold.

### 0.3 Other numbers spot-checked against JSON (all match unless noted)

- Latencies and ratios: G\* 0.910–4.880 s, R-500 0.048–0.194 s, R-125 0.022–0.116 s, student 0.326–0.500 ms.
  Reduced/G\* speed-up 19–47×, student/reduced 62–389×, G\*/student 2,544–9,767×. The G\*/student `half_width_ok` holds
  only in A16-2 (`14_e6_analysis`). There are 1,000 decisions per S cell and 500 in A16-2 (`19_lat_agreement`).
- Reduced-planner loss vs G\* run 1 is 4.4–14.4 pp; S4 R-500 (0.390) < R-125 (0.402).
- Tables 1, 2 and 3: every Δ, ci, p, Holm flag, upper-margin p and BI footnote matches.
- The BI unregistered Holm (S4 and S8 survive) is correct arithmetic.
- Teacher variance (+0.014 … +0.024), first-action agreement (0.245–0.452), and student seed spread (2.8–6.2 pp) match.
- The v5-row update (−1.92 … +0.92 pp), heuristic margins (+6.68 … +17.12; post hoc +4.16 / +5.08 / +2.44), RL rows,
  g_T inversion flags and the A16-2 RL 2.0-probe collapse match.
- E12 shifts (−1.6 / +4.6 / +5.0 / −4.6 / −0.6 pp), flip rates, H5b slope (−0.0070 [−0.137, 0.124]) and travel ranges
  match.
- E7 look-ahead headroom = `indep_gap_nats` C1_512 (S2 0.0658 [0.0297, 0.1084], S12 0.0422 [0.0250, 0.0614]) matches.
- v5 gate effective thresholds = −1.23 … −1.72 pp (`12_d5_analysis` succ thresholds) match.
- "9 of 10 success-reward runs time-guarded" matches `07c_amendment_v5_1.md` l.62.
- S2 held-out regret ranges (0.2803–0.2848 / 0.2776–0.2857) match `16_report_rows.json`.

**Minor numeric or wording discrepancies (not fabrications):**
1. **S12 strongest comparator is a tie.** In S12, B-cov and R-500 are both 0.390 on 0–499. `15_derived_v6.json`
   reports B-cov, and §5.1 reports "B-cov in S12" without mentioning the tie. The margin is +2.44 pp either way.
2. **"Deficits of about 7–8 pp are not excluded"** (abstract, C2, §5.2, §6.2, §8). The ci95 lower bounds are −6.9,
   −7.8, −7.0, −5.3 and −5.0 pp, so the honest range is about 5–8 pp. "About 7–8 pp" holds only for S2, S4 and S8.
3. **"Equivalence required |gap| ≤ 0.15–1.16 pp"** (§5.2) is δ minus the unadjusted 90 % half-width. Under the
   registered Holm over 5 cells, the smallest p_TOST must be ≤ 0.01, so the true requirement is stricter. In A16-2 it is
   effectively unattainable. Label the figure "unadjusted".
4. **§6.2 says "The study was designed with enough episodes for a 4 pp equivalence test".** This contradicts the
   pre-registration's own design note ("equivalence can be shown only if the point gap is near 0") and the paper's
   Power paragraph. The design had very little power for TOST at δ = 4 pp from the outset. C2 is therefore close to a
   designed-in null, and the text should say so plainly.

### 0.4 Topic adherence and length

- **On topic.** All sections serve the stated five-cell characterisation. Environment issues (time guards, resumption,
  2-core runners) appear only as disclosures or limitations, never as contributions. That is good.
- **Mild drift into project history.** The intro paragraph on "the previous round" and its failed gates, §4 "Why TOST
  replaces the previous gate", the §5.2 "v6 update of the previous single-run row", and §6.2 "Comparison with the
  previous round" read as an internal lab log. An external reader has no "previous round". Condense these into one
  sentence plus an appendix.
- **Length (words):** Abstract 245, Intro 803, Related Work 563, Method 1,715, Experiments 1,122, Results 1,999,
  Discussion 857, Limitations 415, Conclusion 214; total about 7,930. Every section clears its minimum, and the paper is
  not under-length. The risk runs the other way: with five tables, Figure 1 and Algorithm 1, about 7,900 words will
  exceed 9 NeurIPS pages, and RSS/CoRL's 8-page limit even more. Results (about 2,000 words of dense number-listing)
  and Method §3.1/3.4 are where to cut. The abstract (245 words) is at the upper limit.
- **Unresolved citation placeholders:** `[CITE-MISSING]` for DeepSets (Zaheer et al. 2017), the bootstrap (Efron) and
  Holm (1979). These must be filled before submission.
- **"TouchBED"** appears in the title and in Limitation 11, but the text never introduces it as the simulator's name.

---

## Reviewer A (robot learning; novelty and significance for robotics)

**Summary.** The paper distils a cost-aware greedy EIG touch planner (G\*) into a DeepSets policy (BC followed by two
DAgger rounds). It compares that policy with two reduced Monte Carlo versions of the planner, with RL and with
heuristics, in a planar simulator: five cells, 500 paired test episodes, and a pre-registered Holm-controlled analysis.
The findings: the student beats the smaller reduced planner everywhere and the larger one in 2/5 cells, at much lower
compute; parity with G\* is neither shown nor refuted; DAgger adds nothing detectable over BC; and the success metric
is sensitive to the evaluator grid and to teacher stochasticity.

### Strengths
1. **Unusually honest and disciplined reporting.** Pre-registered families, Holm, a fresh window reported side by side,
   negative and inconclusive results stated as such, and every post hoc number labelled. Every number I checked
   matches the JSON. This level of rigour is rare in robot-learning papers and is worth acknowledging.
2. **Teacher stochasticity is measured, not assumed away.** Two G\* runs from identical states agree on only 25–45 % of
   first actions. This is a useful observation for anyone distilling a Monte Carlo planner, since the "expert" in
   DAgger is a distribution.
3. **The evaluator-grid check (E12)** shows that changing only the posterior read-out resolution moves a student − G\*
   contrast by about 5 pp and flips 4–13 % of success outcomes. This is a practical warning for tactile-localization
   benchmarks that threshold a gridded posterior.
4. **Fair action-space control.** The reduced planners keep C = 512, and the student, the reduced planners and G\*
   share the action set and the likelihood, so the differences come from selection alone.

### Weaknesses
1. **Limited novelty for RSS/CoRL.** Distilling an information-gathering expert with BC/DAgger is established
   (Choudhury et al. 2017; Nguyen et al. 2024). Amortized design with one-forward-pass policies is established (DAD,
   iDAD). The paper itself says it is "a measurement, not a method". The measurement covers one planar simulator, one
   fingertip on a fixed circle, and a likelihood shared by planner, filter and evaluator. That is too narrow to change
   practice in tactile robotics.
2. **The latency motivation is never tied to a robot.** G\* takes 0.9–4.9 s per decision on a 2-core CPU in
   hand-written numpy. A physical probe (approach, contact, retract, plus travel) also takes on the order of seconds,
   and decisions can be computed during motion. Without a task-time model (acknowledged in Limitation 4), the paper
   cannot show that the 2,500–9,800× compute saving changes episode time, throughput or success on hardware. For a
   robotics venue this is the central gap: the practical question "which fast policy should I deploy?" is posed but
   not answered in robot terms.
3. **The "frontier" is a strawman pair of reduced planners.** Both reductions use the same N·M = 2,000 budget, keep all
   512 candidates, and are still 62–389× slower than the student. No reduced planner sits anywhere near the student's
   latency. Many standard speed-ups are untested: candidate pruning or coarse-to-fine C, caching ball-neighbour lists,
   GPU or vectorised likelihoods, warm-starting from the previous belief, and cheap information-based heuristics such
   as particle-variance or entropy-of-contact-prediction. The claim "distillation buys more accuracy per millisecond
   than shrinking" is therefore supported only against these two points. It also rests on single runs of each reduced
   planner, and the paper's own data show that G\* runs differ by up to 3–5 pp.
4. **Low absolute success limits significance.** All methods, including G\*, succeed on only 43–53 % of episodes. The
   differences being litigated are 2–4 pp. A reader cannot tell whether the setting is in a regime where touch
   planning matters, or whether the success criterion (tolerances read from a sub-8 grid) is the bottleneck. E12
   suggests the latter is partly true.
5. **The competitive picture is weaker than the C1 headline suggests.** Against the strongest non-oracle comparator in
   each cell, the student clears the registered level only in A16-2. In S2, S4, S8 and S12 its margin over R-500, B-cov
   or RL is an untested +2.4 to +4.2 pp (§5.1). This is stated honestly but buried in §5.1. The abstract and C1 lead
   with "beats R-125 in all five cells", and R-125 is the weakest of these comparators.
6. **The RL comparator is not credible.** It was tuned once on S2 with one sweep seed and collapses to 2 of 3 probes in
   A16-2 (4/5 seeds), and the success-reward control was time-truncated in 9/10 runs. These rows add length but not
   evidence. Either tune per cell or move them to the appendix as a sanity check.
7. **The DAgger null is unsurprising and under-explained.** With 3–4 probes per episode and dense per-action labels,
   covariate shift has little room to compound. Checkpoint selection uses regret on G\*-visited states, and the
   student-visited regret DAgger targets was not measured. The ablation therefore says little beyond "short horizons
   do not need DAgger". A horizon sweep (larger n\* or τ) would turn it into a finding.

### Actionable revisions
1. Add a task-time model: probe duration plus travel time from a realistic fingertip speed, with planning overlapped or
   not. Report episode time per method, or at least the latency at which G\* compute becomes the bottleneck.
2. Add at least one reduced or accelerated planner at or near the student's latency (for example C = 32–64 with small
   N and M, or a cached or vectorised G\*), plus one cheap information-based heuristic. Without these, the "frontier"
   has no points in the region the claim is about.
3. Re-run each reduced planner at least once more (salted, like G\* run 2), so that their variance enters the H6b
   intervals. The two marginal R-125 rejections depend on it, and also on the bootstrap seed (§0.2).
4. Put the "strongest comparator per cell" result into the abstract and C1. Rephrase C1 as "beats both reduced
   planners in 2/5 cells and the smaller one in 5/5; against the best alternative it is ahead by untested 2–4 pp in 4/5
   cells".
5. Either drop RL to an appendix sanity row or tune it per cell. Do the same for the success-reward control.
6. If any hardware is available, run even a small real-contact replication (one shape library, G\* vs student,
   about 50 episodes). This is the single change that would most raise relevance for RSS/CoRL.
7. Condense the project-history passages (previous round, gate replacement) to one sentence.

### Would I accept?
No, not at RSS/CoRL in its current form. The paper is an exemplary piece of careful measurement, but its positive
claim is narrow (dominance over two hand-picked reduced planners) and its other three claims are a null, a
non-result, and a methods caution. None of them is tied to a robot or a task-time benefit. As a workshop paper or a
short "lessons for evaluating amortized active perception" note, it would be valuable.

**Score: 3 / 10 (Reject).** The reason is limited novelty and significance for robotics, not flawed evidence.

---

## Reviewer B (methodology and evidence; robot-learning evaluation)

**Summary.** I focus on whether each claim is licensed by the registered analysis and the raw data. I recomputed H6a
(S4, A16-2), H6b (all ten contrasts, eleven bootstrap seeds), H6c (S4, A16-2) and the first-action agreement from the
raw jsonl (§0.2). The paper's numbers are accurate. My concerns are about what those numbers can support.

### Strengths
1. **Claims follow the registered licences.** "More accurate" appears only where Holm rejects with positive sign,
   "neither difference nor equivalence" appears where TOST fails, and DAgger is "not detected". Post hoc margins are
   flagged with "no CI".
2. **The paired design is real.** The same episode, start angle and observation stream are used across methods, and
   the bootstrap resamples episodes jointly, which is the right inferential unit.
3. **Fresh-window replication is reported with every contrast.** The paper correctly states that it replicates the
   direction (9/10 positive) and not the significance (2/10).
4. **Limitations are complete and specific** (12 items), including several a reviewer would otherwise have to raise:
   single runs of the reduced planners, the latency CI rule met in 1/5 cells, BI and g_T outside the Holm families,
   and E12 covering G\* run 1 only.

### Weaknesses
1. **The H6a TOST was close to a designed-in failure.** The pre-registration states that equivalence at δ = 4 pp
   "can be shown only if the point gap is near 0". With observed 90 % half-widths of 2.84–3.85 pp and Holm over five
   cells, the smallest p_TOST must be ≤ 0.01. This needs |gap| well under the unadjusted 0.15–1.16 pp, which A16-2 can
   barely reach even with a gap of zero. §6.2's "designed with enough episodes for a 4 pp equivalence test" is
   therefore wrong (§0.1 item 4), and C2 should be presented as an under-powered test, not as an informative non-result.
   Either justify δ = 4 pp in robot terms, or report the smallest margin that the data would declare equivalent
   (for example the ci90 bound: about 4.1–7.2 pp per cell).
2. **The two-run teacher bootstrap is crude.** Resampling 2 "seeds" with replacement means that in about half of the
   resamples one G\* run is drawn twice. The between-run variance is therefore estimated from two values and is
   unstable, as the paper concedes. A third and fourth G\* run (about 30 CPU-h each per the v6.0 estimate), or a
   random-effects model of run-to-run variance, would make H6a interpretable.
3. **The H6b significance count is fragile.** (a) Each reduced planner is a single Monte Carlo run, while two G\* runs
   on identical states differ by up to 3.2 pp on 0–499 and 5 pp on 300–499. A noisier reduced planner probably varies
   at least as much, which would widen the H6b intervals. (b) Independent of (a), my bootstrap-seed check (§0.2) shows
   that the Holm count falls from 7 to 5 in one of ten alternative seeds. The two contrasts that drop (S4 and S12 vs
   R-125) are exactly the ones whose lower bounds sit at +1.3–1.4 pp. (c) E12 did not re-read the reduced planners, so
   H6b's robustness to the grid is unknown. Given flip rates of 4–13 % in the S cells, a 5–6 pp contrast could move.
4. **The evaluator sensitivity undermines success as the primary metric, not just the parity claim.** The paper
   confines C4 to the student − G\* contrast, but the same read-out decides every success outcome. Sign changes in 3/5
   cells, together with flip rates that differ by policy, mean a policy × grid interaction is present. An analysis that
   reports both grids for all primary contrasts, or a continuous metric such as BI or posterior mass on the ball,
   should carry more weight. The BI result (student lower than G\* in S4 and S8, surviving an unregistered Holm) points
   to a real deficit that the success metric partly hides, and it deserves more prominence in C2.
5. **The latency evidence is thin.** The latencies are point medians from the previous round, one student seed, runners
   that differ across cells, no dispersion, and the G\*/student CI rule met in only 1/5 cells. The ratios are
   descriptive, and the paper says so, but the figure plots them as the frontier's x-axis without uncertainty.
6. **Multiplicity outside the families is handled honestly but inflates the text.** BI, g_T, heuristic, RL and
   fresh-window p-values are numerous. Readers will cherry-pick them, and moving most of them to an appendix table
   would help.
7. **Smaller issues.** The S12 strongest-comparator tie is not disclosed (§0.3 item 1). "Deficits of about 7–8 pp"
   should be "5–8 pp" (item 2). The unadjusted equivalence requirement is not labelled as unadjusted (item 3). Three
   `[CITE-MISSING]` placeholders remain. "TouchBED" is never defined. The commit-order claim about the read-out script
   cannot be verified from the shallow clone.

### Actionable revisions
1. Correct §6.2 ("designed with enough episodes…") and state in §4 that, under Holm, the TOST at δ = 4 pp had very
   little power by design. Add the per-cell smallest margin at which equivalence would be declared.
2. Run G\* runs 3–4 and a second run of each reduced planner, and recompute H6a/H6b. If compute forbids this, report
   H6b with a sensitivity band that adds G\*'s observed run-to-run SD to the reduced-planner side.
3. Report the bootstrap Monte Carlo error of the marginal p-values, or use B = 100,000 for the H6b family. State that
   7/10 depends on two near-threshold contrasts.
4. Extend E12 to the reduced planners on 0–99, so that the frontier's grid sensitivity is known. Alternatively, present
   BI beside success for H6b.
5. Elevate BI in C2: "on ball information the student is below G\* in S4 and S8 (exploratory)".
6. Disclose the S12 tie. Change "7–8 pp" to "5–8 pp". Label 0.15–1.16 pp as unadjusted. Fill the three citations.
   Define TouchBED.
7. Cut length to fit 9 pages (NeurIPS) or 8 (RSS/CoRL). Move RL, success-reward RL, heuristic updates and the
   previous-round comparison to an appendix.

### Would I accept?
No. The evidence is accurate and the claims are carefully worded, but the one positive claim rests on single runs of
two reduced planners and a Holm count near the boundary, and the parity test was under-powered by design. The
contribution is a well-documented negative and methodological result. It suits a workshop or a reproducibility track
better than a main track.

**Score: 4 / 10 (Borderline reject).** The methodology-evidence consistency is excellent. The score reflects
evidential strength and significance.

---

## Consolidated top actions (priority order)
1. Add near-student-latency comparators (an accelerated or pruned G\* and a cheap information heuristic), and give the
   reduced planners at least a second run, so that the frontier claim is not resting on single runs of two
   same-budget points.
2. Add a task-time model, or even a small hardware check, so the compute savings mean something for a robot.
3. Correct the TOST power framing (§6.2), report the margin the data could certify, and add G\* runs 3–4.
4. Disclose the H6b bootstrap-seed fragility (7 → 5 in 1/10 seeds) and extend E12 to the reduced planners.
5. Clean up: S12 tie, "5–8 pp", the unadjusted label, the three missing citations, the TouchBED definition, condensed
   project-history passages, and cut to the page limit.
