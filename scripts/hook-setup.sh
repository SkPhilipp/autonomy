#!/usr/bin/env bash

set -e
set -o pipefail

# Symlink the pre-commit hook
HOOKS_DIR=".git/hooks"
SCRIPT_DIR="$(dirname "$0")"
PRE_COMMIT_SRC="$SCRIPT_DIR/hook-pre-commit.sh"
PRE_COMMIT_DEST="$HOOKS_DIR/pre-commit"

mkdir -p "$HOOKS_DIR"
ln -sf "../../scripts/hook-pre-commit.sh" "$PRE_COMMIT_DEST"
echo "[INFO] Symlinked scripts/hook-pre-commit.sh to .git/hooks/pre-commit." 
