EchoNull (v0.1.2)

Objectif

EchoNull est un mini banc d'essai qui exécute plusieurs analyseurs sur des datasets synthétiques, produit des artefacts auditables (JSON, CSV, hashes) et sert de base stable pour des runs CI reproductibles.

Quickstart

Installation (local) :

    python -m pip install -U pip
    pip install -e ".[dev]"

Run orchestrator :

    echonull-orchestrator --runs 5 --thresholds 0.25,0.5 --out _ci_out --workers 2 --zip

Ou :

    python -m echonull.orchestrator.run --runs 5 --out _ci_out --workers 2 --zip

Doctor :

    echonull-doctor
    echonull-doctor --json

Structure

Code Python (packaging) :

- src/echonull/common : utilitaires partages (hash, timers)
- src/echonull/graph_analysis : analyse graph (NetworkX)
- src/echonull/delta_stats : statistiques simples
- src/echonull/mark_counts : comptages simples
- src/echonull/orchestrator : generateur de datasets, execution multi-runs, packaging zip

CI GitHub Actions

Workflows principaux :

- .github/workflows/ci.yml : lint, mypy, tests, build
- .github/workflows/sweep.yml : sweep leger planifie et declenchable
- .github/workflows/extended_tests.yml : tests et soak sweep planifies
- .github/workflows/release.yml : release GitHub et PyPI sur tags

Docs

- docs/quickstart.md
- docs/architecture.md
- docs/artifacts.md
- docs/reproducibility.md

Hygiene repo

- Ne pas versionner les dossiers de sortie (_ci_out, _soak_out, dist).
- Garder tous les workflows valides et complets.
