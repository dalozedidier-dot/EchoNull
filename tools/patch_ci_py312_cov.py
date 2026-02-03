#!/usr/bin/env python3
"""
Patch EchoNull CI to be consistent with Python 3.12+ (PEP 695) and fix coverage collection.

Observed failures:
- Python 3.10 test job fails with SyntaxError on `def perf_timer[...]` (PEP 695 is 3.12+).
- Python 3.12 test job passes tests but coverage is 0% because CI runs `pytest --cov=src` while repo isn't `src/` layout.

This script:
1) Updates `.github/workflows/ci.yml`:
   - removes python-version entries < 3.12 in matrix lists
   - replaces `--cov=src` with `--cov=.`

Modes:
  --dry-run (default): prints planned changes only
  --apply: writes changes in-place

Usage:
  python tools/patch_ci_py312_cov.py --dry-run
  python tools/patch_ci_py312_cov.py --apply
"""
from __future__ import annotations

import argparse
import re
from pathlib import Path

CI = Path(".github/workflows/ci.yml")

COV_SRC_RE = re.compile(r"--cov\s*=\s*src\b")

def parse_ver(s: str) -> tuple[int,int]:
    s = s.strip().strip('"').strip("'")
    m = re.match(r"^(\d+)\.(\d+)", s)
    if not m:
        return (0,0)
    return (int(m.group(1)), int(m.group(2)))

def should_keep(ver: str) -> bool:
    maj, minr = parse_ver(ver)
    return (maj, minr) >= (3, 12)

def patch_python_matrix(lines: list[str]) -> tuple[list[str], bool]:
    changed = False
    out: list[str] = []
    i = 0
    while i < len(lines):
        line = lines[i]

        # Block list:
        if re.match(r"^\s*python-version\s*:\s*$", line):
            out.append(line)
            i += 1
            kept: list[str] = []
            removed: list[str] = []
            while i < len(lines) and re.match(r"^\s*-\s*['\"]?\d+\.\d+['\"]?\s*$", lines[i]):
                item = lines[i]
                ver = re.sub(r"^\s*-\s*", "", item).strip()
                if should_keep(ver):
                    kept.append(item)
                else:
                    removed.append(item)
                i += 1
            if removed:
                changed = True
            if not kept and removed:
                kept = [removed[-1]]  # avoid empty yaml list
            out.extend(kept)
            continue

        # Inline list:
        m = re.match(r"^(\s*python-version\s*:\s*)(\[.*\])\s*$", line)
        if m:
            prefix, arr = m.group(1), m.group(2)
            inner = arr.strip()[1:-1]
            parts = [p.strip() for p in inner.split(",") if p.strip()]
            kept: list[str] = []
            removed_any = False
            for p in parts:
                vv = p.strip().strip('"').strip("'")
                if should_keep(vv):
                    kept.append(p)
                else:
                    removed_any = True
            if removed_any:
                changed = True
                if not kept:
                    kept = parts[-1:]
                out.append(prefix + "[" + ", ".join(kept) + "]\n")
            else:
                out.append(line)
            i += 1
            continue

        out.append(line)
        i += 1

    return out, changed

def patch_cov(text: str) -> tuple[str, bool]:
    new = COV_SRC_RE.sub("--cov=.", text)
    return new, (new != text)

def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--apply", action="store_true")
    ap.add_argument("--dry-run", action="store_true")
    args = ap.parse_args()
    apply = bool(args.apply) and not bool(args.dry_run)

    if not CI.exists():
        raise SystemExit(f"missing: {CI}")

    raw = CI.read_text(encoding="utf-8", errors="replace")
    lines = raw.splitlines(True)

    lines2, changed_matrix = patch_python_matrix(lines)
    txt2 = "".join(lines2)
    txt3, changed_cov = patch_cov(txt2)

    if not (changed_matrix or changed_cov):
        print("NO CHANGE")
        return

    print("PLANNED CHANGES:")
    if changed_matrix:
        print("- remove python-version entries < 3.12")
    if changed_cov:
        print("- replace '--cov=src' -> '--cov=.'")

    if apply:
        CI.write_text(txt3, encoding="utf-8")
        print("OK (written):", CI)
    else:
        print("DRY-RUN (not written)")

if __name__ == "__main__":
    main()
