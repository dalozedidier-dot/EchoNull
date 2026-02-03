EchoNull CI patch: py3.12-only + coverage cible = .

À appliquer:
1) Remplacer le fichier .github/workflows/ci.yml par celui du bundle.
2) Commit + push.
3) Vérifier que la CI ne lance plus de jobs Python 3.10/3.11 et que la coverage n'est plus à 0% artificiel.

Notes:
- Le seuil de couverture (fail-under=100) est conservé. Si la couverture réelle est < 100%, le job échouera "pour de vrai".
- Si tu as des workflows supplémentaires qui lancent encore une matrix 3.10/3.11, supprime-les ou aligne-les.
