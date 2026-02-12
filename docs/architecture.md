# Architecture

EchoNull est compose de modules simples, relies par un orchestrateur.

## Modules

- echonull.common
  - utilitaires transverses (sha256, timers, protocoles)
- echonull.delta_stats
  - statistiques robustes sur deltas synthetiques
- echonull.graph_analysis
  - construction d un graph simple et metriques (jaccard)
- echonull.mark_counts
  - comptages deterministes (fichier texte)
- echonull.orchestrator
  - generation dataset CSV
  - execution multi-run
  - ecriture d artefacts et packaging zip

## Flux

1) l orchestrateur genere un CSV pour chaque run
2) les analyseurs produisent leurs artefacts dans run_xxxx/
3) overview.json agrege les resultats
4) manifest.json scelle les parametres et le hash de overview.json
