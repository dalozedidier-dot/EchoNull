Mypy hotfix (CI)

This patch addresses the two mypy errors reported in CI:

1) src/null_trace.py: "main" does not return a value
   Fix: ensure main() returns int and SystemExit receives an int.

2) src/nulltrace/null_trace.py: Collection[Collection[str]] has no attribute append
   Fix: replace the annotation with list[list[str]] (append is valid).

Apply:
- Extract this zip at repo root.
- Commit src/null_trace.py.
- Run once (then commit the result):
    python scripts/patch_nulltrace_mypy.py
