EchoNull — CI fix bundle (py3.12-only + coverage target) — 2026-02-03

Observed in logs_56249577047.zip:
- Jobs still run on py3.11 -> SyntaxError at `def perf_timer[...]` (PEP 695).
- py3.12 tests pass but coverage is 0% due to `--cov=src` + `PYTHONPATH=src`.

This bundle patches `.github/workflows/ci.yml` IN PLACE:
1) Removes python 3.10 and 3.11 entries from python-version matrices.
2) Replaces `--cov=src` / `--cov src` with `--cov=.` / `--cov .`
3) Rewrites `PYTHONPATH: src` -> `PYTHONPATH: .` (if present)

How to apply:
1) Unzip at repo root (EchoNull)
2) Run:
     bash scripts/fix_ci_py312_cov.sh
3) Verify:
     git diff
4) Commit + push:
     git commit -am "ci: py312-only + fix coverage target"
     git push

Notes:
- Script creates a backup: `.github/workflows/ci.yml.bak` (do not commit it).
- This bundle does not change `fail-under=100`. If coverage after fix is <100,
  CI will still fail but with a real (non-zero) coverage number.
