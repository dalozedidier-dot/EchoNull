# ruff: noqa
#!/usr/bin/env python3
"""
Sanitize EchoNull repo state (structural hygiene + unblock CI).

What it does (apply mode):
  1) Removes any GitHub Actions workflow in .github/workflows/ whose filename OR `name:` OR content matches "bareflux" (case-insensitive).
  2) Removes accidental tool scripts that were only meant as one-shot helpers:
       - tools/cleanup_workflows_echonull.py
       - tools/purge_bareflux_from_echonull.py
  3) Applies Ruff UP047 fix on common/utils.py (perf_timer -> PEP 695) if present.
  4) Optional: renames .github/workflows/common.yml to match its `name:` field (if safe) to reduce UI confusion.

Modes:
  --dry-run  : print planned actions + write report JSON (default)
  --apply    : perform changes

Usage:
  python tools/sanitize_echonull.py --dry-run
  python tools/sanitize_echonull.py --apply

Outputs:
  _echonull_sanitize_report.json
"""
from __future__ import annotations

import argparse
import json
import os
import re
from pathlib import Path

WORKFLOWS_DIR = Path(".github/workflows")
REPORT = Path("_echonull_sanitize_report.json")

BAREFLUX_RE = re.compile(r"bare\s*flux|bareflux", re.I)
NAME_RE = re.compile(r"^\s*name\s*:\s*(.+?)\s*$", re.M)

# UP047 fixer (embedded, minimal)
DEF_RE = re.compile(r"^(?P<indent>\s*)def\s+perf_timer\s*\(", re.M)
ALREADY_PEP695_RE = re.compile(r"def\s+perf_timer\s*\[", re.M)
PARAMSPEC_LINE_RE = re.compile(r"^\s*(?P<name>[A-Za-z_][A-Za-z0-9_]*)\s*=\s*ParamSpec\(", re.M)
TYPEVAR_LINE_RE = re.compile(r"^\s*(?P<name>[A-Za-z_][A-Za-z0-9_]*)\s*=\s*TypeVar\(", re.M)
TYPING_IMPORT_RE = re.compile(r"^(?P<indent>\s*)from\s+typing\s+import\s+(?P<rest>.*)$", re.M)


def read_text(p: Path) -> str:
    return p.read_text(encoding="utf-8", errors="replace")


def write_text(p: Path, txt: str) -> None:
    p.parent.mkdir(parents=True, exist_ok=True)
    p.write_text(txt, encoding="utf-8")


def get_workflow_name(txt: str) -> str | None:
    m = NAME_RE.search(txt)
    if not m:
        return None
    v = m.group(1).strip()
    if (v.startswith('"') and v.endswith('"')) or (v.startswith("'") and v.endswith("'")):
        v = v[1:-1].strip()
    return v or None


def slugify(name: str) -> str:
    s = name.strip().lower()
    s = re.sub(r"[^a-z0-9]+", "-", s)
    s = re.sub(r"-{2,}", "-", s).strip("-")
    return s or "workflow"


def remove_bareflux_workflows(apply: bool, actions: list[dict]) -> None:
    if not WORKFLOWS_DIR.exists():
        return
    for p in sorted(WORKFLOWS_DIR.iterdir()):
        if not p.is_file() or p.suffix not in (".yml", ".yaml"):
            continue
        txt = read_text(p)
        wf_name = get_workflow_name(txt) or ""
        if BAREFLUX_RE.search(p.name) or BAREFLUX_RE.search(wf_name) or BAREFLUX_RE.search(txt):
            actions.append({"action": "delete_workflow", "path": str(p)})
            if apply:
                p.unlink()


def remove_unwanted_tools(apply: bool, actions: list[dict]) -> None:
    targets = [
        Path("tools/cleanup_workflows_echonull.py"),
        Path("tools/purge_bareflux_from_echonull.py"),
    ]
    for t in targets:
        if t.exists():
            actions.append({"action": "delete_tool", "path": str(t)})
            if apply:
                t.unlink()


def _cleanup_typing_imports(text: str) -> str:
    uses_paramspec = "ParamSpec" in text
    uses_typevar = "TypeVar" in text
    if uses_paramspec or uses_typevar:
        return text

    def fix_line(line: str) -> str:
        m = TYPING_IMPORT_RE.match(line)
        if not m:
            return line
        indent = m.group("indent")
        rest = m.group("rest").strip()

        if rest.startswith("(") and rest.endswith(")"):
            inner = rest[1:-1]
            parts = [p.strip() for p in inner.split(",") if p.strip()]
            parts = [p for p in parts if p not in ("ParamSpec", "TypeVar")]
            if not parts:
                return ""
            return indent + "from typing import (" + ", ".join(parts) + ")\n"

        parts = [p.strip() for p in rest.split(",") if p.strip()]
        parts = [p for p in parts if p not in ("ParamSpec", "TypeVar")]
        if not parts:
            return ""
        return indent + "from typing import " + ", ".join(parts) + "\n"

    out = []
    for ln in text.splitlines(True):
        if "from typing import" in ln:
            ln2 = fix_line(ln)
            if ln2:
                out.append(ln2)
        else:
            out.append(ln)
    return "".join(out)


