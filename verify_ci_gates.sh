#!/usr/bin/env bash
set -euo pipefail

echo "[EchoNull] Diagnostics CI (v0.1.2)"
echo

if [ ! -f "pyproject.toml" ]; then
  echo "ERREUR: pyproject.toml introuvable. Exécute ce script à la racine du repo." >&2
  exit 2
fi

echo "== ls -la"
ls -la
echo

echo '== find . -maxdepth 2 -name "patch_nulltrace_mypy.py" -print'
find . -maxdepth 2 -name "patch_nulltrace_mypy.py" -print
echo

echo "== ruff check ."
ruff check .
echo

echo "== black --check ."
black --check .
echo

echo "== mypy ."
mypy .
echo

echo "== pytest -q"
pytest -q
