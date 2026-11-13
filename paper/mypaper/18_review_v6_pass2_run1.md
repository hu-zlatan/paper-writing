# Stage 18 PEER_REVIEW [v6] pass 2, run 1 — review of the stage-19 pass-1 revision

Reviewed: the paper draft embedded in `paper/mypaper/prompts/stage18_v6_pass2_user.txt` (title "Amortizing a Cost-Aware
Information-Gain Touch Planner: A Pre-Registered Accuracy–Latency Study in TouchBED"), against the evidence in the same
prompt, `docs/07c_amendment_v6_0.md` (with addendum v6.1), `code/analysis_v6.py`, `code/touchbed/stats.py`,
`results/v6/{14_v6_analysis.json, 18_posthoc_v6.json}`, `results/v5/14_e6_analysis.json` and the raw jsonl under
`results/v5/test5/` and `results/v6/test5/`. System role: balanced conference reviewer, rigorous about
methodology-evidence consistency. Nothing in the repository was modified apart from this file.

**CRITICAL FABRICATION: none found.**

| Reviewer | Perspective | Score |
|---|---|---|
| A | Methodology and statistics | **5 / 10** (borderline) |
| B | Significance for robot learning / active perception | **4 / 10** (borderline reject) |

---

## 0. Independent verification (shared by both reviewers)

### 0.1 Recomputed from raw jsonl

I wrote my own loader (v5 records for episodes 0–299 merged with v6 records, same rule as `analysis_v6.py::load`) and
recomputed the headline numbers directly from `results/v{5,6}/test5/*.jsonl`. Every method listed in the paper had all
500 episodes on 0–499 and all 200 on 300–499 in every cell (assertion passed).

| Quantity | Paper | Recomputed | Match |
|---|---|---|---|
| G\* run 1 / run 2 / R-125 / R-500 / student / BC student, success 0–499, S2 | 0.518 / 0.532 / 0.406 / 0.462 / 0.4988 / 0.4856 | identical | yes |
| Same, S4 | 0.496 / 0.494 / 0.402 / 0.390 / 0.4576 / 0.4492 | identical | yes |
| Same, S8 | 0.432 / 0.464 / 0.356 / 0.372 / 0.4188 / 0.4116 | identical | yes |
| Same, S12 | 0.434 / 0.434 / 0.358 / 0.390 / 0.4144 / 0.4140 | identical | yes |
| Same, A16-2 | 0.474 / 0.498 / 0.330 / 0.374 / 0.4832 / 0.4884 | identical | yes |
| H6a Δ 0–499 (S2…A16-2) | −0.0262 / −0.0374 / −0.0292 / −0.0196 / −0.0028 | identical | yes |
| H6a Δ 300–499 | −0.036 / −0.053 / −0.034 / −0.016 / +0.001 | identical | yes |
| H6b Δ, all 20 (both windows) | Table 2 | identical | yes |
| H6c Δ, all 10 | Table 3 | identical | yes |
| First-decision agreement G\* r2 vs r1, 0–499 / 300–499 | 0.274/0.402/0.452/0.426/0.314; 0.245/0.415/0.445/0.420/0.305 | identical | yes |
| ci95 of H6a / H6b (independent bootstrap, own RNG, B = 4,000) | Table 1 / Table 2 | within ±0.002 | yes |

Checked against the JSON: TOST p-values, ci90 bounds and upper-margin p (Table 1 footnote) match
`14_v6_analysis.json`; the A16-2 fresh "fails, p = 0.1557" is the upper-margin p; BI deltas and p-values (S4 p < 1e-4,
S8 0.0048, fresh 0.0206 / 0.0354) match; E12 per-cell contrasts, flip rates and the P1 shift CIs match
`18_posthoc_v6.json`; Table 4 epochs match `P3_checkpoint_epochs` cell by cell; S2 kept-regret ranges
(0.2803–0.2848 / 0.2776–0.2857) match; H5b slope −0.0070 per 100° [−0.137, 0.124] matches; latency medians and all
derived ratios (19–47×, 62–389×, 2,544–9,767×) follow from `frontier.latency_median_s`; heuristic margins
(+6.68/+8.96/+7.48/+5.64/+17.12 pp; best-heuristic +4.16/+5.08/+2.44; A16-2 +16.92) and the S12 tie R-500 = B-cov =
0.390 follow from the means. Episode counts per method (27 instances in S2/S12, 22 elsewhere) match
`episodes_per_method`. The statistical tests claimed (crossed episode × seed bootstrap, B = 10,000, TOST via shifted
bootstrap, Holm) are exactly those present in `code/touchbed/stats.py` and `code/analysis_v6.py`; no ANOVA/t-test is
claimed. The rules in Section 4 match amendment v6.0 (δ = 4 pp, Holm families, E12 report-only, fresh window, Random
not extended, P6 → 733 CPU-h ≤ 800 → no reduction).

### 0.2 Two reviewer-side post hoc checks (not in the paper; offered to the authors)

1. **H6b at B = 100,000** (frozen `crossed_bootstrap_diff`, seed 0): Holm still rejects **7/10**, same seven contrasts.
   S12 − R-125 p = 0.00968 against its Holm cut 0.0100 (rank 6); S4 − R-125 p = 0.0105 against 0.0125 (rank 7). So the
   registered 7/10 is not a bootstrap-seed artefact at higher resolution, but S12 − R-125 sits 0.3 thousandths from the
   cut-off.
2. **30 further bootstrap seeds (11–40), B = 10,000:** 7/10 under 26 seeds, 5/10 under 4. Together with the paper's
   P2 (10 of 11), the count falls to 5/10 under about 5 of 41 seeds (≈ 12 %). The paper's "within bootstrap error of
   the threshold" is an accurate description.

### 0.3 Methodology-evidence discrepancies found (none critical)

| # | Location | Paper says | Evidence | Severity |
|---|---|---|---|---|
| D1 | Abstract | "every method runs the same 500 test episodes, 200 fresh" | Random was not extended past 299 (amendment E8; paper §4 says so) | minor wording |
| D2 | Fig. 1 caption, §4, §5.1, Lim. 6 | latencies are "point medians without dispersion"; G\*/student "2,544–9,767×, post hoc, ratio of medians" | `results/v5/14_e6_analysis.json` holds the **registered** statistic, the median per-decision ratio with ci95: 9,933 [8,179, 10,224], 6,990, 3,463, 2,523 [2,068, 2,675], 8,301 [8,080, 8,472]. Dispersion exists for that ratio; the paper reports a different, unregistered ratio of medians instead | minor; report the registered ratio with its CI |
| D3 | Registered H6b phrase | "more accurate than a reduced planner" | amendment: "…than a reduced planner **of that latency**". The paper's narrower wording is more honest (no reduced planner is at the student's latency); one sentence noting the change is enough | cosmetic |
| D4 | Abstract | < 200 words required by triage item 6 | 240 words | triage not met |

