#!/usr/bin/env python3
"""
EchoNull workflow cleanup (structural hygiene):
- Delete any workflow whose file/name/content matches "bareflux" (case-insensitive)
- Fix the "common.yml" mislabel by renaming .github/workflows/common.yml to match its `name:` (e.g. orchestrator.yml)
  and rewriting internal references `uses: ./.github/workflows/common.yml`.

Modes:
  --dry-run (default): prints planned actions, writes report JSON
  --apply: performs changes (delete/rename/rewrites)

Usage:
  python tools/cleanup_workflows_echonull.py --dry-run
  python tools/cleanup_workflows_echonull.py --apply

Output report:
  _workflow_cleanup_report.json
"""
from __future__ import annotations

import argparse
import os
import re
import json
from pathlib import Path


WORKFLOWS_DIR = Path(".github/workflows")
REPORT_PATH = Path("_workflow_cleanup_report.json")

NAME_RE = re.compile(r"^\s*name\s*:\s*(.+?)\s*$", re.M)
BAREFLUX_RE = re.compile(r"bare\s*flux|bareflux", re.I)


def read_text(p: Path) -> str:
    return p.read_text(encoding="utf-8", errors="replace")


def slugify(name: str) -> str:
    # simple, stable file slug
    s = name.strip().lower()
    s = re.sub(r"[^a-z0-9]+", "-", s)
    s = re.sub(r"-{2,}", "-", s).strip("-")
    if not s:
        s = "workflow"
    return s


def get_workflow_name(yaml_text: str) -> str | None:
    m = NAME_RE.search(yaml_text)
    if not m:
        return None
    v = m.group(1).strip()
    # strip quotes if any
    if (v.startswith('"') and v.endswith('"')) or (v.startswith("'") and v.endswith("'")):
        v = v[1:-1].strip()
    return v or None


def find_workflow_files() -> list[Path]:
    if not WORKFLOWS_DIR.exists():
        return []
    return sorted([p for p in WORKFLOWS_DIR.iterdir() if p.is_file() and p.suffix in (".yml", ".yaml")])


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--apply", action="store_true", help="Apply changes (delete/rename/rewrites). Default is dry-run.")
    ap.add_argument("--report", default=str(REPORT_PATH))
    args = ap.parse_args()

    files = find_workflow_files()
    actions: list[dict] = []

    # 1) delete bareflux workflows (by content or name)
    for p in files:
        txt = read_text(p)
        wf_name = get_workflow_name(txt) or ""
        if BAREFLUX_RE.search(p.name) or BAREFLUX_RE.search(wf_name) or BAREFLUX_RE.search(txt):
            actions.append({"action": "delete", "path": str(p), "reason": "matches_bareflux"})
            if args.apply:
                p.unlink()

    # Refresh list after deletions
    files = find_workflow_files()

    # 2) Fix common.yml mislabel: rename common.yml to <name>.yml if name exists and is different.
    common = WORKFLOWS_DIR / "common.yml"
    if common.exists():
        txt = read_text(common)
        wf_name = get_workflow_name(txt)
        if wf_name:
            desired = WORKFLOWS_DIR / (slugify(wf_name) + ".yml")
            if desired.name != common.name:
                if desired.exists():
                    actions.append({
                        "action": "rename_skip",
                        "from": str(common),
                        "to": str(desired),
                        "reason": "target_exists"
                    })
                else:
                    actions.append({
                        "action": "rename",
                        "from": str(common),
                        "to": str(desired),
                        "reason": f"common_file_name_mismatch(name={wf_name})"
                    })
                    if args.apply:
                        common.rename(desired)

                        # update references in other workflow files
                        for other in find_workflow_files():
                            otxt = read_text(other)
                            newtxt = otxt.replace("./.github/workflows/common.yml", f"./.github/workflows/{desired.name}")
                            newtxt = newtxt.replace(".github/workflows/common.yml", f".github/workflows/{desired.name}")
                            if newtxt != otxt:
                                other.write_text(newtxt, encoding="utf-8")
                                actions.append({
                                    "action": "rewrite_ref",
                                    "path": str(other),
                                    "from_ref": "common.yml",
                                    "to_ref": desired.name
                                })
        else:
            actions.append({"action": "rename_skip", "from": str(common), "reason": "no_name_field"})

    # 3) Write report
    report = {
        "apply": bool(args.apply),
        "workflows_dir": str(WORKFLOWS_DIR),
        "actions": actions,
        "remaining": [str(p) for p in find_workflow_files()],
    }
    Path(args.report).write_text(json.dumps(report, indent=2), encoding="utf-8")

    # 4) Print summary
    print("OK")
    print("apply:", bool(args.apply))
    print("actions:", len(actions))
    print("report:", args.report)


if __name__ == "__main__":
    main()
