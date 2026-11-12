# Stage 18 peer review (v4 draft pass 2, run 2): independent reviewer pair (RSS lens)

Inputs read: `prompts/stage18_v4_pass2_system.txt` (full), `prompts/stage18_v4_pass2_user.txt` (all 7,572 lines in chunks: paper draft lines 30–263, evidence blocks (a) v1 results, (a4) `results/v4/v4_analysis.json`, (a5) `results/v3/a7_integrated.json`, (b) log excerpt, (c) stats grep, (d) pointers); repository files `docs/11_amendment_v4.md`, `docs/10_amendment_v3.md` (A5, B2), `code/analysis_v4.py`, `code/certgrip/sim.py` (constants, instance sampler, touch grid), `code/requirements.txt`, `results/v4/crc_grids_11_{f4,c4,np}.json`, `results/v4/labels/*.jsonl` (headers and rows), `results/v1/h1m_analysis` block, `results/v2/b_analysis.json`, `results/v3/{a_analysis,b2_analysis,b3_analysis}.json`, `docs/02_sources.json` / `05_knowledge_cards.json` (citation keys), and git history of the v4 amendment, code and results.
Recomputed (scripts in `/tmp/rev4/`, repo untouched): every v4 point estimate from the raw replays (C1–C5, all f4 / c4 arm slip / RE / matched RE / mean hold force, per-stratum λ̂ indices, the no-probe arm); a 200-draw rerun of the C1 / C2 bootstrap (seed 2027); the Clopper–Pearson bound on 8 / 800; the CSF-fam family priors from the c4 selection labels; the max F\*_mid against the 32.7 N preload; the S6 break-even arithmetic; the commit order of amendment → code → read-out → replays; an automated trace of ~100 quoted numbers against all result JSONs (excluding prediction files); per-section word counts.

---

## 0. Checks requested by the prompt

### 0.1 Topic adherence
The paper stays on the stated topic: a ramp-down friction-onset probe, per-stratum CRC on a binary physical-slip loss, comparison against the strongest friction-blind conformal baseline (CSF-1, chosen on a selection split), attribution of the saving to the probe rather than the learner (C2, S1), and an online binary-feedback study under three shifts (Section 5.5). No section presents environment or tooling issues as contributions. Two deliberate narrowings are disclosed rather than hidden: (i) the problem is *hold* force after a fixed high-force protocol, not minimal-force grasping in general (Section 1, Limit 6), and (ii) "the probe, not the learner" is restricted to σ 0.2 and relative excess (Sections 1, 5.2). Section 5.4 (earlier-round supporting rows) is long and backward-looking but on topic. Verdict: **on topic; no drift.**

### 0.2 Methodology–evidence consistency

