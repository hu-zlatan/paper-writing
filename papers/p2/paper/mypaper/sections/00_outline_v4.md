# p2 · Stage 16 PAPER_OUTLINE [v4]: RSS 2027 Stage 1 extended abstract

**Format:** at most 5 content pages plus 1 page of references, no supplementary material (deadline 2026-12-04 AoE). Methods are complete; experiments may be preliminary. Main-body target is **3,350 words** (range 3,000–3,500), abstract excluded. **Stated deviation:** the 9-page word floors of hard_constraints §3 do not apply. A longer master draft is allowed, and stage 22 condenses it.

**Binding inputs:** `results/15_decision_v4.md` (PROCEED; reframe around the confirmatory C1–C5 table and the conditions under which the probe saving holds or disappears; the learner is demoted to a C2-level result). The **statements of record 1–9 of `results/14_analysis_v4.md`**, with the pass-2 rewrites (findings 1–16) binding where they differ from pass 1. The v3 statements of record 1–7, the v2 statements and the v1 audit rewrites stand where v4 does not supersede them. The v1 primary verdicts are unchanged: H2a superiority; H2b not confirmed; H1-M failed; H3 inconclusive. The H2-R scope limit stays in abstract-level claims. Where a decision file and an audit rewrite differ in wording, the audit wording is used.

**Revision of:** `sections/00_outline_v3.md`.

**Evidence notation:**
- `v1:block → key` = `results/v1/results_v1.json` (each block is an unchanged analysis file of `results/v1/`).
- `v2:` = `results/v2/results_v2.json`.
- `v3:` = `results/v3/results_v3.json`.
- `v4:row → field` = `results/v4/v4_analysis.json`.
- v4 row keys are named as the read-out names them: `C1`–`C5`, `S1`–`S7`, `S5_C2_crc`, `S5_C4_crc`; fields include `D`, `CI**`, `p`, `p_holm`, `p_tost`, `decision`, `edge`.
- **Writer's check (stage 17):** the planner did not open the JSON. Before printing, confirm each v4 sub-field spelling against `v4_analysis.json`. Every v4 number below is copied from the stage-14 v4 analysis, which pass 2 checked cell by cell against that file.

**Number convention:**
- Every value is copied from the analyses / JSON quoted in the prompt.
- v4 and v3 values are given to 4 significant figures; v1 / v2 values to 4 decimals.
- No new arithmetic enters the paper. Differences, ratios and break-even times are quoted only where a file carries them.
- The **v3 arithmetic break-even** (16.56 / 28.61 / 32.99 / 57.02 s; 13.22 / 25.28 s in the v3 outline) is **retired**. It is replaced by the measured S6 values, 17.74 s and 27.07 s.
- The v4 hold-force difference is **not** printed as a subtraction. Both means are quoted instead: learner 6.115 N, CSF-1 7.125 N on f4.

---

## Status-of-evidence legend (printed once, under Table 1; every table has a "Status" column using these codes)

| Code | Meaning | Rows |
|---|---|---|
| **CONF** | Confirmatory: pre-registered in amendment 11 before any v4 code or run. Fresh objects. Holm at 5 % over five p. | C1–C5 |
| **PRE** | Pre-registered v1 core decision (Bonferroni over 4). Not re-decided. | H2a, H2b, H1-M, H3 |
| **SEC** | Secondary, unadjusted. v1 secondaries carry Holm within family (v3 A3). | S1–S7, v2 / v3 rows, H2-R |
| **DESC** | Descriptive, point values, no test. | A7 force, B2 reactive, S4 per family, S6 force-time |

**Hedge rule (gate paper-level action 2):** the caveats "secondary / unadjusted / single split / route" appear **only** in the Status column and in §6. Prose refers to them by code ("(SEC)"). They are not repeated verbatim.

## Naming in the paper (descriptive names; codes only in the Status column and once in §4)

| Internal code | Name used in the paper |
|---|---|
| f4 | fresh pool (independent friction) |
| c4 | friction-correlated pool |
| CSF-1 | friction-blind conformal baseline (the strongest non-tactile conformal baseline, chosen beforehand) |
| CSF-fam | family friction prior (deployable non-tactile prior: one μ̄ per visible family) |
| CSF-muhat@σ | probe plug-in |
| CSF-shrunk@σ | shrunk probe plug-in |
| full_rd@σ#0 | learned probe model |
| P_onset@0.2#0 | onset-only learned model |
| no-probe CSF-1 | no-probe grasp (same preload, no squeeze / probe phases, CRC-calibrated) |
| CSF-proxy@σ_p | oracle-side friction prior (v2) |
| REACT-blind / REACT-probe | reactive slip-tightening controller (v3, registered negative control) |
| 08c / 08e grids | primary grid / refined grid (v1–v3 rows only) |

Definitions:
- *RE* = mean relative excess (F − F\*_mid)/F\*_mid of the **hold** force.
- *D(a vs b)* = 1 − RE(a)/RE(b). D > 0 means a needs less excess force than b.
- *CI\*\** = 97.5 % two-sided object-cluster bootstrap interval, 2,000 draws, λ̂ refitted in each draw.
- *Matched slip*: RE interpolated at slip 0.10 (the registered route for C1, C2, C4, C5).
- *SESOI* 0.10.

## Wording rules (binding; collected once)

**Certified**
- Always "in simulation, marginal over the pool, in expectation" (CRC) or "per stratum at δ 0.1" (LTT).
- Never "certified saving" without "marginal".
- Never per-stratum, per-family or per-split slip control.

**C2**
- "Equivalent within ±0.10 at σ 0.2 on the registered matched-slip route."
- Always add: on the CRC route equivalence is not shown (−0.06291 [−0.1226, 0.08396]).
- Never "probe + plug-in + CRC suffices" without both qualifiers (σ 0.2; matched route).
- The two-sided p 0.915 is "consistent with", never "confirms", equivalence.

**C4 / C5**
- "Not superior (registered rule); the CI\*\* lies wholly below 0."
- "Inferiority" is the read-out code's label for CI\*\* < 0, and it may be named only as such.
- No prediction was registered for C4 / C5.
- Never write "the tactile saving does not survive a family prior": on c4 the tactile arms still beat CSF-1.
- Never "most of the saving is against an uninformed prior".

**Width sweep (S3)**
- Descriptive trend at σ 0.2 on f4: "crosses 0 between w 0.75 and w 0.5".
- "We hypothesise, but did not test, that this reflects friction spread relative to probe noise."
- It does not explain C4 / C5, and it does not establish a noise-vs-width mechanism.

**σ band (S1)**
- "C2's equivalence is a σ 0.2 result."
- At σ 0.4 the learner outperforms the plug-in (SEC). No "because robust to noisy μ̂".
- The v3 B1 shrunk-plug-in result at σ 0.4 is mentioned as the opposing earlier finding.

**Shrunk plug-in (S2)**
- "Improves on the raw plug-in; whether the gain exceeds the 0.10 SESOI is unresolved."

**Certificate (S7, S4)**
- Strata: "across 200 f4 re-splits, 31.5–70 % have at least one stratum above α".
- Families: "on the single c4 split, family F1 exceeds α for three of four arms".
- Never merge the two designs. CSF-muhat@0.4 was not re-split.

**Break-even (S6)**
- "Measured against a simulated no-probe grasp, point values, no interval."
- For 1 s and 5 s holds the no-probe grasp uses the least force-time.

