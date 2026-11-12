# Stage 18 peer review, draft v4, run 1 (independent reviewer, fresh context)

**Inputs read:** `prompts/stage18_v4_system.txt`; `prompts/stage18_v4_user.txt` in full (paper draft v4 with the Figure 1 prompt, evidence blocks (a) `results/v1/results_v1.json`, (a4) `results/v4/v4_analysis.json`, (a5) `results/v3/a7_integrated.json`, (b) timing log, (c) statistics grep, (d) pre-registration pointers); `docs/11_amendment_v4.md`; `code/analysis_v4.py`, `code/crc_grids_11.py`, `code/certgrip/baselines.py`, `code/certgrip/featsets.py`, `code/certgrip/sim.py` (constants), `code/analysis_v3_a.py` (split / sub-pool helpers); `results/v3/{b1,b2,b3,a_analysis,a_analysis_08e,a3_holm}.json`, `results/v2/b_analysis_edge.json`; git history of `analysis_v4.py`, `docs/11_amendment_v4.md` and `results/v4/crc_f4/`. I did not open earlier review files.

**Recomputed (scripts in `/tmp/rev1/`, outside the repo):**
1. `numcheck.py`: every one of the 283 decimal numbers in the paper body matches some value in a results JSON (no orphan numbers). I then traced the load-bearing ones to their specific keys (about 60 traced).
2. `recompute_v4.py`: my own implementation (no repo code imported) of per-stratum CRC on the monotonised physical loss, RE on avoidable rows, the matched-slip recipe (k = -8..+8, interpolation at test slip 0.10) and the friction-width windows, run on the raw v4 replays (`results/v4/crc_{f4,c4,np}/*.jsonl`, 4,800 instances each, all replayed) and labels. **C1 0.43137, C2 0.01117, C3 0.41348, C4 -0.58143, C5 -0.54606, S1 0.64863 / -0.20648, S3 0.24139 / -0.10944 / -0.69667, every arm's slip, RE, matched RE and hold force: all reproduced exactly.**
3. `boot_check.py`: an independent 300-draw object-cluster bootstrap within family, with lambda-hat refitted in each draw. C1 [0.376, 0.482], C2 [-0.052, 0.065] (0 % of draws outside ±0.10), C3 [0.366, 0.481]. These agree with the reported 2,000-draw CI\*\* to within resampling error.
4. `absforce.py`: absolute hold force and absolute excess force (N) at the CRC point and at matched slip. These are new numbers, not in the paper. They are used in the reviews below.
5. Break-even arithmetic from the S6 integrals, plus a variant that drops the squeeze phase (my own derivation).

---

## Part 0. Checks the user prompt requires

### 0.1 Topic adherence
The paper stays on topic: a ramp-down friction-onset probe, CRC on the binary physical-slip loss, comparison with the strongest friction-blind conformal baseline (CSF-1, chosen on a selection split), attribution of the saving to the probe rather than the learner (C2), and an online binary-feedback study under three shifts (Sec. 5.5). No environment or infrastructure issue is presented as a contribution. One scope note: the topic says "minimal-force grasp", but the paper narrows this to the *hold* force after a fixed 32.7 N preload and a 1.5x squeeze, both of which exceed every instance's F\*_mid. The paper says so openly (Sec. 1 and Limit 6), so this is a framing issue rather than drift. Still, the title and abstract should not leave readers thinking the grasp as a whole uses minimal force.

### 0.2 Methodology-evidence consistency

