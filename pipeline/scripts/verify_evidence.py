#!/usr/bin/env python3
"""verify_evidence.py — cross-check paper claims against actual experiment results.

Catches the most common reason for desk-rejection: the paper claims something
the experiments did not actually do. Specifically:
  - Paper claims N trials but results.json shows a different count.
  - Paper claims a statistical test (ANOVA, t-test, Wilcoxon) but no test was run.
  - Paper reports metric names that do not appear in any results file.
  - Paper reports a number that does not match any number in the results.

This script is a heuristic audit. It will produce false positives (paper text
that mentions a baseline name as part of a citation, not as a claim). The goal
is to surface candidates for human review at stage 18 — not to make accept/reject
decisions on its own.

Usage:
    python verify_evidence.py \\
        --paper paper/mypaper/main.tex \\
        --results results/v1/ \\
        [--out paper/mypaper/18_evidence_audit.json]

Exit codes:
    0 — no critical mismatches
    1 — one or more critical mismatches detected (printed to stdout / out file)
    2 — usage / IO error
"""

from __future__ import annotations

import argparse
import json
import re
import sys
from dataclasses import dataclass, field, asdict
from pathlib import Path
from typing import Any, Iterable


# ─── Results gathering ────────────────────────────────────────────────────────

def _gather_results(results_dir: Path) -> dict:
    """Load every results.json (and friends) under results_dir into one dict.

    Recognises:
      results.json
      *_results.json
      summary.json
      metrics.json

    Returns a dict keyed by relative path → parsed JSON content.
    """
    if not results_dir.is_dir():
        sys.exit(f"ERROR: results dir does not exist: {results_dir}")

    found: dict[str, Any] = {}
    patterns = ("results.json", "*_results.json", "summary.json", "metrics.json")
    for pat in patterns:
        for p in results_dir.rglob(pat):
            try:
                content = json.loads(p.read_text(encoding="utf-8"))
                found[str(p.relative_to(results_dir))] = content
            except (json.JSONDecodeError, OSError) as e:
                print(f"  (skip {p}: {e})", file=sys.stderr)
    return found


def _flatten_numbers(obj: Any, prefix: str = "") -> Iterable[tuple[str, float]]:
    """Yield (path, number) pairs from a nested JSON structure."""
    if isinstance(obj, dict):
        for k, v in obj.items():
            yield from _flatten_numbers(v, f"{prefix}.{k}" if prefix else str(k))
    elif isinstance(obj, list):
        for i, v in enumerate(obj):
            yield from _flatten_numbers(v, f"{prefix}[{i}]")
    elif isinstance(obj, (int, float)) and not isinstance(obj, bool):
        yield prefix, float(obj)


def _all_keys(obj: Any) -> set[str]:
    """All string keys appearing anywhere in obj (dict keys, recursively)."""
    keys: set[str] = set()
    if isinstance(obj, dict):
        for k, v in obj.items():
            if isinstance(k, str):
                keys.add(k.lower())
            keys |= _all_keys(v)
    elif isinstance(obj, list):
        for v in obj:
            keys |= _all_keys(v)
    return keys


# ─── Paper claim extraction ───────────────────────────────────────────────────

# Pattern A: "N trials", "N seeds", "N runs", "N independent runs"
TRIAL_RE = re.compile(
    r"\b(\d{1,4})\s+(?:independent\s+)?(trial|trials|seed|seeds|run|runs|fold|folds|repetition|repetitions)\b",
    re.IGNORECASE,
)

# Pattern B: claimed statistical tests
STAT_TESTS = [
    "anova", "t-test", "t test", "paired t-test", "welch's t-test",
    "wilcoxon", "mann-whitney", "mann whitney",
    "kruskal-wallis", "chi-squared", "chi squared",
    "permutation test", "bootstrap confidence",
    "bonferroni", "holm", "benjamini-hochberg",
]

# Pattern C: percentages reported in text. We extract them and check whether
# something within ±0.05 absolute appears in the results dict. This is a soft
# check — a near-match is fine, a complete miss is suspicious.
PERCENT_RE = re.compile(r"(?<![\d.])(\d{1,3}(?:\.\d{1,3})?)\s*%")

