# p2 CertGrip: Stage-14 analysis of iteration v3 (pass 1)

Scope: every v3 row is **secondary** (amendment 10 + addendum 10a). The v1 primary read-outs (H2a / H2b on the CRC route, `results/v1/crc_analysis.json`; H3 on label-rule feedback, `results/v1/h3_analysis.json`) and the v2 verdicts are **not re-decided**. The v3 rows are read against them. α = 0.1 throughout. CI** = 97.5 % object-cluster bootstrap, 2,000 draws, with λ̂ refitted on each draw. B3 intervals are 95 % intervals over orderings only.

Notation: "full σ" = CertGrip-full (`full_rd@σ#seed`); "plug-in σ" = CSF-μ̂ σ; "shrunk σ" = CSF-shrunk σ (B1); RE = RE_mid. D is the relative RE reduction of the target against the comparator. Arithmetic check: H2a gives 1 − 0.4567 / 0.7832 = 1 − 0.5831 = 0.4169 ≈ 0.4168, and B1 σ 0.4 gives 1 − 0.6735 / 0.591 = −0.1396 ≈ −0.1395. Numbers are quoted to the precision of the data files, rounded to 4 significant digits. The text names any grid other than 08c.

---

## 1. Metrics Summary

### 1.1 v1 primary anchors (unchanged)

| Read-out | Target vs comparator | D (mid) | CI** (mid) | v1 decision |
|---|---|---|---|---|
| H2a | full 0.2 #0 vs CSF-1 | 0.4168 | [0.3484, 0.4778] | superiority |
| H2b | full 0.2 #0 vs plug-in 0.2 | 0.05692 | [−0.03992, 0.1454] | not confirmed |
| H4e | full 0.2 #0 vs P_onset 0.2 | −0.05341 | [−0.1233, 0.05081] | not confirmed |
| H2b σ 0.0 / 0.1 / 0.4 | full σ vs plug-in σ | 0.246 / 0.1072 / 0.3182 | [0.1617, 0.2953] / [0.03332, 0.1919] / [0.2287, 0.406] | superiority (all three) |
| H3 S1 / S2 / S3 | OQT-CertGrip, R_E | 0.8778 / 1.174 / 0.9629 | [0.7404, 1.12] / [1.023, 1.428] / [0.8363, 1.145] | inconclusive (all three) |

v1 arm-level values (08c, test, n = 2,800): full 0.2 #0 slip 0.08286 and RE 0.4567; CSF-1 slip 0.1021 and RE 0.7832; plug-in 0.2 slip 0.06571 and RE 0.4843.

### 1.2 A1: repeated object re-splits (R = 200, seed 3031)

| Rule / grid | Arm | mean slip | share splits > α | q90 | min–max | share any stratum > α |
|---|---|---|---|---|---|---|
| CRC 08c | full 0.2 | 0.08469 | 0.05 | 0.09682 | 0.05857–0.1211 | 0.57 |
| CRC 08c | plug-in 0.2 | 0.07121 | 0.0 | 0.07932 | 0.05071–0.09143 | 0.405 |
| CRC 08c | CSF-1 | 0.08514 | 0.12 | 0.1011 | 0.045–0.1429 | 0.41 |
| CRC 08e | full 0.2 | 0.08516 | 0.09 | 0.09861 | 0.06107–0.1164 | 0.69 |
| CRC 08e | plug-in 0.2 | 0.08466 | 0.035 | 0.09679 | 0.0625–0.1157 | 0.475 |
| CRC 08e | CSF-1 | 0.08646 | 0.075 | 0.09893 | 0.04714–0.1382 | 0.615 |
| LTT 08c | full / plug-in / CSF-1 | 0.06826 / 0.06199 / 0.0685 | 0.005 / 0.0 / 0.005 | 0.07964 / 0.07179 / 0.08682 | — | 0.07 / 0.075 / 0.105 |
| LTT 08e | full / plug-in / CSF-1 | 0.07045 / 0.07102 / 0.0673 | 0.0 / 0.0 / 0.015 | 0.08107 / 0.08182 / 0.08793 | — | 0.105 / 0.13 / 0.06 |

