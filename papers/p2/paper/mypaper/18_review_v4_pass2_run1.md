# Stage 18 peer review, draft v4 pass 2, run 1 (independent reviewer, fresh context)

**Inputs read:** `prompts/stage18_v4_pass2_system.txt` and `prompts/stage18_v4_pass2_user.txt` (all of it: draft, Figure 1 prompt, evidence blocks (a) to (d)); `docs/11_amendment_v4.md` (pre-registration of record for C1 to C5 and S1 to S7); `code/analysis_v4.py`, `code/crc_grids_11.py`, `code/predict_v4.py`, `code/analysis_crc.py` (`lam_index`), `code/analysis_v3_a.py` (bootstrap and re-split helpers), `code/certgrip/baselines.py`, `code/certgrip/featsets.py` (onset noise), `code/certgrip/sim.py` (constants); raw `results/v4/labels/*.jsonl`, `results/v4/crc_{f4,c4,np}/*.jsonl`, `results/v4/crc_grids_11_*.json`; earlier-round JSONs (`results/v1/*.json`, `results/v2/b_analysis_edge.json`, `results/v3/{a_analysis,a_analysis_08e,a3_holm,b1_analysis,b2_analysis,b3_analysis}.json`); git history of the v4 amendment, code and results.

**Recomputed independently** (my own scripts in `/tmp/rev3/`, reading only the raw replays and labels): per-stratum CRC λ̂ on the monotonised physical loss, CRC-route and test-slip-matched RE, hold force and slip for all 8 fresh-pool arms, the 4 correlated-pool arms and the no-probe grasp. I also recomputed the C1 to C5 point estimates (identical to 16 digits), my own 300-draw object-cluster bootstrap for C1 to C5 and C2-CRC (intervals and p-values agree with the 2,000-draw values), the instances with F\*_mid above the preload, the fresh-pool slip by family and by friction tercile (new), and a mean *absolute* excess force at matched slip with a 200-draw bootstrap (new). Every other number in the draft was traced to its source key with a search over all result JSONs (about 90 values checked).

---

## 0. Cross-cutting checks (shared by both reviewers)

### 0.1 Topic adherence
The paper stays on the registered topic: a ramp-down friction-onset probe, CRC on the binary physical-slip loss, the strongest friction-blind conformal baseline (CSF-1, chosen on a selection split), attribution of the saving to the probe rather than the learner (C2, feature chain, tuned margin), and an online binary-feedback study under shift (Section 5.5). It does not drift into unrelated topics. Environment and infrastructure issues (grid floor, label-rule monotonicity, deviations) appear only as disclosed deviations or limitations, never as contributions. The friction-correlated pool, the width sweep and the break-even analysis all extend the "when does it pay off" question, so they are on topic.

### 0.2 Methodology-evidence consistency

