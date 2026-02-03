EchoNull — Sanitize bundle (remove BareFlux workflow + fix UP047 + cleanup tools)
Date: 2026-02-03

Contexte observé (logs_56233836943.zip):
  - Ruff échoue sur:
      common/utils.py: UP047 (perf_timer)
    ET sur des scripts de tools ajoutés par erreur:
      tools/cleanup_workflows_echonull.py (E501/I001/F401)
      tools/purge_bareflux_from_echonull.py (E501/F401)

But:
  - Revenir à une séparation stricte "module-2" (EchoNull) vs "module-4" (BareFlux).
  - Nettoyer les artefacts hors-périmètre.
  - Débloquer la CI Ruff.

Procédure:
  1) Dézip à la racine du repo EchoNull.
  2) Dry-run (voir exactement ce qui sera fait):
       python tools/sanitize_echonull.py --dry-run
  3) Apply:
       python tools/sanitize_echonull.py --apply
  4) Vérifier:
       git status
       git diff
  5) Commit + push sur la branche exécutée par CI.

Note:
  - Ce script ne peut pas "supprimer des fichiers" via un zip; il les supprime localement quand tu l'exécutes.
  - La CI ne change que quand tu commit/push.