| Paper claim | Evidence | Status |
|---|---|---|
| Fresh pool 500 cal / 700 test objects, 2,000 / 2,800 instances; correlated pool 500 / 700, plus 50 selection objects per family | Recomputed: f4 500 / 700 objects, 2,000 / 2,800 instances; c4 500 / 700 objects; c4 label files hold 200 selection instances per family (= 50 objects × 4 strata) | Consistent |
| C1 0.4314 [0.3824, 0.4835]; C2 0.01117 [−0.05552, 0.05686]; C3 0.4135; C4 −0.5814; C5 −0.5461 | Recomputed from raw replays: identical to 16 digits; 200-draw bootstrap C1 [0.375, 0.487], C2 [−0.0545, 0.0563], consistent with the 2,000-draw CI\*\* | Consistent |
| All arm slip / matched RE / hold-force rows (Table 1 DESC rows) | Recomputed exactly (e.g. CSF-1 0.08786 / 0.7518 / 7.125 N; learned 0.08107 / 0.4227 / 6.115 N; CSF-fam 0.05929 / 0.2674 / 5.933 N) | Consistent |
| Holm over C1–C5; C2 by TOST at ±0.10; p formula min(1, 2·min(share ≤ 0, share ≥ 0)) | `analysis_v4.py` l.112–126, 214–229 implement exactly this | Consistent |
| CI\*\* = 97.5 % object-cluster bootstrap within family, λ̂ refitted, 2,000 draws | `analysis_v4.py` docstring and `run_pool` (1.25 / 98.75 percentiles, `V.boot_draws`, λ̂ refit inside `pool_stats`), `valid_draws` 2000 for every row | Consistent |
| Matched route: λ̂ index shifted by up to ±8 steps, RE interpolated at test slip 0.10 | `KS = range(-8, 9)`, `SLIP_MATCH = 0.10` | Consistent |
| 81-point grid, ±1.6 log force, F_max 100 N, no λ̂ at a grid edge | grid files `n_grid` 81, `half_width` 1.6, `F_max` 100; recomputed λ̂ indices lie in 38–42 for every arm and stratum; `edge` false everywhere | Consistent |
| Read-out "committed before any confirmatory replay and run once"; protocol "registered before any of its code was written or run" | git: amendment 11 at 15:08:45, pool code 15:11:02, read-out code 15:18:01, labels 15:27:26, first replay result 15:54:56, `v4_analysis.json` 20:02:09; `analysis_v4.py`, `analysis_v3_a.py`, `analysis_crc.py` unchanged between 9a6749263 and d7a197f6c; one commit of `v4_analysis.json` | Consistent (as far as git can show) |
| C4 / C5 "no prediction registered"; decision code labels them "inferiority" | Amendment: "No prediction"; `confirmatory.C4.decision = "inferiority"` | Consistent, and the paper discloses the label mismatch |
| Monotonicity gate: 8 / 800, CP upper 0.02115 > 0.02, 7 of 8 in D2 | `h1m_analysis`: `cp_upper_98.75` 0.021147, `by_dist.D2` 7 | Consistent, but the paper omits the level (one-sided 98.75 %); at 95 % the bound would be 0.0180 < 0.02, so the level is load-bearing |
| Detector log bias +0.3186, SD 0.1103; preload normal error ≤ 0.1597 N; 0 preload slips | `19_report_rows.json` | Consistent |
| Shrinkage a −0.3858, b 0.7397; η 0.03412; family priors 0.379 / 0.496 / 0.677 / 0.852 | v3 `b1_analysis.ols`; `h3_analysis.eta`; recomputed from c4 selection labels 0.3790 / 0.4965 / 0.6768 / 0.8523 | Consistent (F2 0.4965 rounds to 0.497 or 0.496 depending on convention; trivial) |
| S6 phase integrals, T = 1 / 5 / 30 s force-time, break-even 17.74 / 27.07 s | `S6_noprobe` block; arithmetic re-done: (31.04 + ramp − 13.08 − ramp′) / (7.125 − F) reproduces both values | Consistent |
| S7 200 re-splits, CRC / LTT rows, "31.5–70 %" | `S7_resplits` (R 200, seed 3031) | Consistent (amendment registered learned and plug-in only; CSF-1 added, harmless) |
| Earlier-round rows (H2b 0.0569, feature chain 0.4739 / −0.0534 / −0.0263, oracle prior −0.0299 [−0.1903, 0.0816], tuned margin 0.06571 / 0.4843, REACT ≥ 0.3086, 0.9921 / 0.9514, H2-R −0.2614 / −0.3152 / +0.3754, σ 0.4 shrunk −0.1395 [·, −0.01264], seeds 0.4343 / 0.4197 / 0.3932 / 0.4494) | Each traced to a named key in v1 / v2 / v3 result JSONs (e.g. REACT-blind@0.75 D2 0.30857 is the minimum over arms × strata; A5 `slip:emp` = `slip:crc` = 0.06571) | Consistent |
| Online Table 3 (label and physical feedback, D_RE 0.3107–0.4432, oracle 0.0751 / 0.1346 / 0.0863) | v1 `h3_analysis`, v3 `b3_analysis` | Consistent |
| Simulator: MuJoCo 4.0.0, 2 ms step, 8 × 8 touch grid, 11-replay bisection on [0.1, 100] N, slip > 2 mm / 3°, D1 1–10 m/s², D2 5–20 mm at 2–5 Hz, ramps 0.1 s, window 0.6 s | `requirements.txt`, label headers (`"mujoco": "4.0.0"`), `sim.py` constants (`DT`, `GRID`, `T_DIST`, `bisect_fstar` with 10 halvings) | Consistent |
| "Preload and squeeze exceed every test instance's F\*_mid" (Section 3.2) | Recomputed: max F\*_mid on the fresh **test** split is 33.64 N > F₀ = 32.7 N (one D3 instance); one fresh **cal** instance 39.55 N; c4 one cal and one select instance > F₀. The squeeze peak (49.05 N) does exceed all of them | **Discrepancy (minor wording)**: true for the squeeze, false for the preload on 1 / 2,800 test instances |
| S6 described as "computed in closed form from the commanded force profiles" | Amendment 11 registered a "**measured** break-even … from the replay's commanded profile"; the code computes a closed form and the squeeze term uses the mean measured pad-normal reading (`rec["touch_probe"]`), not the commanded profile | **Undisclosed deviation (minor)**: the paper is candid that it is computed, but the change from the registered "measured" quantity is not in the Deviations list, and "commanded" is not quite accurate for the squeeze term |
| RE = E_x[(F − F\*_mid)/F\*_mid] | Code computes RE on "avoidable" test rows only and forces slip = 1 for unavoidable rows (1 of 2,800 fresh test instances) | Undisclosed but negligible here |
| Figure 2 (a)–(c) referenced throughout 5.2 | Only `figures/figure1_prompt*.txt` exists; no Figure 2 asset or prompt | **Missing asset** |

