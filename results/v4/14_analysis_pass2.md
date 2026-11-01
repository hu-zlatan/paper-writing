# Stage 14 · Adversarial pass (pass 2, v4)

> System: "You are a top-conference area chair who has rejected 80% of papers you've reviewed this cycle. Read the
> analysis below. Identify every claim that is not strictly supported by the cited numbers. For each, output the
> unsupported claim, the contradicting/missing evidence, and a one-sentence rewrite that *is* supported."

**What was checked.**
- Target: `results/v4/14_analysis_pass1.md`.
- Every v4 number was checked against `results/v4/results_v4.json`. Its values are identical to the data block in
  `results/v4/prompts/stage14_pass1_user.txt`.
- Every v3 number was checked against `results/v3/results_v3.json` and `results/v3/14_analysis.md`.
- Rules were checked against `docs/07c_amendment_v4_0.md`.
- Statistics were checked against the code: `code/touchbed/stats.py`, `code/analysis_d4_v4.py`,
  `code/analysis_s2_v4.py` and `code/analysis_e5_v4.py`.

**Pass-2 checks on per-episode files.** These are marked *(pass-2 check)* below. They are not in the data block, so
they should be cited by file, not as `results_v4.json` keys.
- (a) **G\*/student per-episode travel and actions**, from `results/v4/test3/S_k2_{gstar,student_s60x}_*.jsonl`
  (episodes 0–299, no-grid).
- (b) **B-fan action sequences**: v4 `results/v4/test3/S_k2_b_fan_*` compared with v3
  `results/v3/test3_sub8/S_k12_b_fan_*`.
- (c) **RL probe counts**, from `results/v4/test3/S_k2_rl_s61x_*`.
- (d) **g125 vs v3 B-fan**: pass 1's per-episode comparison, rerun from the same files. It reproduces 230/300 success
  agreements, 108 vs 108 successes and 1/300 BI matches.

**Arithmetic.** All of pass 1's arithmetic reproduces:
- D4 threshold −0.0146379, the 0.61 SE shortfall, and Φ(0.671) ≈ 0.75;
- the 21 % gap share, the RL training SD 0.181, the H2 half-widths 0.293 / 0.307, and the test3 SE ≈ 3.1 pp;
- all 10 + 12 point diffs, and which intervals exclude 0.

The problems are in interpretation and in what is compared with what.

---

## Serious

### S1. The student vs B-fan contrast across cells misstates S12, and "first such evidence" is wrong

**Unsupported claims.**
- §2.3: "**In S12 it did not** (`v3:14_m4_analysis.exploratory_b_fan`): success +2.2 pp, ci95 [−2.8, +7.3]; BI
  +0.226."
- §2.3: "This is the first such evidence in the record, and the most useful positive v4 row".
- §2.3: "S2 is a cell where not travelling is costly, and there the distilled student is measurably better than a
  no-learning heuristic."
- §5 (ii): "In S12 it was not separable from B-fan (+2.2 pp, ci95 [−2.8, +7.3])."

**Evidence.**
- The same v3 block gives `student-b_fan:ball_info` = +0.2263 with ci95 **[+0.1412, +0.3110]**, which excludes 0. In
  S12 the student was already measurably above B-fan on BI. Pass 1 quotes the +0.226 but leaves out its interval, so
  the reader is led to think nothing separated.
- What S2 adds is a success interval that excludes 0: +8.1 pp, ci95 [+1.7, +14.7].
  - That interval has the smallest margin of the S2 block (LB +1.7 pp). Pass 1 itself (§3.4) calls it at risk under 22
    uncorrected intervals.
  - No paired or cross-cell test of 8.1 vs 2.2 pp exists. The cells' G\* success also differs: 0.553 vs 0.427.
- "Not travelling is costly" rests only on B-fan − G\* being −18.3 pp vs −6.7 pp across cells, which is an untested
  cross-cell comparison.

**Supported rewrite.** "On S2 test3 the student exceeds B-fan on success (+8.1 pp, ci95 [+1.7, +14.7]) and BI (+0.53,
ci95 [+0.42, +0.64]); in S12 it exceeded B-fan on BI (+0.23, ci95 [+0.14, +0.31]) but not on success (+2.2 pp, ci95
[−2.8, +7.3]), so S2 adds a success separation, exploratory, uncorrected and untested across cells."

### S2. The mechanism for G\*'s lead over RL is asserted but contradicted by the travel numbers

