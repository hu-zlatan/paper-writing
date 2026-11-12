# Stage 18 peer review (v4 draft, run 2): independent reviewer pair (RSS lens)

**Inputs read:** `prompts/stage18_v4_system.txt` (role), `prompts/stage18_v4_user.txt` (all 7,560 lines: task, draft v4, evidence blocks (a) v1 results, (a4) `results/v4/v4_analysis.json`, (a5) `results/v3/a7_integrated.json`, (b) log, (c) stats grep, (d) pointers); `docs/11_amendment_v4.md` and its git history; `code/analysis_v4.py`, `code/analysis_crc.py` (`lam_index`), `code/analysis_v3_a.py` (bootstrap, re-splits), `code/crc_grids_11.py`, `code/certgrip/{sim,baselines,data}.py`, `code/h3_streams.py`, `code/requirements.txt`; `docs/08b_preregistration.md`; `results/v1/{h1m_analysis,19_report_rows,sec08g,h3_analysis,comp_selection,crc_analysis}.json`, `results/v2/b_analysis_edge.json`, `results/v3/{a_analysis,a_analysis_08e,a3_holm,b1_analysis,b2_analysis,b3_analysis,a7_integrated}.json`, `results/v4/crc_grids_11_c4.json`; git log of the v4 commits.
**Recomputed (scripts in `/tmp/rev2/`, no repository file touched):** (1) all v4 arm operating points (slip, RE, matched RE, hold force, per-stratum λ̂ index) on `f4` and `c4` from the raw replays `results/v4/crc_{f4,c4,np}/*.jsonl` with an independently written CRC λ̂ routine; (2) point values of C1–C5, S1 (σ 0.1 / 0.4), S3 width sweep (all four w, object counts), S6 no-probe slip / hold force / λ̂; (3) the 2,000-draw object-cluster bootstrap (seed 2027) for C1, C2 and the CRC-route C2 row, including both p-values; (4) the CSF-fam μ̄ values from the `c4` selection labels; (5) a number search of every earlier-round figure quoted in Sections 1, 3, 4, 5.3–5.5 against `results/v1–v3/*.json`; (6) section word counts; (7) cite-key presence in `docs/0{2,3,4,5}_*`; (8) commit order amendment → code → read-out → labels → replays.

---

## 0. Joint pre-review checks (both reviewers agree on these facts)

### 0.1 Topic adherence
The paper stays on the registered topic: a ramp-down friction-onset probe, per-stratum CRC on the physical binary slip loss, comparison against the strongest friction-blind conformal baseline (CSF-1, selected on a disjoint split), an attribution test locating the saving in the probe rather than the learner (C2, S1, feature chain), and an online binary-feedback study under three shifts. No section drifts to an unrelated topic and no environment problem is presented as a contribution.
One presentation problem comes close: the text is full of pipeline language that belongs in a lab notebook, not a paper: "every v4 row has `edge: false`, which we take, per the read-out code's flag", "first-round / later-round / earlier rounds", "read-out code committed before any v4 replay and run once", seven numbered "Deviations". The content is honest, but at RSS it reads as process logging rather than as part of the scientific argument.

### 0.2 Methodology-evidence consistency (verified against code and raw results)