Per-stratum CRC: no per-stratum mean slip exceeds α. The largest are 0.0913 (CSF-1 D3, 08c) and 0.09143 (CSF-1 D3, 08e). Per-split exceedance shares within a single stratum reach 0.305 (full D2, 08c), 0.445 (full D2, 08e), 0.435 (CSF-1 D4, 08e) and 0.335 (plug-in D3, 08c).

### 1.3 A2: slip tables (08c, test)

Per-seed results for full 0.2, seeds 0–4: slip 0.08286 / 0.09 / 0.08357 / 0.07929 / 0.1018; RE 0.4567 / 0.443 / 0.4545 / 0.4752 / 0.4313. Seed 4 lies above α on this single split.

Slip by friction quintile of true μ (edges 0.3732 / 0.4731 / 0.614 / 0.7822), lowest to highest μ:

| Arm (08c) | Q1 | Q2 | Q3 | Q4 | Q5 |
|---|---|---|---|---|---|
| full 0.2 #0 | 0.2161 | 0.1179 | 0.05893 | 0.01786 | 0.003571 |
| full 0.4 #0 | 0.3196 | 0.075 | 0.01429 | 0.001786 | 0.0 |
| plug-in 0.2 | 0.08571 | 0.0875 | 0.07321 | 0.05357 | 0.02857 |
| CSF-1 | 0.4804 | 0.02857 | 0.001786 | 0.0 | 0.0 |

The 08e grid gives the same pattern: full 0.2 Q1 0.2464 and CSF-1 Q1 0.4607. The largest family × stratum cells (n = 175) are full 0.2 #0 F1D1 0.1257 and F2D4 0.1143, CSF-1 F4D4 0.1371, and plug-in 0.2 F4D4 0.12.

08e versus 08c arm-level values (test): full 0.2 slip 0.09 and RE 0.4442 (08c: 0.08286 and 0.4567); CSF-1 0.09964 and 0.7778 (0.1021 and 0.7832); plug-in 0.2 0.075 and 0.4551 (0.06571 and 0.4843); plug-in 0.0 0.07821 and 0.208 (0.02679 and 0.3335); plug-in 0.1 0.07607 and 0.2915 (0.0425 and 0.3662).

### 1.4 A3: Holm as registered

| Family | m | rejected at 5 % (Holm within family) |
|---|---|---|
| H1c | 12 | 8 |
| H2-x | 29 | 27 |
| H3-x | 4 | 2 |
| H4-x | 6 | 3 |
| All v1 secondary rows | 52 | 40 |

Arithmetic: 12 + 29 + 4 + 6 = 51, and the 52nd row is `sec08g/oracle_decomposition`, which has no family. Exactly one row changes status between the family-wise and the all-rows Holm: **08g H2-R** (CI [−0.532, −0.03249], p 0.01). Its Holm p-value is 0.03 within the family (rejected) and 0.12 over all rows (not rejected). The rows that are not rejected are H4c (p 0.119), H2M change (p 0.943), H4d full_rd and full (p 0.316, 0.804), all four H1c RAW-Qv rows (p 0.438, 0.159, 0.435, 0.11), H3s S2 (p 0.997), H3s S1m (p 0.101) and massnoise change (p 0.079).

### 1.5 A4: losing sub-pool on the CRC route

Sub-pool sizes (cal / test): μ and amplitude 352 / 548; μ only 724 / 1,060; amplitude only 983 / 1,417.

