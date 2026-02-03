EchoNull — Sanitize bundle — logs_56234659392
Date: 2026-02-03

Ce que montrent les logs:
  - Ruff échoue sur:
      common/utils.py: UP047 (perf_timer)
      tools/cleanup_workflows_echonull.py: E501/I001/F401
      tools/purge_bareflux_from_echonull.py: F401/E501

But (sans compensation):
  - Supprimer les 2 tools parasites (ils ne doivent pas être versionnés dans EchoNull).
  - Corriger perf_timer en PEP 695 (UP047).
  - Supprimer tout workflow BareFlux présent dans .github/workflows (hors périmètre module-2).
  - Optionnel: renommer .github/workflows/common.yml selon son `name:` pour corriger l'affichage GitHub Actions.

Procédure:
  1) Dézip à la racine du repo EchoNull.
  2) Dry-run:
       python tools/sanitize_echonull.py --dry-run
       cat _echonull_sanitize_report.json
  3) Apply:
       python tools/sanitize_echonull.py --apply
  4) Vérifier:
       git status
       git diff
  5) Commit + push sur la branche exécutée par CI.

Attendu après commit:
  - Disparition des erreurs Ruff listées ci-dessus.
