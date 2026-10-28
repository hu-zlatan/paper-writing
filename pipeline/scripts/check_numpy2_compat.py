#!/usr/bin/env python3
"""check_numpy2_compat.py — flag NumPy 1.x APIs removed or changed in NumPy 2.x.

Scans Python source files for patterns that break under NumPy 2.x and reports them
in a format suitable for piping into the iterative_refine stage prompt.

Usage:
    python check_numpy2_compat.py <path> [<path> ...]
    python check_numpy2_compat.py code/

Exit codes:
    0 — no issues found
    1 — issues found (printed to stdout)
    2 — usage error

The patterns covered match references/numpy2_compatibility.md. Keep both files in sync.
"""

from __future__ import annotations

import argparse
import json
import re
import sys
from dataclasses import dataclass
from pathlib import Path


# ─── Pattern table ────────────────────────────────────────────────────────────
# Each rule: (regex, severity, message, suggested_fix)
# Patterns use word-boundary anchors so e.g. `np.bool_` is NOT flagged
# (only the bare alias `np.bool` is).

@dataclass(frozen=True)
class Rule:
    pattern: re.Pattern
    severity: str          # "error" | "warning"
    message: str
    fix: str

RULES: list[Rule] = [
    # Removed scalar aliases (np.bool, np.int, np.float, np.object, np.str, np.long, np.complex)
    Rule(re.compile(r"\bnp\.bool\b(?!_)"),    "error",
         "np.bool was removed in NumPy 1.20+ and definitively gone in NumPy 2.0",
         "use built-in `bool` or `np.bool_` (the dtype)"),
    Rule(re.compile(r"\bnp\.int\b(?!_|p|8|16|32|64)"), "error",
         "np.int was removed",
         "use built-in `int` or a sized dtype like `np.int64`"),
    Rule(re.compile(r"\bnp\.float\b(?!_|ing|16|32|64|128)"), "error",
         "np.float was removed",
         "use built-in `float` or a sized dtype like `np.float64`"),
    Rule(re.compile(r"\bnp\.object\b(?!_)"),  "error",
         "np.object was removed",
         "use built-in `object` or `np.object_`"),
    Rule(re.compile(r"\bnp\.str\b(?!_|ing)"),  "error",
         "np.str was removed",
         "use built-in `str` or `np.str_`"),
    Rule(re.compile(r"\bnp\.long\b(?!_|double|long)"), "error",
         "np.long was removed",
         "use built-in `int` or `np.int_`"),
    Rule(re.compile(r"\bnp\.complex\b(?!_|ing|64|128|256)"), "error",
         "np.complex was removed",
         "use built-in `complex` or `np.complex128`"),

    # Removed / renamed functions
    Rule(re.compile(r"\bnp\.trapz\b"),         "error",
         "np.trapz removed in NumPy 2.0",
         "use `np.trapezoid`"),
    Rule(re.compile(r"\bnp\.in1d\b"),          "error",
         "np.in1d removed in NumPy 2.0",
         "use `np.isin`"),
    Rule(re.compile(r"\bnp\.alltrue\b"),       "error",
         "np.alltrue removed in NumPy 2.0",
         "use `np.all`"),
    Rule(re.compile(r"\bnp\.sometrue\b"),      "error",
         "np.sometrue removed in NumPy 2.0",
         "use `np.any`"),
    Rule(re.compile(r"\bnp\.product\b"),       "error",
         "np.product removed in NumPy 2.0",
         "use `np.prod`"),
    Rule(re.compile(r"\bnp\.cumproduct\b"),    "error",
         "np.cumproduct removed in NumPy 2.0",
         "use `np.cumprod`"),
    Rule(re.compile(r"\bnp\.row_stack\b"),     "warning",
         "np.row_stack is an alias kept only for back-compat",
         "use `np.vstack`"),
    Rule(re.compile(r"\bnp\.float_\b"),        "warning",
         "np.float_ removed in NumPy 2.0",
         "use `np.float64`"),
    Rule(re.compile(r"\bnp\.complex_\b"),      "warning",
         "np.complex_ removed in NumPy 2.0",
         "use `np.complex128`"),
    Rule(re.compile(r"\bnp\.longfloat\b"),     "warning",
         "np.longfloat removed",
         "use `np.longdouble`"),

    # Removed submodules
    Rule(re.compile(r"\bnp\.compat\b"),        "error",
         "np.compat module removed in NumPy 2.0",
         "drop the import; the wrappers were Python-2 era"),
    Rule(re.compile(r"\bnp\.PINF\b"),          "error",
         "np.PINF removed",
         "use `np.inf`"),
    Rule(re.compile(r"\bnp\.NINF\b"),          "error",
         "np.NINF removed",
         "use `-np.inf`"),
    Rule(re.compile(r"\bnp\.NaN\b"),           "warning",
         "np.NaN deprecated alias",
         "use `np.nan`"),
    Rule(re.compile(r"\bnp\.Infinity\b"),      "error",
         "np.Infinity removed",
         "use `np.inf`"),

    # Random API (legacy interface still works but new code should use Generator)
    Rule(re.compile(r"\bnp\.random\.seed\b"),  "warning",
         "np.random.seed mutates global RNG state — fragile under parallelism",
         "use `rng = np.random.default_rng(seed)` and call methods on `rng`"),

    # SciPy moves (often paired with numpy2 migrations)
    Rule(re.compile(r"\bscipy\.misc\.\w+"),    "error",
         "scipy.misc removed in modern SciPy",
         "use `scipy.special` / `scipy.ndimage` / `imageio` per the function"),

    # Behaviour changes that compile fine but break at runtime
    Rule(re.compile(r"copy\s*=\s*False"),      "warning",
         "copy=False semantics tightened in NumPy 2.0 — may now raise instead of silently copying",
         "review per-call: pass `copy=None` for 'copy if needed' behaviour"),
]