| Paper claim | Evidence | Verdict |
|---|---|---|
| Fresh pool 500 cal / 700 test objects, 2,800 test instances; correlated pool 500 / 700, family prior from 50 selection objects per family | `v4_analysis.json` n_cal/n_test 500/700; grids 4,800 instances each; `crc_grids_11.py` asserts c4 selection = 800 rows = 200 objects | Consistent |
| First-round pool 2,000 cal / 2,800 test instances | `v1/crc_analysis.json` n_cal_instances 2000, n_test_instances 2800 | Consistent |
| 81-point grid, ±1.6 log-force, centred on selection rows only, F_max 100 N; ±8-step matched route at test slip 0.10 | `crc_grids_11.py` (N_GRID 81, HALF 1.6, q_sel from selection rows); `analysis_v4.py` KS = −8..8, SLIP_MATCH 0.10 | Consistent |
| CI\*\* = two-sided 97.5 % object-cluster bootstrap, 2,000 draws, cal and test resampled within family, λ̂ refitted | `analysis_v4.py` (LO_P/HI_P 1.25/98.75, `boot_draws` within (split, family), λ̂ refitted per draw); valid_draws 2000 for every row | Consistent |
| Bootstrap p = min(1, 2·min(share ≤ 0, share ≥ 0)); TOST as the max of the two one-sided shares at ±0.10; Holm over C1 to C5 | `p_two`, `p_tost`, `holm` in `analysis_v4.py`; amendment 11 says the same | Consistent |
| C1 0.4314 [0.3824, 0.4835]; C2 0.01117 [−0.05552, 0.05686]; C3 0.4135 [0.3578, 0.4903]; C4 −0.5814; C5 −0.5461; all arm slips, RE, matched RE and hold forces in Table 1 | Reproduced exactly from raw replays (my script); my bootstrap gives C1 [0.373, 0.491], C2 [−0.053, 0.068], C3 [0.363, 0.492], C4 [−0.707, −0.467], C5 [−0.654, −0.431] | Consistent |
| C2-CRC −0.06291, TOST p 0.037 | JSON `S5_C2_crc`; my bootstrap gives TOST share 0.033 | Consistent |
| C4/C5: the decision code says "inferiority" but the rule defines only superiority | `analysis_v4.py` l.226–227 assigns "inferiority"; amendment 11 says "Superiority as C1" | Consistent, and honestly disclosed |
| Pre-registration before any v4 code or run; decision code committed before any replay | git: amendment 15:08:45, first `noprobe` code 15:11:02, `analysis_v4.py` 15:18:01, first replay results from 15:27 onwards; the only later edit to the amendment is an appended status note | Consistent |
| No grid-boundary λ̂ | `edge: false` on every row; my λ̂ indices are 38 to 42 for every arm and stratum | Consistent |
| S1 σ band, S2 shrunk, S3 width sweep (windows, n = 134/179 at w 0.25), S4 per family, S6 break-even (17.74 s / 27.07 s; phase integrals), S7 200 re-splits | All values match `v4_analysis.json`; I recomputed the no-probe slip 0.08714 and λ̂ 41 in all strata | Consistent |
| Earlier-round rows (CSF-1 selection 0.7686/0.8294/0.8335; CP upper 0.02115, 8/800 with 7 in D2; H2a 0.4168 and seeds 1 to 4; H2b 0.0569; feature chain; H5 −0.0299; tuned margin 0.06571/0.4843; REACT ≥ 0.3086, 0.9921/0.9514; H2-R −0.2614, Holm 0.03/0.12, refined −0.3152, primary +0.3754; σ 0.4 shrunk −0.1395; Table 3 online values; η 0.03412; OLS a/b; family μ̄) | Each traced to its key in v1, v2 or v3 JSONs; family μ̄ 0.37896/0.49649/0.67683/0.85229 in `crc_grids_11_c4.json`; REACT minimum 0.30857 (REACT-blind@0.75, D2) | Consistent |
| MuJoCo 4.0.0, 2 ms step, 8 × 8 taxel grid, 0.6 s disturbance window, 0.25 s ramp-down, 0.02 s return, 0.1 s re-hold | Replay headers `"mujoco": "4.0.0"`; `sim.py` DT 0.002, GRID 8, T_DIST 0.6; RD2 T 0.25, t_up 0.02 | Consistent |
| **"Preload and squeeze exceed every test instance's F\*_mid" (§3.2)** | v4 labels: f4 **test** instance F2/215/D3 has F\*_mid = 33.64 N > F₀ = 32.7 N. Two calibration instances (39.55 N, 32.97 N) and one selection instance (33.19 N) also exceed F₀. The squeeze peak (1.5 F₀ = 49.05 N) does exceed all of them. | **Discrepancy (minor, factual)** |
| **"[The learned model] is not re-trained here: … single frozen first-round fit"** | `predict_v4.py`: the v1 fits stored predictions, not models, so each model is *re-fitted* deterministically from the stored config and accepted only if it reproduces the stored v1 predictions (max \|diff\| ≤ 1e-5; commit message says 5e-7) | **Wording discrepancy (minor)**: functionally frozen, but the procedure should be stated |
| Abstract and conclusion: "for the plug-in at high probe noise (−0.2065; the learned model keeps a saving there, 0.1675)" | −0.2065 is the matched route (S1_C1@0.4); 0.1675 is the CRC route (S1_C3@0.4). From the JSON arm values the matched-route learned-vs-CSF-1 at σ 0.4 is 1 − 0.6134/0.7518 = 0.184 (no CI exists) | **Route juxtaposition (minor)**: §5.2 labels the routes correctly; the abstract and conclusion do not |
| "Matched-rate co-requirement fails in the friction and family shifts (0.032 / −0.035)" | 0.032 is `audit/S1\|matched_physical/diff`; the S1 label-window difference is 0.0265; −0.035 is in both | Mixed sources (minor); name the audit metric |
| H3 "inconclusive" | Correct under the registered 1.10 margin, but family shift R_E = 1.1739 [1.0234, 1.4283]: the CI excludes 1, so tracking holds *more* excess than the oracle there. The draft does not state this direction | Incomplete reporting (minor) |
| Correlated pool: "narrow, mostly non-overlapping family bands" | Amendment 11: F1 [0.30, 0.45], F2 [0.40, 0.60], F3 [0.55, 0.80], F4 [0.70, 1.00]; adjacent bands overlap | Acceptable, but the bands should be given |
| Limitation (10): "per-friction and per-family slip tables on the fresh pool … were not run" | These tables need no new simulation; I computed them from the existing replays in seconds (see 0.4) | Misleading as written: "not reported", not "not run" |

