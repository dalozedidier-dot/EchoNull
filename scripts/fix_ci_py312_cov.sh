#!/usr/bin/env bash
set -euo pipefail

# EchoNull CI fix: enforce Python 3.12-only (PEP 695) + fix coverage target (repo not in src/ layout)
# - Removes python 3.10 and 3.11 from workflow matrices (both inline and block lists)
# - Replaces --cov=src / --cov src -> --cov=. / --cov .
# - Replaces PYTHONPATH: src -> PYTHONPATH: .
# - Creates .bak backup next to the workflow file

ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"

# Default target: .github/workflows/ci.yml (fallback to ci.yaml)
WF1="$ROOT/.github/workflows/ci.yml"
WF2="$ROOT/.github/workflows/ci.yaml"

if [[ -f "$WF1" ]]; then
  WF="$WF1"
elif [[ -f "$WF2" ]]; then
  WF="$WF2"
else
  echo "ERROR: could not find .github/workflows/ci.yml or ci.yaml" >&2
  echo "Tip: if your workflow has a different name, edit this script to point to it." >&2
  exit 1
fi

BAK="$WF.bak"
if [[ ! -f "$BAK" ]]; then
  cp "$WF" "$BAK"
  echo "Backup created: $BAK"
else
  echo "Backup already exists: $BAK"
fi

# 1) Fix coverage target (repo not in src/ layout)
# Replace --cov=src -> --cov=.
# Replace --cov src -> --cov .
perl -i -pe 's/--cov=src\b/--cov=./g; s/--cov\s+src\b/--cov ./g' "$WF"

# 2) Fix PYTHONPATH
# Replace PYTHONPATH: src / "src" / '\''src'\'' -> PYTHONPATH: .
perl -i -pe 's/\bPYTHONPATH:\s*["'\'']?src["'\'']?\b/PYTHONPATH: ./g' "$WF"

# 3) Remove Python 3.10 and 3.11 from matrices (works for inline lists and block lists)
# Inline list removal: delete elements "3.10" and "3.11" with comma hygiene
perl -i -pe '
  s/\b["'\'']?3\.10["'\'']\s*,\s*//g;
  s/,\s*\b["'\'']?3\.10["'\'']\b//g;
  s/\b["'\'']?3\.11["'\'']\s*,\s*//g;
  s/,\s*\b["'\'']?3\.11["'\'']\b//g;
' "$WF"

# Block list removal: delete YAML list items "- 3.10" / "- \"3.10\"" / "- '\''3.10'\''" (same for 3.11)
# This is intentionally broad: if you listed Python versions anywhere, 3.10/3.11 lines will be removed.
perl -i -ne '
  if (/^\s*-\s*["'\'']?3\.(10|11)["'\'']?\s*$/) { next; }
  print;
' "$WF"

# 4) Light cleanup: collapse empty inline python-version lists if they occur (rare)
# If python-version: [] happens, replace with python-version: ["3.12"]
perl -i -pe 's/(\bpython-version:\s*)\[\s*\]/$1["3.12"]/g' "$WF"

echo "Patched: $WF"
echo "Now run:"
echo "  git diff"
echo "  git commit -am \"ci: py312-only + fix coverage target\""
echo "  git push"
