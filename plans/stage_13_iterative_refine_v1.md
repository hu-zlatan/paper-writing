# Stage 13 · ITERATIVE_REFINE · v1

## Goal
Repair runtime issues found in stage-12 logs at their root cause; list improvements that need a design decision.

## Tasks
- [x] Scan results/v1/logs for nan / inf / RuntimeWarning / Traceback and results for non-finite values.
- [x] iterative_repair: `RuntimeWarning: divide by zero encountered in log1p` (pf.py, contact-proposal density). Root cause: log[Φ(a) − Φ(b)] computed as log Φ(a) + log1p(−exp(log Φ(b) − log Φ(a))) underflows to log1p(−1) when both a, b ≫ 0 (query far beyond the segment end). Fix: use the mirrored tail Φ(−b) − Φ(−a) when b > 0. Verified: 20,000 random far-away queries give finite log-densities with warnings promoted to errors; PF tests pass. No try/except or nan_to_num used.
- [ ] iterative_improve (needs a decision, handed to stages 14/15): evaluation-PF mixing (N=8k vs 32k disagreement), and the failed myopia-gap manipulation check (results/v1/12_manipulation_checks.md).

## Output Summary
- One root-cause repair; no non-finite values in any result file. Improvement items forwarded to stage 14/15.
- **Decision:** PROCEED → stage 14 (fresh-context analysis of the pre-run evidence).
