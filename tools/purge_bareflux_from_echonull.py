#!/usr/bin/env python3
"""
Purge files that are not supposed to be in EchoNull: BareFlux workflow & related artifacts.

What it does:
- Remove any workflow file in `.github/workflows/` that:
    - has 'bareflux' in its filename OR
    - contains the token 'bareflux' (case-insensitive) in its content.
- Optionally remove standalone files that look like accidental BareFlux drops:
    - `ci_snippets/github_actions_steps.yml`
    - `README.txt` / `PATCH_README.txt` that mention bareflux (only if explicitly requested)

Default is SAFE:
- Only touches `.github/workflows/*` based on filename/content.
- Does not touch EchoNull main lint workflow (unless it contains 'bareflux', which it shouldn't).

Usage:
  python tools/purge_bareflux_from_echonull.py
  python tools/purge_bareflux_from_echonull.py --dry-run
  python tools/purge_bareflux_from_echonull.py --also-snippets

Exit codes:
  0 = success (even if nothing removed)
  2 = removed files (signals change to CI if you want)
"""
from __future__ import annotations

import argparse
import os
from pathlib import Path

BAREFLUX_TOKEN = "bareflux"

def file_contains_token(path: Path, token: str) -> bool:
    try:
        txt = path.read_text(encoding="utf-8", errors="ignore")
    except Exception:
        return False
    return token.lower() in txt.lower()

def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--dry-run", action="store_true")
    ap.add_argument("--also-snippets", action="store_true", help="Also remove known snippet files if present")
    args = ap.parse_args()

    removed = []

    wf_dir = Path(".github/workflows")
    if wf_dir.exists():
        for p in sorted(wf_dir.glob("*.yml")) + sorted(wf_dir.glob("*.yaml")):
            name_hit = BAREFLUX_TOKEN in p.name.lower()
            content_hit = file_contains_token(p, BAREFLUX_TOKEN)
            if name_hit or content_hit:
                removed.append(str(p))
                if not args.dry_run:
                    p.unlink(missing_ok=True)

    if args.also_snippets:
        extra = [
            Path("ci_snippets/github_actions_steps.yml"),
        ]
        for p in extra:
            if p.exists():
                removed.append(str(p))
                if not args.dry_run:
                    p.unlink(missing_ok=True)

    if removed:
        print("REMOVED:" if not args.dry_run else "WOULD REMOVE:")
        for r in removed:
            print(" -", r)
        raise SystemExit(2)  # signal that changes occurred

    print("OK (nothing to remove)")

if __name__ == "__main__":
    main()