### 0.3 Trial count
The evidence states: one confirmatory read-out (run once), 4,800 instances per pool (f4, c4, no-probe), 2,000 bootstrap draws, 200 re-splits, 20 stream orderings per shift, a single trained learned model (seed 0) for every v4 row, first-round seeds 0–4 for the C3 spread. The paper claims exactly these numbers and repeatedly flags the single seed. **No trial-count fabrication.**

### 0.4 Length
Word counts (from the draft): Abstract 246, Introduction 898, Related Work 639, Method 1,017, Experimental Setup 793, Results 2,714, Limitations/Discussion 577, Conclusion 145; total ≈ 7,050. Every section is above the prompt's minima. The opposite risk applies: with three dense tables and two figures, ~7,000 words is likely **over** an RSS 8-page body, and the abstract (246 words) is long for RSS. Results is dense to the point of being hard to read (many four-decimal numbers per sentence).

### 0.5 Fabrication flags
**None.** Every quoted number I traced (≈ 100, including all v4 confirmatory and descriptive values recomputed from raw replays) matches a result file. The issues found are a wording error (preload vs F\*_mid), an unlisted registration deviation (S6), a missing figure asset and a missing CP level, not invented results.

---

## Reviewer A (robotics / grasping systems, RSS)

**Summary.** After a fixed 32.7 N preload and squeeze, a log-linear ramp-down detects incipient slip from simulated taxels; μ̂ = mg/(2F_onset) feeds a Coulomb plug-in (or a frozen gradient-boosted model), and per-stratum CRC on a replayed physical-slip loss sets the hold-force multiplier. In MuJoCo, on fresh objects at an assumed onset noise σ 0.2, the plug-in needs less relative excess hold force than a friction-blind conformal rule (C1 D 0.43), the learner is equivalent on relative excess (C2), and a one-number-per-family prior beats both tactile arms when friction follows the visible family (C4/C5). The probe's force-time is repaid only for holds > 17.7–27.1 s, which were not simulated.

**Strengths.**
1. Unusually honest scoping. The paper says what it does not show (no hardware, assumed σ, no long holds, no published controllers reproduced, marginal-only guarantee, single seed) and reports its own negative results (C4/C5, σ 0.4 reversal, width sweep, break-even).
2. The protocol design isolates the friction channel cleanly: a friction-uninformative preload (verified: pad normal within 0.16 N of F₀) leaves the onset as the only source of friction information, so the comparison against friction-blind rules is interpretable.
3. The boundary map (σ, friction width, family-predictable friction, hold duration) is the most useful part for a practitioner: it tells you when *not* to probe.
4. The force-time accounting with the probe's return and re-hold included is a good correction of an easy-to-make optimistic error.

