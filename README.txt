EchoNull — Workflow cleanup bundle (suppression BareFlux + correction common.yml)
Date: 2026-02-03

Objet:
  - Supprimer le workflow "BareFlux CI - Tests + Shadow Diff ..." présent dans EchoNull (hors périmètre module-2).
  - Corriger l'incohérence "orchestrator" pointant sur `.github/workflows/common.yml` :
      -> renommer common.yml selon son champ `name:` (ex: orchestrator.yml)
      -> réécrire les références `uses: .../common.yml` vers le nouveau nom.

Usage:
  1) Dézip à la racine du repo EchoNull.
  2) Dry-run:
       python tools/cleanup_workflows_echonull.py --dry-run
  3) Apply:
       python tools/cleanup_workflows_echonull.py --apply
  4) Commit + push.

Rapport généré:
  - _workflow_cleanup_report.json

Note:
  - Le script supprime tout workflow dont le fichier, le `name:` ou le contenu match "bareflux" (case-insensitive).
  - Si `.github/workflows/common.yml` n'existe pas ou n'a pas de `name:`, il ne renomme pas.
