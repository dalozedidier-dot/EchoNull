EchoNull — patch Ruff UP047 (perf_timer) — logs_56229258607
EchoNull — patch Ruff UP047 (perf_timer) — logs_56229486958
Date: 2026-02-03

Constat:
  - ruff check . -> common/utils.py:30:5: UP047 Generic function `perf_timer` should use type parameters

Correctif:
  - Convertit perf_timer vers PEP 695:
      def perf_timer[**P, R](...) ...

Procédure:
  1) Dézip à la racine du repo EchoNull
  2) Exécute:
       python tools/fix_up047_perf_timer.py --file common/utils.py
  3) Commit + push
  4) Relance le workflow lint