No trial-count discrepancy: 500 / 200 episodes per method, 5 student / BC / RL seeds, 2 G\* runs, 1 run of each reduced
planner and heuristic, 100 episodes for E12 — all as in `episodes_per_method` and the E12 blocks.

### 0.4 Length

Section word counts (paper body, excluding Figure 1 prompt): Abstract 240, Introduction 1,103, Related Work 709,
Method 2,170, Experiments 1,334, Results 2,352, Discussion 1,194, Limitations 706, Conclusion 296, Appendices 449;
**total ≈ 10,550**. No section is under its minimum. The problem is the opposite: with 5 tables and a figure, this is
roughly 14–16 NeurIPS pages, not 9. Results and Discussion repeat each other (C1–C4 are stated in the abstract, in the
contribution list, in §5, in §6.2 and in §8, each time with the same qualifiers).

### 0.5 Topic

The paper stays on the registered topic throughout. Environment issues (time-guard stops, runner differences, resumed
jobs) appear only as disclosures and limitations, not as contributions. The C4 "methods note" is a legitimate part of
the registered design (E12, second G\* run), not a drift.

---

## Reviewer A — methodology and statistics (5 / 10)

### Strengths
1. **Exemplary pre-registration hygiene.** Amendment v6.0 and addendum v6.1 fix δ, the Holm families, both windows,
   E12 and the compute-reduction order before any run; the read-out script predates the first record (triage confirmed
   by commit order). Every number I checked is reproduced from raw jsonl exactly.
2. **The teacher is treated as a random variable.** Two independent G\* runs enter the parity contrast; first-decision
   agreement of 0.25–0.45 is a striking and useful number for anyone distilling Monte Carlo planners.
