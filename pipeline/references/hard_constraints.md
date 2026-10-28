# Hard Constraints — The Five Red-Line Groups

These are non-negotiable. The pipeline exists *because* of these constraints — without them, you produce a fluent-sounding but rejectable paper. Cross any of these and the pipeline must self-interrupt and roll back.

---

## 1. Compute & Resource Guard (stages 9, 10, 11, 12)

**The problem this solves:** experiments that "almost finish" and produce 30% of the data the paper claims. Reviewers spot this immediately.

### Mandatory time estimate
Before any main experiment loop runs, run a **single-condition pilot** end-to-end and have the code print:

```
TIME_ESTIMATE: <Xs> per condition × <N> conditions × <M> seeds = <total_seconds>s total
```

Multiply out and check against the budget. If over, apply scaling rules below.

### Dynamic scaling rules
- If experiment conditions > 100 → drop seed count to 3–5 (do **not** force 20 just because that's a clean number).
- If time budget is tight → cap optimization steps at ≤5,000 per run.
- If memory budget is tight → prefer batched/streaming evaluation over loading everything in RAM.

### Graceful shutdown
Every long-running script must include a `time_guard` that:
1. Records start time.
2. Checks elapsed time at every iteration boundary.
3. At 80% of the budget, stops cleanly and writes whatever data is collected so far to `results.json`.
4. Logs the early stop with a clear `EARLY_STOP_AT_80_PCT_BUDGET` marker so the analyst sees it.

A drop-in template lives in `scripts/time_guard.py`.

---

## 2. Authenticity Red Line (stages 10, 13, 17)

**The problem this solves:** LLMs love generating "loss curves" with `random.uniform()`. This is fraud, and reviewers running ablations find it instantly.

### Forbidden patterns

- `random.uniform(0.5, 0.9) for _ in range(epochs)` masquerading as a loss curve.
- `np.linspace(start, end, epochs) + np.random.normal(...)` masquerading as a learning curve.
- Hardcoded `convergence_rate = 0.95` returned as a "metric".
- Trivial arithmetic returned as a metric (`return final_loss / initial_loss`).
- Identical metric values across "different" algorithms.

### Required patterns

- Real algorithms implemented with NumPy matrix ops:
  - Real gradient computation (analytic or autodiff).
  - Real cross-entropy / MSE / NLL on real or rule-generated synthetic data.
  - Real optimizer state (Adam moments, momentum buffers, etc.).
- Real convergence stop:
  ```python
  if abs(obj_curr - obj_prev) < 1e-8:
      patience_counter += 1
      if patience_counter >= patience:
          break  # genuinely converged
  else:
      patience_counter = 0
  ```
  Not just `for step in range(max_steps):`.
- Deterministic seeds:
  ```python
  np.random.seed(seed)
  random.seed(seed)
  # if torch is used:
  torch.manual_seed(seed)
  ```
- Per-algorithm metrics that **must** differ across algorithms (otherwise the comparison is meaningless).

### NaN/Inf handling — no band-aids

When you see `nan`, `inf`, `RuntimeWarning: divide by zero`, `RuntimeWarning: overflow`, or `RuntimeWarning: invalid value`:

- **Diagnose the root cause:**
  - Learning rate too high → divergence.
  - Divide by a quantity that goes to zero → guard with `+ epsilon` *only if mathematically justified*, otherwise restructure.
  - Log of a non-positive number → likely missing softmax/clipping somewhere upstream.
  - Uninitialized array → fix the init.
  - Missing normalization → normalize.
- **Forbidden fixes:**
  - `try: ... except: pass` to silence the warning.
  - `np.nan_to_num(x, nan=0)` to "smooth over" NaNs.
  - `result = result if not np.isnan(result) else 0` masking real divergence.

If you genuinely cannot find the root cause within 3 repair iterations, escalate: snapshot the failing condition, mark it as `KNOWN_FAILURE` in `results.json`, and write the failure into the Limitations section honestly. **Hiding it is worse than admitting it.**

---

## 3. Top-Conference Writing Standard (stages 17–19)

**The problem this solves:** technically correct papers that get rejected for poor presentation, weak narrative, or missing structural elements that reviewers expect.

### Sushi, not curry — the focus principle
A good paper has 1–2 core novelties. Everything else stays simple, clean, and rigorous. Resist the urge to pile on additional modules just because you can. A paper with one well-defended idea beats a paper with five half-defended ones.

### Figure 1 supremacy
**Sketch Figure 1 before drafting Section 1.** Many reviewers read only Abstract → Figure 1 → Conclusion before deciding their inclination. Figure 1 must:

- Stand alone — convey the core contribution without prose.
- Show the *what* and the *why* — not just the architecture, but what the architecture *enables*.
- Be visually clean — no eye-chart text, no ambiguous arrows.

In LaTeX, leave a comment block above `\includegraphics` with the *exact* prompt for Nano Banana 2 (or whichever image generator) describing every visual element: shapes, colors, labels, layout, axis ranges if applicable. Do not just write "a diagram showing the method".

### Mandatory ablations
For every component you claim is "effective", "important", "novel", or "key":

- The code must contain a flag that disables it.
- The results must contain a row with that flag off.
- The paper must report and discuss the delta.

If a component has no ablation row, **delete the claim or run the ablation.** No exceptions.

### Strong baselines
Reviewers know which baselines are well-tuned and which were "implemented in 30 minutes with default hyperparameters to make our method look better." Tune baselines with the same effort as your method:
- Same hyperparameter sweep budget.
- Same hardware.
- Same number of seeds.
- Document the tuning protocol explicitly in Experiments.

### Length floors (NeurIPS/ICML/ICLR-style)
| Section | Min words |
|---|---|
| Abstract | 150 |
| Introduction | 800 |
| Related Work | 600 |
| Method | 1000 |
| Experiments | 800 |
| Results | 600 |
| Discussion | 400 |
| Limitations | 200 |
| Conclusion | 200 |

Total main body target: 5,000–6,500 words.

If a section is short, expand by:
- Deepening gap analysis with concrete prior-work limitations.
- Adding mathematical detail (derivations, complexity analysis).
- Adding qualitative analysis of results.

**Never expand by:**
- Restating the same point in different words.
- Padding with "in this paper, we propose..." boilerplate.
- Listing related work without analyzing it.

---

## 4. Evidence & Relevance Audit (stages 18, 23)

**The problem this solves:** the most damning failure mode — paper claims that aren't backed by code or data. Reviewers verifying claims against the supplementary find this and instantly reject.

### Methodology-evidence consistency check

Run this check before stage 19 (revision) and again before stage 22 (LaTeX export):

For every quantitative claim in the paper, verify:

| Claim type | Where to verify |
|---|---|
| "We ran N trials" | Count actual runs in `results/` or run logs |
| "We tested K datasets" | Count distinct dataset entries in `results.json` |
| "We performed an ANOVA / t-test / Mann-Whitney" | grep the code for the corresponding `scipy.stats` call |
| "Method X improved metric Y by Z%" | Pull X's and baseline's Y values from `results.json` and verify Z |
| "We used N hyperparameter configurations" | Count entries in the hyperparameter sweep config |
| "Training took T hours on hardware H" | Verify against actual run logs |

`scripts/verify_evidence.py` automates a chunk of this — run it after every paper revision.

### CRITICAL FABRICATION

If any of the following is true, declare CRITICAL FABRICATION and roll back to stage 13:

- Paper says "10 datasets" but logs show only 2.
- Paper claims "statistical significance via t-test" but no t-test exists in the code.
- Paper reports a metric (e.g. "F1 = 0.87") that does not appear in `results.json`.
- Paper describes a method (e.g. "we use temperature scaling") that is not in the code.
- Paper claims "our method runs in O(n log n)" but the code is `O(n²)`.

Do not soften the claim to match the truth — that erodes the contribution. Either run the experiments to back the claim, or remove the claim.

### Citation fidelity (stage 23)

Every `\cite{...}` must satisfy:

1. **`cite_key` traceability:** the key in `\cite{...}` exists in the `.bib`, and was preserved unchanged from the literature retrieval stage. (LLMs love silently rewriting cite keys.)
2. **DOI/URL resolves:** at least one of `doi`, `url`, or `arxiv_id` resolves to the actual paper. Hallucinated citations fail here.
3. **Topical relevance:** the cited paper is actually about the topic at hand. A high-quality but irrelevant citation (e.g., citing a CV paper in an NLP method section because both involve "attention") is a flag — reject it.

---

## 5. Environment & Library Compatibility (stage 10)

**The problem this solves:** generated code that doesn't run because it relies on deprecated APIs or unnecessarily heavy dependencies.

### Prefer the lightweight stack
- Default: `stdlib + numpy + math + statistics + scipy`.
- Pull in `torch` / `tensorflow` / `jax` only when the contribution genuinely requires GPU autodiff. For optimization-algorithm papers, pure-numpy implementation is usually preferable — reviewers can read it.
- Pull in `transformers` / `datasets` / etc. only when the paper is *about* those models.

### NumPy 2.x mandatory migrations

| Deprecated / removed | Replacement |
|---|---|
| `np.trapz` | `np.trapezoid` |
| `np.erfinv` | `from scipy.special import erfinv` |
| `np.bool` | Python `bool` |
| `np.int` | Python `int` |
| `np.float` | Python `float` |
| `np.complex` | Python `complex` |
| `np.str` | Python `str` |
| `np.object` | Python `object` |
| `np.math.factorial` etc. | `import math; math.factorial(...)` |
| `np.product` | `np.prod` |
| `np.cumproduct` | `np.cumprod` |

Run `scripts/check_numpy2_compat.py code/` before the first execution — it greps for these patterns and reports.

### Forbidden in generated code

- `subprocess`, `os.system`, `eval`, `exec`, `socket`, raw network calls.
- `shutil.rmtree` against anything outside the project's own directories.
- Anything that mutates the user's home directory or pip-installs at runtime.

If a stage genuinely needs a missing package, surface it to the user with a one-line `pip install` suggestion — do not auto-install.