**Holm**
- p = 0.0 means two-sided p < 0.001 (C2's one-sided TOST p < 0.0005).
- The largest Holm-adjusted bound is ≤ 0.005.

**Grid edge**
- "`edge: false` in every v4 row, which we take, per the read-out code's flag, as no λ̂ at grid index 0 or 80."

**Motivation (gate action 7)**
- The method chooses a hold force after a fixed high-force protocol (preload 32.7 N). Never claim it is a minimal-force or fragile-object protocol.
- Prosthetics and fragile objects may be named only as a long-term motivation for hold-force reduction, together with the preload caveat.

**v1–v3 carry-overs**
- The v3 wording rules for H2-R (no mechanism; grid-dependent), the online study ("consistent with convergence to α"), the reactive controllers ("this registered design fails"; a negative control, partly a design artefact because of the raw μ̂ bias +0.3186) and the empirical margin stand unchanged.

**General**
- No provenance language ("recomputed", "results index").
- The Figure 1 generation prompt is **not** in the manuscript. Only the caption is.

---

## What changed vs the v3 outline (for the writer)

1. **Frame.** The paper is now a *confirmatory, condition-mapped answer* to "when does a tactile friction-onset probe plus conformal calibration reduce hold force at a slip-rate guarantee?" The C1–C5 table comes first. The σ band, width sweep, family prior and measured break-even form the **boundary map**. The v1–v3 rows are supporting evidence.
2. **Attribution is confirmatory** (gate action 1): C1 and C2 on 700 fresh test objects, with the C2 qualifiers (σ 0.2; matched route).
3. **Design dependence tested** (gate action 2): friction-correlated pool c4 with the deployable family prior (C4 / C5), plus a pre-specified width sweep (S3).
4. **No-probe grasp simulated** (gate action 3): S6 replaces the arithmetic break-even.
5. **σ as a band** (gate action 4): S1 at σ 0.1 / 0.2 / 0.4 is reported as the result. It is not grounded in hardware (§6).
6. **Readability** (gate actions 5–6):
   - The abstract has one sentence each for: the confirmed result, its conditions, and the attribution.
   - Holm and route details move to the body.
   - The status legend replaces repeated hedges.
7. **Title and motivation** (gate action 7): about calibrated hold-force selection after a high-force probe protocol, in simulation. The fragile / prosthetic framing is tempered.
8. **Figures** (gate action 8): Fig. 1 is a protocol schematic plus a real-data C1–C5 forest plot. Fig. 2 is a real-data boundary map (three panels). No generation prompt appears in the body.
9. **Demoted to master draft / dropped from print:**
   - v3 break-even and integrated-force rows (a7_integrated)
   - v2 uniform-margin rows except one line
   - v1 σ-curve detail of learned vs unshrunk plug-in
   - feature-chain detail beyond one sentence
   - CSF-proxy beyond one sentence
   - tail / 16-cell rows
   - A2 friction quintiles (superseded in print by S7 / S4; kept as one sentence)

---

## Title
**When Does a Friction-Onset Probe Pay Off? Conformal Slip-Risk Control of Grip Hold Force, Mapped in Simulation**

Alternative: *Probe, Then Calibrate — Under Which Conditions? Confirmatory Tests of Tactile Friction Probing with Conformal Risk Control in Simulation.*

The topic phrase "certified slip" appears in the abstract and introduction, always with "in simulation" and "marginal".

---

## Abstract (≈ 170 words; outside the main-body count)

**Goal:** a reader can extract (i) what is confirmed, (ii) under which conditions it fails, and (iii) what the learner contributes. One number per claim. No route, Holm or grid labels.

**Content, in order:**
1. **Problem:** choose a grip **hold** force whose physical slip rate is ≤ α. Without friction information, a conformal rule must cover the whole friction range.
2. **Method:**
   - After a fixed preload, a ramp-down probe reads friction from the incipient-slip onset.
   - A one-line Coulomb plug-in (or a learned model) turns the onset into a force.
   - Conformal risk control (CRC) on the binary physical-slip loss calibrates it per disturbance stratum.
   - The result is a marginal, in-expectation slip bound in simulation.
3. **Confirmed result (one sentence; pre-registered, fresh objects):**
   - Against the strongest friction-blind conformal baseline, the probe plug-in lowers relative excess hold force by D = 0.4314 (CI\*\* [0.3824, 0.4835]).
   - A learned model adds nothing at the assumed onset noise (equivalent within ±0.10).
4. **Conditions (one sentence):**
   - The saving reverses when friction is predictable from the visible object family: a one-number family prior beats the probe, D −0.5814.
   - It also reverses at high probe noise (σ 0.4: −0.2065) and as the friction range narrows.
   - It repays the probe's force-time only for holds longer than 17.74 s against a measured no-probe grasp.
5. **Scope (one clause):** the bound is marginal: single disturbance strata exceed α in up to 70 % of re-splits. In a narrow mid-friction band the baseline was better in earlier rounds.
6. **Online (one clause):** binary-feedback tracking returns slip near α after shift; efficiency vs oracle recalibration is inconclusive.

**Evidence:**
- `v4:C1 → {D, CI**}`
- `v4:C2 → {D, CI**, decision}`
- `v4:C4 → D`
- `v4:S1 → σ 0.4 C1-type D`
- `v4:S3`
- `v4:S6 → break-even full_rd@0.2#0`
- `v4:S7 → CRC share any stratum > α`
- `v1:sec08g.json → H2R.D`
- `v3:b3_analysis.json → shifts.*.physical_feedback.CertGrip."1501-2000".slip_phys.mean`
- `v1:h3_analysis.json → H3_primary`
- cite: `angelopoulos2022conformal`, `angelopoulos2023conformala`

---

## 1 Introduction (≈ 450 words)

**Goal:**
- Motivate slip-bounded hold-force selection.
- Name the missing ingredient (friction read online).
- State the research question as a *conditional* one.
- Give contributions, each mapped to a CONF or explicitly scoped result.
- Every paragraph connects to the question: *when does a short tactile probe make a distribution-free physical-slip bound cheaper in hold force, and which component carries the saving?*

**Paragraphs:**
1. **Why a slip bound on the hold force.**
   - Grip force above need wastes actuation and loads the object. Humans scale grip to friction after brief contact (`johansson1984roles`).
   - Tactile controllers react to slip or estimate friction (`dong2019maintaining`, `khamis2021real`, `boonstra2024estimate`, `niu2026synchronized`, `veiga2020grip`, `willemet2024grip`, `berman2025autonomous`), but give no distribution-free bound on slip rate.
   - Tempered framing: we study the hold phase after a fixed high-force probe protocol, not a minimal-force grasp from first contact.
2. **Why conformal methods alone are not enough.**
   - CRC certifies any force rule (`angelopoulos2022conformal`, `lei2017distribution`).
   - Without friction information, the calibrated multiplier must cover the whole μ range.
   - Hence the comparison against the *strongest* friction-blind conformal baseline, selected on a disjoint split: CSF-1 RE 0.7686 vs Mondrian-CSF 0.8294 and CertGrip-P 0.8335.
   - And, new in this version, against a deployable family prior when friction is family-predictable.
3. **Research question (three parts):**
   - (i) Does the probe lower hold force at a certified (marginal) physical slip rate ≤ α, and is the learned model needed?
   - (ii) Under which conditions does the saving hold or disappear: probe noise, friction range, friction-informative prior, hold duration?
   - (iii) Does calibration recover under shift with only binary slip feedback?
4. **Contributions (3 bullets):**
   - **(C-i) Method.**
     - A protocol in which a friction-uninformative preload leaves the ramp-down onset as the only friction channel.
     - Per-stratum CRC on the monotonised physical binary slip loss turns a one-line Coulomb plug-in on that onset into a rule with marginal expected slip ≤ α in simulation.
     - We use the physical loss because the label rule is not exactly monotone (8 / 800).
   - **(C-ii) Confirmatory evaluation on fresh objects.**
     - Five pre-registered decisions with Holm correction.
     - The plug-in beats the baseline (C1). The learner is equivalent to the plug-in at σ 0.2 on the registered route (C2). The v1 result replicates (C3).
     - A family prior beats both tactile arms on a friction-correlated pool (C4 / C5).
   - **(C-iii) Boundary map.**
     - σ band, friction-width sweep, measured break-even against a simulated no-probe grasp, and a 200-re-split check of the marginal certificate.
     - An online binary-feedback study under three shifts.
5. **Status sentence (one line):**
   - Three of five confirmatory predictions are met.
   - The two unpredicted rows (C4 / C5) are not superior, with intervals below 0.
   - The earlier pre-registered learned-vs-plug-in and label-validity decisions were not confirmed.
   - Online efficiency is inconclusive.

**Evidence:**
- `v1:comp_selection.json → candidates.{"CSF-1","Mondrian-CSF","CertGrip-P"}.RE_mean, COMP`
- `v1:h1m_analysis.json → {non_monotone, n}`
- `v4:C1`–`C5 → decision`
- `v1:crc_analysis.json → contrasts.{H2a,H2b}.decision`
- `v1:h3_analysis.json → H3_primary`

---

## 2 Related Work (≈ 300 words, three compact paragraphs + novelty sentence)

**Goal:** position the paper between tactile grip-force control and conformal safety in robotics, and say exactly what is new.

1. **Friction reading and tactile grip control.**
   - Incipient-slip friction reading: `marconi1996incipient`; reviews `chen2018tactile`, `romeo2020methods`; `khamis2021real`, `dong2019maintaining`.
   - Human grip: `johansson1984roles`, `willemet2024grip`.
   - Learned / reactive controllers: `james2020slip`, `grover2022detect`, `boonstra2024estimate`, `niu2026synchronized`, `kuo2025tracing`, `feng2026tactilereflex`, `lach2024zero`, `ayral2026reactive`, `almohammed2022switched`, `veiga2020grip`.
   - Prior-based pre-grasp force selection: `shang2026exp`. This links to our family-prior result.
   - Gap: no coverage guarantee on slip rate.
2. **Robust grasping under uncertainty:** `cloutier2018examining`, `cortez2019control`, `kim2024robust`, `enwerem2026firmgrasp`, `enwerem2026variational`. Their margins depend on assumed uncertainty sets.
3. **Conformal prediction and risk control.**
   - Foundations: `vovk2005algorithmic`, `romano2019conformalized`, `angelopoulos2023conformal`, `angelopoulos2022conformal`, `angelopoulos2026conformal`, `angelopoulos2025learn`, `bian2023training`, `ding2023class`.
   - Shift / online: `gibbs2021adaptive`, `gibbs2022conformal`, `angelopoulos2023conformala`, `angelopoulos2024online`, `farinhas2023non`, `ge2024stochastic`.
   - Robotics: `lekeufack2024conformal`, `lindemann2025formal`, `dixit2022adaptive`, `marques2026particle`, `lindemann2023conformal`, `ren2023robots`, `huang2023conformal`, `strawn2023conformal`, `zhang2024bayesian`, `zhao2024conformalized`, `kumar2026learnable`.
   - Gap: none calibrates a contact outcome as a binary loss in force space.

**Novelty sentence (modest):**
- Reading friction from slip onset, CRC, LTT and quantile tracking are all used as published.
- What is new:
  - (i) a protocol where the onset is the only friction channel, so its value can be isolated;
  - (ii) a marginal bound on the *physical* slip rate of the resulting hold force, in simulation;
  - (iii) confirmatory tests that locate the saving in the probe and map the conditions under which it disappears.

Simulators (one sentence, in §4): `wang2022tacto`, `akinola2025tacsl`, `leins2025hydroelastictouch`, `luu2025manifeel`, `birtalan2026impact`.

---

## 3 Problem Formulation and Method (≈ 700 words)

**Goal:** a self-contained technical description (not a workflow). Every Results symbol is defined here. Order: probe → force rule → calibration → online.

### 3.1 Problem (≈ 110 w)
- Instance x: object, pose, disturbance stratum D1–D4.
- F\*(x): minimal no-slip hold force under the slip criterion (2 mm tangential, 3°, or contact loss).
- Choose F(x) to minimise E[(F − F\*)/F\*] subject to P(slip at F(x)) ≤ α.
- F\*_lo / F\*_hi / F\*_mid come from 11-replay log-space bisection on [0.1, 100] N. They exist only in simulation.

### 3.2 Grasp protocol and friction-onset probe (≈ 150 w)
- Fixed preload F₀ = 32.7 N for every instance; it encodes neither m nor μ.
- Sequence: lift and hold; squeeze F₀ → 1.5 F₀ → F₀; **ramp-down probe** at a fixed rate.
- A touch-only detector on the pad shear/normal ratio stops at incipient slip. This gives F_onset and μ̂ = m g / (2 F_onset).
- Onset noise: log F_onset + σ ε, σ ∈ {0.1, 0.2, 0.4} (v4; v1 also used σ 0). Primary σ 0.2, assumed.
- The grip then ramps to the chosen hold force F. A slip during the probe counts.
- **State once here:**
  - The protocol is fixed. Preload and squeeze exceed every test instance's F\*_mid.
  - The probe induces micro-slip by design.
  - The method chooses only the hold force.
  - The **no-probe grasp** (S6) uses the same preload and skips the squeeze and probe phases.

### 3.3 Force rules (≈ 170 w)
All rules have the form F(x; λ) = min(F_max, F_base(x) e^λ).
- **Probe plug-in:** F_base = m(g + a_cmd)/(2 μ̂).
- **Shrunk plug-in:** log μ̂_s = a + b log μ̂, with OLS fitted on the selection split only and frozen from v3. σ 0.2: a −0.3858, b 0.7397.
- **Learned probe model (option):** gradient-boosted quantile predictor on proprioception + static touch + squeeze + onset.
- **Friction-blind baseline CSF-1:** F_base = m(g + a_cmd)/(2 μ̄). Selected on the selection split before any calibration or test access.
- **Family prior CSF-fam (new, deployable):** μ̄ per visible family, fitted on calibration objects. On c4: F1 0.379, F2 0.496, F3 0.677, F4 0.852.
- **Supporting arms (one line each, v1–v3):**
  - onset-only learner;
  - oracle-side friction prior μ̃ = clip(μ·exp(σ_p ε_p), 0.1, 3.0);
  - probe + one uniform margin;
  - probe + empirically tuned per-stratum margin;
  - reactive slip-tightening controllers (registered negative control).

### 3.4 Calibration on the physical binary loss (≈ 180 w)
- **Loss:** L_i(λ) = 1{physical slip in direct replay}. Monotonised: L̃_i(λ) = max_{λ' ≥ λ} L_i(λ').
- **CRC (primary):** per stratum, λ̂ = min{λ ∈ Λ : (n R̃_n(λ) + 1)/(n + 1) ≤ α} (`angelopoulos2022conformal`).
  - Then E[slip] ≤ α for an exchangeable test instance.
  - The bound is marginal over instances and friction, and holds in expectation over the calibration draw.
  - It is **not** conditional on stratum realisation or object family.
- **LTT (secondary):** slip risk ≤ α with probability ≥ 1 − δ, δ 0.1, per stratum (`angelopoulos2025learn`, `bian2023training`).
- **Why the physical loss:** the label rule failed the monotonicity gate (8 / 800, CP upper 0.02115 > 0.02, 7 of 8 in D2). Label-route CQR (`romano2019conformalized`) is secondary.
- **Deployability (stated once here and in §6):** offline calibration needs a replay at every grid force, so it is a simulation procedure. The online tracker of §3.5 needs one binary outcome per grasp.

### 3.5 Online calibration from binary feedback (≈ 90 w)
- Score-space quantile tracking (`angelopoulos2023conformala`): q_{t+1} = q_t + η (slip_t − α).
- One tracker per stratum; η = 0.03412 (frozen); anti-windup at F_max.
- Score space rather than ACI (`gibbs2021adaptive`).
- References: decaying step (`angelopoulos2024online`), frozen calibration, oracle recalibration.

**Evidence:**
- `v1:h1m_analysis.json → {non_monotone,"cp_upper_98.75",by_dist}`
- `v3:b1_analysis.json → ols."CSF-shrunk@0.2"`
- `v4:` CSF-fam μ̄ per family (field to confirm)
- `v1:h3_analysis.json → eta`
- `v2:a_analysis.json → {alpha, delta}`

---

## 4 Experimental Setup (≈ 350 words)

**Goal:** enough detail to reproduce the work and to read the decisions. The registration and every deviation are listed here, once.

**Simulator and objects**
- MuJoCo 4.0.0; parallel-jaw gripper with pad touch grids.
- Families: F1 boxes, F2 cylinders, F3 ellipsoids / capsules, F4 off-CoM composites; F5 thin plates / disks (shift only).
- Static-touch check: max |pad normal − F₀| 0.1597 N; preload slip count 0.

**Pools**
- **v1 pool (08c):** μ log-uniform on [0.3, 1.0], independent of all non-tactile inputs; m [0.05, 1.0] kg; n_cal 2,000, n_test 2,800.
- **f4 (fresh, v4):** same design, new objects. 500 cal / 700 test objects. Used for C1–C3 and S1–S3, S6, S7.
- **c4 (friction-correlated, v4):** friction drawn in narrow, mostly non-overlapping family bands. 500 / 700. Used for C4 / C5 and S4.
- No-probe replays: 4,800 instances. 0 duplicates; no model re-trained.

**Strata, shifts and streams**
- Strata: D1 lift acceleration, D2 shake, D3 lateral pull, D4 payload.
- Shifts (online): S1 μ × 0.6, S2 new family F5, S3 amplitude × 1.5. (Shift labels are distinct from the secondary rows S1–S7; the paper calls them "friction / family / amplitude shift" to avoid the clash.)
- Streams: T 2,000, shift at step 501, 20 orderings.

**Statistics**
- **CONF:** C1–C5, Holm at 5 % over five p. p = 0.0 means two-sided p < 0.001; largest Holm bound ≤ 0.005. Superiority if the CI\*\* lower limit > 0; equivalence (C2) by TOST at ±0.10.
- Object-cluster bootstrap, 2,000 draws, all valid. `edge: false` in every v4 row.
- v1 core decisions: Bonferroni over 4. v1 secondaries: Holm within family (52 rows, no v1 verdict changes).
- S1–S7 and the v2 / v3 rows: unadjusted.

**Deviations (one compact paragraph)**
1. The CRC route was written after the monotonicity counts were seen, before any predictor existed.
2. The v1 primary-grid floor was handled by a post hoc refined grid (v1–v3 rows only).
3. Selection-object range typo in the v1 pre-registration (the JSON uses 150–199).
4. v2 / v3 rounds were registered after earlier read-outs and cannot change a v1 decision.
5. The registered physical-replay online oracle was not produced.
6. The v4 amendment was registered before any v4 code or run. The read-out code was committed before any v4 replay and run once.
7. No prediction was registered for C4 / C5, and the registered rule defines only superiority there.

**Evidence:**
- `v1:crc_analysis.json → {n_cal_instances, n_test_instances, draws}`
- `v1:comp_selection.json → objects`
- `v1:19_report_rows.json → static_touch_check`
- `v3:a3_holm.json → families, all`
- `v4:C1`–`C5 → {p, p_holm, edge}`
- `v4:` pool sizes (f4, c4, noprobe)

---

## 5 Results (≈ 1,200 words; Table 1, Fig. 1b, Fig. 2, Table 2, Table 3 — in this order)

**Goal:** quantitative outcomes in this order:
1. confirmatory table;
2. boundary map (σ, width, prior, hold time);
3. how the certificate behaves;
4. supporting attribution from earlier rounds;
5. online shift.

Each subsection opens with its result sentence. Status codes replace hedges.

### 5.1 Confirmatory tests on fresh objects (≈ 300 w; Table 1, Fig. 1b)

**Result sentence:** on 700 fresh test objects at σ 0.2, all three registered predictions hold. On the friction-correlated pool, the family prior beats both tactile arms.

- **C1 (CONF):** probe plug-in vs CSF-1, matched slip: D 0.4314 [0.3824, 0.4835], superiority.
- **C2 (CONF):** learner vs plug-in, matched slip: D 0.01117 [−0.05552, 0.05686], equivalence within ±0.10.
  - Qualifier in the same sentence: on the CRC route (`S5_C2_crc`) D is −0.06291 [−0.1226, 0.08396], so equivalence is not shown there.
  - It is a σ 0.2 result (see §5.2).
- **C3 (CONF):** learner vs CSF-1, CRC route: D 0.4135 [0.3578, 0.4903], superiority. This replicates v1 H2a (D 0.4168 [0.3484, 0.4778] on the v1 pool; seeds 1–4 0.4343 / 0.4197 / 0.3932 / 0.4494).
- **C4 / C5 (CONF, no prediction registered):** on c4, plug-in vs CSF-fam −0.5814 [−0.7208, −0.4563]; learner vs CSF-fam −0.5461 [−0.6590, −0.4290].
  - Registered outcome: not superior. The CI\*\* lies wholly below 0.
  - CSF-fam reaches RE_match 0.2674 at slip 0.05929.
  - On c4 the tactile arms still beat CSF-1: 0.4285 [0.3648, 0.4741] and 0.4412 [0.3876, 0.4817]. CSF-fam vs CSF-1 is 0.6386 [0.6043, 0.6620].
  - CRC-route versions agree in sign: −0.5166 / −0.4733 (C1 on CRC 0.4482).
- **Arm level (one line, Table 1 lower block):** f4 mean hold force: learner 6.115 N, plug-in 6.463 N, shrunk plug-in 6.181 N, CSF-1 7.125 N. On c4, CSF-fam 5.933 N.
- **Reading (one sentence):** the confirmed saving is a saving against a friction-blind prior. When the friction class is visible, a one-number family prior is better than a σ 0.2 probe. No hybrid prior + probe arm was tested (§6).

**Evidence:**
- `v4:C1`–`C5 → {D, CI**, p_holm, decision}`
- `v4:S5_C2_crc`, `v4:S5_C4_crc`, `v4:S5` (C1 CRC, C5 CRC, c4 vs CSF-1 rows, CSF-fam vs CSF-1)
- `v4:` arm table f4 / c4 → {slip, RE, RE_match, hold_F_N_mean}
- `v1:crc_analysis.json → contrasts.{H2a,H2a_seed1..4}`

### 5.2 Boundary map: noise, friction range, hold time (≈ 300 w; Fig. 2)

**Result sentence:** the saving shrinks and then reverses as probe noise rises or the friction range narrows. It repays the probe's force-time only for longer holds.

- **σ band (S1, SEC; Fig. 2a):**
  - D(plug-in vs CSF-1) 0.6486 [0.6100, 0.6733] / 0.4314 / −0.2065 [−0.3280, −0.1112] at σ 0.1 / 0.2 / 0.4. At σ 0.4 the plug-in test slip is 0.1014, above α.
  - Learner vs plug-in: −0.1076 [−0.1819, −0.02922] at σ 0.1 (learner worse; p_tost 0.5445) and 0.3238 [0.2778, 0.3817] at σ 0.4 (learner better). So C2 is a σ 0.2 result.
  - Learner vs CSF-1: 0.5683 / 0.4135 / 0.1675.
  - Opposing earlier finding (one clause): in v3 a shrunk plug-in beat the learner at σ 0.4 (−0.1395 [−0.1832, −0.01264], v1 pool). The cause of the difference is not tested.
- **Friction-width sweep (S3, SEC, descriptive; Fig. 2b):**
  - D(plug-in vs CSF-1) 0.4314 → 0.2414 → −0.1094 → −0.6967 as w goes 1.0 → 0.75 → 0.5 → 0.25. The CI\*\* at w 0.5 is [−0.2383, 0.01393]; at w 0.25 it is [−0.9507, −0.4238].
  - Learner: 0.4377 / 0.2793 / −0.01792 / −0.5039.
  - The sweep crosses 0 between w 0.75 and w 0.5.
  - CSF-1's matched RE falls from 0.7518 to 0.2307, while the plug-in stays between 0.3915 and 0.4275. The decline in D is therefore driven mainly by CSF-1 improving.
  - Sample sizes at w 0.25: 134 cal / 179 test.
  - Hypothesis, not tested: this reflects friction spread relative to probe noise.
  - Consistent in direction with the v1–v3 narrow mid-friction sub-pool (H2-R D −0.2614), no mechanism claimed.
- **Measured break-even (S6, DESC; Fig. 2c):**
  - The no-probe grasp has slip 0.08714 and hold force 7.125 N (λ̂ index 41 in all strata).
  - Integrated force-time at T 1 / 5 / 30 s (N·s):
    - no-probe 22.20 / 50.70 / 228.8
    - learner 39.10 / 63.57 / 216.4
    - plug-in 39.47 / 65.32 / 226.9
    - CSF-1 with probe 40.17 / 68.67 / 246.8
  - Break-even vs the no-probe grasp: learner 17.74 s, plug-in 27.07 s. CSF-1 with the probe never breaks even.
  - Phase integrals (N·s): preload 13.08, squeeze 12.91, ramp-down 1.444, return 0.3480, re-hold 3.27.
  - Reading: for holds of 1–5 s, skipping the probe is cheapest. The fixed preload and squeeze dominate force-time.

**Evidence:**
- `v4:S1 → σ ∈ {0.1,0.2,0.4} × {C1-type, C2-type, C3-type}.{D, CI**, p_tost}`, `v4:` arm `CSF-muhat@0.4` slip
- `v4:S3 → w ∈ {1.0,0.75,0.5,0.25}.{μ window, n_cal, n_test, D muhat, D full, CI**, p, RE_match}`
- `v4:S6 → {noprobe slip, hold_F_N_mean, lam_idx, integrated_Ns T1/T5/T30, break_even_T_s, phase_Ns}`
- `v3:b1_analysis.json → rows."D:full_rd@0.4#0_vs_CSF-shrunk@0.4"`
- `v1:sec08g.json → H2R`

### 5.3 How the certificate behaves (≈ 200 w; Table 2 upper block)

**Result sentence:** over 200 re-splits of the fresh pool, mean slip stays below α for every arm, but the bound is marginal. Single strata and one object family exceed α often.

- **S7 (SEC), CRC.** Mean slip / share of splits > α / share of splits with any stratum > α:
  - learner 0.08360 / 0.095 / 0.7
  - plug-in 0.08513 / 0.08 / 0.645 (D1 share 0.47)
  - CSF-1 0.08670 / 0.145 / 0.315
  - Max split slip 0.1146 / 0.1104 / 0.1271.
- **S7, LTT (more conservative).** Mean 0.06818 / 0.07141 / 0.06929; share > α 0.0 / 0.0 / 0.01; any stratum 0.16 / 0.07 / 0.08.
- **S4 (DESC, single c4 split, about 175 test objects per family, no CIs).**
  - In F1, three of four arms exceed α: CSF-1 0.3157, learner 0.2014, plug-in 0.1143.
  - In F2–F4 all arms are ≤ 0.09. Only CSF-fam stays ≤ α in every family (max 0.09286).
  - Per family D vs CSF-fam: plug-in −0.4441 / −0.3420 / −0.5557 / −0.7373 (F1–F4). The learner's F1 value of 0.1102 comes at slip 0.2014 and is not a like-for-like gain.
- **Label validity (one sentence, v1):** the label monotonicity gate failed (8 / 800). The label vs physical check passes in all four arm × α combinations.
- **Shrunk plug-in (S2, SEC; one sentence):** improves on the raw plug-in, D 0.1119 [0.04864, 0.1449] (TOST p 0.477). Whether the gain exceeds the SESOI is unresolved. Against CSF-1: 0.4950 [0.4514, 0.5273].

**Evidence:**
- `v4:S7 → rules.{crc,ltt}.{full_rd@0.2#0, CSF-muhat@0.2, CSF-1}.{mean_slip, share_above_alpha, q90, max, share_any_stratum_above_alpha, per_stratum}`
- `v4:S4 → family.{F1..F4}.{slip, D muhat vs fam, D full vs fam}`
- `v4:S2`
- `v1:h1m_analysis.json`; `v1:h1v_analysis.json → *.Delta`

### 5.4 Supporting attribution and competitors from earlier rounds (≈ 220 w; Table 2 lower block)

**Result sentence:** on the v1 pool, the same picture appears before the confirmatory round. A tuned margin lands where CRC does. The registered reactive design fails, and the mid-friction band is where the baseline wins.

- **v1 pre-registered learned vs plug-in (PRE):** H2b D 0.0569 [−0.0399, 0.1454], not confirmed. The registered TOST was not met. C2 now supplies the confirmatory answer at σ 0.2 on the matched route.
- **Feature chain (SEC, one sentence):** adding the onset gives D 0.4739 [0.4148, 0.5229]. Full vs onset-only: −0.0534 [−0.1233, 0.0508]. Squeeze: no evidence it helps (−0.0263).
- **Oracle-side prior (SEC, one sentence):** against a prior of log-noise σ_p 0.2, no advantage is shown (−0.0299 [−0.1903, 0.0816]). This is consistent in direction with C4 / C5.
- **Tuned per-stratum margin (v3 A5, SEC):** reproduces the CRC test points on the primary grid (plug-in slip 0.06571, RE 0.4843). At 500 calibration grasps per stratum, CRC adds the finite-sample guarantee, not a different operating point.
- **Reactive slip-tightening (v3 B2, DESC, registered negative control):**
  - Slip ≥ 0.3086 in every arm and stratum.
  - REACT-probe uses a raw μ̂ whose log bias is +0.3186, so the failure is at least partly a design artefact.
  - No claim against reactive control in general.
- **Mid-friction sub-pool (v1 H2-R, SEC):** D −0.2614 [−0.5320, −0.0325] for μ ∈ [0.5, 0.8].
  - Holm p 0.03 within its family, 0.12 over all 52 v1 secondaries.
  - On the refined CRC grid −0.3152; on the primary grid +0.3754.
  - Grid-dependent; slip unmatched; no mechanism.

**Evidence:**
- `v1:crc_analysis.json → contrasts.{H2b,H4e_vs_onset_only}`
- `v1:h4a_label_rule.json → contrasts.{H4a_onset_full_rd_vs_full,H4a_squeeze_full_vs_S}`
- `v2:b_analysis_edge.json → H5."H5@0.2_08e"`
- `v3:a_analysis.json → A4_A5_A6.{"slip:emp:CSF-muhat@0.2","RE:emp:CSF-muhat@0.2"}`
- `v3:b2_analysis.json → arms.*.{overall,stratum}.slip_phys`
- `v1:19_report_rows.json → detector_id_sigma0`
- `v1:sec08g.json → H2R`
- `v3:a3_holm.json → rows[row="sec08g/H2R/CI**"]`
- `v3:a_analysis_08e.json → A4_A5_A6."sub:mu_and_amp:D:full_vs_CSF-1"`
- `v3:a_analysis.json → A4_A5_A6."sub:mu_and_amp:D:full_vs_CSF-1"`

### 5.5 Online calibration under shift (≈ 180 w; Table 3)

**Result sentence:** frozen calibration breaks under friction and amplitude shift. Binary-feedback tracking returns slip near α after a transient, and the probe arm keeps its force advantage. Efficiency vs oracle recalibration stays inconclusive.

- **Pre-registered (PRE, label feedback, 20 orderings):**
  - Frozen probe arm 0.3056 (friction shift) and 0.2461 (amplitude shift); frozen baseline 0.5101 (friction shift).
  - Tracking label slip 0.0999–0.1016.
  - H3 inconclusive: R_E 0.8778 / 1.1739 / 0.9629. The matched-rate co-requirement fails in the friction and family shifts (0.032 / −0.035).
- **Physical feedback (v3 B3, SEC, ordering-only intervals):**
  - Transient 501–1,000: probe arm 0.1389 [0.1365, 0.1413] / 0.0981 / 0.1368 [0.1337, 0.14].
  - Late window 1,501–2,000: 0.1001 / 0.1008 / 0.1018, with intervals containing α. This is consistent with convergence to α.
  - D_RE 0.3107–0.4432 across shifts and windows.
- **Oracle (one sentence):** no physical-replay oracle was produced. The label-route oracle itself slips 0.1346 in the family shift.

**Evidence:**
- `v1:h3_analysis.json → shifts.*.arms.{"Frozen-CertGrip","Frozen-COMP","OQT-CertGrip"}.slip_label_window`, `shifts.*.R_E`, `H3_primary`, `audit."{S1,S2}|matched_physical"`
- `v3:b3_analysis.json → shifts.{S1,S2,S3}.physical_feedback.CertGrip."{501-1000,1501-2000}".slip_phys.{mean,CI95}`, `shifts.*.D_RE.*.point`, `reference_08d_label_route.S2."Oracle-CertGrip".slip_label_window`

---

## 6 Limitations and Discussion (≈ 280 words; each caveat stated here once in full)

**What the evidence licenses (3 sentences):**
1. In simulation, with friction independent of what the robot can see and at onset noise σ 0.2, a ramp-down probe plus a CRC-calibrated one-line plug-in lowers relative excess hold force against a friction-blind conformal baseline. Pooled slip stays near α on average. A learned model is not needed on the registered route.
2. The saving disappears when friction is family-predictable, at σ 0.4, as the friction range narrows, and for holds shorter than 17.74–27.07 s.
3. The practical recommendation is therefore conditional: probe when friction is not predictable from appearance and holds are long.

**Limits (full statements; referenced from elsewhere):**
1. *Simulation only; σ assumed.* One simulator, rigid contact, modelled detector. The sign of the result changes across σ 0.1 → 0.4 (0.6486 → −0.2065). No hardware or published-detector-error grounding was done.
2. *c4 is a stylised correlated design.* It uses narrow, mostly non-overlapping bands. C4 / C5 were measured for one band layout and one σ; their dependence on band width or σ was not tested. **No hybrid prior + probe arm** was tested, so C4 / C5 do not show that touch is useless where a prior exists.
3. *Width sweep descriptive.* One σ; no family prior; small samples at w 0.25. The noise-vs-width reading is a hypothesis.
4. *Marginal guarantee.* Over the pool, in expectation. 31.5–70 % of re-splits have a stratum above α. On the single c4 split, F1 exceeds α for three of four arms. LTT is the conservative alternative. CSF-muhat@0.4 was not re-split.
5. *Deployability.* Offline CRC needs replays at every grid force. The deployable route is online tracking (ordering-only intervals, transient overshoot to 0.1389, no physical-replay oracle). Replay-free calibration was not done.
6. *Fixed high-force protocol.* The 32.7 N preload and the squeeze exceed every instance's F\*_mid and dominate force-time. No adaptive or low preload was run. The work is about hold force, not first-contact force.
7. *Competitors.* Published controllers (`khamis2021real`, `dong2019maintaining`, `boonstra2024estimate`, `niu2026synchronized`) were not reproduced. The one reactive design is a negative control, and its corrected re-design was not run.
8. *Multiplicity.* Holm covers C1–C5 and the v1 secondaries. S1–S7 and the v2 / v3 rows are unadjusted. The S6 break-even depends on commanded profiles and has no interval.

**Future work (one line):** a hybrid family prior + probe rule, probe-noise measurement on hardware with an adaptive preload, and replay-free online calibration.

**Evidence:** as cited in §5; `v4:S4`, `v4:S7`.

---

## 7 Conclusion (≈ 70 words)

**Goal:** restate:
- the confirmed claim: C1 D 0.4314 [0.3824, 0.4835]; C3 0.4135; simulation, marginal;
- the attribution: probe, not learner (C2 equivalent at σ 0.2, matched route);
- the boundary: the family prior wins (C4 −0.5814); σ 0.4 reversal (−0.2065); the width trend; break-even 17.74 s;
- the online finding: consistent with convergence to α; efficiency inconclusive.

**Evidence:** as in the Abstract and §5.1–5.2.

---

## Figure 1 plan (full width, two panels, ≈ 0.35 page)

**Story:** "probe, then calibrate — and when it pays."
- The probe adds friction information at a measured force-time cost.
- Calibration turns a probe-fed rule into one with marginal slip ≤ α.
- The confirmatory tests show for whom it pays: friction-blind priors, yes; a visible family prior, no.

**(a) Protocol timeline with absolute forces** (schematic shape, real numbers):
- Grip force vs time: preload 32.7 N; squeeze to 1.5 F₀; **ramp-down probe** with F_onset marked; return; ramp to the hold force.
- Phase integrals annotated (N·s): preload 13.08, squeeze 12.91, ramp-down 1.444, return 0.3480, re-hold 3.27.
- A dashed alternative trace for the **no-probe grasp** that skips squeeze and probe.
- Hold-force band: learner 6.115 N, plug-in 6.463 N, CSF-1 7.125 N (f4).
- Side note: "break-even vs no-probe 17.74 s (learner)".

**(b) Confirmatory forest plot (real data):**
- Point D with CI\*\* for C1, C2, C3 (f4) and C4, C5 (c4) as horizontal intervals.
- Vertical lines at 0 and ±0.10 (SESOI). C2 is drawn with its ±0.10 equivalence band shaded.
- Status markers: filled for registered predictions met; open for C4 / C5 (no prediction).
- A small grey tick per row at the CRC-route value (C1 0.4482, C2 −0.06291, C4 −0.5166, C5 −0.4733).

**Evidence:**
- `v4:S6 → phase_Ns, hold_F_N_mean (no-probe), break_even_T_s`
- `v4:` f4 arm table → hold_F_N_mean
- `v4:C1`–`C5 → {D, CI**}`
- `v4:S5_C2_crc`, `v4:S5_C4_crc`, `v4:S5` (C1 / C5 CRC)

**Caption (printed; no generation prompt in the manuscript):** *Probe, then calibrate (simulation). (a) Every grasp starts from the same 32.7 N preload, so only the ramp-down probe's onset carries friction information. The method chooses the hold force (mean 6.115 N for the learned model vs 7.125 N for the friction-blind baseline on fresh objects). Against a simulated grasp that skips the probe, the probe's force-time is repaid after a 17.74 s hold. (b) Pre-registered tests on fresh objects: the probe plug-in beats the friction-blind conformal baseline (C1), a learned model is equivalent to the plug-in within ±0.10 (C2), and the earlier result replicates (C3). On a pool where friction follows the visible object family, a family prior beats both tactile arms (C4, C5). Bars are 97.5 % object-cluster bootstrap intervals; grey ticks show the unmatched-slip CRC route.*

## Figure 2 plan (full width, three small panels, ≈ 0.25 page; real data)

**Story:** the boundary map — where the saving holds and where it disappears.

- **(a) σ band:** D vs σ ∈ {0.1, 0.2, 0.4} with CI\*\*.
  - Plug-in vs CSF-1: 0.6486 / 0.4314 / −0.2065.
  - Learner vs CSF-1: 0.5683 / 0.4135 / 0.1675.
  - Learner vs plug-in: −0.1076 / 0.01117 / 0.3238.
  - Lines at 0 and ±0.10.
- **(b) Friction width:** D vs w ∈ {1.0, 0.75, 0.5, 0.25}.
  - Plug-in: 0.4314 / 0.2414 / −0.1094 / −0.6967.
  - Learner: 0.4377 / 0.2793 / −0.01792 / −0.5039.
  - x-axis labels carry the μ window. Caption says "descriptive, σ 0.2".
- **(c) Force-time vs hold duration:** integrated N·s at T 1 / 5 / 30 s for the no-probe grasp, learner, plug-in and CSF-1 with probe (values in §5.2). Break-even markers at 17.74 s and 27.07 s. Points are joined by straight lines and labelled "measured at three T".

**Evidence:**
- `v4:S1`
- `v4:S3`
- `v4:S6`

**Caption (short):** *Boundary map (fresh pool, simulation; secondary rows). (a) The probe's advantage over the friction-blind baseline shrinks with onset noise and reverses at σ 0.4. The learned model is equivalent to the plug-in only at σ 0.2. (b) As the friction range narrows, the baseline improves and the advantage reverses between w 0.75 and 0.5 (σ 0.2). (c) Integrated grip force over the whole grasp: skipping the probe is cheapest for holds of 1–5 s; the probe-fed arms pull ahead only for longer holds.*

---

## Tables (numbered in order of appearance; Status column uses the legend; row # → evidence)

### Table 1 (§5.1): Confirmatory tests and arm-level operating points

| # | Row | Value(s) | Status | Evidence |
|---|---|---|---|---|
| 1 | C1 plug-in vs CSF-1 (f4, matched) | 0.4314 [0.3824, 0.4835], superiority; CRC 0.4482 | CONF | `v4:C1`; `v4:S5` |
| 2 | C2 learner vs plug-in (f4, matched) | 0.01117 [−0.05552, 0.05686], equivalence ±0.10; CRC −0.06291 [−0.1226, 0.08396] not shown | CONF | `v4:C2`; `v4:S5_C2_crc` |
| 3 | C3 learner vs CSF-1 (f4, CRC) | 0.4135 [0.3578, 0.4903], superiority | CONF | `v4:C3` |
| 4 | C4 plug-in vs CSF-fam (c4, matched) | −0.5814 [−0.7208, −0.4563], not superior (CI\*\* < 0); CRC −0.5166 [−0.7461, −0.3859] | CONF | `v4:C4`; `v4:S5_C4_crc` |
| 5 | C5 learner vs CSF-fam (c4, matched) | −0.5461 [−0.6590, −0.4290], not superior (CI\*\* < 0); CRC −0.4733 [−0.6822, −0.3683] | CONF | `v4:C5`; `v4:S5` |
| 6 | c4 tactile arms vs CSF-1; CSF-fam vs CSF-1 | 0.4285 [0.3648, 0.4741] / 0.4412 [0.3876, 0.4817]; 0.6386 [0.6043, 0.6620] | SEC | `v4:S5` |
| 7 | f4 arms: slip / RE_match / hold N | CSF-1 0.08786 / 0.7518 / 7.125; plug-in 0.09786 / 0.4275 / 6.463; shrunk 0.08321 / 0.3797 / 6.181; learner 0.08107 / 0.4227 / 6.115 | DESC | `v4:` f4 arm table |
| 8 | c4 arms: slip / RE_match / hold N | CSF-1 0.08214 / 0.7399 / 7.506; plug-in 0.08607 / 0.4229 / 6.646; learner 0.08821 / 0.4134 / 6.256; CSF-fam 0.05929 / 0.2674 / 5.933 | DESC | `v4:` c4 arm table |
| 9 | v1 H2a on the v1 pool (text) | 0.4168 [0.3484, 0.4778]; seeds 1–4 0.4343 / 0.4197 / 0.3932 / 0.4494 | PRE | `v1:crc_analysis.json → contrasts.{H2a,H2a_seed1..4}` |
| 10 | Baseline selection (text, §1) | CSF-1 0.7686, Mondrian-CSF 0.8294, CertGrip-P 0.8335 | PRE | `v1:comp_selection.json → candidates.*.RE_mean` |

Footnote: two-sided p < 0.001 for all five rows (C2 TOST p < 0.0005); largest Holm bound ≤ 0.005; 2,000 valid draws; `edge: false`.

### Table 2 (§5.3–5.4): Certificate behaviour and supporting rows

| # | Row | Value(s) | Status | Evidence |
|---|---|---|---|---|
| 11 | S7 CRC, 200 re-splits: mean slip / share > α / any stratum > α | learner 0.08360 / 0.095 / 0.7; plug-in 0.08513 / 0.08 / 0.645; CSF-1 0.08670 / 0.145 / 0.315 | SEC | `v4:S7 → rules.crc.*` |
| 12 | S7 LTT | learner 0.06818 / 0.0 / 0.16; plug-in 0.07141 / 0.0 / 0.07; CSF-1 0.06929 / 0.01 / 0.08 | SEC | `v4:S7 → rules.ltt.*` |
| 13 | S4 c4 per family, F1 slip | CSF-1 0.3157, learner 0.2014, plug-in 0.1143; CSF-fam max 0.09286; F2–F4 all ≤ 0.09 | DESC | `v4:S4` |
| 14 | S2 shrunk vs raw plug-in; vs CSF-1 | 0.1119 [0.04864, 0.1449] (TOST p 0.477); 0.4950 [0.4514, 0.5273] | SEC | `v4:S2` |
| 15 | v1 H2b learned vs plug-in | 0.0569 [−0.0399, 0.1454], not confirmed | PRE | `v1:crc_analysis.json → contrasts.H2b` |
| 16 | Label monotonicity / validity (text) | 8 / 800, CP upper 0.02115; label vs physical all pass | PRE | `v1:h1m_analysis.json`; `v1:h1v_analysis.json` |
| 17 | Tuned per-stratum margin, plug-in (primary grid) | slip 0.06571, RE 0.4843 (= CRC) | SEC | `v3:a_analysis.json → A4_A5_A6.{"slip:emp:CSF-muhat@0.2","RE:emp:CSF-muhat@0.2"}` |
| 18 | Reactive slip-tightening (all arms) | slip ≥ 0.3086 every arm and stratum; REACT-probe 0.9921 / 0.9514 | DESC | `v3:b2_analysis.json → arms.*` |
| 19 | Mid-friction sub-pool μ ∈ [0.5, 0.8] | label route −0.2614 [−0.5320, −0.0325] (Holm 0.03 family / 0.12 all); refined CRC −0.3152 [−0.5231, −0.0172]; primary +0.3754 | SEC | `v1:sec08g.json → H2R`; `v3:a3_holm.json`; `v3:a_analysis_08e.json`, `v3:a_analysis.json → A4_A5_A6."sub:mu_and_amp:D:full_vs_CSF-1"` |

### Table 3 (§5.5): Online calibration under shift (friction / family / amplitude)

| # | Row | Value(s) | Status | Evidence |
|---|---|---|---|---|
| 20 | Frozen probe arm / frozen baseline, label slip | 0.3056 / 0.5101; 0.1017 / 0.1051; 0.2461 / 0.1910 | PRE | `v1:h3_analysis.json → shifts.*.arms."Frozen-*".slip_label_window` |
| 21 | Tracking probe arm, label feedback (slip / RE) | 0.1016 / 0.4763; 0.0999 / 0.4262; 0.1000 / 0.5067 | PRE | `v1:h3_analysis.json → shifts.*.arms."OQT-CertGrip"` |
| 22 | H3 efficiency vs oracle | R_E 0.8778 [0.7404, 1.1204]; 1.1739 [1.0234, 1.4283]; 0.9629 [0.8363, 1.1449]; inconclusive | PRE | `v1:h3_analysis.json → shifts.*.{R_E,"R_E_CI**"}, H3_primary` |
| 23 | Physical feedback, transient 501–1,000 (probe / CSF-1) | 0.1389 / 0.2087; 0.0981 / 0.0938; 0.1368 / 0.126 | SEC | `v3:b3_analysis.json → shifts.*.physical_feedback.{CertGrip,CSF1}."501-1000".slip_phys` |
| 24 | Physical feedback, late 1,501–2,000 (probe slip [CI95] / RE) | 0.1001 [0.0969, 0.1033] / 0.4746; 0.1008 [0.0974, 0.1043] / 0.4144; 0.1018 [0.098, 0.1055] / 0.4999 | SEC | `v3:b3_analysis.json → shifts.*.physical_feedback.CertGrip."1501-2000"` |
| 25 | Label-route oracle slip (reference) | 0.0751; 0.1346; 0.0863 | PRE | `v3:b3_analysis.json → reference_08d_label_route.*."Oracle-CertGrip".slip_label_window` |

---

## Ablation rows appearing in Results (mapped to result keys)

| Ablation (what is removed / swapped) | Row | Value | Key |
|---|---|---|---|
| Remove probe information (plug-in → friction-blind μ̄) | C1 | 0.4314 [0.3824, 0.4835] | `v4:C1` |
| Remove learner (learner → one-line plug-in) | C2 | 0.01117 [−0.05552, 0.05686]; CRC −0.06291 | `v4:C2`, `v4:S5_C2_crc` |
| Learner vs friction-blind (replication) | C3 | 0.4135 [0.3578, 0.4903] | `v4:C3` |
| Swap friction-blind for a deployable family prior | C4 / C5 | −0.5814 / −0.5461 | `v4:C4`, `v4:C5` |
| Remove the probe phases entirely (no-probe grasp) | S6 | break-even 17.74 / 27.07 s; T 1 s 22.20 vs 39.10 N·s | `v4:S6` |
| Vary probe noise | S1 | 0.6486 / 0.4314 / −0.2065 | `v4:S1` |
| Narrow the friction range | S3 | 0.4314 → −0.6967 | `v4:S3` |
| Shrink the plug-in estimate | S2 | 0.1119 vs raw | `v4:S2` |
| Matched-slip → CRC route | S5 | C1 0.4482, C4 −0.5166, C5 −0.4733 | `v4:S5`, `v4:S5_C4_crc` |
| CRC → LTT; re-split the pool | S7 | Table 2 rows 11–12 | `v4:S7` |
| Remove the onset from the learner's features | v1 H4a | 0.4739 [0.4148, 0.5229] | `v1:h4a_label_rule.json → contrasts.H4a_onset_full_rd_vs_full` |
| Remove the squeeze | v1 H4a | −0.0263 | `v1:h4a_label_rule.json → contrasts.H4a_squeeze_full_vs_S` |
| Replace CRC by a tuned per-stratum margin | v3 A5 | slip 0.06571, RE 0.4843 | `v3:a_analysis.json → A4_A5_A6` |
| Replace calibration by reactive tightening | v3 B2 | slip ≥ 0.3086 | `v3:b2_analysis.json` |
| Replace probe by oracle-side prior σ_p 0.2 | v2 H5 | −0.0299 [−0.1903, 0.0816] | `v2:b_analysis_edge.json → H5."H5@0.2_08e"` |
| Frozen vs tracking calibration under shift | v1 H3, v3 B3 | Table 3 | `v1:h3_analysis.json`; `v3:b3_analysis.json` |

---

## Space plan (5 pages)
- Figures: Fig. 1 ≈ 0.35 page; Fig. 2 ≈ 0.25 page.
- Tables: Table 1 ≈ 0.35 page (rows 1–8 printed; 9–10 in text); Table 2 ≈ 0.35 page (rows 11–14, 17–19 printed; 15–16 in text); Table 3 ≈ 0.25 page.
- Text by section: Intro 450, Related 300, Method 700, Setup 350, Results 1,200, Limitations 280, Conclusion 70 = **3,350 words**.
- Every number in prose has a table row above, or a key in its subsection's evidence list.

## Gate required-action ledger (for the stage-19 response; not printed)

| Gate action (v3 stage 20) | Status in v4 | Where |
|---|---|---|
| Confirmatory replication of attribution on fresh objects, matched slip | done: C1, C2 (σ 0.2, matched route only), C3 | §5.1, Table 1, Fig. 1b |
| Correlated-friction pool + deployable prior + width sweep | done: C4 / C5, S3 (descriptive) | §5.1–5.2, Fig. 2b |
| Simulate the no-probe grasp | done: S6 | §5.2, Fig. 1a, 2c |
| Ground σ or report a band as primary | band reported (S1); hardware grounding not done | §5.2, Fig. 2a, §6 limit 1 |
| Abstract / contributions readability | done (three-sentence structure) | Abstract, §1 |
| Hedges once; status legend | done | Legend, §6 |
| Reframe title / temper motivation | done | Title, §1 ¶1, §6 limit 6 |
| Remove Figure 1 prompt; real Figure 2 | done | Fig. 1 caption only; Fig. 2 real data |
