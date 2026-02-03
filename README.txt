EchoNull CI patch bundle: py3.12-only + real coverage target

Why:
- common/utils.py uses PEP 695 type parameter syntax, which requires Python 3.12+.
- CI was still running 3.10/3.11 (SyntaxError during collection).
- Under 3.12, tests passed but coverage was 0% because CI used --cov=src and PYTHONPATH=src while the repo is not in a src/ layout.

What this patch does (scripts/fix_ci_py312_cov.sh):
- Targets .github/workflows/ci.yml (fallback: ci.yaml)
- Creates a backup next to it: ci.yml.bak (only once)
- Removes Python 3.10 and 3.11 from workflow matrices (inline list and block list)
- Replaces:
    --cov=src  -> --cov=.
    --cov src  -> --cov .
    PYTHONPATH: src -> PYTHONPATH: .

How to apply:
  bash scripts/fix_ci_py312_cov.sh
  git diff
  git commit -am "ci: py312-only + fix coverage target"
  git push

Notes:
- If your workflow file isn't named ci.yml/ci.yaml, edit the script and set WF to the correct file.
- If fail-under=100 is enabled, CI may still fail after this patch with a REAL coverage value below the threshold.
