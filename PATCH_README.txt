EchoNull — patch CI (Python 3.12+ + coverage) — 2026-02-03

Constats (logs_56244230274.zip):
- job test Python 3.10 : SyntaxError sur `def perf_timer[...]` (PEP 695 non supporté)
- job test Python 3.12 : tests OK mais coverage = 0% car `pytest --cov=src` (pas de dossier src)

Correctif:
- retirer les versions < 3.12 dans la matrix python-version
- remplacer `--cov=src` par `--cov=.`

Procédure:
1) Dézip à la racine du repo EchoNull.
2) Dry-run:
   python tools/patch_ci_py312_cov.py --dry-run
3) Apply:
   python tools/patch_ci_py312_cov.py --apply
4) Commit + push.

