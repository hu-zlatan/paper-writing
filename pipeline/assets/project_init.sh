#!/usr/bin/env bash
# project_init.sh — scaffold a research project with the canonical layout.
#
# Usage:
#   bash project_init.sh <project_name> [target_venue]
#
# Example:
#   bash project_init.sh sparse-attention-bench NeurIPS

set -euo pipefail

PROJECT_NAME="${1:-}"
TARGET_VENUE="${2:-NeurIPS}"

if [[ -z "$PROJECT_NAME" ]]; then
  echo "Usage: $0 <project_name> [target_venue]" >&2
  exit 1
fi

if [[ -e "$PROJECT_NAME" ]]; then
  echo "Error: $PROJECT_NAME already exists. Refusing to overwrite." >&2
  exit 1
fi

# Resolve path to skill assets (script lives at <skill>/scripts/, assets at <skill>/assets/)
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
ASSETS_DIR="$(cd "$SCRIPT_DIR/../assets" && pwd)"

echo "→ Creating project: $PROJECT_NAME (target venue: $TARGET_VENUE)"

mkdir -p "$PROJECT_NAME"/{code,data,docs,paper/mypaper,paper/mypaper/figures,plans,results,results/v1}

# Copy templates
cp "$ASSETS_DIR/PROGRESS.template.md"   "$PROJECT_NAME/PROGRESS.md"
cp "$ASSETS_DIR/RESTRICTS.template.yaml" "$PROJECT_NAME/RESTRICTS.yaml"

# Substitute basic placeholders
NOW="$(date -u +%Y-%m-%dT%H:%M:%SZ)"
sed -i.bak "s|<project_name>|$PROJECT_NAME|g; s|<ISO timestamp>|$NOW|g" "$PROJECT_NAME/PROGRESS.md"
sed -i.bak "s|<project_name>|$PROJECT_NAME|g; s|<ISO timestamp>|$NOW|g; s|target_venue: \"NeurIPS\"|target_venue: \"$TARGET_VENUE\"|" "$PROJECT_NAME/RESTRICTS.yaml"
rm -f "$PROJECT_NAME/PROGRESS.md.bak" "$PROJECT_NAME/RESTRICTS.yaml.bak"

# .gitignore
cat > "$PROJECT_NAME/.gitignore" <<'EOF'
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
EOF

# .gitkeep markers so empty dirs are tracked
touch "$PROJECT_NAME/data/.gitkeep" \
      "$PROJECT_NAME/docs/.gitkeep" \
      "$PROJECT_NAME/plans/.gitkeep" \
      "$PROJECT_NAME/results/v1/.gitkeep" \
      "$PROJECT_NAME/paper/mypaper/figures/.gitkeep"

# README — points to the skill itself rather than duplicating content
cat > "$PROJECT_NAME/README.md" <<EOF
# $PROJECT_NAME

Target venue: **$TARGET_VENUE**
Created: $NOW

This project is managed under the \`auto-research-pipeline\` skill. See:

- \`PROGRESS.md\` — single source of truth for stage progress.
- \`RESTRICTS.yaml\` — pipeline constraints (do not relax CRITICAL fields).
- \`plans/\` — per-stage plans, written before each stage runs.
- \`docs/\` — pipeline artefacts (problem tree, knowledge cards, synthesis, hypothesis).
- \`code/\` — experiment code; every script runs a 5-minute pilot first.
- \`results/\` — versioned per loop (v1, v2, ...).
- \`paper/mypaper/\` — manuscript drafts, reviews, audits, rebuttals.

## Resume protocol
1. Read the latest entry in \`PROGRESS.md\`.
2. If it has a "Finished" timestamp and decision PROCEED, continue at the next stage.
3. If it is a LOOP MARKER, continue at the loop's target stage.
4. If "Finished" is missing, open \`plans/\` for that stage and resume from where it stopped.
EOF

# git init + initial commit
(
  cd "$PROJECT_NAME"
  git init -q
  git add -A
  git commit -q -m "stage 0 PROJECT_INIT: scaffold for $PROJECT_NAME (venue=$TARGET_VENUE)"
)

echo "✓ Project scaffolded at: $(cd "$PROJECT_NAME" && pwd)"
echo "  Next: write plans/stage_01_topic_init.md, then run stage 1."