| # | Paper claim | Evidence | Verdict |
|---|---|---|---|
| 1 | C1-C5 values, CI\*\*, decisions, Holm over five p | `v4_analysis.json` rows and `confirmatory`; recomputed exactly | **Consistent** |
| 2 | 500 cal / 700 test objects per pool; 2,000 draws, all valid; 97.5 % CI | `n_cal_objects` 500, `n_test_objects` 700, `valid_draws` 2000; code uses the 1.25 / 98.75 percentiles | Consistent |
| 3 | Read-out code committed before any v4 replay, run once | git: amendment 15:08, `analysis_v4.py` 15:18 (only commit), first replay 15:54, read-out 20:02 (2026-11-10) | Consistent |
| 4 | `edge: false` for every v4 row = no lambda-hat at index 0 / 80 | `arm_eval`: `edge \|= j in (0, J-1)` on the point fit | Consistent |
| 5 | CSF-fam mu-bar F1 0.379 / F2 0.496 / F3 0.677 / F4 0.852 from 50 selection objects | `crc_grids_11_c4.json` source; 800 selection instances = 200 objects | Consistent |
| 6 | Shrunk plug-in a -0.3858, b 0.7397 frozen | `v3/b1_analysis.json` ols | Consistent |
| 7 | eta 0.03412; T 2,000; 20 orderings; physical-feedback slips 0.1389 / 0.1001 / 0.1008 / 0.1018; D_RE 0.3107-0.4432 | `h3_analysis.json`, `v3/b3_analysis.json` | Consistent. The 0.4432 upper end is the *pre-shift* window 1-500, so "across shifts and windows" includes a window that is not post-shift. |
| 8 | Monotonicity gate 8 / 800, CP upper 0.02115, 7 of 8 in D2 | `h1m_analysis.json` (one-sided 98.75 % CP) | Consistent |
| 9 | Comparator selection 0.7686 / 0.8294 / 0.8335 | `comp_selection.json` | Consistent |
| 10 | S6 integrals, phase integrals, break-even 17.74 / 27.07 s | `S6_noprobe`; slope / intercept check reproduces both | Consistent |
| 11 | "CSF-1: one friction value mu-bar, **selected on the selection split** before any calibration or test access" (Sec. 3.3) | `certgrip/baselines.py`: `MU_BAR = sqrt(0.3 * 1.0)`, hard-coded as the geometric mean of the generator's design range. The selection split chose the comparator *type* (CSF-1 vs Mondrian vs CertGrip-P), not mu-bar. | **Discrepancy (description).** The outcome is unaffected because e^lambda absorbs mu-bar, but the sentence is inaccurate. |
| 12 | "Simulated touch is clean, so we add onset noise" (Sec. 3.2) | `sim.py` `TAXEL_NOISE = {mult 0.05, add 0.002 N, gain 0.10}`. At sigma = 0 the detector already has log error bias +0.3186 and SD 0.110 (F3 SD 0.196) (`19_report_rows.detector_id_sigma0`). The added sigma sits on top: `log F_onset + sigma*eps`. | **Discrepancy (description).** The nominal sigma is not the total onset noise; the effective log SD is about 0.15 / 0.23 / 0.41. |
| 13 | Mid-friction sub-pool "mu in [0.5, 0.8]" (Sec. 5.4, Table 2): -0.2614, refined -0.3152, primary +0.3754 | `docs/08g` H2-R and `analysis_v3_a.py`: the sub-pool is mu in [0.5, 0.8] **and** amplitude inside the per-stratum inter-quartile range (`mu_and_amp`). The -0.3152 / +0.3754 rows are `sub:mu_and_amp:D:full_vs_CSF-1` (learned vs CSF-1). | **Discrepancy (definition omitted).** The amplitude condition and the arm (learned, not plug-in) are not stated. On the refined grid the plug-in row is -0.680, and the mu-only row is also negative (-0.172). |
| 14 | Feature chain: "adding the onset gives D 0.4739 ..., squeeze -0.0263", "full vs onset-only -0.0534" | 0.4739 and -0.0263 are from `h4a_label_rule.json` (**label route**); -0.0534 is from `crc_analysis.json` (CRC route) | **Mixed routes, not disclosed** |
| 15 | Fig. 2a: "plug-in 0.6486 / 0.4314 / -0.2065; learned 0.5683 / 0.4135 / 0.1675" | Plug-in values are matched-route (S1_C1, C1). Learned values are **CRC-route** (S1_C3, C3); the learned matched values at sigma 0.2 vs CSF-1 would be 0.4377. | **Mixed routes in one panel, not disclosed** |
| 16 | Abstract: "the plug-in lowers ... D = 0.4314 ...; it repays the probe's force-time only for holds beyond 17.74 s"; Conclusion: "breaks even after 17.74 s" | 17.74 s is the **learned** model. The plug-in, the subject of both sentences, breaks even at **27.07 s**. | **Discrepancy (misattribution in the headline)** |
| 17 | C1 decision: "superiority if the CI\*\* lower limit exceeds 0" (Sec. 4) | Registered rule (`11_amendment_v4.md`, code): Holm-adjusted p < 0.05 and point > 0 | Restated rule differs from the registered one; outcome unchanged |
| 18 | C2: "the two-sided p of 0.915 is consistent with equivalence" | A non-significant difference test is not evidence of equivalence. The decision correctly rests on TOST p (0.0). | Statistical misstatement; delete the sentence |
| 19 | "CSF-fam reaches matched RE 0.2674 at slip 0.05929" | 0.2674 is RE interpolated at slip 0.10; 0.05929 is the CRC-route slip | Conflates two routes |
| 20 | Mass | Every rule receives the **true mass** (`i["mass"]`) and the commanded acceleration. The paper never says so. For the plug-in, mass cancels exactly: F_base = F_onset (1 + a_cmd/g), up to the mu-hat clip. CSF-1 depends on mass. A 10 % mass-noise check exists (`sec08h_massnoise.json`) but is not reported. | Undisclosed assumption (it favours the baseline, if anything) |
| 21 | Learned model | v4 uses only the frozen v1 **seed-0** fit (`full_rd@σ#0`). v1 seed spread on H2a is 0.393-0.449. | Not stated in Sec. 3.3 / 4; matters for C2 |
| 22 | First-round secondaries "Holm within family (no verdict changes)" | `a3_holm.json`: no change within family. Over all 52, H2-R loses significance (0.12), and the paper reports that. | Consistent |
| 23 | MuJoCo 4.0.0 | `requirements.txt` and replay headers: `mujoco 4.0.0`, numpy 2.5.3 | Consistent |
| 24 | Statistical procedures | Bootstrap CI, TOST, Holm, CP / beta present in `code/` (evidence c); no ANOVA or t-test is claimed | Consistent |

