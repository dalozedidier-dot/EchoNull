Notes de patch (v0.1.1)

Ce patch fait deux choses.

1) Stabilise le benchmark "usage_report" avec Pandas 3.0
   Le chargement des CSV de consommation GitHub Actions nettoie maintenant toutes les colonnes de type texte, y compris les nouveaux dtypes string de Pandas. Cela évite un cas où le job "test" n'était plus reconnu, et où le résumé plantait avec un IndexError.

2) Nettoie les workflows GitHub Actions
   Les workflows fragmentaires et mal indentés ont été retirés. Il reste trois workflows valides.
   - ci.yml : lint, mypy, tests
   - sweep.yml : sweep planifié léger
   - extended_tests.yml : exécution planifiée plus lourde, incluant un soak sweep