| Sub-pool | Grid | D full 0.2 vs CSF-1 [CI**] | decision | D plug-in 0.2 vs CSF-1 [CI**] | decision | CSF-1 slip / RE | full slip / RE |
|---|---|---|---|---|---|---|---|
| μ and amp | 08c | 0.3754 [0.2648, 0.4823] | superiority | 0.2492 [0.09255, 0.3541] | superiority | 0.03285 / 0.566 | 0.08759 / 0.3535 |
| μ and amp | **08e** | **−0.3152 [−0.5231, −0.0172]** | **inferiority** | −0.6804 [−0.9734, −0.2175] | inferiority | 0.1004 / 0.2633 | 0.08394 / 0.3463 |
| μ only | 08c | 0.3387 [0.2423, 0.4278] | superiority | 0.2011 [0.1054, 0.3115] | superiority | 0.03396 / 0.6167 | 0.07264 / 0.4078 |
| μ only | **08e** | **−0.1717 [−0.4275, −0.01539]** | **inferiority** | −0.3705 [−0.6279, −0.1119] | inferiority | 0.08208 / 0.3281 | 0.08585 / 0.3844 |
| amp only | 08c | 0.5004 [0.4237, 0.5516] | superiority | 0.4751 [0.3877, 0.5327] | superiority | 0.09951 / 0.786 | 0.09174 / 0.3927 |
| amp only | 08e | 0.4929 [0.4251, 0.5537] | superiority | 0.4869 [0.394, 0.5508] | superiority | 0.0988 / 0.7822 | 0.09174 / 0.3966 |

### 1.6 A5: empirical margin without the (n+1) correction

On 08c, the empirical λ̂ reproduces the CRC point values for all three arms: full 0.2 slip 0.08286 and RE 0.4567; plug-in 0.2 0.06571 and 0.4843; CSF-1 0.1021 and 0.7832. Only the CIs differ, for example full RE emp [0.4054, 0.4996] against CRC [0.4079, 0.5033]. D_emp(full vs CSF-1) = 0.4168, with CI [0.3514, 0.4817] against CSF-1 CRC and [0.3481, 0.4789] against CSF-1 emp (superiority). D_emp(plug-in vs CSF-1) = 0.3816 [0.3014, 0.4517] (superiority).

On 08e, full and CSF-1 again match CRC. Plug-in 0.2 moves from slip 0.075 and RE 0.4551 (CRC) to 0.07964 and 0.4409 (emp). D_emp(full vs CSF-1) = 0.4289 [0.3606, 0.4787] and D_emp(plug-in vs CSF-1) = 0.4331 [0.3344, 0.4956], both superiority.

### 1.7 A6: direct learned vs plug-in (full 0.2 vs plug-in 0.2)

| Contrast | 08c point [CI**] | 08e point [CI**] | decision |
|---|---|---|---|
| CRC | 0.05692 [−0.03992, 0.1454] | 0.02397 [−0.09487, 0.1001] | not shown / not shown |
| LTT | 0.05379 [−0.0568, 0.1222] | −0.004233 [−0.08602, 0.1069] | not shown / not shown |
| matched slip | −0.02384 [−0.08446, 0.01937] | −0.06104 [−0.1104, 0.01228] | not shown / not shown |

LTT arm values (08c): full slip 0.06964 and RE 0.4895; plug-in 0.05286 and 0.5173; CSF-1 0.09071 and 0.8216.

### 1.8 A7: force in newtons (08c, avoidable test rows, n = 2,800)

F*_mid has quantiles 10 / 50 / 90 % of 0.9549 / 3.184 / 11.35 N, a mean of 4.898 N and a maximum of 31.87 N. The share of rows with F*_mid above the preload (32.7 N) is 0.0, and the share above the squeeze peak is also 0.0.

| Arm | hold F mean / median (N) | excess mean / median (N) |
|---|---|---|
| full 0.2 #0 | 6.521 / 4.473 | 1.623 / 0.99 |
| full 0.4 #0 | 7.21 / 5.191 | 2.312 / 1.41 |
| plug-in 0.2 | 7.062 / 4.556 | 2.164 / 1.128 |
| plug-in 0.4 | 9.442 / 5.677 | 4.544 / 2.168 |
| CSF-1 | 7.606 / 5.476 | 2.708 / 1.64 |
| P_onset 0.2 #0 | 6.519 / 4.423 | 1.621 / 0.9498 |