### 0.3 Trial count
The paper makes no claim of N independent trials or seeds that the evidence contradicts. Its replication units are objects (500 / 700 per pool, 4 strata each = 4,800 instances, every one replayed once on an 81-point grid; replays are deterministic, `all_within_identical: True`), 2,000 bootstrap draws, 200 re-splits, 20 stream orderings, and v1 seeds 1-4 for the H2a replication (verified in `crc_analysis.json`). **No CRITICAL trial-count fabrication.** The one omission is that every v4 learned-model row uses a single training seed (seed 0); see item 21.

### 0.4 Paper length (word counts from my script; tables excluded where noted)

| Section | Words | Threshold | Status |
|---|---|---|---|
| Abstract | 198 | ≥ 150 | OK |
| Introduction | 441 | ≥ 700 | **Too short** |
| Related Work | 298 | ≥ 500 | **Too short** |
| Method (Sec. 3) | 814 | ≥ 800 | Borderline (includes the algorithm box) |
| Experimental Setup (Sec. 4) | 397 | ≥ 600 | **Too short** |
| Results (Sec. 5) | 2,217 (1,630 without tables) | ≥ 500 | OK |
| Total | ≈ 4,800 | ≥ 4,000 | Not critically under-length |

The density is very high. Sec. 4 and Sec. 5 read like a ledger of codes (CONF / PRE / SEC / DESC, S1-S7, H2b, H2-R) and lack explanatory prose.

### 0.5 Fabrication flags
**No CRITICAL FABRICATION found.** All headline numbers were recomputed exactly from raw replays, and every decimal in the paper traces to a results file. The flagged items are **reporting discrepancies**: #16 (misattributed break-even in the abstract and conclusion), #13 (sub-pool definition), #12 (the "clean touch" / sigma meaning), #11 (CSF-1 mu-bar provenance), #14 and #15 (undisclosed route mixing), #18 and #19 (statistical wording), #20 and #21 (undisclosed assumptions).

---

## Reviewer A (methodology, statistics and certification)

**Summary.** After a fixed preload and squeeze, the paper reads a friction estimate from the incipient-slip onset of a ramp-down. It maps that estimate to a hold force with a Coulomb plug-in or a learned quantile model, and calibrates a per-stratum log-multiplier by CRC on the monotonised physical slip loss. Five pre-registered, Holm-corrected tests on a fresh object pool show that:
- the plug-in beats the friction-blind conformal baseline (D 0.43);
- the learned model is equivalent to the plug-in within ±0.10 on relative excess;
- the earlier result replicates;
- a family friction prior beats both tactile arms when friction follows the visible family.

Secondary analyses map a noise band, a friction-width sweep, a measured break-even, re-split certificate behaviour and online tracking.