### 0.3 Trial count and fabrication check
The evidence states no single "number of runs". The relevant counts are objects, instances, bootstrap draws, re-splits, orderings and seeds. Every count in the draft matches the code and raw files: 700 fresh test objects, 2,800 test instances, 2,000 valid draws, 200 re-splits (seed 3031), 20 orderings, T = 2,000 and one training seed (seed 0) for every v4 learned row, with seeds 1 to 4 only for the first-round C3 counterpart. Seed limits are disclosed. **No CRITICAL FABRICATION found.** Every headline number reproduces from raw data, and the statistical procedures the paper names (bootstrap, TOST, Holm, Bonferroni-as-97.5 % CI, Clopper–Pearson, LTT) exist in `code/`.

### 0.4 New numbers from the raw replays (reviewer computations, not in the paper)
- **Absolute excess hold force at matched slip 0.10 (fresh pool, mean F − F\*_mid in N):** CSF-1 2.360, plug-in 1.800, shrunk plug-in 1.386, learned 1.320 (mean F\*_mid 4.644 N). The implied D on absolute excess, with my 200-draw cluster bootstrap and 97.5 % interval:
  - learned vs plug-in: **0.26 [0.18, 0.32]**
  - plug-in vs CSF-1: 0.26 [0.13, 0.33]
  - shrunk vs learned: −0.056 [−0.12, −0.001]
- **Fresh-pool CRC-point slip by friction tercile** (μ edges 0.446, 0.655), low / mid / high:
  - CSF-1: **0.264** / 0.000 / 0.000
  - plug-in: 0.131 / 0.088 / 0.075
  - learned: 0.173 / 0.062 / 0.009
- **Fresh-pool slip by family:** every arm lies between 0.070 and 0.104.

---

## Reviewer A (robotics and tactile manipulation; focus on significance, baselines and practical claims)

**Summary.** The paper chooses a grip *hold* force after a fixed high-force protocol (preload 32.7 N, squeeze, ramp-down probe). Friction is read from the incipient-slip onset, a Coulomb plug-in or a learned model turns it into a base force, and per-stratum CRC on the binary physical-slip loss calibrates it. In simulation, on fresh objects, the plug-in needs less relative excess force than the strongest friction-blind conformal baseline (C1 D 0.43). A learned model is equivalent to the plug-in in relative excess at σ 0.2 (C2). A per-family friction prior beats both tactile arms when friction follows the visible family (C4, C5). The saving reverses at σ 0.4 for the plug-in and as the friction range narrows. The probe's force-time cost is repaid only for holds longer than 17.7 to 27.1 s.

