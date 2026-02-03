EchoNull — patch Ruff UP047 (perf_timer) — logs_56228969919
Date: 2026-02-03

Constat:
  - ruff check . -> common/utils.py:30:5: UP047 Generic function `perf_timer` should use type parameters

Correctif:
  - Convertit perf_timer vers PEP 695:
      def perf_timer[**P, R](...) ...

Procédure (recommandée):
  1) Dézip à la racine du repo EchoNull
  2) Exécute:
       python tools/fix_up047_perf_timer.py --file common/utils.py
  3) Commit + push
  4) Relance le workflow lint

Option CI (bloquer tant que non commité):
  - Colle ci_snippets/autofix_up047_before_ruff.yml avant `ruff check .`
