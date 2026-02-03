EchoNull CI patch: afficher les lignes manquantes de coverage (term-missing) tout en gardant py3.12-only.

Contexte:
- La CI est désormais cohérente avec PEP 695 (Python 3.12 uniquement).
- Les tests passent mais la couverture réelle est ~96% et fail-under=100 fait échouer le job.

But de ce bundle:
- Ajouter un rapport "term-missing" dans les logs CI pour identifier précisément les lignes non couvertes.
- Ne change pas le seuil (fail-under=100) : l'échec reste un échec réel tant que la couverture n'est pas à 100.

Application:
1) Remplacer .github/workflows/ci.yml par celui du bundle.
2) Commit + push.
3) Relancer Actions et lire la section "coverage" (term-missing) pour savoir quoi tester/exclure.
