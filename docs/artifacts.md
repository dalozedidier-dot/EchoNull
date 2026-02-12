# Artefacts et contrats

## Racine de sortie

- overview.json
- manifest.json
- run_0001/
- run_0002/
- ...

## Par run

- multi.csv
- delta_stats/stats.json
- mark_counts/count.txt
- graph_analysis/thr_0.25_report.json (un fichier par seuil)

## Validation

Le script scripts/validate_artifacts.py verifie la presence des fichiers attendus.
Les schemas JSON sont dans schemas/.