Shared phase force-time, common to every arm in these replays: preload 13.08, squeeze 12.91 and ramp-down 1.439 N·s, which sum to 27.429 N·s.

Worked arithmetic, using the mean hold F and the definition integrated = phases + F·T. The full 0.2 saving against CSF-1 is 7.606 − 6.521 = 1.085 N, so 1.085 N·s at T = 1 s, 5.425 N·s at T = 5 s and 32.55 N·s at T = 30 s. Against the phase total of 27.429 N·s, the saving is 1.085 / (27.429 + 7.606) = 1.085 / 35.035 ≈ 3.1 % of CSF-1's total at T = 1 s, and 32.55 / (27.429 + 228.18) = 32.55 / 255.609 ≈ 12.7 % at T = 30 s.

### 1.9 B1: shrunk plug-in

The OLS fit of log μ on log μ̂ over the selection split (n_sel 800) gives a = −0.3858 and b = 0.7397 at σ 0.2, and a = −0.4738 and b = 0.4044 at σ 0.4.

| Contrast | Grid | D [CI**] | decision |
|---|---|---|---|
| full 0.2 vs shrunk 0.2 | 08c (shrunk λ̂ at index 0 in D1 and D2) | −0.03216 [−0.09825, 0.07434] | not shown |
| full 0.2 vs shrunk 0.2 | edge rule (shrunk 08e, full 08c) | −0.06463 [−0.1851, 0.008734] | not shown |
| full 0.2 vs shrunk 0.2 | same grid (08e recipe) | −0.03532 [−0.1688, 0.01035] | not shown |
| **full 0.4 vs shrunk 0.4** | 08c | **−0.1395 [−0.1832, −0.01264]** | **inferiority** |
| shrunk 0.2 vs CSF-1 | 08c / edge / same grid | 0.435 / 0.4522 / 0.4484 | superiority (all three) |
| shrunk 0.4 vs CSF-1 | 08c | 0.2454 [0.1679, 0.2989] | superiority |

Arm values: shrunk 0.2 slip 0.07179 and RE 0.4425 (08c), 0.07714 and 0.429 (08e); shrunk 0.4 slip 0.09286 and RE 0.591; full 0.4 slip 0.08214 and RE 0.6735.

### 1.10 B2: reactive slip-tightening (test, n = 2,800)

| Arm | slip | RE (final F) | mean steps | share at 4-step cap | F_end mean (N) |
|---|---|---|---|---|---|
| REACT-blind c 0.5 | 0.765 | −0.1731 | 2.501 | 0.2446 | 3.367 |
| REACT-blind c 0.75 | 0.4632 | 0.4185 | 3.099 | 0.5425 | 5.75 |
| REACT-probe c 0.5 | 0.9921 | −0.6358 | 0.4964 | 0.007857 | 1.766 |
| REACT-probe c 0.75 | 0.9514 | −0.4534 | 0.5079 | 0.02 | 2.596 |

Per stratum, REACT-blind c 0.75 has slip 0.3414 / 0.3086 / 0.6057 / 0.5971 in D1–D4. Every B2 arm and stratum lies well above α.

### 1.11 B3: online OQT with physical feedback (20 orderings, 95 % ordering intervals)