**Unsupported claim** (§2.2, under the heading "RL lead over G\* fits RL's travel pattern"): "Where travel matters, the
RL policy, which always stops at 3 probes and travels 2.9× as far as G\* (derived: 136.8 / 46.9), loses more ground on
success."

**Evidence.**
- **"Loses more ground" is not tested.** G\* − RL is +13.0 pp, ci95 [+6.4, +19.4], in S2 against +7.0 pp, ci95 [+0.2,
  +13.7], in S12. The intervals overlap over 6.4–13.7 pp, and no cross-cell test exists.
- **The travel ratio is not specific to S2.**
  - In S12, RL already travelled 23.0 / 25.8 / 25.7° per seed against G\*'s 6.13°. That is about **4.0×** (derived:
    mean 24.81 / 6.13), which is more than S2's 2.9×.
  - RL ends at 3 probes in both cells. In v3 the probe histograms were all 3; in v4 every one of 900 test3 episodes has 3
    probes *(pass-2 check c)*.
- So neither "travels more" nor "stops at 3" separates the cells. No ablation identifies the cause. (The heading also
  reverses the sign; see m1.)

**Supported rewrite.** "G\* − RL success is +13.0 pp (ci95 [+6.4, +19.4]) in S2 and +7.0 pp (ci95 [+0.2, +13.7]) in
S12; RL ends at 3 probes and travels several times G\*'s distance in both cells (2.9× in S2, about 4× in S12), so the
record does not identify why the gap differs, and no cross-cell test of it exists."

### S3. "The student imitates the travel" rests on one mean, and the per-episode data contradict close imitation

**Unsupported claims.**
- §2.1.1: "The student follows it: 39.1°, or 83 % of G\*'s travel … In S2, then, distillation imitates a moving policy."
- §5 (i): "the student imitates the travel (39.1°)".

**Evidence.**
- **The cited number is one population mean.** Matching mean travel does not show that the student moves when and where
  G\* moves.
- **Per-episode data, test3 0–299 no-grid** *(pass-2 check a)*:

  | Seed | Pearson r of travel with G\* | First action identical to G\*'s | Full action sequence identical |
  |---|---|---|---|
  | 601 | 0.16 | 40 % of episodes | 0 of 300 |
  | 602 | 0.24 | 32 % of episodes | 0 of 300 |
  | 603 | 0.14 | 34 % of episodes | 0 of 300 |

- **What the student does show:** it travels a G\*-like *amount*, with per-seed medians 36–41° against G\*'s 46.5°.
- **What it does not show:** tracking of G\*'s episode-level travel decisions.

**Supported rewrite.** "In S2 the student travels a similar amount to G\* on average (39.1° vs 46.9° per episode, test3
0–299), unlike S12 (1.5–2.1° vs 6.1°), but its per-episode travel is only weakly correlated with G\*'s (r 0.14–0.24 by
seed), so S2 shows the student is not confined to stay-and-probe, not that it reproduces G\*'s travel decisions."

---

## Moderate

### M1. Saying "g_T ranks G\* below both learned policies in both cells" overstates the S12 evidence

**Unsupported claims.**
- §5 (iii): "g_T ranks G\* below both learned policies in both cells."
- §2.2: "In v3 S12, g_T(G\*) 5.299 was also below both learned policies (5.368 each)".

**Evidence.**
- **The S12 margin is small and has no interval.** It is 0.069 nats (derived: 5.368 − 5.299), with no interval for
  G\* − learner g_T in either cell.
- **The S12 per-seed values straddle G\*.**
  - Learner seeds below g_T(G\*) 5.299 (`v3:14_h2_analysis.per_seed_*`): student 501 (5.279), RL 512 (5.271) and RL 513
    (5.178). That is 3 of the 6 learner seeds.
  - RL's per-seed SD is 0.253 (`v3:14_derived`), 3.7× the margin.
- **S2 has no per-seed g_T** (pass 1 says so itself, §1.4). The S2 ordering rests on point means only. RL − G\* is 0.58
  nats and student − G\* is 0.14 nats.

**Supported rewrite.** "On seed-averaged point estimates g_T(G\*) is below both learned policies in S2 (5.40 vs 5.53 /
5.98) and marginally in S12 (5.30 vs 5.37, with 3 of 6 S12 learner seeds below G\*); no interval exists for these
contrasts."

### M2. A reverse-direction g_T verdict is stated, while pass 1 itself says a test is still needed

