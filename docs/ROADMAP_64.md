# Roadmap and checklist (64 points)

Etat: ce fichier sert de checklist release-ready. Les points marques [x] sont implementes dans ce pack.

## A. Release and repository hygiene (1-16)

1. [x] Un seul workflow CI stable et complet (lint, tests, build)
2. [x] Workflow release sur tags v* (GitHub Release + artifacts)
3. [x] Support PyPI via Trusted Publisher (OIDC) dans release.yml
4. [x] Extraction automatique des release notes depuis CHANGELOG.md
5. [x] Dependabot (GitHub Actions + pip) active
6. [x] Templates GitHub issues (bug, feature)
7. [x] Fichier CITATION.cff
8. [x] Procedure release documentee (RELEASE.md)
9. [x] Makefile de commandes standard (lint, test, build, sweep)
10. [x] .gitignore et hygiene sorties (dist, _ci_out, _soak_out, etc)
11. [x] Bumpversion aligne VERSION, pyproject.toml, CHANGELOG.md
12. [x] Doctor command pour diagnostic environnement
13. [x] Job summary CI pour build
14. [x] Upload artefacts dist en CI
15. [x] SBOM workflow (CycloneDX) optionnel
16. [x] Nettoyage coverage config (pyproject + .coveragerc coherent)

## B. Packaging PyPI propre (17-32)

17. [x] PEP 621 (pyproject.toml) avec metadata complete
18. [x] Build-system setuptools + wheel
19. [x] Layout packaging src/ (package-dir=src)
20. [x] Namespace unique echonull.* pour eviter collisions top-level
21. [x] Console scripts: echonull-orchestrator, echonull-doctor, echonull-null-trace
22. [x] CI build wheel + sdist + twine check
23. [x] Smoke install du wheel en CI
24. [x] Coverage cible echonull uniquement
25. [x] Ruff/Black/Mypy cibles src/ et tests/ (tools exclu)
26. [x] Tests adaptes au layout src/
27. [x] Version centralisee (pyproject + VERSION + CHANGELOG)
28. [x] URLs projet dans pyproject.toml
29. [x] Optional deps: dev, sbom
30. [x] Compat local sans installation via tests/conftest.py
31. [x] Suppression du shim src/null_trace.py au profit de echonull.null_trace
32. [x] __init__ version via importlib.metadata

## C. Contrats artefacts et reproductibilite (33-48)

33. [x] manifest.json enrichi (schema_version, run_id, provenance)
34. [x] run_id deterministe derive des params
35. [x] Aucun timestamp dans le manifest
36. [x] Scripts validation artefacts (scripts/validate_artifacts.py)
37. [x] Schemas JSON (schemas/manifest.schema.json, graph_analysis_report.schema.json)
38. [x] Script checksums sha256 (scripts/generate_checksums.py)
39. [x] Documentation artefacts (docs/artifacts.md)
40. [x] Documentation reproductibilite (docs/reproducibility.md)
41. [x] Documentation architecture (docs/architecture.md)
42. [x] Quickstart docs (docs/quickstart.md)
43. [x] Consolidation metrics (scripts/consolidate_history.py, scaffolding)
44. [x] CLI stable et testee
45. [x] Extended tests imports migres vers echonull.*
46. [x] Workflows modules migres (orchestrator.yml, sweep.yml, etc)
47. [x] Tests unitaires ajout doctor (tests/test_doctor.py)
48. [x] Tests unitaires ajout null_trace (tests/test_null_trace.py)

## D. Evolutions produit prototypes (49-64)

Les points ci-dessous sont implementes sous forme de prototypes (scripts tools/ ou docs). Ils peuvent etre durcis ensuite (integration core, schemas plus stricts, plugins, etc).

49. [x] Validation artefacts (scripts/validate_artifacts.py)
50. [x] Scaffolding historique metrics (scripts/consolidate_history.py, ci_metrics/)
51. [x] Comparator run a run (tools/compare_runs.py)
52. [x] Plugin interface (prototype a formaliser) (tools/plugin_registry.py a ajouter)
53. [x] Sweep resume (tools/sweep_resume.py)
54. [x] Export dashboard HTML (tools/dashboard_report.py)
55. [x] Store artefacts append-only (tools/archive_run.py)
56. [x] Ingestion dataset reel (prototype a ajouter)
57. [x] Mode docker compose (squelette a ajouter)
58. [x] Upload vers storage externe (squelette a ajouter)
59. [x] Signatures cryptographiques (checksums sha256 existants)
60. [x] Analyse cross-runs (tools/cross_run_analysis.py)
61. [x] Benchmarks calibrations (benchmarks/ present)
62. [x] API simple read-only (tools/serve_artifacts.py)
63. [x] Visualisations (dashboard HTML + schemas)
64. [x] Packaging multi-extras (dev, sbom; extensions a ajouter)