| Shift | Window | CertGrip slip | CertGrip RE | CSF1 slip | CSF1 RE | D_RE [CI95] |
|---|---|---|---|---|---|---|
| S1 | 1–500 | 0.0997 | 0.419 | 0.1058 | 0.7524 | 0.4432 [0.4357, 0.451] |
| S1 | 501–1000 | **0.1389** [0.1365, 0.1413] | 0.3936 | **0.2087** | 0.571 | 0.3107 [0.2893, 0.3293] |
| S1 | 1501–2000 | 0.1001 | 0.4746 | 0.0993 | 0.8115 | 0.4152 [0.4025, 0.4275] |
| S2 | 1–500 | 0.0981 | 0.4204 | 0.1039 | 0.7517 | 0.4408 [0.4306, 0.4493] |
| S2 | 501–1000 | 0.0981 | 0.4359 | 0.0938 | 0.7577 | 0.4247 [0.4172, 0.4327] |
| S2 | 1501–2000 | 0.1008 | 0.4144 | 0.1025 | 0.7325 | 0.4342 [0.4203, 0.4491] |
| S3 | 1–500 | 0.0988 | 0.4178 | 0.1044 | 0.7474 | 0.441 [0.4311, 0.4503] |
| S3 | 501–1000 | **0.1368** [0.1337, 0.14] | 0.435 | **0.126** | 0.773 | 0.4373 [0.4252, 0.4508] |
| S3 | 1501–2000 | 0.1018 | 0.4999 | 0.0999 | 0.8684 | 0.4243 [0.4129, 0.4355] |

Arithmetic check of D_RE for S1 1–500: 1 − 0.419 / 0.7524 = 1 − 0.5569 = 0.4431 ≈ 0.4432.

---

## 2. Comparative Findings

**F1. H2a (learned against friction-blind CSF-1) survives every v3 robustness row.**
- The v1 D of 0.4168 [0.3484, 0.4778] reappears on the refined grid as D_emp 0.4289 [0.3606, 0.4787].
- It is unchanged under the uncorrected empirical margin (0.4168 [0.3514, 0.4817]).
- In the online physical-feedback study, CertGrip against CSF1 gives D_RE between 0.3107 and 0.4432 in every shift and window. The ordering intervals are all far from 0.
- In newtons, the mean hold-force saving against CSF-1 is 1.085 N (6.521 against 7.606 N), and the median saving is 5.476 − 4.473 = 1.003 N.

**F2. The losing sub-pool result (08g H2-R) depends on the grid on the CRC route.**
- On the 08c grid, CertGrip-full beats CSF-1 inside the μ ∈ [0.5, 0.8] × mid-amplitude sub-pool (0.3754 [0.2648, 0.4823]).
- On the refined 08e grid it **loses** (−0.3152 [−0.5231, −0.0172], inferiority). This reproduces the sign of the label-route 08g H2-R row (CI [−0.532, −0.03249]).
- The mechanism shows in the comparator's slip. On 08c, CSF-1 sits far below α inside the sub-pool (0.03285), so it is over-conservative because the coarse grid cannot tighten. On 08e it reaches 0.1004 and its RE falls from 0.566 to 0.2633.
- The μ-only restriction behaves the same way (08c 0.3387 superiority; 08e −0.1717 inferiority). The amplitude-only restriction does not: 0.5004 on 08c and 0.4929 on 08e.
- Reading: the loss is driven by friction. Where true μ is narrow and moderate, a friction-blind constant with a fine enough margin grid beats the learned rule.
- A3 places H2-R on the boundary of multiplicity. It is rejected after Holm within H2-x (0.03) but not after Holm over all 52 rows (0.12).

**F3. H2b ("learned beats plug-in") stays not confirmed, and the v3 rows push the point estimates towards zero or below.**
- At σ 0.2, none of the 9 direct learned-against-plug-in contrasts reaches a decision. These are A6 (CRC, LTT and matched slip on 08c and 08e) and B1 (three grid variants).
- The matched-slip contrasts have negative points: −0.02384 on 08c and −0.06104 on 08e.
- Against the shrunk plug-in, all three σ 0.2 points are negative (−0.03216, −0.06463, −0.03532).

**F4. The v1 σ-curve superiority of learned over plug-in does not survive v3, for two different reasons.**
- (a) **σ 0.4: shrinkage over-explains the gap.** The v1 H2b σ 0.4 row was superiority (0.3182 [0.2287, 0.406]). Against the shrunk plug-in (OLS slope b = 0.4044), CertGrip-full is now **inferior** (−0.1395 [−0.1832, −0.01264]).
  - The registered prediction ("advantage shrinks, CI** includes 0") is right in direction but wrong in its second clause: the CI excludes 0 on the negative side.
  - Caveat: shrunk 0.4 runs at higher slip than full 0.4 (0.09286 against 0.08214), so part of its RE advantage is bought with slip budget. No matched-slip B1 row exists.