**Strengths.**
1. The comparison is fair: every arm sees the same mass, commanded acceleration and stratum, so the probe's value is isolated, and the baseline type was fixed on a disjoint selection split.
2. The confirmatory round is unusually clean for a robotics paper. It is pre-registered on fresh objects, the decision code was committed before any replay (I verified the git order), Holm is applied over five decisions, and a grid-boundary rule is in place. I could reproduce every point estimate from the raw replays.
3. The paper reports its own failure modes: the family prior beats touch, the plug-in reverses at σ 0.4, the width sweep reverses, short holds are cheaper without the probe, and the reactive control is a design artefact.
4. The force-time accounting is candid: the integrated force over 1 to 5 s holds favours the no-probe grasp, and the preload dominates.

**Weaknesses.**
1. **The attribution headline depends on the metric.** C2 shows equivalence on *relative* excess, which weights light, low-F\* objects heavily. On mean absolute excess force at the same matched slip, the learned model beats the plug-in by about 0.26 [0.18, 0.32] (my recomputation, §0.4). That is as large as the plug-in's own gain over CSF-1. In newtons, the learner delivers about half of the total saving (2.36 → 1.80 → 1.32 N), and the shrunk plug-in, a two-parameter OLS, recovers almost all of it. The draft's own Table 1 hints at this (6.115 vs 6.463 N, with lower slip), but the title, abstract, contributions and conclusion still say "the probe, not the learner, carries the saving". RE was pre-registered, so C2 stands as stated. The interpretation, though, must be limited to relative excess.
2. **Practical significance is thin.** The hold forces (6 to 7 N) are about one fifth of the preload the method requires. The absolute saving is 0.66 N (plug-in) or 1.0 N (learned) out of 7.1 N. Break-even needs 17.7 to 27.1 s holds, yet slip was evaluated only over a 0.6 s window. The only regime in which the probe pays for itself is therefore exactly the regime in which the certificate is unevidenced. The paper says this, but the "probe when holds are long" recommendation (§6) still rests on it.
3. **Baselines.** CSF-1 is a constant-μ physics formula with a calibrated multiplier. That is reasonable as a "friction-blind" anchor, but no published tactile controller is reproduced (Khamis, Dong, Boonstra). The reactive comparator is admitted to be a flawed design, and the obvious hybrid (family prior + probe) is not run. C4/C5 then shows only that a sharp prior beats a noisy probe, which is close to tautological under the stylised band layout.
4. **Simulation fidelity.** The setup is rigid MuJoCo contact with a modelled taxel detector. σ is assumed and added on top of a detector whose own log error has SD 0.11 (and SD 0.20 for F3; `detector_error_structure`), and the sign of the main effect flips between σ 0.2 and 0.4. Without some hardware or literature anchor for σ, the boundary map cannot be placed on any real sensor.
5. **A minor factual error:** the preload does not exceed every test F\*_mid (one fresh test instance at 33.64 N; a calibration instance at 39.55 N). Only the squeeze does.

**Actionable revisions.**
- A1. Add the absolute-excess D (and mean hold force at matched slip) for learned vs plug-in, plug-in vs CSF-1 and shrunk vs learned as a labelled *post hoc* secondary row. Rewrite the title, abstract, C-ii, §6 and the conclusion so the "probe, not learner" attribution is explicitly limited to relative excess at σ 0.2. State that in absolute newtons the learned model (or the shrunk plug-in) adds about as much as the probe alone.
- A2. Either run a long-hold simulation at the certified force (e.g. 20 to 30 s with repeated disturbances, for a few hundred test objects), or remove the "probe when holds are long" deployment advice and present break-even only as an accounting bound.
- A3. Correct §3.2 to "the squeeze exceeds every instance's F\*_mid; the preload exceeds all but one test instance (33.64 N vs 32.7 N)".
- A4. Give the c4 family bands numerically and acknowledge that adjacent bands overlap.
- A5. If compute allows, run one hybrid (CSF-fam multiplied by the probe ratio, or shrinkage of μ̂ towards the family μ̄). Without it, say plainly that C4/C5 is a stress test of a sharp prior, not evidence against touch.

