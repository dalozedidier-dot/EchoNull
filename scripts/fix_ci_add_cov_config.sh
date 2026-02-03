#!/usr/bin/env bash
set -euo pipefail

ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
WF_DIR="$ROOT/.github/workflows"

if [[ ! -d "$WF_DIR" ]]; then
  echo "ERREUR: dossier .github/workflows introuvable"
  exit 1
fi

if [[ ! -f "$ROOT/.coveragerc" ]]; then
  echo "ERREUR: .coveragerc absent a la racine. Copie-le depuis le bundle."
  exit 1
fi

# sed -i compatible GNU et BSD
sed_inplace() {
  local expr="$1"
  local file="$2"
  if sed --version >/dev/null 2>&1; then
    sed -i -E "$expr" "$file"
  else
    sed -i '' -E "$expr" "$file"
  fi
}

patched=0
shopt -s nullglob
for f in "$WF_DIR"/*.yml "$WF_DIR"/*.yaml; do
  cp "$f" "$f.bak"

  if grep -qE 'pytest\b.*--cov(=|\s)' "$f" && ! grep -qE 'pytest\b.*--cov-config=\.coveragerc' "$f"; then
    sed_inplace 's/(pytest[^\n]*--cov=[^ \t\n]+)/\1 --cov-config=.coveragerc/' "$f"
    sed_inplace 's/(pytest[^\n]*--cov[ \t]+[^ \t\n]+)/\1 --cov-config=.coveragerc/' "$f"
    patched=$((patched+1))
    echo "OK: patch $f"
  else
    echo "INFO: rien a faire $f"
  fi
done

echo "Termine. Workflows modifies: $patched"
echo "Des sauvegardes .bak ont ete creees."