**Matches (verified exactly):**
| Paper claim | Evidence | Status |
|---|---|---|
| C1 0.4314 [0.3824, 0.4835]; C2 0.01117 [−0.05552, 0.05686]; C3 0.4135 [0.3578, 0.4903]; C4 −0.5814 [−0.7208, −0.4563]; C5 −0.5461 [−0.6590, −0.4290] | `v4_analysis.json`; my independent CRC recomputation reproduces every point to machine precision; my rerun of the 2,000-draw bootstrap reproduces the C1/C2 CI** and p exactly | ✔ |
| 500 cal / 700 test objects per pool, 2,800 test instances, 2,000 valid draws | grids and labels: 4,800 instances per pool, 0 missing / 0 duplicate replays; `valid_draws` 2000 on every row | ✔ |
| `edge: false` on every v4 row, i.e. no λ̂ at index 0 or 80 | code `edge |= j in (0, J-1)`; recomputed λ̂ indices are 38–42 for every arm and stratum, so the ±8 matched-slip shifts are never clipped either | ✔ |
| Holm over five p; Table 1 caption "p = 0.0 means < 0.001 (TOST < 0.0005)" | `analysis_v4.py` `holm()`, `p_two`, `p_tost`; 2,000 draws ⇒ resolution 1/2000 | ✔ |
| CSF-fam μ̄ F1 0.379, F2 0.496, F3 0.677, F4 0.852 from 50 selection objects/family | recomputed 0.3790 / 0.4965 / 0.6768 / 0.8523 (n = 50 each); same values in `crc_grids_11_c4.json` | ✔ |
| Shrunk plug-in a −0.3858, b 0.7397 frozen | amendment and `crc_grids_10e.json` | ✔ |
| S1 σ band, S2, S3 sweep (windows, 386/532, 262/361, 134/179 objects), S6 phases (13.08 / 12.91 / 1.444 / 0.348 / 3.27 N·s), break-even 17.74 / 27.07 s, S7 re-split statistics, S4 per-family slips | `v4_analysis.json`; S3 and S6 recomputed | ✔ |
| Pre-registration order | amendment commit 29b05b0 15:08:45 → first v4 code 15:11 → `analysis_v4.py` 9a67492 15:18 (only commit touching it) → labels / grids 15:27 → first replay 15:54 → read-out d7a197f 20:02; amendment later received only an appended status note | ✔ |
| Earlier-round numbers (0.7686 / 0.8294 / 0.8335; 0.1597 N; 8/800, CP 0.02115, 7 of 8 in D2; η 0.03412; H2a 0.4168 [0.3484, 0.4778] and seeds 0.4343/0.4197/0.3932/0.4494; H2b 0.0569 [−0.0399, 0.1454]; −0.0534; −0.0263; 0.4739; −0.0299; tuned-margin 0.06571 / 0.4843; reactive ≥ 0.3086, 0.9921 / 0.9514; H2-R −0.2614 [−0.5320, −0.0325], Holm 0.03 / 0.12 over 52; −0.3152 / +0.3754; −0.1395 [·, −0.01264]; all of Table 3) | located in `results/v1–v3/*.json` | ✔ |
| Streams T = 2,000, shift from step 501, 20 orderings | `h3_streams.py`: T_PRE 500, T_SHIFT 1500, N_ORD 20 | ✔ |
| Bonferroni over 4 (first round) | `08b_preregistration.md` §4 | ✔ |
| MuJoCo 4.0.0 | `code/requirements.txt` | ✔ |
| All 55 cite keys | present in the literature records of `docs/` | ✔ (existence of the works not checked here) |

**Discrepancies (the paper says something the evidence does not support, or describes it differently):**