**Weaknesses.**
1. **The practical gain is small and the headline metric inflates it.** D = 0.43 is on *relative excess* over F\*_mid. In absolute hold force the plug-in saves 0.66 N of 7.13 N (9.3 %) and the learned model 1.01 N (14.2 %), while the probe protocol itself costs ≈ 18 N·s and a 32.7 N preload / 49 N squeeze peak that exceed nearly every object's need. For an RSS audience the absolute numbers belong in the abstract next to D.
2. **The comparison is structurally favourable.** Friction is drawn independently of every non-tactile input in the fresh pool, so no friction-blind rule (CSF-1, Mondrian, proprioceptive learner) can do better than a constant; C1 therefore largely confirms that information about friction helps when nothing else carries it. The one realistic non-tactile competitor (family prior) wins (C4/C5), and the natural combination (prior + probe) was not run. Published tactile controllers (Khamis, Dong, Boonstra, Niu) were not reproduced; the one reactive design run is a self-described flawed negative control.
3. **Simulation fidelity limits the conclusion.** Rigid MuJoCo contact with Coulomb friction, a modelled taxel detector, noise *added* to a detector that already has 0.32 log bias and 0.11 SD, σ chosen by assumption, and the sign of the main effect flips between σ 0.1 and σ 0.4. Without even a bench measurement of onset error, the reader cannot place a real sensor on the σ axis, so "when does the probe pay off" has no answer for hardware.
4. **The certificate is not deployable as evaluated.** Offline CRC needs a replay of each calibration grasp at all 81 grid forces, which only a simulator can provide; the replay-free online route has ordering-only intervals, an overshoot to 0.139 slip for 500 steps, and no physical-replay oracle.
5. **Every rule receives the true mass, commanded acceleration and disturbance stratum.** Mass noise and an unknown stratum would change all arms; the plug-in's mass cancellation (F_base = F_onset(1 + a_cmd/g)) is elegant but assumes the onset is read under the same gravity load as the hold.
6. **Break-even regime unsimulated.** The only regime where the probe pays (≥ 17.7 s holds) has no slip evidence; creep and repeated disturbances are exactly what would break a certified 0.6 s result.
7. Small factual error: Section 3.2 says the preload and squeeze exceed every test instance's F\*_mid; one fresh test instance (D3) needs 33.64 N > 32.7 N (one cal instance 39.55 N). Only the squeeze peak exceeds all.
8. Figure 2 is referenced for three sub-panels but no figure asset or prompt exists.

**Actionable revisions.**
- Report absolute hold-force saving (N and %) and absolute force-time alongside D in the abstract, Table 1 and conclusion.
- Fix the preload sentence (e.g. "the squeeze peak exceeds every instance's F\*_mid; the preload exceeds all but two of 4,800 fresh instances, both D3").
- Produce Figure 2 or remove the references.
- Either add the prior + probe hybrid on c4 (the obvious next comparator, already named as future work) or recast C4/C5 as the main boundary result in the abstract's first sentences.
- State D3 / D4 amplitude ranges and units (code: 0.5–2.0 × mg pull, 0.2–1.0 × m payload).
- Even a small hardware or published-sensor estimate of onset error would move σ from assumed to anchored; if impossible, say in the abstract that σ is not grounded.

**Questions for authors.** Why is the preload fixed at 32.7 N rather than adapted (the main source of force-time)? Would a probe-only protocol without the squeeze shorten the break-even below a few seconds? How does the detector behave under soft-pad contact?

**Score: 4 / 10 (Borderline, leaning reject for RSS).** Methodologically careful and honest, but the robotics contribution is a simulation-only, small absolute saving under structurally favourable comparisons, beaten by a trivial prior where friction is visible and unprofitable for realistic hold times; nothing yet transfers to hardware. I would not recommend acceptance at RSS in this form.

---

## Reviewer B (statistics / conformal methodology, rigour of claims)

**Summary.** The value of the paper is its confirmatory design: five decisions pre-registered (git confirms amendment → code → read-out → replays order, read-out code unchanged afterwards), Holm over five, bootstrap TOST for equivalence, CI\*\* for display, grid-edge rule fixed in advance. I recomputed all v4 point estimates from the raw replays and they reproduce exactly.

**Strengths.**
1. Pre-registration with verifiable ordering, a single read-out, and honest reporting of C4/C5 "no prediction" including the decision code's "inferiority" label versus the registered superiority-only rule.
2. Correct use of CRC on a monotonised loss (L̃ ≥ L so the bound transfers) with an explicit, failed monotonicity gate justifying the physical route; LTT reported as the high-probability alternative.
3. The re-split study (S7) and per-family table (S4) show concretely what a marginal guarantee does and does not deliver (any stratum > α in 31.5–70 % of re-splits; F1 slip 0.32 for CSF-1 on c4). This is a good contribution to how conformal guarantees should be reported in robotics.
4. The decomposition of the σ-band and width-sweep results (CSF-1 improving vs the plug-in degrading) avoids over-interpretation.

