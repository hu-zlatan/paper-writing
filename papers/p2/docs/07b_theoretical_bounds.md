# Stage 8.5 · THEORETICAL_BOUNDS — paper 2 (CertGrip), preliminary

Prompt template: `pipeline/references/stage_prompts/theoretical_bounds.md`, verbatim (system "You are a theoretical
computer scientist with a strong applied math background. You produce concise, honest preliminary analysis — never
fabricate proofs or guarantees. When the analysis is informal, mark it clearly as such."; user: required sections 1–6),
{hypotheses} = `docs/07_hypotheses.md`, {method_sketch} = its §1.4 (one-sided multiplicative CQR, Mondrian strata,
score-space online quantile tracking with anti-windup). Written by this session (strongest model). The two guarantees
below are standard results restated for our setting with their premises; nothing here is new theory, and nothing here
is a measured result.

## 1. Setup & notation

- Grasp instance i = (object, pose offset, disturbance); features x_i (proprioception, mass, disturbance type, tactile,
  probe-squeeze response). Minimal no-slip normal force F\*_i; bisection bracket [F\*_lo, F\*_hi] with
  F\*_hi / F\*_lo ≤ 1 + ε (ε ≈ 0.007 at the planned depth).
- Slip outcome at force F: Y_i(F) ∈ {0, 1}. **Monotonicity premise (M):** Y_i(F) = 1{F < F\*_i} for all F in
  [F_min, F_max].
- Quantile model ĝ_τ(x), τ = 1 − α. Score s_i = log F\*_hi,i − log ĝ_τ(x_i). Calibration set of n instances (from
  m_c objects; strata by family × disturbance for the Mondrian variant). q̂ = ⌈(n+1)(1−α)⌉-th smallest score.
  Chosen force F(x) = min(F_max, ĝ_τ(x)·e^{q̂}).
- Online: stream t = 1..T; q₁ = q̂; F_t = min(F_max, ĝ_τ(x_t)·e^{q_t}); after acting observe slip_t = Y_t(F_t);
  if F_t < F_max: q_{t+1} = q_t + η (slip_t − α), else q_{t+1} = q_t (anti-windup).
- Predictor: gradient-boosted trees with B trees of depth d; feature dimension p; training size N.

## 2. Time complexity

| Operation | Cost | Note |
|---|---|---|
| Label one instance (bisection) | O(k · C_sim) with k = ⌈log₂(log(F_max/F_min)/log(1+ε))⌉ replays | k ≈ 10 for F_max/F_min = 50 and ε = 0.007; C_sim = one replay (≈ seconds, pilot-measured). This dominates the whole study. |
| Monotonicity grid (H1-M) | O(G · C_sim) per instance, G = grid points | G = 40 in the pre-registration; 800 instances → 32,000 replays. |
| Train ĝ_τ | O(B · N p log N) (histogram GBDT: O(B · N p)) | Once per seed and τ. |
| Calibrate (offline) | O(n · B d) to score + O(n) selection (quickselect) or O(n log n) sort | Per stratum for Mondrian; total O(n log n). |
| Decide a force (offline method) | O(B d) | One tree-ensemble evaluation + one exp; microseconds to sub-ms on CPU. |
| Online update | O(1) per step | One addition; no stored scores. |
| ACI (exploratory) | O(log n) per step (lookup in sorted scores) | Needs the calibration scores in memory. |

## 3. Space complexity

- Offline: O(n) scores (only q̂ must be kept at deployment, i.e. O(1)), plus O(B · 2^d) for the model.
- Online OQT: O(1) state (q_t). ACI: O(n). Oracle recalibration: O(n_oracle) labelled shifted instances — the
  labels, not the memory, are the real cost (they need F\*, unavailable on hardware).

## 4. Convergence / validity statements

**(G1) Offline marginal validity — standard theorem, restated.** If calibration and test instances are exchangeable
(here: objects exchangeable and instances drawn i.i.d. within objects, with the split made at the object level, and
the test object drawn from the same population), then for the label rule
  α − 1/(n+1) ≤ P(F\*_hi,test > F(x_test)) ≤ α
(the lower inequality needs continuous scores / no ties; with F_max capping, the event F\*_hi > F_max counts as a miss
and the upper bound still holds) — `lei2017distribution`, `angelopoulos2023conformal`; per stratum for the Mondrian
variant. **Caveat — object clustering:** with several instances per object, exchangeability holds at the object level;
the clean statement is for one test instance from a fresh object with calibration *objects* exchangeable. Using several
instances per calibration object makes the scores within an object dependent; validity in the instance-level sense is
then not covered by the plain theorem. The design (07_hypotheses UT3) checks it by object-level re-splits. A rigorous
clustered version (e.g. calibrate on one randomly chosen instance per object, or a cluster-level score) is known to
restore the bound at a cost in n; which one we use is a stage-9 decision.
**From labels to physical slip:** under (M), F ≥ F\*_hi ⇒ F ≥ F\* ⇒ no slip, so
  P(slip at F) ≤ P(F < F\*_hi) ≤ α.
Using F\*_hi (upper bracket end) makes the label rule conservative by at most the bracket width ε in force; using the
midpoint can under-cover by at most the probability mass of F\* within a bracket of the chosen force (bounded by the
replay audit, H1). Without (M) this implication fails, and the slip loss is not monotone in F; conformal risk control
for non-monotone losses (`angelopoulos2026conformal`) then gives a weaker, stability-dependent bound — that is the
pre-registered fallback.

**(G2) Online long-run slip rate — deterministic bound, restated.** For OQT with constant η and anti-windup, summing
the update over uncapped steps U ⊆ {1..T} gives the identity
  Σ_{t∈U} (slip_t − α) = (q_{T+1} − q₁)/η,
so |(1/|U|) Σ_{t∈U} slip_t − α| ≤ (max_t q_t − min_t q_t)/(η |U|). This needs **no** distributional assumption
(any sequence of instances, any shift) and **does not need (M)** — it controls the observed slip frequency directly,
because the feedback *is* the slip event (`angelopoulos2023conformala`; the level-space analogue is
`gibbs2021adaptive`). It is only informative if q stays bounded: q_t increases by η(1−α) after a slip and decreases by
ηα otherwise; once e^{q_t}·ĝ exceeds F\* for the bulk of instances, slips become rarer than α and q drifts down, so q is
bounded whenever the shifted F\*/ĝ ratio has a finite (1−α)-quantile reachable below F_max. **Informal argument; a full
boundedness proof for an arbitrary sequence is not available** — it fails exactly when the shift pushes F\* above
F_max for more than an α fraction of instances (then every step is capped and the anti-windup freezes q), which UT8
rules out by design. Caveats: (i) the bound covers uncapped steps only; capped steps are counted and reported
separately; (ii) it is a long-run *average* statement — the transient after a shift spends exactly Δq/η "extra"
slips (identity above), so the transient cost is the size of the shift in score space divided by η; (iii) it says
nothing about force efficiency.

**Rate.** For a stationary segment, deviation ≤ R/(η T) with R the range of q; with η = 0.1·IQR and R of a few IQR,
this is O(10–50/T) — e.g. ≤ 0.02 after a few thousand uncapped steps (rough, to be replaced by the pilot's score IQR).

## 5. Comparison with the closest baselines

| Method | Guarantee | Assumptions | Decision cost |
|---|---|---|---|
| Fixed safety factor on a friction-model force (`khamis2021real`) | none on slip rate | friction estimate | O(1) |
| CSF calibrated on the calibration set (1-parameter conformal) | G1 holds (it is split conformal with ĝ = nominal force) | exchangeability | O(1) |
| Mondrian-CSF | G1 per stratum | exchangeability within strata; strata known | O(1) |
| CertGrip (offline) | G1 | exchangeability; (M) for physical slip | O(B d) |
| CertGrip-online (OQT) | G2 (long-run, any sequence) | bounded q (UT8) | O(1) |
| CVaR friction margin (`enwerem2026firmgrasp`) | P(force closure) ≥ β *under the assumed friction distribution* | correct friction prior | optimisation per grasp (not stated in abstract) |
| Tactile CBF grasping (`kim2024robust`, `cortez2019control`) | deterministic constraint satisfaction | bounded disturbance / model | QP per control step |
| Online conformal with safety feedback (`zhang2024bayesian`) | long-run violation rate | — (BO setting) | GP update |

Asymptotically all conformal variants have the same guarantee; they differ only in force efficiency (the quantity H2
measures) and in what they need at deployment (labels vs binary feedback). CertGrip's decision is slower than a scalar
factor by one tree-ensemble call, negligible against a grasp cycle.

## 6. Honesty section

- **(M) can fail** in MuJoCo (soft-contact penetration, rolling/ejection at high force, wedging): then G1 bounds label
  coverage, not slip. Invalidating observation: non-monotone fraction above the H1-M gate, or a replay audit gap > 0.02.
- **Object-level dependence** can make instance-level coverage deviate from α even when G1's object-level form holds;
  invalidating observation: UT3 re-split mean outside its band.
- **Exchangeability fails under shift by construction**; G1 then gives nothing, which is why the online variant exists.
  G2 survives shift but only on average and only if q stays bounded (UT8).
- **Determinism / label noise**: if replays are not bit-identical across runners (UT6), F\* is a random variable and the
  bracket bound is not exact.
- **Sim-to-real**: none of the bounds concerns the real world beyond G2's assumption-free structure; offline calibration
  on hardware would need F\* labels that hardware does not provide (stated limitation).
- **Efficiency has no guarantee**: G1/G2 hold for any predictor, including a useless one (which yields large forces).
  Whether touch reduces force excess (H2) is purely empirical.