**Strengths.**
1. The confirmatory design is exemplary for this literature. The amendment was committed before the code, and the code before the replays (I checked the git timestamps). The decision rules are written in code. C4 / C5 are reported honestly even though they go against the method. I reproduced every C1-C5 point estimate exactly with an independent implementation, and a fresh bootstrap gives matching intervals.
2. The CRC route is correctly applied to a loss that is not monotone, via the max-over-larger-lambda monotonisation (L-tilde ≥ L). The paper states that the bound is marginal, in expectation, and requires simulator replays. The S7 re-splits (31.5-70 % of splits have some stratum above alpha) make the marginal character concrete, which is rare and valuable.
3. Negative and boundary results are prominent: sigma 0.4 reversal, width-sweep crossover, family-prior loss, break-even, the reactive design flagged as a negative control with a known artefact, and online efficiency inconclusive.
4. The comparator was chosen on a disjoint selection split among three friction-blind conformal candidates.

**Weaknesses.**
1. **The "learner adds nothing" conclusion depends on the metric.** C2 is equivalence on *relative* excess (D 0.011). On the CRC route the learned model is not shown to be equivalent (-0.063 [-0.123, 0.084]), yet it holds less absolute force (6.115 vs 6.463 N) *and* slips less (0.081 vs 0.098). My recomputation on absolute excess force at matched slip 0.10 gives 1.320 N for the learned model vs 1.800 N for the plug-in. That is a point D_abs of about 0.27, well beyond the SESOI. The 2-parameter shrunk plug-in reaches 1.386 N. So the defensible statement is "a learner is not needed *once the onset estimate is shrunk*; the raw plug-in leaves about 0.5 N on the table". The paper's own Figure 1 and break-even use absolute force, and on that scale the learned model is the best arm. The conclusion "the probe, not the learner, carries the saving" should be qualified accordingly.
2. **The matched-slip route uses test outcomes.** RE is interpolated at the *test* slip of 0.10 by shifting lambda-hat indices. This makes the route a frontier comparison, not a comparison of deployable certified rules. C1, C2, C4 and C5 all rest on it. That is acceptable as registered, but Sec. 4 should say "test-slip-matched" explicitly. The CRC-route rows (deployable) should be shown alongside in the main table, not only as grey ticks.
3. **Route mixing goes undisclosed** (items 14, 15, 19): Fig. 2a puts matched plug-in values next to CRC-route learned values, the feature chain mixes label-route and CRC-route numbers, and the CSF-fam sentence conflates two operating points.
4. **What sigma means is misdescribed** (item 12). Touch is not clean (taxel noise is modelled), and the sigma-0 detector already has log-error SD 0.11 with bias +0.32. A reader will take "sigma 0.2" as the total probe error, but the effective error is about 0.23. Because the main boundary claim is about noise, this needs correcting.
5. **C4 / C5 are largely predictable by construction.** The within-family log-friction SD of the c4 bands is about 0.10-0.12 (log-uniform over ratios of 1.43-1.5), below the probe's effective log-error of about 0.23. The width sweep is consistent with the same rule: the full-range log-SD is 0.35, and windows w 0.75 / 0.5 give SD 0.26 / 0.17, so the crossover sits where the friction spread falls to the probe error. The paper "hypothesises but did not test" this. A one-paragraph variance argument, or a plot of D against spread/error, would turn a set of disconnected boundary facts into a single explanation, and would show readers that C4 / C5 follow from the design.
6. **Single learned seed in v4** (item 21). The v1 seed spread of H2a (0.39-0.45, range 0.056) is more than half the SESOI, so an equivalence claim based on one fitted model should state that and ideally re-run seeds 1-4 (they already exist in `results/v1/preds/`).
7. **Statistical wording.** "p 0.915 is consistent with equivalence" should be removed. The restated C1 rule should match the registered rule. "D_RE 0.3107-0.4432 across shifts and windows" includes the pre-shift window.
8. **Undisclosed oracle inputs.** True mass and commanded acceleration are given to every rule. For the plug-in, mass cancels (F_base = F_onset (1 + a/g)), which is worth stating: it shows the "friction reading" is really a direct measurement of the static holding force, and that CSF-1 depends on an oracle mass.