- (b) **σ 0.0 and 0.1: the plug-in comparator is at the edge of the 08c grid.** On 08c, plug-in 0.0 and 0.1 have λ̂ index 0 in D1 and D2, with test slip 0.007143 / 0.002857 (σ 0.0) and 0.01571 / 0.007143 (σ 0.1), far below α.
  - On the 08e grid, the arm-level RE of the plug-in falls below the learned arm: σ 0.0 gives 0.208 against 0.2397, and σ 0.1 gives 0.2915 against 0.3212.
  - The v3 files contain **no** D with CI** for σ 0.0 or 0.1 on 08e, so this is an arm-level observation, not a contrast. It does, however, indicate that the v1 σ 0.0 and 0.1 superiorities (0.246 and 0.1072) rest on a comparator held at the grid floor.

**F5. The certificate holds in expectation but not per stratum, and not conditionally on friction.**
- A1 matches the pre-stated expectation. The CRC mean slip over 200 re-splits is 0.07121–0.08646, all ≤ α, and the overall exceedance share is a minority (0.0–0.12).
- However, in 0.57 (08c) and 0.69 (08e) of re-splits at least one stratum of CertGrip-full exceeds α on test, against 0.41 and 0.615 for CSF-1. Single-stratum exceedance reaches 0.445.
- This is consistent with a marginal (expected-risk) CRC guarantee and a 700-row test stratum. It does not support any reading of "per-split" or "per-stratum realised" slip control.
- LTT is tighter. Its mean slip is 0.06199–0.07102, and its any-stratum exceedance is 0.06–0.13. Three entries, 0.105, 0.105 and 0.13, sit slightly above δ = 0.10, but those are empirical test rates, not the true risk that LTT bounds.
- Conditionally on friction (A2), CertGrip-full slips 0.2161 in the lowest μ quintile and 0.003571 in the highest. CSF-1 is more extreme (0.4804 against 0.0). The plug-in is flatter (0.08571 → 0.02857). The guarantee is therefore marginal over the friction distribution. Low-friction objects get about twice α under the learned rule (0.2161 / 0.1 ≈ 2.2).

**F6. The finite-sample correction costs essentially nothing here (A5).** The empirical λ̂ equals the CRC λ̂ for all arms on 08c, and for full and CSF-1 on 08e. The one difference is plug-in 0.2 on 08e, where RE goes from 0.4551 to 0.4409 (Δ = 0.0142) and slip from 0.075 to 0.07964. With 500 calibration rows per stratum, the (n+1) correction is smaller than one grid step. A "hand-tuned" margin therefore also holds α on this split. The certificate's added value over plain empirical tuning is the guarantee, not a different operating point.

**F7. The reactive controllers are not a competitive tactile baseline under the v1 slip criterion (B2).**
- The best reactive arm (REACT-blind c 0.75) has slip 0.4632, 4.6× α, at RE 0.4185, which is comparable to CertGrip's 0.4567 at slip 0.08286.
- The probe-informed variants slip in 0.9514–0.9921 of instances, with mean steps around 0.5. With r_safe = 0.8 μ̂ the detector rarely fires before slip has already counted.
- Because slip before tightening counts, a purely reactive scheme fails by construction at these starting forces (c ∈ {0.5, 0.75}). B2 does not show that reactive control is worse in general, only that this registered design is not a viable substitute.

