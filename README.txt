EchoNull CI fix (v2)

Problem
- Code uses PEP 695 (Python 3.12+ required), but CI still runs 3.10/3.11 => SyntaxError.
- CI uses --cov=src and PYTHONPATH=src, but repo is not in a src/ layout => Coverage 0%.

What this bundle does
- Patches all workflows under .github/workflows/*.yml|*.yaml
  * removes 3.10/3.11 from python version lists
  * replaces --cov=src / --cov src -> --cov=. / --cov .
  * replaces PYTHONPATH: src -> PYTHONPATH: .
- Creates per-file backups: <workflow>.bak

How to apply
1) Copy scripts/fix_ci_py312_cov.sh into your repo at scripts/fix_ci_py312_cov.sh
2) Run:
   bash scripts/fix_ci_py312_cov.sh
3) Check:
   git diff
4) Commit & push:
   git commit -am "ci: py312-only + fix coverage target"
   git push

If CI still fails after that
- It will be a *real* coverage failure if fail-under=100 is set and actual coverage < 100.
- Or it can be ruff linting files outside the intended scope.
