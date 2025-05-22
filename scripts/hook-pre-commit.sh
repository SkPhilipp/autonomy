#!/usr/bin/env bash

set -e
set -o pipefail
trap '[ "$?" -ne 0 ] && echo "[WARN] Commit cancelled."' EXIT

# Run mypy
echo "[INFO] pre-commit: Running type checker."
uv run mypy .

# Run black on all Python files
echo "[INFO] pre-commit: Running formatter."
uv run black .
if git diff --quiet; then
  echo "[INFO] pre-commit: Formatter passed."
else
  echo "[WARN] pre-commit: Please review formatter changes and stage them."
  exit 1
fi

# Run pytest with coverage
echo "[INFO] pre-commit: Running tests with coverage."
if uv run pytest --cov=. --cov-report term:skip-covered --cov-report json:.cov.json; then
  echo "[INFO] pre-commit: Tests passed."
else
  echo "[WARN] pre-commit: Tests failed."
  exit 1
fi