**Unsupported claims.**
- §2.2: "RL scores higher than the student on its own training objective by 0.445 nats."
- §5 H2 row: "UB −0.162 < 0, i.e. RL scores higher on its own objective".
- §5 (iii): "On g_T, RL's own objective, RL is ahead".

**Evidence.**
- **Pass 1 contradicts itself.** §3.5 item 2 says a one-sided test is required "for any sentence claiming that RL wins
  on g_T" and that this is "currently only implied by the bootstrap UB". Yet §2.2 and §5 make that claim.
- **The statistic exists but is not a pre-registered test.** In `stats.py`, `upper` is the 95 % one-sided bound and
  `p_less` = mean(boot ≥ 0) = 0.0064, so a one-sided crossed-bootstrap statistic for RL > student does exist. It was not
  pre-registered (07c defines only the student > RL + 0.10 direction).
- **The wording collides with the verdict.** "RL scores higher on its own objective" mirrors the pre-registered verdict
  phrase ("distillation scores higher on RL's own objective") and reads as a verdict.

**Supported rewrite.** "H2-S2 is not detected (LB −0.749 ≤ +0.10); in exploratory terms the crossed-bootstrap point
estimate favours RL by 0.445 nats on g_T (one-sided 95 % UB of student − RL −0.162, bootstrap p 0.0064, not
pre-registered)."

### M3. Explanation (c) for the val3/test3 gap is presented as seed-specific, but every seed's gap widens

**Unsupported claim** (§3.3 (c)): "a seed-specific effect: seed 602 drops from −2.8 pp on val3 to −14.0 pp on test3",
together with §2.5: "Seed 602 is the outlier on test3".

**Evidence.**
- **Every seed widens.** Per-seed student − G\* success from val3 (`12_d4_analysis.succ.per_seed`) to test3 (derived
  from `test3_sub8.rows.student.per_seed_success` − 0.5533):

  | Seed | val3 | test3 | Change |
  |---|---|---|---|
  | 601 | −3.6 pp | −9.0 pp | −5.4 pp |
  | 602 | −2.8 pp | −14.0 pp | −11.2 pp |
  | 603 | −2.0 pp | −7.7 pp | −5.7 pp |

  Even excluding 602, the gap widens by more than 5 pp per seed. A seed-specific effect can therefore explain at most
  part of the 7.4 pp change.
- **Both rows move.** G\* success rises (0.514 → 0.553) and student success falls (0.486 → 0.451). Pass 1's table shows
  this but does not discuss it.
- **"Outlier" is not supported.** Seed 602 is 5.0–6.3 pp below the other two seeds at n = 300 per seed (binomial SE
  ≈ 2.9 pp per seed, derived). With 3 seeds, "outlier" has no basis.

**Supported rewrite.** "The test3 gap is wider than the val3 gap for every seed (by 5.4, 11.2 and 5.7 pp), and both the
G\* (+3.9 pp) and student (−3.5 pp) rows move, so the discrepancy is not confined to seed 602; its cause is untested."

---

## Minor

### m1. The section heading reverses the sign

**Claim** (§2.2 heading): "**RL lead over G\* fits RL's travel pattern.**"

**Evidence.** G\* leads RL: G\* − RL = +13.0 pp.

**Rewrite.** Retitle it "G\*'s lead over RL", and use the S2 rewrite for the body.

### m2. "In S2 the BI deficit excludes 0" does not say which split

**Claim** (§2.1.4): "In S2 the BI deficit excludes 0."

**Evidence.**
- The statement is true only for test3 (ci95 [−0.269, −0.094]).
- val3 has a bootstrap SE (0.0386) but no interval.

**Rewrite.** "On S2 test3 the student − G\* BI ci95 [−0.269, −0.094] excludes 0; on val3 the deficit is −0.105 (SE
0.039), with no interval computed."

### m3. The v3 and v4 behaviour comparisons mix episode ranges, and one range is rounded

**Claims.**
- §1.6 and §2.1.1: "G\* travels 46.9° per episode on test3, against 6.1° in S12".
- "In S12 the student travelled about 1.5–2.0°".

**Evidence.**
- The v4 behaviour block is test3 0–299, whereas the v3 G\*, student and random travel figures are n = 500 (0–499).
- v3 student seed 502 travelled 2.05°.

**Rewrite.** "G\* travels 46.9° per episode on S2 test3 0–299 against 6.1° on S12 test3 0–499; the S12 students
travelled 1.5–2.1°."

