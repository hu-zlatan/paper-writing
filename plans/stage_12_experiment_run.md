# Stage 12 · EXPERIMENT_RUN · v1

## Goal
Execute docs/11_schedule.json on GitHub Actions; every output under results/v1/ with logs; watch for nan/inf/RuntimeWarning (→ stage 13).

## Tasks (in dependency order; each launched via a manifest in experiments/)
- [ ] T0 PF convergence check → decide N_eval (results/v1/pfcheck/, analysis results/v1/12_pfcheck_analysis.json).
- [ ] T1 hyperparameter search (experiments/hpsearch_v1.json) → select one config per learned method on validation success at T=5.
- [ ] T3 manipulation checks (confusability, myopia gap G(O), R_NC) — code + run.
- [ ] T2 baseline tuning (coverage C; greedy Pareto on validation).
- [ ] T4–T9 main training, ablations, test evaluation, MuJoCo, oracle/positive control, H5′.
- [ ] Aggregate into results/v1/results.json with provenance (manifest, Actions run id, commit).

## Hard-constraint checks
- [ ] Logs scanned for nan / inf / RuntimeWarning / Traceback; any hit → stage 13 with root-cause fix.
- [ ] Trial counts in results.json equal what actually ran (EARLY_STOP markers counted).
