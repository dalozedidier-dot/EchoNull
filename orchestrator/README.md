# orchestrator

Orchestrateur isolé qui :
- génère un dataset minimal par run (CSV)
- appelle les analyzers via `AnalyzerProtocol`
- produit un `overview.json` et un `manifest.json`
- optionnellement zippe le dossier de sortie

Exemple :
```bash
python -m orchestrator.run --runs 100 --out _out --workers 4 --zip
```