**Actionable revisions.**
- A1. Report D on absolute excess force (N) alongside RE for C1, C2, C4 and S2, with CI\*\*. Rephrase C2's conclusion to "equivalent on relative excess; on absolute excess the learned and shrunk arms save more than the raw plug-in".
- A2. Label the matched route as test-slip-matched in Sec. 4. Give a CRC-route column for every confirmatory row in Table 1.
- A3. Fix Fig. 2a (one route per panel, or mark the routes) and the feature-chain sentence (state the label route).
- A4. Rewrite the sigma paragraph: modelled taxel noise, intrinsic detector error (bias 0.32, SD 0.11), and sigma as *added* noise; give the effective total.
- A5. Add the spread-versus-probe-error explanation (analytic or a plot) for C4 / C5 and S3.
- A6. State "single training seed (v1 seed 0), frozen" in Sec. 3.3. If possible, report C2 for seeds 1-4 as a secondary result.
- A7. Remove the p-0.915 sentence, align the C1 rule text with the amendment, and restrict the D_RE range to post-shift windows.
- A8. State that true mass and commanded acceleration are given to every rule, note the mass cancellation for the plug-in, and report the existing 10 % mass-noise row.

**Questions for authors.** (i) What is D(learned vs shrunk) on absolute excess? (ii) Does C2 hold for seeds 1-4? (iii) Could the per-stratum conditional failures (D1 47 % of splits for the plug-in) be removed with Mondrian-by-family CRC at a quantified force cost?

**Score: 5 / 10 (Borderline).** The statistics are unusually careful and the honesty is commendable. Against that, the attribution claim depends on the metric, the confirmatory route relies on test outcomes, and the main tested regime (sigma, correlated pool) is stylised enough that several conclusions follow from the design.

---

## Reviewer B (robotics significance, novelty and practicality)

**Summary.** See Reviewer A. My focus is on whether the result changes how a roboticist would choose grip force.

**Strengths.**
1. A clear, well-posed question ("when does a short probe pay off?") with an honest answer that includes the conditions under which it does not.
2. The measured break-even against a no-probe grasp is the right practical yardstick, and few tactile-grasping papers report one.
3. The protocol is designed so that the onset is the *only* friction channel (preload encodes neither m nor mu; 0 preload slips and 0 missed onsets in 10,400 v4 instances, verified). This isolates the probe's value cleanly.
4. The online study shows binary-feedback quantile tracking returning slip to α after friction and amplitude shifts (1,501-2,000 window intervals contain 0.10), using only the one bit a real robot would observe.

**Weaknesses.**
1. **Limited novelty.** The components (onset-based friction reading, Coulomb force, CRC, LTT, quantile tracking) are used as published, as the paper says. Once mass cancels, the plug-in is "hold at a calibrated multiple of the measured slip-onset force times (1 + a/g)". That is essentially the classical slip-margin rule (Johansson-style grip scaling, robotic safety-margin controllers), with the margin set by CRC instead of by hand. The paper's own Sec. 5.4 finds that a per-stratum margin tuned on calibration data lands on the same operating point as CRC. So what is new is the *certificate* and the *confirmatory map*, not the controller. That is a modest contribution for NeurIPS/ICML.
2. **The practical saving is small, and negative for typical holds.** D 0.43 on relative excess corresponds to 7.125 → 6.463 N mean hold force (-9 %) for the plug-in, and -14 % for the learned model. The protocol's preload and squeeze (13.08 + 12.91 N·s) are about 5x the hold force. For 1-5 s holds the no-probe grasp uses the least force-time, and the plug-in needs holds longer than 27 s to break even. The abstract's "beyond 17.74 s" quotes the learned model's figure for the plug-in (item 16).
3. **The squeeze inflates the break-even and is not needed by the plug-in.** The plug-in does not use squeeze features, and the paper finds no evidence that the squeeze helps the learner (-0.0263). Removing the squeeze phase (12.91 N·s) from the S6 intercepts gives break-evens of about **5.0 s (learned) and 7.6 s (plug-in)**. This is my arithmetic and would need replays of a probe-only protocol, since removing the squeeze changes the contact state. Even so, it suggests the paper understates the probe's practical value under a leaner protocol, and that "probe-only (no squeeze)" is the obvious missing arm.
4. **Simulation only, with an assumed noise model.** The sign of the main effect flips between sigma 0.1 and 0.4, and sigma is not grounded on hardware or on published detector error. The deployable story therefore hinges on an unmeasured quantity. Offline CRC also needs replays at every grid force, which cannot be done on a real robot (acknowledged). For a robotics-heavy claim at an ML venue, at least a small hardware sigma measurement, or a citation-grounded sigma, is expected.
5. **The comparators are weak or not reproduced.** No published tactile controller (Khamis 2021, Dong 2019, Boonstra 2024) is reproduced. The only reactive design is a negative control with a known artefact (raw mu-hat with log bias +0.32). The family prior that wins C4 / C5 is built from *true* friction of selection objects, and no hybrid prior + probe arm was run, so the most useful practical question (does a probe help on top of a prior?) is unanswered.
6. **The marginal guarantee is weak in practice.** One object family (F1, low friction) slips at 0.11-0.32 for three of four arms on the correlated pool, and 31.5-70 % of re-splits have a stratum above α. A practitioner usually needs per-object-class guarantees. LTT helps (0.07-0.16), and its force cost should be reported next to the CRC operating point.
7. **Presentation.** Intro, Related Work and Setup fall below the length targets. Sec. 5 is a ledger of status codes (CONF / PRE / SEC / DESC, S1-S7, H2b, H2-R, C-i...) that is hard for a reader outside the project to follow. The mid-friction sub-pool omits its amplitude condition (item 13). The CSF-1 mu-bar provenance is misdescribed (item 11).

