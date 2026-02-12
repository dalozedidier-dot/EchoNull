# Reproductibilite

Principes :

- seeds deterministes
- pas de timestamps dans les manifests
- formats JSON stables (separators compacts, ordre stable quand applicable)

Conseils :

- figer les dependances si tu veux une reproductibilite cross-machine
- capturer un manifeste de provenance par run (git_sha, python)
