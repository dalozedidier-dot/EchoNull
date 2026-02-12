#!/usr/bin/env bash
set -euo pipefail

echo "[EchoNull] Diagnostics CI (v0.1.2)"
echo

if [ ! -f "pyproject.toml" ]; then
  echo "ERREUR: pyproject.toml introuvable. Exécute ce script a la racine du repo." >&2
  exit 2
fi

echo "== install"
python -m pip install -U pip
pip install -e ".[dev]"
echo

echo "== ruff check src tests"
ruff check src tests
echo

echo "== black --check src tests"
black --check src tests
echo

echo "== mypy src tests"
mypy src tests
echo

echo "== pytest -q --cov=echonull"
pytest -q --cov=echonull --cov-report=term-missing:skip-covered --cov-fail-under=100
