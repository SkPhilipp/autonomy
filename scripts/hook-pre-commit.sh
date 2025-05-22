#!/usr/bin/env bash

set -e
set -o pipefail
trap '[ "$?" -ne 0 ] && echo "[WARN] Commit cancelled."' EXIT

export PYTHONPATH=src

# Run mypy
echo "[INFO] pre-commit: Running type checker."
uv run mypy src/

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
if uv run pytest --cov=. --cov-report json:.coverage.json; then
  echo "[INFO] pre-commit: Tests passed."
else
  echo "[WARN] pre-commit: Tests failed."
  exit 1
fi

# Check for files with 0% test coverage (excluding files with no statements)
zero_cov_files=$(jq -r '.files | to_entries[] | select(.value.summary.num_statements > 0 and .value.summary.percent_covered == 0) | .key' .coverage.json)
if [ -n "$zero_cov_files" ]; then
  echo "[WARN] The following files have 0% test coverage:"
  echo "$zero_cov_files"
  exit 1
else
  echo "[INFO] All files have some test coverage."
fi
