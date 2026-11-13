# Stage 18 PEER_REVIEW [v6] — pass 2 merged record (run 50, 2026-11-13)

Second pass on the stage-19 pass-1 draft (`v6/draft_v6_stage19pass1.md`); two fresh opus subagents, same template and
evidence (`paper/mypaper/prompts/stage18_v6_pass2_user.txt`).

| Run | File | Reviewer A | Reviewer B | Fabrication |
|---|---|---|---|---|
| 1 | `18_review_v6_pass2_run1.md` | 5 / 10 (methods & statistics) | 4 / 10 (significance) | **none found**; every point estimate of Tables 1–3 and the first-decision agreement recomputed exactly |
| 2 | `18_review_v6_pass2_run2.md` (RSS / CoRL pair) | 4 / 10 (robotics significance) | 5 / 10 (methodology) | **none found**; episode counts, H6a / H6b / H6c, P1 and P2 recomputed |

Pass-1 triage status (both runs): items 1–5 and 7 fixed; item 6 partly (abstract 240 words, length ≈ 10.5k words,
3 [CITE-MISSING], Figure 1 unrendered) — deferred to stages 22–23 by design.

## Main-session check
- Both reviewers re-ran H6b at 100,000 resamples. Reproduced in-repo: `code/analysis_v6_posthoc.py` P4 →
  `results/v6/18_posthoc_v6.json > P4_h6b_100k_resamples`: 0–499 → 7 / 10 rejections (same set as the registered
  10,000-resample read-out); 300–499 → 2 / 10. The p-values near the Holm cut are in that file.

## Triage for stage 19 pass 2 (paper-level only)
- P1 "every method ran every test episode": verify against `episodes_per_method` in `14_v6_analysis.json` and word it
  exactly (name any method that does not have every episode, or drop the phrase).
- P2 Latency: report the registered G\*/student latency ratio with its ci95 from `results/v5/14_e6_analysis.json`
  (copy), state that ratios of medians are point values; state that the gain is computational only (no task-time or
  hardware model).
- P3 H6b robustness: Appendix B adds P4 (100,000 resamples: 7 / 10 on 0–499, 2 / 10 fresh) with the near-cut p-values
  copied from the file, next to the P2 seed check.
- P4 Wording: no "registered level" for post-hoc comparators; say the pre-registration is an internal, timestamped
  repository commit (not a public registry); student − G\* run 1 alone is available as a report-only row
  (`v5_row_updates > student_minus_gstar_run1_success`) — cite it if parity per run is discussed; no new statistics.
- Deferred to stage 22 / 23: abstract < 200 words and 5-page cut, Figure 1 rendering, 3 [CITE-MISSING].
- Evidence-level requests (task-time model / hardware, variance inflation for reduced planners, near-latency comparators,
  more G\* runs): not executable (cap); Limitations only.
