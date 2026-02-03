#!/usr/bin/env bash
set -euo pipefail

# EchoNull CI fix (v2): enforce Python 3.12-only (PEP 695) + fix coverage target (repo not in src/ layout)
#
# What it does:
# - Patches *all* workflow files under .github/workflows/*.yml|*.yaml
# - Removes Python 3.10 and 3.11 from version lists (inline + block YAML lists)
# - Replaces coverage target:  --cov=src / --cov src  ->  --cov=. / --cov .
# - Replaces PYTHONPATH: src -> PYTHONPATH: .
# - Creates a .bak backup next to every modified workflow

ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
WF_DIR="$ROOT/.github/workflows"

if [[ ! -d "$WF_DIR" ]]; then
  echo "ERROR: $WF_DIR not found" >&2
  exit 1
fi

shopt -s nullglob
WORKFLOWS=("$WF_DIR"/*.yml "$WF_DIR"/*.yaml)
shopt -u nullglob

if (( ${#WORKFLOWS[@]} == 0 )); then
  echo "ERROR: no workflow files found in $WF_DIR" >&2
  exit 1
fi

patched=0

for WF in "${WORKFLOWS[@]}"; do
  # Only patch if it looks like it sets up Python or runs pytest/coverage.
  if ! grep -Eq "setup-python|python-version|pytest|--cov=src|PYTHONPATH:\s*src" "$WF"; then
    continue
  fi

  BAK="$WF.bak"
  if [[ ! -f "$BAK" ]]; then
    cp "$WF" "$BAK"
  fi

  # 1) Coverage target
  perl -i -pe 's/--cov=src\b/--cov=./g; s/--cov\s+src\b/--cov ./g' "$WF"

  # 2) PYTHONPATH
  perl -i -pe 's/\bPYTHONPATH:\s*["'\''']?src["'\''']?\b/PYTHONPATH: ./g' "$WF"

  # 3) Remove 3.10 + 3.11 from inline lists (with comma hygiene)
  perl -i -pe '
    s/\b["'\''']?3\.10["'\''']\s*,\s*//g;
    s/,\s*\b["'\''']?3\.10["'\''']\b//g;
    s/\b["'\''']?3\.11["'\''']\s*,\s*//g;
    s/,\s*\b["'\''']?3\.11["'\''']\b//g;
  ' "$WF"

  # 4) Remove 3.10 + 3.11 YAML block list items
  perl -i -ne '
    if (/^\s*-\s*["'\''']?3\.(10|11)["'\''']?\s*$/) { next; }
    print;
  ' "$WF"

  # 5) If python-version became empty list, set it to ["3.12"]
  perl -i -pe 's/(\bpython-version:\s*)\[\s*\]/$1["3.12"]/g' "$WF"

  patched=$((patched+1))
  echo "Patched: $WF"
done

if (( patched == 0 )); then
  echo "No workflows matched patch criteria."
  echo "Tip: confirm your CI workflow is under .github/workflows/ and contains 'python-version' or 'pytest'."
  exit 2
fi

echo
echo "Done. Next:" 
echo "  git diff"
echo "  git status"
echo "  git commit -am 'ci: py312-only + fix coverage target'"
echo "  git push"