3. **Calibrated language.** The revision now distinguishes registered from post hoc results everywhere, reports the
   TOST as low-power by design, gives the deficit side of the ci90 as the certifiable margin, and states the H6b
   bootstrap-seed fragility in the abstract and C1.
4. **The ablation is reported with its recipe.** Table 4 and Algorithm 1 now make the warm-start / early-checkpoint
   behaviour visible, and C3 is correctly scoped to "this recipe".

### Weaknesses
1. **The positive claim rests on single runs of the comparators.** R-125 and R-500 were run once; G\*'s own runs differ
   by up to 3.2 pp, and the two marginal rejections (S4, S12 vs R-125) have lower bounds of +1.3–1.4 pp. The H6b CIs are
   therefore too narrow by an unknown amount. The paper says so, but it remains the main threat to C1.
2. **H6b is at the edge of its Holm cut.** My B = 100,000 rerun keeps 7/10 but S12 − R-125 lands at p = 0.00968 against
   0.0100. Combined with (1), the defensible headline is "5/10 robustly, 7/10 at the registered resolution". The paper
   comes close to this but still leads with 7/10.
3. **The two-run teacher bootstrap is degenerate.** Resampling two "seeds" with replacement draws the same run in half
   of the resamples. The paper acknowledges this (Lim. 1), but a simple sensitivity — the H6a interval with the G\*
   component held at the two-run mean, or against each run separately — is cheap analysis, not a new experiment, and
   would show how much the teacher term widens Table 1.
4. **Latency statistic (D2).** The registered E6 ratio with ci95 exists and should be reported; the half-width rule
   failing in 4/5 cells is about the CI width relative to the median, not about the absence of a CI.
5. **E12 does not cover the reduced planners,** so the one positive claim has no evaluator-sensitivity check, while the
   null claims do. This asymmetry should be stated in the C1 bullet, not only in §5.1 and Lim. 5.
6. **H6c null without a power statement.** The 95 % upper bounds (≤ 4.8 pp) are given, which is good; but the
   "no DAgger benefit detected" headline would be clearer with the minimum effect detectable at 80 % power.

### Actionable revisions
- A1. Report the registered E6 ratio (median per-decision ratio with ci95) beside or instead of the ratio of medians;
  drop "without dispersion" for that ratio.
- A2. Add the B = 100,000 H6b result as a post hoc line in Appendix B (it is pure re-analysis of frozen records and does
  not breach the refinement cap), and state S12 − R-125's distance from its cut.
- A3. Add a teacher-fixed sensitivity of H6a (student − each G\* run separately, already partly in Appendix A) to Table 1.
- A4. Fix D1 ("every method except Random").
- A5. State in C1 that H6b has no evaluator check.

---

## Reviewer B — significance for robot learning and active perception (4 / 10)

### Strengths
1. A clear, practitioner-facing question (distil or shrink?), answered with honest uncertainty.
2. The methods lesson (C4) — that a thresholded grid read-out and teacher Monte Carlo noise each move few-pp contrasts by
   about the size of a typical equivalence margin — is transferable to other amortized information-gathering work.
3. Related work is adequate in breadth (tactile localization, greedy/submodular information gathering, amortized BOED,
   imitation of information-gathering experts), and positions the paper as a measurement, not a method.

### Weaknesses
1. **Limited novelty and significance.** Distilling an expensive planner into a fast network is standard, and that it is
   much faster is expected by construction. The only registered positive result is that the student beats two reduced
   planners that are themselves 62–389× slower than it; nothing sits near the student's latency except heuristics and an
   RL policy tuned once on S2. The interesting frontier question — student vs. a planner at comparable latency
   (candidate subsampling, an accelerated G\*, a cheap information heuristic) — is untested.
2. **Parity is a designed-in null.** The paper admits the TOST had little power, so the headline about the teacher
   relation is "undecided, deficits up to 5–8 pp not excluded". BI shows a significant exploratory deficit in S4 and S8.
   For a top venue this is a weak scientific yield for the main hypothesis family.
3. **Narrow scope.** Planar simulation, one finger on a fixed circle, a likelihood shared by planner, filter and
   evaluator, 3–4 probes per episode, no task-time model, no hardware. The short horizon is also the most plausible
   reason the DAgger ablation is null, which makes C3 uninformative about DAgger in realistic horizons.
4. **The paper is far too long and repetitive** (≈ 10,550 words). Every claim is stated with full qualifiers four or five
   times. A 9-page version needs roughly a 40 % cut; the qualifier lists should live once, in §7.