### m4. "Identical B-fan travel … is expected" gives an incomplete reason

**Claim** (§2.3): "B-fan is belief-free, and its actions do not depend on κ."

**Evidence.**
- B-fan's allowed mask uses the budget reservation `c(a) ≤ τ_rem − max(0, n* − t − 1)`
  (`code/touchbed/heuristics.py`), and τ differs between cells: 4.9 in S12, 4.7 in S2. Identity is therefore not
  guaranteed a priori.
- It is an empirical fact: all 300 action sequences are identical across the two cells *(pass-2 check b)*.

**Rewrite.** "B-fan's 300 action sequences are identical in S12 and S2 (belief-free, and the τ difference never changed
an allowed action), so the cells differ only in how those actions are scored (success 0.36 vs 0.37, BI 5.973 vs
5.962)."

### m5. The H2 robustness remark cites noise that is not in the data

**Claim** (§3.2): "No plausible change of instrument noise would reverse a non-detection."

**Evidence.** The record contains no estimate of g_T instrument noise (fixed J 16 / L 4,095 draws). The available
quantity is the bootstrap width.

**Rewrite.** "The LB (−0.749) is 0.85 nats below the threshold, about 2.9 one-sided half-widths (0.293), so the
non-detection is not near the margin."

### m6. The val3/test3 difference in SE units is rounded down, and the bias of the approximation is not named

**Claim** (§3.3): "the difference is about 1.9 combined SE … That is borderline".

**Evidence.**
- The value is 7.42 / √(2.18² + 3.12²) = 1.95, i.e. about 2.0 (derived).
- Shared students imply a positive covariance between the splits. The independence SE is therefore an *over*-estimate,
  which biases z toward 0.

**Rewrite.** "About 2.0 combined SE under independence, which is conservative given the shared students; untested and
not pre-registered."

### m7. The statistics note is imprecise about which quantiles apply

**Claim** (Scope): "Every interval comes from the paired crossed bootstrap … `lower`/`upper` = 5 % / 95 % quantiles"; and
"For D4 the SE is the SD of that bootstrap".

**Evidence.**
- 5 % / 95 % applies to H2 only. The ci95 contrasts call `crossed_bootstrap_diff(..., alpha=0.025)`, which gives 2.5 % /
  97.5 % (`analysis_s2_v4.py`).
- D4 uses its own `boot_sd` in `analysis_d4_v4.py`. It resamples episodes and student seeds and treats G\* as a single
  run.

**Rewrite.** "H2 bounds are the 5 % / 95 % crossed-bootstrap quantiles; ci95 contrasts are the 2.5 % / 97.5 % quantiles;
the D4 SE is the SD of an analogous episode × student-seed bootstrap in `analysis_d4_v4.py`."

### m8. The anomaly 2 statement does not match the flags

**Claim** (§3.2): "every v4 analysis block reports `complete: true` with the planned n, except the random row."

**Evidence.**
- `test3_sub8.complete` is `true` even though the block includes random n = 190: the code excludes random from the
  completeness set (`skip=("random",)`).
- `behaviour` and `students_S2_training` carry no `complete` flag.

**Rewrite.** "The D4, test3, H2 and E5 blocks report `complete: true` with the planned n (test3 completeness excludes
the random anchor, n = 190 of 300); the behaviour and training blocks carry no completeness flag."

### m9. "Agreement with the v3 pilot" compares different splits

**Claim** (§2.4): "These complete n = 300 rows sit close to the incomplete pilot3 rows".

**Evidence.**
- pilot3 and test3 are different episode sets, so nothing is paired.
- The success values differ by −2.2 pp (g125) and −1.3 pp (g500), and the latencies are 14 % and 4 % higher.

**Rewrite.** "On a different split (pilot3, n = 186 / 177, incomplete) the same configurations scored 0.382 / 0.390
success at 18.2 / 44.1 ms, against 0.360 / 0.377 at 20.8 / 46.0 ms here; unpaired."

---

## Pre-registered verdicts pass 1 may have got wrong

None.
- **D4 = FAIL** is correct: −0.0280 < −0.01464, which fails clause (i), while clauses (ii) and (iii) pass.
- **H2-S2 = not detected** is correct: LB −0.749 ≤ +0.10.
- **E5** is reported without a verdict, as required.
- **v3 verdicts** are unchanged, as required.

The problems are confined to the exploratory readings: S1–S3, M1–M3 and m1–m9.