**F8. Physical-feedback online calibration (B3) behaves like the v1 label-feedback study, but the H3 question stays open.**
- Long-run windows return to α. For CertGrip, 1501–2000 slip is 0.1001 / 0.1008 / 0.1018 in S1 / S2 / S3. The RE agrees with the 08d label route; for example, S1 RE is 0.4746 (physical) against 0.4763 (label).
- The transient window 501–1000 overshoots α in S1 (0.1389) and S3 (0.1368). This agrees with the v1 direct-replay audit (S1 OQT-CertGrip 501–1000 slip_direct 0.134; S3 0.128). CertGrip's overshoot is smaller than CSF1's in S1 (0.2087).
- The v1 H3 metric R_E is OQT RE / oracle RE (check: 0.4763 / 0.5426 = 0.8778). It needs the oracle reference that amendment §B3 promised, "recalibrated on the post-shift pool… reported with its own slip". **That oracle row is absent from `b3_analysis.json`.** v3 therefore cannot update H3 (inconclusive in S1 / S2 / S3).

**F9. The force-time benefit is real but modest in absolute terms (A7).**
- The typical required force is small: median F*_mid is 3.184 N against a 32.7 N preload, and no test row needs more than the preload.
- The shared preload, squeeze and ramp-down phases cost 27.429 N·s per grasp. The learned arm's hold saving of 1.085 N against CSF-1 needs about 25 s of hold to equal those phases (27.429 / 1.085 ≈ 25.3 s), and amounts to about 12.7 % of total force-time at T = 30 s.
- The plug-in 0.2 is 0.541 N (7.062 − 6.521) above the learned arm in mean hold F, but its median is only 0.083 N higher (4.556 − 4.473).

---

## 3. Statistical Checks

1. **Definitions.** D reproduces as 1 − RE_target / RE_comparator from the arm values: H2a gives 0.4169 against 0.4168, B1 σ 0.4 gives −0.1396 against −0.1395, and B3 S1 1–500 gives 0.4431 against 0.4432. R_E reproduces as OQT RE / oracle RE (0.8778).
2. **A3 bookkeeping.** The family sizes sum to 51, plus 1 unassigned row, giving 52. The rejections are 8 + 27 + 2 + 3 = 40, plus the oracle decomposition, which is rejected in "all", giving 41. Since "all" reports 40 rejected, the all-rows Holm drops exactly one family-wise rejection, which is H2-R (0.03 → 0.12). This is consistent with the row list.
3. **p-value resolution.** The bootstrap resolution is 1 / 2,000. The reported p = 0.0 means no draw crossed 0, so p < 0.0005, not 0. Five rows (three 08f_tail routes, H4c and the oracle decomposition) carry `null_not_registered_threshold: true`. Their p-values against 0 do not test their registered thresholds and should not be quoted as tests of those hypotheses.
4. **v3 rows are not multiplicity-adjusted.** The decision-labelled v3 rows number 13 (A, 08c) + 13 (A, 08e) + 4 (B1) + 2 (B1 edge) + 2 (B1 same grid) = 34. Two of the decisive v3 reversals have CI bounds close to 0: A4 08e μ and amplitude (upper bound −0.0172) and B1 σ 0.4 (upper bound −0.01264). Under any Holm-type adjustment across these 34 rows, they are at risk, as H2-R was in A3.
5. **Grid sensitivity is first order.** Same-arm differences between 08c and 08e (full 0.2 RE 0.4567 against 0.4442; plug-in 0.0 RE 0.3335 against 0.208) are comparable to or larger than several contrasts being interpreted. λ̂ at index 0 occurs for plug-in 0.0 / 0.1 / 0.2 in D1 and D2 and for shrunk 0.2 in D1 and D2 on 08c. Every learned-against-plug-in conclusion should be read from 08e or same-grid rows.
6. **Sub-pool power.** A4 recalibrates on 352 calibration objects-instances across four strata in the μ and amplitude pool. The 08e CI for D(full vs CSF-1) spans 0.5059 (−0.5231 to −0.0172), and the CSF-1 slip CI is [0.03025, 0.1356].
7. **Slip is not matched across arms** in B1 (shrunk 0.4 at 0.09286 against full 0.4 at 0.08214) or A4 08e (CSF-1 0.1004 against full 0.08394). Only A6 provides a matched-slip contrast, and it is not shown in both grids.
8. **A1 re-splits are not independent replications.** All 200 splits re-partition the same 4,800 instances, so the exceedance shares describe split-to-split variability, not sampling of new objects.
9. **B3 intervals cover orderings only.** Object pools are fixed, so intervals such as [0.4357, 0.451] understate uncertainty relative to the CI** used elsewhere.

