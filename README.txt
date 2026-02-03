EchoNull CI: correction coverage 100%

But
Exclure des rapports de couverture les fichiers qui ne doivent pas etre couverts par les tests unitaires:
benchmarks, tests, tools.

Pourquoi
Les logs montrent 16 lignes manquantes uniquement dans:
- benchmarks/benchmark_graph_analysis.py (0%, non execute par pytest)
- tests/conftest.py et tests/test_reproducibility.py (branches non prises)

Contenu
- .coveragerc: configuration Coverage.py appliquee par pytest-cov
- scripts/fix_ci_add_cov_config.sh: ajoute --cov-config=.coveragerc aux commandes pytest des workflows

Application
1) Copier .coveragerc a la racine du repo
2) Executer: bash scripts/fix_ci_add_cov_config.sh
3) Verifier: git diff
4) Commit et push

Note
Si tu preferes ne pas modifier le workflow, pytest-cov detecte souvent .coveragerc automatiquement.
Le script rend le lien explicite pour eviter tout comportement dependant de l'environnement.
