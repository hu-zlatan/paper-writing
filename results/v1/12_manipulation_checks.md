# Stage 12 (v1) — pre-run manipulation checks and evaluation-PF check (real runs)

Sources: results/v1/checks/*.json (sandbox, code/run_checks.py), results/v1/pfcheck/*.jsonl + results/v1/12_pfcheck_analysis.json
(GitHub Actions run 40668209040), code/analysis_pfcheck.py.

## Confusability (requirement C(S) ≥ 0.90, C(A) ≤ 0.80) — PASS
C(S) = 0.971, C(A) = 0.772 (multi-start Nelder–Mead IoU maxima; lower bounds of the true maxima).

## Myopia gap (requirement G(S) ≥ 0.10, G(A) ≤ 0.03) — FAIL for S
100-belief banks, belief = 1,000-particle PF; nested MC with C1 = 16 first actions, Y1 = 8 outcomes, C2 = 16, M = 16; the
two selected first actions (two-step-optimal and greedy) re-estimated with fresh samples (2·Y1 outcomes, 4·M samples).

| target | set | G (mean rel. gap) | median | mean absolute gap (nats) ± SE | R_NC | mean max EIG1 (nats) |
|---|---|---|---|---|---|---|
| full state | S | −0.033 | 0.000 | −0.110 ± 0.035 | 0.03 | 3.07 |
| full state | A | −0.020 | 0.000 | −0.112 ± 0.035 | 0.07 | 3.48 |
| identity only (exploratory) | S | +0.003 | 0.000 | +0.005 ± 0.012 | — | 0.92 |

Reading: no evidence of any two-step advantage over greedy, for either the full state or the identity alone. The
negative full-state gaps mean that picking the first action by noisy two-step estimates did worse than picking it by
one-step EIG, i.e. the two-step estimator is noisy at this budget, but there is no sign of a positive gap to detect.
NC-relevance is low (3–7 % of beliefs have a greedy action with P(no contact) in [0.2, 0.8]).

## Evaluation-PF convergence (amendment A3 rule) — FAIL at N = 8,000
Paired on identical episodes (300 per cell unless noted), N = 8,000 vs 32,000 particles: success differences up to
−2.4 pp (A, T=3, random) and +6 pp on a 40-episode subset of S, T=10 (0.425 vs 0.525); ball information
systematically 0.1–0.4 nats higher at 32k. A 2,000-particle filter with 30 MH steps gave 0.50 / 6.53 nats on that
subset (vs 0.525 / 6.60 at 32k × 3 MH), so mixing, not particle count, is the bottleneck.

## Greedy vs random (precondition of H1a: greedy ≥ random + 10 pp at T ≤ 5) — met
T = 3, 300 pilot episodes, N_eval = 32k: success A 0.767 vs 0.123; S 0.420 vs 0.133.

## Addendum (after stage 14): myopia-bank check on the positive-control set PC (2 shapes, rectangle ± notch)
Same estimator and bank construction (100 beliefs; results/v1/checks/myopia_PC.json, myopia_identity_PC.json):

| target | G | mean absolute gap (nats), 95 % bootstrap CI over beliefs | mean max EIG1 | mean EIG2* |
|---|---|---|---|---|
| full state | −0.052 | −0.183 [−0.261, −0.110] | 2.80 | 3.84 |
| identity | −0.006 | +0.006 [−0.005, +0.017] | 0.118 | 0.261 |

The bank estimator also finds no look-ahead gap on PC; the significantly negative full-state gap shows that choosing
the first action by noisy two-step estimates is worse than choosing it by one-step EIG at this sample size, i.e. the
estimator cannot detect small gaps. Note this is a bank of random beliefs, not the specific analytic H2b-P2 scenario
(T = 2 from the prior), whose optimum was never computed. Deviation to record: C1/Y1/C2/M = 16/8/16/16 were used instead
of the pre-registered 32/32/32 (cost: ≈ 5 s per belief vs ≈ 64× more).
