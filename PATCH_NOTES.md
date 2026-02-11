Notes de patch (v0.1.2)

Ce patch supprime des incohérences qui pouvaient faire perdre du temps lors d'une reprise.

1) Gates coverage alignées
   - Le README et la configuration coverage visent 100%.
   - La CI utilisait encore --cov-fail-under=80.
   - La CI est alignée sur 100%.

2) Workflow hors dossier workflows clarifié
   - GitHub Actions ne détecte que les workflows placés dans .github/workflows.
   - Le fichier .github/extended_tests.yml n'était donc pas exécuté et créait une confusion.
   - Il est remplacé par un petit fichier YAML informatif qui renvoie vers .github/workflows/extended_tests.yml.

3) src/null_trace.py rendu sûr
   - Le module ne fait plus un import obligatoire de nulltrace au chargement.
   - L'import est optionnel et effectué dans main(), avec un message explicite si nulltrace n'est pas installé.
