#!/usr/bin/env bash
set -euo pipefail

echo "[EchoNull] Correctif duplication de module (v0.1.2)"
echo

# 0) Préconditions
if [ ! -d ".git" ]; then
  echo "ERREUR: ce dossier ne semble pas être la racine d'un dépôt git (.git absent)." >&2
  exit 2
fi

if [ ! -f "pyproject.toml" ]; then
  echo "ERREUR: pyproject.toml introuvable. Exécute ce script à la racine du repo." >&2
  exit 2
fi

ROOT_FILE="patch_nulltrace_mypy.py"
SCRIPTS_FILE="scripts/patch_nulltrace_mypy.py"

echo "[1/5] Vérification présence des fichiers ciblés"
if [ ! -f "$SCRIPTS_FILE" ]; then
  echo "ERREUR: $SCRIPTS_FILE absent. Attendu: conserver ce fichier." >&2
  exit 3
fi

if [ ! -f "$ROOT_FILE" ]; then
  echo "ATTENTION: $ROOT_FILE absent. Rien à supprimer."
else
  echo "OK: doublon racine détecté: $ROOT_FILE"
fi
echo

echo "[2/5] Recherche de toutes les occurrences du fichier (diagnostic)"
find . -name "patch_nulltrace_mypy.py" -print
echo

echo "[3/5] Suppression du doublon en racine (si présent)"
if [ -f "$ROOT_FILE" ]; then
  git rm -f "$ROOT_FILE"
  echo "OK: git rm $ROOT_FILE"
else
  echo "SKIP: aucun doublon en racine."
fi
echo

echo "[4/5] Vérification unicité (attendu: un seul chemin)"
COUNT="$(find . -name "patch_nulltrace_mypy.py" -print | wc -l | tr -d ' ')"
if [ "$COUNT" -ne 1 ]; then
  echo "ERREUR: unicité non satisfaite. Nombre de fichiers trouvés: $COUNT" >&2
  find . -name "patch_nulltrace_mypy.py" -print >&2
  exit 4
fi
echo "OK: unicité satisfaite."
echo

echo "[5/5] Exécution gates locales (ruff -> black --check -> mypy -> pytest -q)"
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
echo
echo "Terminé. Si tout est OK: commit + push, puis relance CI."