**Score: 4 / 10 (Borderline, leaning reject).** The paper is rigorous and honest, but the contribution is a simulation-only map with modest absolute gains. Its central attribution claim weakens under an equally reasonable metric, and the regime where the method pays off is not simulated. At NeurIPS/ICML it would struggle on significance. A robotics venue (RSS/CoRL) with hardware validation would suit it better.

---

## Reviewer B (statistics and conformal methodology; focus on guarantees, inference and claim-evidence fit)

**Summary.** Same as Reviewer A. My focus is whether the stated guarantees and the confirmatory inference are valid, and whether each claim follows from its row.

**Strengths.**
1. The guarantee is stated correctly and with the right qualifiers. The bound is marginal over the pool, holds in expectation over the calibration draw, and covers the monotonised loss, which upper-bounds the physical loss. The paper explicitly says the bound is neither conditional nor high-probability, and it offers LTT as the high-probability variant. The CRC implementation (`lam_index`: (n R̃ + 1)/(n + 1) ≤ α with B = 1) matches the theorem.
2. The inference design is good: an object-cluster bootstrap within family that refits λ̂ in every draw, TOST with a stated SESOI, Holm over the confirmatory family, and a pre-registered grid-boundary rule. The matched route is disclosed as using test outcomes, which makes it a frontier comparison, and the CRC route is reported alongside every matched row; C1 agrees in sign and size on both routes (0.4314 vs 0.4482).
3. The 200-re-split check (S7) is a useful empirical audit of the expectation-over-calibration guarantee. Mean slip stays below α for every arm, while 31.5 to 70 % of re-splits have a stratum above α. This is exactly the right way to show what "marginal" means.
4. Deviations are listed rather than hidden (CRC route written after the monotonicity counts, post hoc refined grid in earlier rounds, the online oracle not produced).

**Weaknesses.**
1. **The marginal guarantee hides friction-conditional risk, and the paper underplays it.** The certificate averages over friction, so the relevant sub-population for a grip controller is the slippery objects. From the existing replays (§0.4), the low-friction tercile slips at 0.264 under CSF-1, 0.173 under the learned model and 0.131 under the plug-in. The other terciles slip far less, down to 0 for CSF-1 and 0.009 for the learned model. So the arms "achieve slip ≤ α" by moving risk onto low-μ objects to different degrees. The learned model's absolute-force advantage over the plug-in (Reviewer A, W1) comes with more concentration of slip on slippery objects (0.173 vs 0.131). That is a trade-off the paper never reports. Limitation (10) says the per-friction tables were "not run", but they need no new simulation.
2. **Route mixing in summary statements.** The abstract and conclusion pair a matched-route value (−0.2065) with a CRC-route value (0.1675) in one sentence. Since the paper insists elsewhere that routes are not interchangeable, each summary figure needs its route label. The matched-route learned-vs-CSF-1 at σ 0.4 is about 0.184 from the arm values.
3. **The C2-CRC "passes at 5 %" remark** (TOST p 0.037) sits next to a 97.5 % interval [−0.123, 0.084] that leaves the margin. The two statements are at different levels (TOST at 5 % corresponds to a 90 % interval), which a reader can easily misread. I suggest dropping the "passes" sentence or reporting the 90 % interval with it.
4. **Single learned-model seed.** C2, C3 and C5 rest on seed 0. The first-round seed spread on C3 (0.393 to 0.449) is over half the SESOI. C2 is an equivalence claim at margin ±0.10, so seed variability matters directly. Applying the stored seeds 1 to 4 to the v4 pools needs only predictions plus one grid of replays per seed.
5. **Online study.** The physical-feedback intervals cover orderings only (not objects), and no physical oracle exists. In the family shift the efficiency ratio R_E = 1.174 has a CI [1.023, 1.428] that excludes 1, so tracking needs more excess than the oracle recalibration there. "Inconclusive" is correct under the registered 1.10 margin, but the direction should be stated. The co-requirement values cite the physical-audit difference for S1 (0.032) next to a label-window difference for S2; name the metric.
6. **Minor wording:** "not re-trained" should read "deterministically re-fitted from the stored configuration and verified to reproduce the stored first-round predictions (max |Δ| ≤ 1e-5)". Also, the break-even was registered as "measured" (amendment 11, S6) but is computed in closed form. The paper's "computed" is the honest term; note the change from the registered wording as a deviation.
7. **Density and length.** The body is about 7,000 words plus three dense tables. Every section clears the minimum lengths, but the draft is likely over 9 pages, and the abstract (246 words) is crowded with numbers. Earlier-round material (§5.4, half of Table 2) could move to an appendix.

