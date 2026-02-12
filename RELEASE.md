# Release procedure

This repository supports two release modes:

1) GitHub Release only (tag + release notes)
2) GitHub Release + PyPI publish (Trusted Publisher recommended)

## Preconditions

- Working tree clean
- CI green on main
- Version aligned:
  - pyproject.toml version
  - VERSION file
  - CHANGELOG.md section

## Tag

Example:

- git tag -a v0.1.2 -m "EchoNull v0.1.2"
- git push origin v0.1.2

## GitHub Release

The workflow .github/workflows/release.yml will:

- build wheel + sdist
- extract notes from CHANGELOG.md
- create GitHub Release with attached dist artifacts

## PyPI

If PyPI Trusted Publisher is configured, the same workflow can publish.

Notes:

- Use environment "pypi" in GitHub Actions
- Prefer OIDC (id-token: write)
