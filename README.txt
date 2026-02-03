EchoNull — Correctif CI (py3.12-only + coverage) — 2026-02-03

Constats (logs_56244230274.zip):
- py3.10/py3.11: échec en collection (SyntaxError) car `perf_timer[...]` est PEP 695 (Python 3.12+).
- py3.12: 15 tests passent, mais couverture = 0% (No data was collected) car CI utilise `--cov=src`
  alors que le repo n'est pas en layout `src/`.

But:
- Aligner la CI sur Python 3.12+ (cohérent avec PEP 695).
- Collecter une couverture réelle (remplacer `--cov=src` par `--cov=.`).
- Nettoyer le `PYTHONPATH` (src -> .).

Application:
1) Dézip à la racine du repo EchoNull.
2) Exécute:
     bash scripts/echonull_fix_ci.sh
3) Vérifie:
     git diff
4) Commit + push:
     git commit -am "ci: py312-only + fix coverage target"
     git push

Notes:
- Le script fait un backup: .github/workflows/ci.yml.bak
- Si tu veux rester compatible py3.10/py3.11, il faut *revenir* à un perf_timer non-PEP695
  (TypeVar/ParamSpec) + config Ruff adaptée. Ce bundle ne vise pas ce régime-là.