**Actionable revisions.**
- B1. Add a fresh-pool table of slip by friction tercile (or quintile) and by family at the CRC point for all arms, computed from the existing replays. Discuss it as the concrete content of "marginal", and move it out of the "not run" list.
- B2. Label the route on every number in the abstract and conclusion, or use same-route pairs (matched: −0.2065 vs ≈ 0.184; CRC: S1_C1@0.4 CRC vs 0.1675 if available).
- B3. Report C2's 90 % bootstrap interval with the TOST statement for both routes, or remove the "passes at 5 %" sentence for the CRC route.
- B4. Run seeds 1 to 4 of the frozen learned model on the v4 pools for C2 and C3 (secondary). At minimum, report the seed sensitivity of C2's point estimate.
- B5. In §5.5, state that tracking is less efficient than oracle recalibration in the family shift (CI above 1, below the 1.10 margin's decision boundary), and name the metric behind 0.032.

**Score: 5 / 10 (Borderline).** The statistics are carefully executed, reproducible and honestly reported; I found no fabricated or unsupported numbers. The weaknesses lie in scope and interpretation rather than errors. The certificate is the paper's selling point but is only marginal, and its friction-conditional failure is computable yet unreported. The key attribution is metric-dependent, and the learned arms rest on one seed. With B1 to B4 and Reviewer A's A1, this would be a solid, if incremental, methods paper. I would not yet recommend it for NeurIPS/ICML.

---

## Consolidated record

**Scores:** Reviewer A 4/10, Reviewer B 5/10 (mean 4.5).

**CRITICAL FABRICATION flags:** none. Every confirmatory and arm-level number reproduces from raw replays, and every earlier-round number traces to a result file.

**Discrepancies (non-critical):**
- D1. §3.2 "preload and squeeze exceed every test instance's F\*_mid" is false for the preload: f4 test F2/215/D3 has F\*_mid 33.64 N > 32.7 N; the v4 maximum is 39.55 N (calibration).
- D2. "Not re-trained" glosses a deterministic refit with a reproduction check.
- D3. The abstract and conclusion pair a matched-route value with a CRC-route value without labels.
- D4. The H3 co-requirement mixes the physical-audit and label-window metrics; the family-shift R_E direction is not stated.
- D5. Limitation (10) calls per-friction and per-family fresh-pool tables "not run", but they are computable from existing replays.
- D6. S6 was registered as "measured" but is computed; the paper's wording is the correct one, so record it as a deviation.

**Top 5 must-fix:**
1. Limit the "probe, not learner" attribution (title, abstract, C-ii, §6, conclusion) to *relative* excess. Add a post hoc absolute-excess row: learned vs plug-in ≈ 0.26 [0.18, 0.32]; shrunk ≈ learned.
2. Report fresh-pool slip by friction tercile and by family from the existing replays. Low-μ tercile: CSF-1 0.264, learned 0.173, plug-in 0.131. Discuss this as the content of "marginal".
3. Fix D1 (the preload claim) and D2 (the refit wording).
4. Label routes in the abstract and conclusion (−0.2065 matched vs 0.1675 CRC; matched-route learned vs CSF-1 at σ 0.4 ≈ 0.184). Fix the C2-CRC "passes at 5 %" phrasing.
5. Resolve the long-hold tension: either simulate long holds at the certified force or drop the "probe when holds are long" advice. Also run (or at least report sensitivity to) learned-model seeds 1 to 4 on the v4 pools for C2 and C3.
