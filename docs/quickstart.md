# Quickstart

## Installation

    python -m pip install -U pip
    pip install -e ".[dev]"

## Run minimal

    echonull-orchestrator --runs 2 --thresholds 0.25 --out _ci_out --workers 1

## Verifier les artefacts

    python scripts/validate_artifacts.py --out _ci_out

## Determinisme

Deux runs avec les memes parametres doivent produire les memes fichiers (hash identiques).
