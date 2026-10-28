# Stage 13 — ITERATIVE_REFINE  (self-healing)

## Purpose
Fix problems in the experiment code. This stage covers three sub-modes from the original pipeline:

| Sub-mode | When to use |
|---|---|
| **`code_repair`** | Static validation errors (syntax, import errors, undefined names) caught before/just after first run. |
| **`iterative_repair`** | Runtime failures (NaN, Inf, divide-by-zero, overflow, RuntimeWarning) — diagnose root cause, never band-aid. |
| **`iterative_improve`** | Code runs and finishes, but results are weak — improve the experiment based on prior run summaries. |

Pick the right sub-mode by what failed:

- Did the code fail to import / parse / pass static checks? → **code_repair**.
- Did it run but emit NaN/Inf or RuntimeWarnings? → **iterative_repair**.
- Did it complete cleanly but the metrics are uninformative or worse than baseline? → **iterative_improve**.

## Mode
- LLM: code-specialized model.
- json_mode: false.
- **max_tokens: 8192.**

---

## 13a. CODE_REPAIR (static validation errors)

### System:
```
You fix Python code validation errors while preserving functionality.
```

### User:
````
The file `{fname}` in the experiment project has validation errors. Fix ALL issues and return ONLY the corrected file.


## Validation Issues in {fname}

{issues_text}


## All Project Files

{all_files_ctx}


IMPORTANT: Do NOT use subprocess, os.system, eval, exec, or any network/shell calls.

Return ONLY the corrected code for `{fname}`.
````

### Placeholders
- `{fname}` — the file with errors.
- `{issues_text}` — concatenated validator output / linter warnings / NumPy 2.x compat report.
- `{all_files_ctx}` — every `code/*.py` concatenated, each prefixed with ` ```filename:<name>.py ```.

---

## 13b. ITERATIVE_REPAIR (runtime bugs — NaN/Inf/divide-by-zero/overflow)

### System:
```
You fix Python code issues — both static validation errors and runtime bugs (NaN, Inf, division by zero, overflow). Diagnose the ROOT CAUSE from warnings and error messages. Do not add unsafe behavior.
```

### User:
````
Fix all issues in the experiment code and return corrected Python code using ```filename:xxx.py format for each file.

IMPORTANT: If you see NaN/Inf or RuntimeWarning about division or invalid values, trace the bug to its source (e.g. division by zero, uninitialized array, missing convergence check) and fix the actual code logic — do NOT just add try/except to suppress the error.


## Issues Found

{issue_text}


## All Project Files

{all_files_ctx}
````

### Placeholders
- `{issue_text}` — concatenated runtime warnings, exceptions, and NaN/Inf traces from the failed run.
- `{all_files_ctx}` — every `code/*.py`.

### Hard rule for this sub-mode
The fix must be a **root-cause** fix. Reject the LLM's output if the diff includes:
- `try: ... except: pass`
- `np.nan_to_num(...)` (unless the original computation genuinely allows NaN as a meaningful value)
- `if np.isnan(x): x = 0` masking what was actually a divergence
- `with np.errstate(...): pass` to silence warnings

If the LLM keeps band-aiding after 2 iterations, escalate to the user with the full failing trace and ask for guidance.

---

## 13c. ITERATIVE_IMPROVE (working code, weak results)

### System:
```
You improve experiment projects and return valid executable Python code. Use ```filename:xxx.py format for each file.
```

### User:
````
Improve the experiment code based on prior run results.

Return the improved files using ```filename:xxx.py format for each file.

Primary metric key: {metric_key}

Metric direction: {metric_direction}

Do not use subprocess, os.system, eval, exec, or any network/shell calls.

Current project files:

{files_context}

Run summaries (JSON):

{run_summaries}
````

### Placeholders
- `{metric_key}` — e.g. `final_loss`, `accuracy`, `wall_clock_seconds`.
- `{metric_direction}` — `"minimize"` or `"maximize"`.
- `{files_context}` — concatenated `code/*.py` with filename markers.
- `{run_summaries}` — JSON of last few `results.json` snapshots, one per condition.

---

## After any sub-mode completes

1. Save the returned files (overwrite, but keep the prior version under `code/v<N>/` if this is a major loop).
2. Re-run `scripts/check_numpy2_compat.py code/`.
3. Re-run the 1-condition pilot.
4. If clean, return to stage 12 (experiment_run).
5. Update `PROGRESS.md` with the version bump and the diff summary.
