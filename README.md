EchoNull (v0.1.1)

Objectif

EchoNull est un mini banc d'essai qui exécute plusieurs analyseurs sur des datasets synthétiques, produit des artefacts auditables (JSON, CSV, hashes), et sert de base stable pour des runs CI reproductibles.

Structure

- common : utilitaires partagés (hash, timers)
- graph_analysis : analyse graph (NetworkX)
- delta_stats : statistiques simples
- mark_counts : comptages simples
- orchestrator : générateur de datasets, exécution multi-runs, packaging zip
- benchmarks : utilitaires de benchmark, dont un résumé de consommation GitHub Actions

Installation (local)

1) Créer un virtualenv
2) Installer les dépendances

    pip install -r requirements.txt -r requirements-dev.txt
    pip install -r common/requirements.txt -r graph_analysis/requirements.txt -r delta_stats/requirements.txt -r mark_counts/requirements.txt -r orchestrator/requirements.txt

3) Lancer les gates

    ruff check .
    black --check .
    mypy .
    pytest --cov --cov-report=term-missing --cov-fail-under=100

Run orchestrator

Exemple simple :

    python -m orchestrator.run --runs 5 --out _ci_out --workers 2 --zip

Cela crée :
- _ci_out/ (runs + overview.json + manifest.json)
- _ci_out.zip

CI GitHub Actions

Trois workflows sont fournis :

- .github/workflows/ci.yml : lint, mypy, tests
- .github/workflows/sweep.yml : sweep léger planifié et déclenchable à la demande
- .github/workflows/extended_tests.yml : exécution planifiée plus lourde (tests étendus + soak sweep)

Hygiène repo

- Ne pas versionner les dossiers de sortie (_ci_out, _soak_out).
- Garder tous les workflows valides et complets. Les fragments YAML cassent Actions et les hooks check-yaml.
