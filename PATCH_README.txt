EchoNull — purge workflow BareFlux (suppression)
Date: 2026-02-03

Objet:
  - Retirer de EchoNull un workflow "bareflux-*" (ou tout workflow contenant 'bareflux') qui n'a pas de rôle
    dans le module EchoNull.

Deux méthodes:

A) Script (robuste, ne dépend pas du nom exact)
  1) Dézip à la racine du repo EchoNull
  2) Dry-run (liste ce qui serait supprimé):
       python tools/purge_bareflux_from_echonull.py --dry-run
  3) Suppression:
       python tools/purge_bareflux_from_echonull.py
  4) Vérification:
       git status
       git diff
  5) Commit + push

B) Patch git (si le fichier s'appelle exactement .github/workflows/bareflux-improvements.yml)
  1) git apply patches/remove_bareflux_workflow.patch
  2) git status / commit / push

Notes:
  - Le script ne touche pas aux workflows EchoNull standards, sauf s'ils contiennent le token 'bareflux'.
  - Code retour 2 = fichiers supprimés (utile si tu l'appelles dans CI).
