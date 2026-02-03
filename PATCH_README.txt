EchoNull — Solution bundle Ruff UP047 (perf_timer)
Date: 2026-02-03

Ce bundle vise un cas unique:
  - ruff: common/utils.py:..: UP047 Generic function `perf_timer` should use type parameters

Pourquoi tu vois toujours la même erreur dans les logs ?
  - Le job lint checkout un commit précis.
  - Tant que la modif de `common/utils.py` n'est pas COMMITÉE sur la branche exécutée (souvent main),
    ruff revoit l'ancienne version et échoue.

Pourquoi “une ligne BareFlux” peut apparaître dans tes échanges ?
  - Ce n'est pas dans les logs EchoNull. C'est un effet de contexte (noms de zips / snippets / messages).
  - Dans `lint/system.txt` de tes logs: le job est défini dans dalozedidier-dot/EchoNull.

Procédure déterministe (sans hypothèse):
  1) Dézip à la racine du repo EchoNull.
  2) Exécute:
       python tools/fix_up047_perf_timer.py --file common/utils.py
  3) Vérifie:
       git diff
  4) Commit + push sur la branche exécutée par le workflow.
  5) Relance le workflow.

Option CI (garde-fou):
  - insérer ci_snippets/enforce_up047_fix_before_ruff.yml AVANT ruff check.