# Files / directories to skip
SKIP_PARTS = {".git", ".venv", "__pycache__", "node_modules", ".tox", ".mypy_cache"}


def iter_python_files(roots: list[Path]):
    for root in roots:
        if root.is_file() and root.suffix == ".py":
            yield root
            continue
        if not root.is_dir():
            continue
        for path in root.rglob("*.py"):
            if any(part in SKIP_PARTS for part in path.parts):
                continue
            yield path


def check_file(path: Path):
    """Yield (line_no, line, rule) tuples for matches in path."""
    try:
        text = path.read_text(encoding="utf-8")
    except (UnicodeDecodeError, OSError):
        return
    for line_no, line in enumerate(text.splitlines(), start=1):
        # Skip obvious comments / docstring lines
        stripped = line.lstrip()
        if stripped.startswith("#"):
            continue
        for rule in RULES:
            if rule.pattern.search(line):
                yield line_no, line.rstrip(), rule


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("paths", nargs="+", help="files or directories to scan")
    parser.add_argument("--json", action="store_true", help="emit JSON instead of text")
    parser.add_argument("--errors-only", action="store_true",
                        help="suppress warnings; only report errors")
    args = parser.parse_args()

    roots = [Path(p) for p in args.paths]
    findings = []
    for path in iter_python_files(roots):
        for line_no, line, rule in check_file(path):
            if args.errors_only and rule.severity != "error":
                continue
            findings.append({
                "file": str(path),
                "line": line_no,
                "severity": rule.severity,
                "message": rule.message,
                "fix": rule.fix,
                "code": line,
            })

    n_errors = sum(1 for f in findings if f["severity"] == "error")
    n_warnings = sum(1 for f in findings if f["severity"] == "warning")

    if args.json:
        json.dump({"errors": n_errors, "warnings": n_warnings, "findings": findings},
                  sys.stdout, indent=2)
        sys.stdout.write("\n")
    else:
        for f in findings:
            tag = "ERROR" if f["severity"] == "error" else "WARN "
            print(f"{tag}  {f['file']}:{f['line']}  {f['message']}")
            print(f"        > {f['code']}")
            print(f"        fix: {f['fix']}")
        print(f"\nSummary: {n_errors} error(s), {n_warnings} warning(s).")

    return 1 if n_errors > 0 else 0


if __name__ == "__main__":
    raise SystemExit(main())