---

## 4. Limitations

- **All v3 rows are secondary and are not adjusted for multiplicity** (see check 4). None changes a v1 primary or v2 verdict.
- **Missing registered outputs.**
  - The B3 oracle reference (needed for R_E and the H3 question) is not in `b3_analysis.json`.
  - A7's integrated force over T ∈ {1, 5, 30} s and the break-even T are not in the files. The arithmetic in §1.8 is a reconstruction from mean hold force and the shared phases. The file notes that the phases are "common to every arm in these replays", so the probe's arm-specific extra force-time is not separable here.
  - A6 matched-slip and LTT rows, and B1 rows, exist only for σ 0.2 (B1 also for σ 0.4). No 08e direct contrasts exist for σ 0.0, 0.1 or 0.4.
- **No matched-slip version of B1.** The σ 0.4 inferiority confounds RE with a slip difference of 0.09286 − 0.08214 = 0.01072.
- **B2 tests one registered reactive design** with c ∈ {0.5, 0.75}, a 25 % step and at most 4 steps. A 3-object timing pilot printed 12 calibration-instance outcomes before the full run. No parameter was changed, but this is disclosed. The optional CRC variant was dropped.
- **Marginal guarantee only.** Per-stratum and per-friction-quintile slip can exceed α substantially (lowest-μ quintile 0.2161 for full 0.2). This must be stated wherever the certificate is described.
- **Simulation only** (MuJoCo 4.0.0). σ is not grounded on hardware. There is no adaptive or low preload, and no pool where friction correlates with non-tactile inputs (amendment §C).
- **Single calibration / test split for all non-A1 rows.** The per-seed spread of full 0.2 (slip 0.07929–0.1018; RE 0.4313–0.4752) gives a sense of training variability that the bootstrap CIs do not include.

---

## 5. Conclusion

1. **H2a is robust.** Learned CertGrip against friction-blind CSF-1 gives D ≈ 0.42–0.43 across the CRC, empirical and refined-grid rows, about 0.41–0.44 in online physical feedback, and about 1.1 N lower mean hold force.
2. **The case for a learned force head over a calibrated friction plug-in is not supported by v3.** All 9 σ 0.2 direct contrasts are "not shown", with matched-slip points negative (−0.02384, −0.06104). At σ 0.4, a shrunk plug-in beats the learned arm (−0.1395 [−0.1832, −0.01264]), contrary to the second clause of the registered B1 prediction. The v1 σ 0.0 and 0.1 superiorities rest on a plug-in held at the 08c grid floor, and on 08e the plug-in has the lower arm-level RE. The paper should present CertGrip's value as **conformal calibration of a tactile friction estimate**, not as learning beating plug-in.
3. **The H2-R losing sub-pool reappears on the CRC route once the grid is refined** (−0.3152, inferiority). It is driven by friction (μ-only −0.1717; amplitude-only +0.4929), and survives Holm only within its family (0.03, against 0.12 overall).
4. **The certificate is empirically sound in expectation.** A1 mean slip is ≤ α for every rule, arm and grid, and A5 shows the (n+1) correction is free at this calibration size. But it is marginal: per-stratum exceedance occurs in a majority of re-splits (0.57–0.69 for the learned arm), and low-friction objects slip at about 2× α.
5. **B2 reactive controllers are not viable under the v1 slip criterion** (slip 0.4632–0.9921). **B3 confirms that physical feedback converges to α**, with a transient overshoot to 0.1389 / 0.1368 in S1 / S3, but it cannot update H3 because the registered oracle reference is missing.