5. **Missing references remain:** three [CITE-MISSING] markers (DeepSets, Efron bootstrap, Holm) — trivial to fill.
6. **Figure 1 is still a prompt,** not a figure; the data panels must be plotted before submission.

### Would I recommend acceptance at NeurIPS/ICML?
Not in this form. It is a careful, honest, reproducible negative-leaning measurement study with one fragile positive
contrast. Its natural home is a workshop on robot learning evaluation or a reproducibility/benchmarking track, or a
main-track paper once a comparator near the student's latency and repeated reduced-planner runs are added.

### Actionable revisions
- B1. Cut to 9 pages: one statement of each claim with qualifiers, move Table 4, Appendix A and the heuristic/RL detail
  to the supplement.
- B2. Abstract ≤ 200 words.
- B3. Fill the three citations; render Figure 1 from the JSON.
- B4. (Evidence-level, owner decision) one comparator at sub-10 ms latency and a second run of each reduced planner;
  these would turn C1 from "beats two slow planners" into a frontier statement.

---

## Triage status (items of `paper/mypaper/18_peer_review.md`)

| # | Triage item | Status | Evidence in the revised draft |
|---|---|---|---|
| 1 | H6b fragility and fresh window up front; single-run, same-budget planners | **Fixed** | Abstract ("7/10 contrasts; 5/10 under one of 11 bootstrap seeds… fresh 2/10… single-run, same-budget"); C1 bullet; §5.1 "How fragile the count is"; Appendix B |
| 2 | C3 softened; warm start and kept epochs disclosed | **Fixed** | Algorithm 1 step 3 (warm start bold), step 2 (lowest-R̄ checkpoint); §3.3 qualifiers; Table 4 (matches P3 exactly); C3 "No DAgger benefit detected under this recipe" |
| 3 | C4 with uncertainty (P1 ci95; only S12 excludes 0) | **Fixed** | C4 bullet, §6.1 with all five P1 CIs, abstract "post hoc ci95 excludes 0 in one cell", Lim. 5 |
| 4 | TOST power framing, no "500 sufficed" | **Fixed** | §4 "Power" paragraph (half-widths 2.84–3.85 pp, derived correctly from Table 1 ci90); §6.2; Lim. 11. No sufficiency statement remains |
| 5 | "5–8 pp"; S12 tie; "0.15–1.16 pp" unadjusted; define TouchBED | **Fixed** | "5–8 pp" in abstract, C2, §5.2, §6.2, §8 (ci95 lower bounds −5.0 to −7.8 pp); S12 tie disclosed in §5.1; "Unadjusted" before 0.15–1.16 pp in §4 and §5.2; TouchBED defined in §1 ¶4 and §3.1 |
| 6 | History narrative cut to one sentence; abstract < 200 words; keep 3 CITE-MISSING; Fig. 1 for stage 22 | **Partly fixed** | History: one sentence in §1, rest in Appendix A (fixed). **Abstract is 240 words (not fixed).** CITE-MISSING kept (3, as intended). Figure 1 still a prompt (deferred, as intended) |
| 7 | Limitations: no comparator near student latency; single-run planners; no task-time/hardware; G\* 2 runs; bootstrap-seed sensitivity | **Fixed** | Lim. 4, 2, 6, 1, 3 respectively |

Evidence-level requests of the triage (comparators near the student's latency, reduced-planner reruns, G\* runs 3–4,
E12 on reduced planners, alternative DAgger checkpoints, task-time model) remain open and are correctly listed in
Lim. 15 and the conclusion. Note that A2 and A3 above are re-analyses of frozen records, not new experiments.

## Top remaining actions (priority order)

1. Cut the paper to 9 pages (≈ 10,550 → ≈ 6,000 words of body text) and the abstract to ≤ 200 words.
2. Report the registered E6 latency ratio with its ci95 (D2) and fix "every method" in the abstract (D1).
3. Add the B = 100,000 H6b check (7/10; S12 − R-125 p = 0.00968 vs cut 0.0100) to Appendix B, and note in C1 that H6b
   has no evaluator check.
4. Add a teacher-fixed sensitivity of H6a (contrast against each G\* run) to quantify the two-run bootstrap problem.
5. Fill the three [CITE-MISSING] references and render Figure 1 from the JSON; evidence-level items (a comparator near
   the student's latency, reduced-planner reruns) remain the path to a stronger venue.