def fix_up047_perf_timer(apply: bool, actions: list[dict]) -> None:
    path = Path("common/utils.py")
    if not path.exists():
        return
    txt = read_text(path)
    if "perf_timer" not in txt:
        return
    if ALREADY_PEP695_RE.search(txt):
        actions.append({"action": "up047_already_fixed", "path": str(path)})
        return

    m = DEF_RE.search(txt)
    if not m:
        return

    # remove nearby ParamSpec/TypeVar assignment lines above perf_timer (first occurrences)
    lines = txt.splitlines(True)
    def_line = txt[:m.start()].count("\n")
    start = max(0, def_line - 30)
    block = "".join(lines[start:def_line])

    p_name = None
    r_name = None
    for mm in PARAMSPEC_LINE_RE.finditer(block):
        # try to capture name via "P = ParamSpec("
        p_name = mm.group("name")
    for mm in TYPEVAR_LINE_RE.finditer(block):
        r_name = mm.group("name")

    p_name = p_name or "P"
    r_name = r_name or "R"

    removed_p = removed_r = False
    out_lines = []
    for i, ln in enumerate(lines):
        if i < def_line and (not removed_p) and re.match(rf"^\s*{re.escape(p_name)}\s*=\s*ParamSpec\(", ln):
            removed_p = True
            continue
        if i < def_line and (not removed_r) and re.match(rf"^\s*{re.escape(r_name)}\s*=\s*TypeVar\(", ln):
            removed_r = True
            continue
        out_lines.append(ln)

    txt2 = "".join(out_lines)

    # pep695ize def
    def repl(mm: re.Match) -> str:
        indent = mm.group("indent")
        return f"{indent}def perf_timer[**{p_name}, {r_name}]("
    txt3 = DEF_RE.sub(repl, txt2, count=1)

    txt4 = _cleanup_typing_imports(txt3)

    if txt4 != txt:
        actions.append({"action": "fix_up047", "path": str(path), "p": p_name, "r": r_name})
        if apply:
            write_text(path, txt4)


def rename_common_workflow(apply: bool, actions: list[dict]) -> None:
    common = WORKFLOWS_DIR / "common.yml"
    if not common.exists():
        return
    txt = read_text(common)
    wf_name = get_workflow_name(txt)
    if not wf_name:
        return
    desired = WORKFLOWS_DIR / (slugify(wf_name) + ".yml")
    if desired.name == common.name:
        return
    if desired.exists():
        actions.append({"action": "rename_common_skip", "from": str(common), "to": str(desired), "reason": "target_exists"})
        return

    actions.append({"action": "rename_common", "from": str(common), "to": str(desired)})
    if apply:
        common.rename(desired)
        # rewrite internal references in other workflows
        if WORKFLOWS_DIR.exists():
            for p in sorted(WORKFLOWS_DIR.iterdir()):
                if not p.is_file() or p.suffix not in (".yml", ".yaml"):
                    continue
                otxt = read_text(p)
                newtxt = otxt.replace("./.github/workflows/common.yml", f"./.github/workflows/{desired.name}")
                newtxt = newtxt.replace(".github/workflows/common.yml", f".github/workflows/{desired.name}")
                if newtxt != otxt:
                    write_text(p, newtxt)
                    actions.append({"action": "rewrite_ref", "path": str(p), "to": desired.name})


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--apply", action="store_true")
    ap.add_argument("--dry-run", action="store_true")
    args = ap.parse_args()
    apply = bool(args.apply) and not bool(args.dry_run)

    actions: list[dict] = []
    remove_bareflux_workflows(apply, actions)
    remove_unwanted_tools(apply, actions)
    fix_up047_perf_timer(apply, actions)
    rename_common_workflow(apply, actions)

    report = {
        "apply": apply,
        "actions": actions,
        "note": "Commit+push required to affect CI; dry-run reports planned actions only.",
    }
    write_text(REPORT, json.dumps(report, indent=2))

    print("OK")
    print("apply:", apply)
    print("actions:", len(actions))
    print("report:", str(REPORT))


if __name__ == "__main__":
    main()
