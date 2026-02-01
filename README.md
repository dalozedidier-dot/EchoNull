EchoNull — Correctif structurel (duplication de module) — v0.1.2

Objet
-----
Corriger l'échec mypy "Duplicate module named 'patch_nulltrace_mypy'" en supprimant
le doublon en racine, en conservant scripts/patch_nulltrace_mypy.py.

Invariants
----------
- Aucun renommage des 4 blocs (BareFlux / RiftLens / NullTrace / VoidMark).
- Pas d'exclusion de fichiers pour contourner.
- Correction unique, propre, reproductible.

Contenu du zip
--------------
- fix_duplicate_module.sh : applique le correctif minimal (git rm du doublon racine) + vérifs.
- verify_ci_gates.sh      : exécute la séquence de diagnostics (ruff/black/mypy/pytest).

Mode d'emploi
-------------
1) Dézipper à la racine du repo EchoNull (même niveau que pyproject.toml).
2) Exécuter:
     bash fix_duplicate_module.sh
3) Optionnel (si tu veux revalider sans modifier):
     bash verify_ci_gates.sh

Notes
-----
- Le script échoue explicitement si le repo n'est pas un dépôt git, ou si les fichiers attendus
  ne sont pas présents.
- Le script ne commit pas automatiquement (pour laisser la gouvernance au repo).