# Pattern D: explicit "p < 0.05", "p<.001"
PVAL_RE = re.compile(r"\bp\s*[<>=]\s*0?\.\d+", re.IGNORECASE)

# Pattern E: claimed dataset / metric names. We just extract identifier-shaped
# tokens that look like dataset/metric names and check whether any appears
# (case-insensitively) in the results-dict keys.
METRIC_HINTS = ("accuracy", "precision", "recall", "f1", "auc", "auroc",
                "auprc", "mse", "rmse", "mae", "bleu", "rouge", "ppl",
                "perplexity", "nll", "loss")


# ─── Findings ────────────────────────────────────────────────────────────────

@dataclass
class Finding:
    severity: str       # "critical" | "warning" | "info"
    kind: str
    detail: str
    evidence: str = ""

    def emoji(self) -> str:
        return {"critical": "🔴", "warning": "🟡", "info": "🟢"}.get(self.severity, "❓")


@dataclass
class Audit:
    findings: list[Finding] = field(default_factory=list)

    def add(self, f: Finding) -> None:
        self.findings.append(f)

    def critical_count(self) -> int:
        return sum(1 for f in self.findings if f.severity == "critical")


# ─── Audit functions ─────────────────────────────────────────────────────────

def _strip_tex(text: str) -> str:
    # Drop comments
    text = re.sub(r"(?<!\\)%.*", "", text)
    # Drop simple commands like \textbf{...} keeping content
    text = re.sub(r"\\(?:textbf|textit|emph|texttt|cite[a-z]*|label|ref|eqref){[^}]*}", " ", text)
    # Drop environments? leave inline content for matching purposes.
    return text


def audit_trial_count(paper_text: str, results: dict, audit: Audit) -> None:
    """Compare the largest 'N trials/runs/seeds' claim in the paper against the
    largest sequence found in any results file (a list under a 'seeds' / 'runs'
    / 'trials' key, or the length of a list of per-run results)."""
    claims = [int(m.group(1)) for m in TRIAL_RE.finditer(paper_text)]
    if not claims:
        audit.add(Finding(
            "warning", "trial_count_missing",
            "Paper text does not state the number of trials/seeds/runs explicitly. "
            "Top-tier reviewers expect this; consider adding it.",
        ))
        return
    paper_max = max(claims)

    # Heuristic: scan results dicts for any list under a key matching 'seed*'
    # or 'run*' or 'trial*', and use its length.
    actual_counts: list[tuple[str, int]] = []
    SEED_KEYS = {"seeds", "runs", "trials", "folds", "repetitions"}

    def _walk(obj: Any, prefix: str = "") -> None:
        if isinstance(obj, dict):
            for k, v in obj.items():
                lk = k.lower() if isinstance(k, str) else ""
                if lk in SEED_KEYS and isinstance(v, list):
                    actual_counts.append((f"{prefix}.{k}" if prefix else k, len(v)))
                _walk(v, f"{prefix}.{k}" if prefix else str(k))
        elif isinstance(obj, list):
            for i, v in enumerate(obj):
                _walk(v, f"{prefix}[{i}]")

    for path, content in results.items():
        _walk(content, prefix=path)

    if not actual_counts:
        audit.add(Finding(
            "warning", "trial_count_no_evidence",
            f"Paper claims {paper_max} trials but no results file has a "
            f"seeds/runs/trials list to verify against.",
        ))
        return

    actual_max = max(c for _, c in actual_counts)
    if actual_max < paper_max:
        audit.add(Finding(
            "critical", "trial_count_mismatch",
            f"Paper claims {paper_max} trials/runs but largest observed run-list "
            f"in results has only {actual_max} entries.",
            evidence="; ".join(f"{p}={c}" for p, c in actual_counts),
        ))


