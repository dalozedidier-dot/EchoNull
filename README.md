# EchoNull

Monorepo Python 3.12+ structuré en modules isolés, nommés par fonction.
Objectif : exécuter des sweeps multi-runs rapidement avec une base CI stricte.

## Arborescence
- `orchestrator/` : orchestrateur, génération datasets, exécution multi-runs, packaging de sorties
- `graph_analysis/` : graphs, edges, Jaccard, thresholds
- `delta_stats/` : deltas absolus et stats robustes (p50–p99, MAD)
- `mark_counts/` : comptage de marks
- `common/` : utilitaires minimaux (hashing, timing, protocol)
- `benchmarks/` : scripts de perf
- `.github/workflows/` : CI isolée par module + un sweep global

## Démarrage rapide (local)
```bash
python -m venv .venv
source .venv/bin/activate
pip install -r requirements-dev.txt
pip install -r common/requirements.txt -r graph_analysis/requirements.txt -r delta_stats/requirements.txt -r mark_counts/requirements.txt -r orchestrator/requirements.txt

ruff check .
black --check .
mypy .
pytest -q --cov --cov-report=term-missing --cov-fail-under=100
```

## Lancer un sweep minimal
```bash
PYTHONPATH=src python -m orchestrator.run --runs 5 --out _out --zip
```

Notes
- Squelette fonctionnel, orienté perf, prêt à être durci.
- Les analyzers respectent une interface stricte via `AnalyzerProtocol`.
