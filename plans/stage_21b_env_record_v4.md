# Stage 21 follow-up [v4] — environment record (run 12, 2026-11-02)

Context: the stage-20 v4 escalation is still unanswered (no open issues, AUTOPILOT §1 unchanged, RESTRICTS
`max_refine_cycles` still 3). OWNER_TODO default → low-risk work only. `docs/21_retrospective.md` lists "pin the
environment" as open housekeeping. This plan closes it without changing any result, claim, paper text or workflow.

Steps
1. `code/tools_env_census.py`: read the header line of every `results/**/*.jsonl` shard and count the recorded
   (python, numpy, thread-env) tuples per version directory → `results/v4/env_census.json`. Pure bookkeeping over
   files already in the repo.
2. `code/requirements-lock.txt`: exact versions taken verbatim from the `pip install -r code/requirements.txt` log of
   Actions job 124884356660 (run 41318760187, 2026-11-01, CPython 3.12.15, ubuntu-26.04 image 20261025.179.1).
   State plainly that only numpy / Python are confirmed for every runner shard (via shard headers); other package
   versions are confirmed only for that job's date. The workflow keeps installing `code/requirements.txt` (no change to
   `.github/workflows/`, so nothing re-runs differently).
3. Append a dated addendum to `docs/21_retrospective.md` (the original stage output is not rewritten).
4. PROGRESS, commit, push.

Red lines (hard_constraints.md): no numbers enter the paper; no results changed; versions copied from a real log.
