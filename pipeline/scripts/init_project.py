#!/usr/bin/env python3
"""init_project.py — scaffold a research project with the canonical layout.

Cross-platform alternative to assets/project_init.sh. Prefer this on systems
without bash/sed (Windows) or when Python is available everywhere.

Usage:
    python init_project.py <project_name> [--venue NeurIPS] [--topic "..."]

Example:
    python init_project.py sparse-attention-bench --venue NeurIPS \\
        --topic "Sparse attention for long-context efficiency"
"""

from __future__ import annotations

import argparse
import datetime as _dt
import shutil
import subprocess
import sys
from pathlib import Path

# Directory layout that matches references/project_layout.md
LAYOUT = [
    "code",
    "data",
    "data/fixtures",
    "docs",
    "paper/mypaper",
    "paper/mypaper/figures",
    "plans",
    "results",
    "results/v1",
]

GITIGNORE = """\
# data files (keep small fixtures only)
data/*
!data/.gitkeep
!data/fixtures/

# Python
__pycache__/
*.pyc
.venv/
*.egg-info/

# results — keep summaries, not raw blobs
results/**/raw/
results/**/checkpoints/
*.npz
*.npy
*.pt
*.pth
*.ckpt

# paper build artefacts
paper/mypaper/*.aux
paper/mypaper/*.log
paper/mypaper/*.out
paper/mypaper/*.bbl
paper/mypaper/*.blg
paper/mypaper/*.synctex.gz

# secrets
.env
*.key
"""

README_TEMPLATE = """\
# {name}

Target venue: **{venue}**
Topic: {topic}
Created: {now}

This project is managed under the `auto-research-pipeline` skill. See:

- `PROGRESS.md` — single source of truth for stage progress.
- `RESTRICTS.yaml` — pipeline constraints (do not relax CRITICAL fields).
- `plans/` — per-stage plans, written before each stage runs.
- `docs/` — pipeline artefacts (problem tree, knowledge cards, synthesis, hypothesis).
- `code/` — experiment code; every script runs a 5-minute pilot first.
- `results/` — versioned per loop (v1, v2, ...).
- `paper/mypaper/` — manuscript drafts, reviews, audits, rebuttals.

## Resume protocol
1. Read the latest entry in `PROGRESS.md`.
2. If it has a "Finished" timestamp and decision PROCEED, continue at the next stage.
3. If it is a LOOP MARKER, continue at the loop's target stage.
4. If "Finished" is missing, open `plans/` for that stage and resume from where it stopped.
"""


def _resolve_assets_dir(script_path: Path) -> Path:
    candidate = script_path.parent.parent / "assets"
    if not candidate.is_dir():
        sys.exit(
            f"ERROR: cannot locate assets/ directory (looked at {candidate}). "
            "init_project.py must live inside the skill's scripts/ folder."
        )
    return candidate


def _substitute(text: str, mapping: dict) -> str:
    out = text
    for key, val in mapping.items():
        out = out.replace(key, val)
    return out


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("project_name", help="kebab-case project directory name")
    parser.add_argument("--venue", default="NeurIPS",
                        help="Target conference (default: NeurIPS)")
    parser.add_argument("--topic", default="<one-sentence research topic>",
                        help="Research topic (will be inserted into RESTRICTS.yaml)")
    parser.add_argument("--no-git", action="store_true",
                        help="Skip git init / initial commit")
    args = parser.parse_args()

    project_name = args.project_name
    project_root = Path(project_name).resolve()
    if project_root.exists():
        sys.exit(f"ERROR: {project_root} already exists; refusing to overwrite.")

    assets_dir = _resolve_assets_dir(Path(__file__).resolve())
    progress_template = (assets_dir / "PROGRESS.template.md").read_text(encoding="utf-8")
    restricts_template = (assets_dir / "RESTRICTS.template.yaml").read_text(encoding="utf-8")

    print(f"→ Creating project: {project_name} (venue={args.venue})")

    # Make directories
    for sub in LAYOUT:
        (project_root / sub).mkdir(parents=True, exist_ok=True)

    # Substitute placeholders
    now = _dt.datetime.now(_dt.timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")
    sub = {
        "<project_name>": project_name,
        "<ISO timestamp>": now,
        "<one-sentence research topic>": args.topic,
        'target_venue: "NeurIPS"': f'target_venue: "{args.venue}"',
    }
    (project_root / "PROGRESS.md").write_text(_substitute(progress_template, sub), encoding="utf-8")
    (project_root / "RESTRICTS.yaml").write_text(_substitute(restricts_template, sub), encoding="utf-8")

    # README
    (project_root / "README.md").write_text(
        README_TEMPLATE.format(name=project_name, venue=args.venue, topic=args.topic, now=now),
        encoding="utf-8",
    )

    # .gitignore + .gitkeep
    (project_root / ".gitignore").write_text(GITIGNORE, encoding="utf-8")
    for keep in ("data", "docs", "plans", "results/v1", "paper/mypaper/figures"):
        (project_root / keep / ".gitkeep").touch()

    # git init
    if not args.no_git and shutil.which("git"):
        try:
            subprocess.run(["git", "init", "-q"], cwd=project_root, check=True)
            subprocess.run(["git", "add", "-A"], cwd=project_root, check=True)
            subprocess.run(
                ["git", "commit", "-q", "-m",
                 f"stage 0 PROJECT_INIT: scaffold for {project_name} (venue={args.venue})"],
                cwd=project_root,
                check=True,
            )
        except subprocess.CalledProcessError as e:
            print(f"  (git init failed: {e}; project still scaffolded)", file=sys.stderr)

    print(f"✓ Project scaffolded at: {project_root}")
    print(f"  Next: write plans/stage_01_topic_init.md, then run stage 1.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