**Weaknesses.**
1. **The registered primary route uses test outcomes.** C1, C2, C4 and C5 are evaluated at a test-slip-matched operating point (λ̂ shifted on the *test* outcomes to reach slip 0.10). This is a frontier comparison, not a comparison of certified rules. The paper says so in Section 4, but the abstract quotes D = 0.4314 without naming the route. The CRC-route values (C1 0.4482; C2 −0.06291, not equivalent at the 97.5 % level) should be co-reported in the abstract, especially for C2, whose equivalence holds only on the matched route.
2. **Route mixing in the abstract and conclusion.** "for the plug-in at high probe noise (−0.2065; the learned model keeps a saving there, 0.1675)" juxtaposes a matched-route value with a CRC-route value. The matched-route learned-vs-CSF-1 value at σ 0.4 is 1 − 0.6134/0.7518 ≈ 0.184 (point only; not a registered row, no CI). Use one route per sentence.
3. **C2 rests on one fitted model.** The first-round seed spread on C3 (0.3932–0.4494, range 0.056) is more than half the SESOI; an equivalence claim at ±0.10 on a single seed is a statement about one model, not about "a learned model". The paper says this in Limits (10) but the abstract and C-ii state equivalence generically.
4. **Unlisted registration deviation (S6).** Amendment 11 registered a "measured break-even … from the replay's commanded profile"; the delivered S6 is a closed-form computation, and its squeeze term uses the measured mean pad-normal reading. The paper is open that the value is computed, but this belongs in the Deviations list.
5. **Reporting details.** The monotonicity gate's CP level (one-sided 98.75 %) is omitted although it decides the gate (at 95 % the bound would be 0.0180 < 0.02, and the gate would pass). Unavoidable instances are counted as slips and dropped from RE (1 of 2,800 here) without mention. The S3 width sweep had a registered directional prediction ("D shrinks with w"), which was met; the paper calls S3 purely descriptive and does not say so.
6. **Online intervals over orderings only** (20 permutations of one pool) are much narrower than an across-pool interval and should not be read as evidence of convergence; "consistent with convergence to α" is the right strength, and H3 efficiency stays inconclusive.
7. **Multiplicity outside C1–C5** is unadjusted for S1–S7 and later rows; with ~20 secondary contrasts, statements like "learned beats plug-in at σ 0.4" should be phrased as exploratory.
8. Density: Results has four-decimal numbers in nearly every clause; Table 2 mixes v4 and first-round rows. Moving Section 5.4 to an appendix would sharpen the paper.

**Actionable revisions.**
- Abstract and Table 1: label every D with its route; give C1 and C2 on both routes; say C2's equivalence is on the matched route and one model.
- Replace the σ 0.4 "0.1675" in the abstract and conclusion by a same-route value, or label it.
- Add S6 ("measured" → computed) to Deviations; state the CP level; mention the unavoidable-instance convention; note S3's registered prediction was met.
- Shorten Section 5.4 and move first-round rows to an appendix.

**Score: 5 / 10 (Borderline).** As a statistics-of-certification study it is rigorous and, as far as I could verify, entirely honest. The methodological novelty is limited (CRC, LTT and quantile tracking used as published; the new element is the protocol and the confirmatory framing), and the headline numbers need route labels and absolute-force context before they can be read correctly.

---

## Consolidated verdict

- Scores: **Reviewer A 4 / 10, Reviewer B 5 / 10** (mean 4.5, borderline; not yet RSS-ready).
- **CRITICAL FABRICATION flags: none.** Trial counts, statistical procedures and all traced numbers match code and results; all v4 points reproduce exactly from raw replays.
- Discrepancies: (D1) preload vs F\*_mid claim false for 1 fresh test instance (33.64 N > 32.7 N); (D2) S6 registered as "measured", delivered as computed, not listed as a deviation; (D3) Figure 2 asset missing; (D4) CP level omitted; (D5) route mixing in abstract/conclusion; (D6) unavoidable-instance convention undisclosed.

### Top 5 must-fix
1. **Label routes in the abstract, Table 1 and conclusion**: give C1/C2 on both the matched (test-outcome) route and the CRC route; state that C2's equivalence holds only on the matched route and for one trained model; replace or label the σ 0.4 "0.1675" (CRC) next to "−0.2065" (matched).
2. **Report absolute savings** (plug-in 0.66 N / 9.3 %, learned 1.01 N / 14.2 % of mean hold force; probe protocol ≈ 18 N·s) next to D on relative excess in the abstract and Table 1.
3. **Correct Section 3.2**: the preload does not exceed every test instance's F\*_mid (one fresh test D3 instance needs 33.64 N; one cal instance 39.55 N); only the squeeze peak does.
4. **Complete the deviation and reporting record**: add S6 (registered "measured break-even", delivered closed-form with a measured squeeze term) to Deviations; state the 98.75 % one-sided CP level for the gate; disclose the unavoidable-instance convention; note S3's registered prediction was met.
5. **Supply Figure 2** (or remove its references) and cut density: move Section 5.4 / first-round rows to an appendix so the confirmatory story and the boundary map fit an 8-page RSS body. (Substantive, if time allows: the prior + probe hybrid on c4, which is the comparison an RSS committee will ask for first.)
