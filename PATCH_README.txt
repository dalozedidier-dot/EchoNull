EchoNull — Correctif Ruff UP047 (perf_timer) — bundle
Date: 2026-02-03
Log: logs_56228682453.zip
Commit: df6c0c2fa6afb1298887f14e44d1c48c66b4e91d

Symptôme:
  common/utils.py:30:5: UP047 Generic function `perf_timer` should use type parameters

Correction attendue:
  - utiliser PEP 695 (Python 3.12+), ex:
      def perf_timer[**P, R](func: Callable[P, R]) -> Callable[P, R]:

Procédure (recommandée):
  1) Dézip à la racine du repo EchoNull
  2) Exécute:
       python tools/fix_up047_perf_timer.py --file common/utils.py
  3) Vérifie:
       git diff
  4) Commit + push sur main
  5) Relance le workflow CI (lint)

Option CI (garde-fou):
  - colle `ci_snippets/autofix_up047_before_ruff.yml` avant le step ruff.