| # | Severity | Paper says | Evidence shows |
|---|---|---|---|
| E1 | **Moderate (factual error)** | §5.1: "CSF-fam reaches matched RE 0.2674 at slip 0.05929." | Matched RE is by definition interpolated at test slip **0.10** (`SLIP_MATCH = 0.10`). 0.05929 is CSF-fam's slip at its *CRC* operating point, where its RE is **0.2995**, not 0.2674. The sentence attaches one route's RE to the other route's slip. |
| E2 | **Moderate (route mixing in a figure)** | Fig. 2a: "plug-in 0.6486 / 0.4314 / −0.2065; learned 0.5683 / 0.4135 / 0.1675" as one noise curve. | The plug-in values are **matched-slip** D vs CSF-1 (S1_C1); the learned values are **CRC-route** D vs CSF-1 (S1_C3). Plotting them together compares two different estimands. My matched-route recomputation for the learned arm, from the same file's `RE_match`: 0.611 (σ 0.1), 0.438 (σ 0.2), **0.184 (σ 0.4)**. |
| E3 | **Moderate (overclaim)** | Abstract "the saving reverses … at high probe noise (−0.2065)"; §6 "The saving disappears … at σ 0.4"; §7 "the saving reverses at σ 0.4"; §6 "a learned model is not needed". | Only the **plug-in** reverses at σ 0.4. The learned arm keeps a significant saving vs CSF-1 (CRC 0.1675 [0.1064, 0.2560]; matched ≈ 0.184) and beats the plug-in by **0.3238 [0.2778, 0.3817]**. The paper's own §5.2 says so, but the abstract, discussion and conclusion generalise a plug-in result to "the saving". "The probe, not the learner, carries the saving" holds at σ 0.2 only; at σ 0.1 the learner is worse (−0.1076) and at σ 0.4 it is needed. |
| E4 | Minor (rule misdescribed) | §4: "superiority if the CI\*\* lower limit exceeds 0". | The registered and coded rule is: **Holm-adjusted bootstrap p < 0.05 and point > 0** (`analysis_v4.py` docstring and `dec` block; amendment §Confirmatory). The verdicts are the same here (all p = 0), but the rule as written is not the one that was registered. |
| E5 | Minor (inconsistent criterion) | §5.1 / Table 1: CRC-route C2 "−0.06291 [−0.1226, 0.08396], equivalence not shown". | The same row in the file has **TOST p = 0.037** (unadjusted), which passes a 5 % TOST. The paper uses the 97.5 % CI for this row and the TOST p for S1_C2@0.1 (0.5445). Use one criterion. The conservative reading is defensible, but it should be stated as the criterion. |
| E6 | Minor (wording) | §5.2 "Measured break-even"; Fig. 2c "measured at three T". | `analysis_v4.py` computes force-time from the **commanded** profile in closed form (preload F₀·0.4 = 13.08, re-hold F₀·0.1 = 3.27 exactly; hold = F·T; break-even = gap / ΔF). Only the no-probe slip and λ̂ come from a replay. Also, no hold longer than the 0.6 s disturbance window is simulated, so slip ≤ α over a 17–27 s hold is **not** evidenced. Limit (8) mentions the commanded profiles, but the "measured" label remains. |
| E7 | Minor (scope of a quoted sub-pool) | Table 2 / §5.4: "Mid-friction sub-pool μ ∈ [0.5, 0.8] … refined CRC −0.3152, primary +0.3754"; Abstract: "in a narrow mid-friction band the baseline was better in earlier rounds". | In `v3/a_analysis*.json` the row is `sub:mu_and_amp` (μ ∈ [0.5, 0.8] **and** mid-half amplitude), and the arm is the **learned** model (`full_vs_CSF-1`), which the table does not name. The primary-grid value has the opposite sign (+0.3754), so the abstract's flat statement that "the baseline was better" overstates a grid-dependent result. |
| E8 | Minor (route mixing in the feature chain) | §5.4 feature chain: "adding the onset gives D 0.4739 …, full vs onset-only −0.0534, squeeze −0.0263". | 0.4739 and −0.0263 come from `h4a_label_rule.json` (label route); −0.0534 comes from `crc_analysis.json` (CRC route). The routes are not stated. |
| E9 | Minor (statistical phrasing) | C2: "the two-sided p of 0.915 is consistent with equivalence". | A non-significant difference test is not evidence of equivalence. The evidence is the TOST p (< 0.0005). Drop the 0.915 sentence or reword it. |
| E10 | Minor (unstated assumptions) | §3.3 formulae use m; §3.4 calibrates per stratum. | `baselines.py` uses the **true mass** for every arm (the plug-in's m cancels except through the μ̂ clip), and λ̂ is selected **by known disturbance stratum**. Both are deployment assumptions the paper never states. The pool draws m **log-uniform** (`data.py`), not just "on [0.05, 1.0]". |
| E11 | Trivial | Table 3 family-shift frozen probe slip 0.1017. | The file has 0.10165 (a rounding-boundary value; 0.1016 is the nearer printed value). |

**Trial count check (item 3).** I found **no fabricated trial count**. Every count in the paper matches the evidence: 700 fresh test objects / 2,800 instances; 500 calibration objects; 2,000 bootstrap draws (all valid); 200 re-splits (`R: 200`, seed 3031); 20 orderings; first-round seeds 1–4. One caveat: every v4 learned arm is the single frozen seed-0 fit (`full_rd@σ#0`). The paper does not claim otherwise, but it also never says that C2, C3 and C5 rest on **one** trained model, while the first round shows a seed spread of 0.39–0.45 on C3 and 15.2–18.0 s on the probe-phase break-even (`v3/a7_integrated.json`). This must be stated.
**CRITICAL FABRICATION flags: none.**

### 0.3 Length check (item 4)
| Section | Words | Threshold | Flag |
|---|---|---|---|
| Abstract | 198 | ≥ 150 | ok |
| 1 Introduction | 441 | ≥ 700 | **short** |
| 2 Related Work | 298 | ≥ 500 | **short** |
| 3 Method | 814 | ≥ 800 | ok (barely; counts the algorithm block) |
| 4 Experimental Setup | 397 | ≥ 600 | **short** |
| 5 Results | 2,217 | ≥ 500 | ok (table-heavy) |
| 6 Limitations + 7 Conclusion | 331 + 91 | — | — |
| **Total** | ≈ 4,805 | ≥ 4,000 | not critically under-length |

For RSS (8 pages plus references) the total is about right. The density is the problem: Sections 1, 2 and 4 are compressed lists of numbers and citations, while Results carries most of the prose. Neither figure exists as an image: Figure 1 is a generation prompt and Figure 2 has only a caption.

---

## Reviewer A (robotics systems and grasping; RSS area chair perspective)

**Summary.** The paper asks when a short tactile probe (a ramp-down from a fixed 32.7 N preload until a modelled touch detector flags incipient slip) makes a conformal physical-slip bound cheaper in hold force. In MuJoCo, with friction independent of appearance and onset noise σ = 0.2 assumed, a Coulomb plug-in on the onset, calibrated by per-stratum CRC, needs about 43 % less relative excess hold force than the best friction-blind conformal rule (6.46 N vs 7.13 N mean). A learned model adds nothing at σ 0.2. The saving vanishes when friction is predictable from the object family, for the plug-in at σ 0.4, as the friction range narrows, and for holds shorter than about 18–27 s.

**Strengths.**
1. The framing is unusually honest for this area. The paper's headline result includes its negative boundary conditions (family prior wins; break-even ≥ 17.7 s; σ 0.4 reversal), and the limitations section is concrete.
2. The comparator is chosen properly: CSF-1 was selected on a disjoint split against a Mondrian variant and a learned proprioceptive model, so the tactile gain is not measured against a straw man.
3. The confirmatory round is clean. I verified that the amendment, the read-out code, the labels and the replays were committed in that order, and that every C1–C5 number reproduces exactly from the raw replays.
4. Calibrating on the physical binary loss, rather than on bisection labels, is justified by a failed monotonicity gate (8/800). This is the right choice and is rarely made.
5. The force-time accounting against a no-probe grasp is the question a practitioner would ask, and the answer (no gain for 1–5 s holds) is reported rather than buried.

**Weaknesses.**
1. **No hardware, and σ is assumed.** The central effect changes sign across σ ∈ [0.1, 0.4] (0.65 → −0.21 for the plug-in), and σ is not grounded in any measured detector. For RSS this is the decisive weakness. The result is a map conditional on an unknown parameter, and the paper cannot say where on that map a real GelSight- or BioTac-class sensor sits. Even the simulator's own clean detector has a log bias of +0.32 and an SD of 0.11 (`19_report_rows`), and the paper does not relate that SD to σ.
2. **The force saving is about 1 N on a protocol that applies 32.7–49 N first.** The preload and squeeze exceed every object's F\*_mid, which defeats the usual motivation for minimal-force grasping (fragile objects). The paper acknowledges this (Limit 6), but then the practical claim reduces to actuator effort during long holds, which leads to weakness 3.
3. **Break-even beyond 17.7 s is not backed by long-hold physics (E6).** Slip is certified over a 0.6 s disturbance window. A 17–27 s hold at the lower force, with creep, repeated disturbances or thermal and viscoelastic effects, is never simulated, yet the paper's practical recommendation ("probe when … holds are long") depends on exactly that regime. The break-even is also a closed-form calculation from commanded profiles, not a measurement.
4. **The σ 0.4 statements overreach (E3, E2).** At σ 0.4 the learned model still saves force and beats the plug-in by 0.32, so for a noisy real sensor the learner may be what matters. The abstract and conclusion say the opposite. Figure 2a plots matched-route plug-in values next to CRC-route learned values.
5. **C4/C5 are close to built in.** The correlated pool's family bands are about 0.3 of the full log-width. The width sweep already shows that CSF-1 wins at w ≤ 0.5, so a per-family prior that reduces each family to a narrow band will beat a σ 0.2 probe almost by construction. The interesting experiment, a prior + probe hybrid, is missing. Without it, C4/C5 do not tell a practitioner whether to add touch to a perception prior.
6. **Deployability of the certificate.** Offline CRC needs a replay of every calibration grasp at 81 forces, which is impossible on hardware. The online tracker is the deployable piece, but its physical-feedback evaluation has ordering-only intervals and no oracle. The rules also use the **true mass** and a **known disturbance stratum** (E10), neither of which is stated.
7. **Competitors.** No published tactile grip controller is reproduced. The only reactive baseline is a registered design with a known biased μ̂ (+0.32 log), and it fails at slip ≥ 0.31. The paper is right to call it a negative control, but then the paper has no competitive tactile baseline.
8. **Presentation.** Neither figure exists. The prose is number-dense, with five-to-ten four-significant-figure values per sentence, and pipeline jargon ("v4 row", "read-out code", "first round") pervades the text. Sections 1, 2 and 4 are under-developed (§0.3).

**Actionable revisions.**
- A1. Either ground σ (a bench measurement of onset-force repeatability on one real sensor, or a published incipient-slip detector error converted to log F_onset noise) or recast the title and abstract explicitly as a conditional map. At minimum, report the simulator's own detector SD (0.11) next to σ.
- A2. Rewrite the abstract, §6 and §7 so that "reverses at σ 0.4" names the **plug-in**, and add that the learned model retains a saving (0.1675 CRC; matched value from `RE_match`) and beats the plug-in at σ 0.4. Make Figure 2a single-route (matched for both arms, with CRC as ticks).
- A3. Simulate at least one long hold (e.g. 20–30 s, with repeated disturbances) at the certified force, or state plainly that slip over long holds is untested and that the break-even is computed, not measured. Report the first-round seed range of the break-even.
- A4. Add a hybrid arm (family prior as F_base centre, probe as a correction, for instance a shrinkage of log μ̂ toward the family μ̄) on the correlated pool, or remove the practical recommendation that depends on its absence.
- A5. State the known-mass and known-stratum assumptions, and add the existing noisy-mass variant (`_mn` features, 08h) as a robustness row if it was run.
- A6. Produce both figures, expand Introduction / Related Work / Setup to the thresholds, move the Deviations list to an appendix, and replace pipeline terms with scientific ones ("pre-registered confirmatory round", "grid-boundary check").

**Questions to authors.** (i) What σ does your own simulated detector imply after bias removal, and is σ 0.2 added on top of it? (ii) Why is CSF-fam's CRC slip so low (0.059) compared with every other arm (0.08–0.10)? (iii) On `c4` F1, the tactile arms slip at 0.20 (learned) and 0.11 (plug-in). Is low-friction under-coverage systematic on the fresh pool too (per-μ-quintile slip)?

**Recommendation.** Weak reject at RSS. The experimental hygiene is excellent, but there is no hardware, the effect depends on an ungrounded σ, the protocol undercuts the minimal-force motivation, and the practical break-even claim lacks long-hold evidence. A workshop or a robotics-learning venue with a simulation track would be a better fit as it stands.
**Score: 4 / 10** (borderline, significant weaknesses).

---

## Reviewer B (conformal / statistical methodology; methodology-evidence consistency)

**Summary.** The paper applies standard CRC (Angelopoulos et al.) per disturbance stratum to a monotonised binary physical-slip loss on an 81-point log-force grid, with LTT as a high-probability alternative and quantile tracking for online shift. Its contribution is an evaluation design: pre-registered confirmatory tests on fresh objects, a matched-slip comparison route, and a boundary map.

**Strengths.**
1. The CRC construction is correct. L̃_i(λ) = max_{λ′≥λ} L_i(λ′) is non-increasing and dominates L, and the threshold (n R̃ + 1)/(n+1) ≤ α is the B = 1 CRC rule. Per-stratum calibration uses one instance per object per stratum, so within-stratum exchangeability holds. I re-implemented λ̂ independently and obtained identical indices.
2. The paper is candid about what the guarantee is: marginal, in expectation over the calibration draw, not stratum- or family-conditional. The 200-re-split check (mean slip 0.084–0.087 < α; LTT 0.068–0.071) is the right sanity check and matches the theory.
3. The registered decision code is real and was frozen before the data existed. Holm, TOST and the bootstrap p are implemented as described in the amendment, and the 2,000-draw intervals reproduce exactly (seed 2027).
4. Multiplicity is tracked honestly. Unadjusted rows are labelled, and first-round secondaries carry family-wise and global Holm values (e.g. H2-R 0.03 / 0.12).

**Weaknesses.**
1. **The confirmatory estimand is not the certified rule.** C1, C2, C4 and C5 are on the matched-slip route, which shifts each stratum's λ̂ index by up to ±8 using **test-set** slip and interpolates RE at slip 0.10. That is a test-tuned operating point, not something the CRC certificate covers. It is a legitimate comparison device, but the conclusions should be stated as "at equal realised slip", and route sensitivity matters: C2's equivalence holds on the matched route but not on the certified CRC route at the 97.5 % level (−0.063 [−0.123, 0.084]). The paper's own TOST p for that row is 0.037 (E5), so the CRC-route C2 status depends on which criterion is applied. Report both criteria explicitly.
2. **Factual and route-mixing errors in the results text (E1, E2, E7, E8).** "Matched RE 0.2674 at slip 0.05929" pairs one route's RE with the other route's slip (the CRC-point RE is 0.2995). Figure 2a mixes matched and CRC routes. The feature chain mixes label and CRC routes. The mid-friction sub-pool omits its amplitude restriction and its arm. None of these changes a confirmatory verdict, but in a paper whose selling point is methodological care, each one undermines the reader's trust.
3. **Decision rule misdescribed (E4).** §4 states a CI-based superiority rule. The registered and coded rule is Holm-adjusted bootstrap p < 0.05 with a positive point. Note also that a 97.5 % CI is the Bonferroni-4 interval of the first round and is not Holm-calibrated for five tests. Say what the CI\*\* is for (display) and what decides (p).
4. **"Equivalence" phrasing (E9).** Quoting the two-sided p = 0.915 as "consistent with equivalence" is a textbook error. Keep only the TOST evidence.
5. **Single learned-model seed.** C2, C3 and C5 rest on the frozen seed-0 fit. The first round's seed spread on C3 (0.39–0.45) is comparable to the C2 SESOI band. An equivalence claim within ±0.10 for "a learned model" in general needs at least the existing seeds 1–4 replayed on `f4`, or it should be scoped to "this fitted model".
6. **Conditional coverage is where the safety question lives, and it is under-analysed.** The "single strata exceed α in up to 70 % of re-splits" statistic is largely expected binomial noise (about 700 test instances per stratum, SD ≈ 0.011 around a mean of about 0.085). Presented as a worrying failure, it is misleading in the opposite direction. The informative failure is systematic: on `c4` the low-friction family F1 slips at 0.20 (learned) and 0.11 (plug-in) and CSF-1 at 0.32, while F2–F4 sit far below α. That points to friction-dependent miscoverage that the marginal bound hides. Report slip by true-μ quintile on the fresh pool and consider Mondrian CRC by family (on `c4`) or by μ̂ bin. This is a natural, cheap extension and it bears directly on the claimed safety.
7. **σ 0.4 conclusion (E3).** As Reviewer A notes, the attribution "probe, not learner" is a σ 0.2 result. At σ 0.4 the data say the learner matters (+0.32 vs plug-in). The abstract and conclusion must be scoped accordingly.
8. **Novelty is incremental methodologically.** CRC, LTT and score-space quantile tracking are used off the shelf, and the paper says so (§2 Novelty). The contribution is therefore the empirical protocol and boundary map, which raises the bar on robustness: more than one simulator or contact model, more than one σ on the correlated pool, and more than one model seed. Most of these are absent.

**Methodology-evidence consistency verdict.** The paper is high-fidelity to its evidence: every number I checked (more than 120 values across v1–v4) is present in the result files, and every count matches. There is **no fabrication and no trial-count inflation**. The defects are one factual mis-pairing (E1), route-mixing in a figure and two text passages (E2, E7, E8), a scope overclaim on σ 0.4 (E3), and a misdescribed decision rule (E4), all listed in §0.2.

**Actionable revisions.**
- B1. Correct E1 (CSF-fam: matched RE 0.2674 at slip 0.10; CRC point slip 0.0593 / RE 0.2995), E2 (single-route Figure 2a), E7 (name the arm and the amplitude restriction; soften the abstract sentence), E8 (label each feature-chain row's route), E9.
- B2. Restate the confirmatory rule as registered (Holm-adjusted bootstrap p, point sign). For the CRC-route C2, state the criterion and report the TOST p = 0.037 alongside the CI.
- B3. Replay seeds 1–4 of the learned model on `f4` for C2 and C3 (labels and grids exist; this is replay-only compute), or scope C2 to the fitted model.
- B4. Add per-μ-quintile slip on `f4` and a Mondrian-by-family CRC row on `c4`, and reframe the "70 % of re-splits" sentence with its binomial expectation.
- B5. Scope the abstract, discussion and conclusion attribution to σ 0.2, and add the σ 0.4 learned-arm saving.
- B6. State that mass is known and that the stratum is known at deployment (E10), and state that the m draw is log-uniform.

**Recommendation.** Borderline. The statistical machinery is sound and verifiably pre-registered, and the results reproduce exactly. The paper falls short of a strong methods contribution because the method is off the shelf, the confirmatory estimand is a test-matched route, the attribution claim rests on one seed and one σ, and several route-mixing slips sit in a paper whose main asset is rigour.
**Score: 5 / 10** (borderline, significant weaknesses).

---

## Consolidated must-fix list (both reviewers)

1. **Scope the σ 0.4 / "probe, not learner" claims (E3) and make Figure 2a single-route (E2).** At σ 0.4 the learned arm still saves force (CRC 0.1675 [0.106, 0.256]) and beats the plug-in by 0.3238. The abstract, §6 and §7 currently say the saving reverses or disappears.
2. **Correct the factual and route errors:** CSF-fam "matched RE 0.2674 at slip 0.05929" (E1); mid-friction sub-pool arm, amplitude restriction and grid-dependence, plus the abstract sentence (E7); feature-chain routes (E8); "p 0.915 consistent with equivalence" (E9); the decision rule as registered (E4); the CRC-route C2 criterion versus TOST p 0.037 (E5).
3. **Break-even and long-hold validity (E6):** rename "measured" to "computed from commanded profiles", report the seed spread, and either simulate long holds at the certified force or state that slip over 17–27 s holds is untested.
4. **Ground or bound σ and state the deployment assumptions:** relate σ to the simulator's own detector SD (0.11) or to a real-sensor figure, and state that true mass and known stratum are used (E10).
5. **Strengthen attribution and safety evidence cheaply:** replay learned-model seeds 1–4 on `f4` (C2 currently rests on one fit), add per-μ / per-family conditional slip (the `c4` F1 slip is 0.20 / 0.11 for the tactile arms) and, if possible, a prior + probe hybrid arm on `c4`. Then render both figures, bring Introduction / Related Work / Setup up to length, and remove the pipeline jargon.

**Scores:** Reviewer A 4 / 10; Reviewer B 5 / 10 (mean 4.5). **CRITICAL FABRICATION:** none found. **Trial-count discrepancy:** none (single learned-model seed in v4 must be stated).
