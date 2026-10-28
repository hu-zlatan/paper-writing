# Stage 1 · TOPIC_INIT · v1

## Goal
Choose a CPU-feasible research topic inside the owner's field (dexterous manipulation / tactile sensing / robot learning) and a verified target venue, then produce the SMART goal (`docs/00_topic_init.md`), `MEGA_PROMPT.md`, the project fields of `RESTRICTS.yaml`, and the three design docs.

## Tasks
- [ ] Check open issues for owner instructions (WebFetch).
- [ ] Verify next deadlines of candidate venues on official sites (RSS 2027, ICML 2027, CoRL, NeurIPS).
- [ ] Scan recent literature for a gap that is CPU-feasible (WebSearch), pick one topic with 1–2 core novelties.
- [ ] Hardware detection (stage 1+), log in PROGRESS.md.
- [ ] Run the stage-1 prompt template (`stage_prompts/topic_init.md`) verbatim → `docs/00_topic_init.md` with sections Topic, Scope, SMART Goal, Constraints, Success Criteria, Generated.
- [ ] Fill every placeholder of `pipeline/MEGA_PROMPT.template.md` → `MEGA_PROMPT.md` (cloud adaptations per AUTOPILOT §3; the "abstract already submitted" line replaced per AUTOPILOT §2).
- [ ] Fill RESTRICTS.yaml project block + venue page limit.
- [ ] Write `docs/整体构想.md`, `docs/实验构想.md`, `docs/文献与问题.md`.
- [ ] Record the venue's LLM policy in AI_USAGE.md.
- [ ] Update PROGRESS.md, commit, push.

## Inputs (must exist before starting)
- AUTOPILOT.md, pipeline/MEGA_PROMPT.template.md, RESTRICTS.yaml, pipeline/references/stage_prompts/topic_init.md

## Expected outputs
- docs/00_topic_init.md, MEGA_PROMPT.md, RESTRICTS.yaml (project), docs/整体构想.md, docs/实验构想.md, docs/文献与问题.md, AI_USAGE.md (policy)

## Hard-constraint checks for this stage
- [ ] Deadline taken from the venue's official CFP page, with timezone.
- [ ] Topic runnable on CPU (2 vCPU / 7 GB sandbox + GitHub Actions runners).
- [ ] No citation in the docs is presented as verified before stage 4 verifies it.
- [ ] Sushi, not curry: ≤2 core novelties.

## Notes / risks
- Active tactile perception is a crowded area; the novelty must be the *amortized, non-myopic information-gain policy*, not active touch per se.
- RSS 2027 uses a two-stage process (extended abstract Dec 4 2026 → invited full paper Apr 16 2027); submission is the owner's decision.

---

## Output Summary  (filled in AFTER the stage runs)
- **Venue:** RSS 2027 (verified on the official CFP). Two-stage process: Stage 1 extended abstract (5 pages + 1 page refs, no supplement) 2026-12-04 23:59 AoE; Stage 2 full paper (8 pages excl. refs, invited only) 2027-04-16 23:59 AoE; conference July 6–11 2027, Athens. Chosen over ICML 2027 (deadline only an unofficial estimate, ~2027-01-22 AoE, CFP not yet out) because RSS is the best fit for tactile localization and its full-paper deadline leaves time for ≥2 full loops; the extended abstract is an intermediate milestone the owner may choose to use.
- **Topic:** amortized, non-myopic active tactile localization (TouchBED): policy-based sequential BED trained on the sPCE bound of total EIG; two core novelties (non-myopic amortized policy for non-differentiable contact; explicit negative information under multimodal beliefs). Gap evidence: Gordon et al. 2025 (arXiv:2510.13595) use local Fisher-information EIG with stated local-minimum failures; Shahidzadeh et al. 2025 (arXiv:2509.13591) use RL exploration without an information objective.
- **Hardware:** 2 vCPU, 7 GB RAM, no GPU; MuJoCo 3.17.0 installs via pip. CPU-only plan.
- **Outputs:** docs/00_topic_init.md (6 required sections present), MEGA_PROMPT.md (no placeholders left), RESTRICTS.yaml project block + pages_target 8, docs/整体构想.md, docs/实验构想.md, docs/文献与问题.md, AI_USAGE.md venue policy.
- **Deviation:** the RSS LaTeX template (https://roboticsconference.org/docs/paper-template-latex.tar.gz) is not downloadable from the shell (network limited to package registries + GitHub); it will be fetched via a GitHub Actions workflow before stage 22.
- **Decision:** PROCEED → stage 2.
