# Stage 10 — CODE_GENERATION

## Purpose
Generate the full experiment Python project from the experiment plan. **This is where authenticity discipline matters most** — most reviewer-detectable fraud (faked loss curves, missing convergence checks) starts here.

## Mode
- LLM: code-specialized model (e.g. a Claude/Sonnet-class or a strong code model).
- json_mode: false.
- **max_tokens: 8192.**

## Prompt template

**System:**
```
You are a computational scientist who writes real, runnable experiments. Your code implements actual algorithms with real mathematical operations. You NEVER fake results with random number generators. Always use the ```filename:xxx.py format for each file. Use numpy for numerical computation. Keep code self-contained and deterministic.
```

**User:**
````
Generate a Python experiment project for the following research topic:
TOPIC: {topic}

CRITICAL REQUIREMENTS — your code MUST satisfy ALL of these:
1. Implement REAL algorithms (e.g., gradient descent, Adam, SGD, etc.) using numpy arrays — NOT random.uniform() loops that fake results.
2. Define REAL objective/loss functions (e.g., Rosenbrock, quadratic, cross-entropy on synthetic data) with proper mathematical formulas.
3. Run REAL optimization loops that compute gradients and update parameters.
4. Collect REAL metrics (loss values, convergence rates) from the optimization.
5. The code must be scientifically meaningful — a reviewer should see actual algorithm implementations, not random number generators.

OUTPUT FORMAT — return multiple files using this exact format:
```filename:main.py
# entry point code
```

```filename:optimizers.py
# optimizer implementations
```

CODE STRUCTURE:
- main.py: entry point that runs experiments and prints metrics
- Additional modules for algorithms, objective functions, utilities
- Primary metric key: {metric}
- main.py must print metric lines as `name: value` (one per line)
- main.py must ALSO write a `results.json` file with structured experiment results
  (e.g. per-algorithm, per-function, per-dimension metrics as nested dicts/lists)
- Use deterministic seeds (numpy.random.seed or random.seed)
- No external data files, no network calls, no GPU required
- FORBIDDEN: subprocess, os.system, eval, exec, shutil, socket
- MUST implement convergence stopping criteria (e.g. stop when objective change < 1e-8 for
  N consecutive iterations) — do NOT just run a fixed number of iterations
{pkg_hint}
ANTI-PATTERNS (do NOT do these):
- Do NOT generate random numbers and pretend they are experiment results
- Do NOT use `random.uniform()` to simulate a decreasing loss curve
- Do NOT hardcode metric values or use trivial arithmetic as metrics
- Do NOT run a fixed number of iterations without any convergence check
- Do NOT implement convergence_rate or similar metrics as dummy return values
  (e.g. returning 1.0 or a constant) — measure actual iterations to convergence
- If you report convergence_rate, define it as iterations_to_convergence / max_iterations
  or similar — it MUST differ between algorithms

NUMPY 2.x COMPATIBILITY (CRITICAL):
- np.trapz is REMOVED → use np.trapezoid
- np.erfinv does NOT exist → use scipy.special.erfinv
- np.bool, np.int, np.float, np.complex are REMOVED → use Python builtins
- np.str, np.object are REMOVED → use str, object
- np.math is REMOVED → use math module

Experiment plan:
{exp_plan}
````

## Placeholders

- `{topic}` — research topic.
- `{metric}` — the primary metric key (e.g. `final_loss`, `iterations_to_convergence`, `accuracy`).
- `{exp_plan}` — full contents of `docs/08_experiment_plan.yaml`.
- `{pkg_hint}` — optional sentence such as "You may use numpy, scipy, and matplotlib only." or "torch is allowed because the method requires autograd."

## Mandatory post-generation checks

After the LLM returns code, **before considering this stage done**:

1. Save each file to `code/<filename>.py`.
2. Run `python scripts/check_numpy2_compat.py code/` — fix any flagged patterns in stage 13.
3. Verify `main.py` writes `results.json` with a structured layout.
4. Verify a `time_guard` is present (see `scripts/time_guard.py` for the pattern). If missing, inject it.
5. Verify a real convergence stop is present (search for `< 1e-8` and `consecutive` / `patience`). If missing, kick back to stage 13.
6. Run a 1-condition pilot and confirm it prints `TIME_ESTIMATE: Xs`.

## Output

- `code/main.py`, `code/<modules>.py`, `code/requirements.txt`, `code/README.md`.
