# NumPy 2.x Compatibility Cheat Sheet

NumPy 2.0 (released June 2024) removed a swath of long-deprecated aliases and changed behavior in places that LLM-generated code routinely trips over. This file is the migration table; `scripts/check_numpy2_compat.py` automates checking.

## Removed aliases for built-in types

These were deprecated since NumPy 1.20 and are gone in 2.0. Use Python built-ins.

| Old (broken in NumPy 2) | New |
|---|---|
| `np.bool` | `bool` |
| `np.int` | `int` |
| `np.float` | `float` |
| `np.complex` | `complex` |
| `np.object` | `object` |
| `np.str` | `str` |
| `np.long` | `int` |
| `np.unicode` | `str` |

> Note: the **typed** aliases like `np.int32`, `np.float64`, `np.bool_` (with the trailing underscore) are still valid — only the builtin-aliasing forms were removed.

## Removed / renamed numerical functions

| Old | New |
|---|---|
| `np.trapz(y, x)` | `np.trapezoid(y, x)` |
| `np.product(...)` | `np.prod(...)` |
| `np.cumproduct(...)` | `np.cumprod(...)` |
| `np.alltrue(...)` | `np.all(...)` |
| `np.sometrue(...)` | `np.any(...)` |
| `np.round_(...)` | `np.round(...)` |

## Functions that never existed in NumPy (LLMs hallucinate these)

| LLM hallucination | What you actually want |
|---|---|
| `np.erfinv(...)` | `from scipy.special import erfinv` |
| `np.erf(...)` | `from scipy.special import erf` |
| `np.gammaln(...)` | `from scipy.special import gammaln` |
| `np.softmax(...)` | implement: `e = np.exp(x - x.max()); e / e.sum()` |
| `np.sigmoid(...)` | implement: `1 / (1 + np.exp(-x))` |
| `np.relu(...)` | implement: `np.maximum(0, x)` |

## Removed submodules

| Old | New |
|---|---|
| `np.math.factorial(n)` | `import math; math.factorial(n)` |
| `np.math.pi` | `math.pi` |
| `np.math.e` | `math.e` |
| `np.testing.dec.*` | use `pytest` markers |
| `np.deprecate*` | use Python's `warnings.warn(..., DeprecationWarning)` |

## Behavior changes (silent breaks — easy to miss)

- **`np.copy(a, subok=True)`** — `subok` default changed; explicitly pass it if you rely on subclass preservation.
- **Scalar promotion rules** — mixing a Python int with a NumPy array no longer triggers up-casting in some cases. If you see precision loss, pin the dtype: `np.array(x, dtype=np.float64)`.
- **`np.array(generator)`** — now raises instead of materializing. Wrap in `list()` first: `np.array(list(gen))`.
- **`np.set_string_function`** — removed. Use `np.set_printoptions(formatter=...)`.
- **`np.in1d`** — replaced by `np.isin` (the old name still warns; prefer `np.isin`).

## NumPy 2-safe imports for typical experimental code

```python
import math
import numpy as np
from scipy.special import erf, erfinv, gammaln  # if needed

# common helpers — define once, use everywhere
def softmax(x, axis=-1):
    e = np.exp(x - np.max(x, axis=axis, keepdims=True))
    return e / e.sum(axis=axis, keepdims=True)

def sigmoid(x):
    return 1 / (1 + np.exp(-x))

def relu(x):
    return np.maximum(0, x)
```

## Quick check command

```bash
python scripts/check_numpy2_compat.py code/
```

Run before stage 12 (experiment_run). If it returns nonzero, fix in stage 13 (iterative_refine).
