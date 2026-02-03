EchoNull — Correctif Ruff UP047 (perf_timer)
Date: 2026-02-03

Constat:
  - ruff: common/utils.py:..: UP047 Generic function `perf_timer` should use type parameters

Cause:
  - `perf_timer` est défini avec ParamSpec/TypeVar alors que Ruff attend des paramètres de type PEP 695 (Python 3.12+).

Correctif fourni:
  - tools/fix_up047_perf_timer.py :
      - convertit `perf_timer` vers: def perf_timer[**P, R](...)
      - retire les lignes `P = ParamSpec("P")` / `R = TypeVar("R")` si elles sont proches de la fonction
      - nettoie les imports `typing` si ParamSpec/TypeVar deviennent inutiles

Procédure déterministe:
  1) Dézip à la racine du repo EchoNull.
  2) Exécute:
       python tools/fix_up047_perf_timer.py --file common/utils.py
  3) Vérifie:
       git diff
  4) Commit + push (sur la branche exécutée par la CI).
  5) Relance le workflow lint.

Option CI (garde-fou, sans auto-commit):
  - ci_snippets/enforce_up047_fix_before_ruff.yml
    (échoue si le fix n'est pas commité, en affichant le diff)