**Actionable revisions.**
- B1. Correct the abstract and conclusion: plug-in 27.07 s, learned 17.74 s. Lead with absolute hold-force numbers next to D.
- B2. Add a probe-only protocol arm (preload → ramp-down → hold, no squeeze), or at least report the S6 break-even with the squeeze phase excluded, labelled as an estimate.
- B3. Add a hybrid family-prior + probe rule (for example, shrink mu-hat toward the family mu-bar) on the correlated pool. That is the arm that decides practical value.
- B4. Ground sigma: cite measured onset-detection error from tactile hardware, or run a small hardware calibration. Report the total, not the added, noise.
- B5. Report per-family (Mondrian) CRC and LTT operating points with their force cost, so that readers can pay for conditional coverage.
- B6. State the mid-friction sub-pool definition fully (mu in [0.5, 0.8] and mid-IQR amplitude; learned vs CSF-1) and the CSF-1 mu-bar source (geometric mean of the design range, not selected on the split).
- B7. Expand the Introduction (motivation, a worked example of the force-time trade-off), Related Work (classical slip-margin control, Mondrian / conditional conformal, safe-grasp CBFs in more depth) and Setup (gripper, detector, strata parameters, label procedure) to the target lengths. Replace most status codes with plain-language labels.

**Would I recommend presentation at NeurIPS/ICML?** Not in its current form. The work is rigorous and honest, but the contribution is a careful empirical map of a known controller with a standard certificate, in simulation, with a small and conditional practical gain. A version with a probe-only protocol, a hybrid prior arm and a grounded sigma would be a solid workshop or RSS/CoRL-track paper.

**Score: 4 / 10 (Borderline, leaning reject).**

---

## Consolidated must-fix list (ranked)
1. **Abstract and conclusion break-even misattribution** (17.74 s is the learned model; the plug-in is 27.07 s).
2. **Qualify C2 / "the probe, not the learner"**: on absolute excess force at matched slip, learned 1.320 N vs plug-in 1.800 N (point D about 0.27 > SESOI; shrunk 1.386 N). Report the absolute-force D with CIs and rephrase.
3. **Correct the method descriptions**: touch is not clean (taxel noise; sigma-0 detector bias 0.32, SD 0.11; sigma is added noise); CSF-1 mu-bar = √(0.3·1.0), fixed by design; true mass is given to all rules (it cancels for the plug-in); single learned seed in v4.
4. **Disclose route mixing**: Fig. 2a (matched plug-in vs CRC learned), the feature chain (label route vs CRC), "CSF-fam matched RE at slip 0.05929". Label the matched route as test-slip-matched, and add CRC-route columns to Table 1.
5. **Fix the sub-pool and statistics wording**: the mid-friction sub-pool also restricts amplitude (and the reported rows are learned vs CSF-1); delete "p 0.915 consistent with equivalence"; align the C1 rule text with the registered rule; then expand Intro, Related Work and Setup to the length targets.

Recommended additions (not blocking): a probe-only protocol and break-even (estimated about 5.0 / 7.6 s without the squeeze), a hybrid prior + probe arm, a spread-versus-probe-error explanation for C4 / C5 / S3, and per-family CRC / LTT force costs.

## Memory note
No user memory was consulted or needed for this review.