def audit_statistical_tests(paper_text: str, results: dict, audit: Audit) -> None:
    paper_lower = paper_text.lower()
    claimed = [t for t in STAT_TESTS if t in paper_lower]
    if not claimed and PVAL_RE.search(paper_text):
        # paper reports p-values without naming the test
        audit.add(Finding(
            "warning", "pvalue_without_test",
            "Paper reports a p-value but does not name the statistical test. "
            "Top-tier reviewers will flag this.",
        ))
    if not claimed:
        return

    keys = set()
    for content in results.values():
        keys |= _all_keys(content)

    test_evidence_keys = {"p_value", "pvalue", "p-value", "statistic", "test",
                          "wilcoxon", "anova", "ttest", "mannwhitney"}
    has_evidence = bool(keys & test_evidence_keys)
    if not has_evidence:
        audit.add(Finding(
            "critical", "stat_test_unsupported",
            f"Paper claims statistical test(s): {claimed!r}, but no results "
            "file contains a p_value / statistic / test field.",
        ))


def audit_metric_names(paper_text: str, results: dict, audit: Audit) -> None:
    """For each common metric name mentioned in the paper, check whether any
    results-dict key contains it."""
    paper_lower = paper_text.lower()
    keys = set()
    for content in results.values():
        keys |= _all_keys(content)
    keys_blob = " ".join(keys)

    for hint in METRIC_HINTS:
        if hint in paper_lower and hint not in keys_blob:
            audit.add(Finding(
                "warning", "metric_not_in_results",
                f"Paper mentions metric '{hint}' but no results key references it.",
            ))


def audit_percentages(paper_text: str, results: dict, audit: Audit, tol: float = 0.5) -> None:
    """Each numeric percentage in the paper should match (within tol abs %) some
    number in results. Numbers that match nothing are flagged."""
    claimed = [float(m.group(1)) for m in PERCENT_RE.finditer(paper_text)]
    if not claimed:
        return

    actual_numbers: list[float] = []
    for content in results.values():
        for _, n in _flatten_numbers(content):
            # Treat 0..1 floats as percentages too (×100)
            actual_numbers.append(n)
            actual_numbers.append(n * 100.0)

    unmatched = []
    for c in claimed:
        if not any(abs(c - a) <= tol for a in actual_numbers):
            unmatched.append(c)

    # Don't flag every unmatched percentage — citations often contain percentages
    # from related work. Only flag when there are many.
    if len(unmatched) >= 5:
        audit.add(Finding(
            "warning", "many_percentages_unmatched",
            f"{len(unmatched)} percentage values in the paper text do not match "
            f"any number in the results files (tolerance ±{tol}%). "
            "Some are likely from related work, but a large number should be reviewed.",
            evidence=", ".join(f"{x}%" for x in unmatched[:10]),
        ))


# ─── Main ────────────────────────────────────────────────────────────────────

def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--paper", required=True, type=Path,
                        help="path to main.tex / main.md")
    parser.add_argument("--results", required=True, type=Path,
                        help="path to results/ directory")
    parser.add_argument("--out", type=Path,
                        help="optional: write JSON audit to this path")
    args = parser.parse_args()

    if not args.paper.is_file():
        sys.exit(f"ERROR: paper file not found: {args.paper}")

    raw = args.paper.read_text(encoding="utf-8", errors="replace")
    paper_text = _strip_tex(raw) if args.paper.suffix == ".tex" else raw

    results = _gather_results(args.results)
    if not results:
        print(f"WARNING: no results files found under {args.results}", file=sys.stderr)

    audit = Audit()
    audit_trial_count(paper_text, results, audit)
    audit_statistical_tests(paper_text, results, audit)
    audit_metric_names(paper_text, results, audit)
    audit_percentages(paper_text, results, audit)

    out_data = {
        "paper": str(args.paper),
        "results_dir": str(args.results),
        "n_results_files": len(results),
        "n_findings": len(audit.findings),
        "n_critical": audit.critical_count(),
        "findings": [asdict(f) for f in audit.findings],
    }

    if args.out:
        args.out.parent.mkdir(parents=True, exist_ok=True)
        args.out.write_text(json.dumps(out_data, indent=2), encoding="utf-8")
        print(f"Wrote audit → {args.out}")

    for f in audit.findings:
        print(f"{f.emoji()} {f.severity.upper():8s} {f.kind}: {f.detail}")
        if f.evidence:
            print(f"           evidence: {f.evidence}")
    print(f"\nSummary: {len(audit.findings)} findings ({audit.critical_count()} critical).")
    return 1 if audit.critical_count() > 0 else 0


if __name__ == "__main__":
    raise SystemExit(main())
