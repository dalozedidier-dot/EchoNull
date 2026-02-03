# ruff: noqa
#!/usr/bin/env python3
"""
Autofix Ruff UP047 for generic function `perf_timer` using PEP 695 (Python 3.12+).

Transforms:
  P = ParamSpec("P")
  R = TypeVar("R")
  def perf_timer(func: Callable[P, R]) -> Callable[P, R]:

Into:
  def perf_timer[**P, R](func: Callable[P, R]) -> Callable[P, R]:

Also:
- removes the standalone ParamSpec/TypeVar assignment lines if found near perf_timer.
- removes ParamSpec/TypeVar from `from typing import ...` if unused after the change.

Usage:
  python tools/fix_up047_perf_timer.py --file common/utils.py
"""
from __future__ import annotations

import argparse
import re
from pathlib import Path

DEF_RE = re.compile(r"^(?P<indent>\s*)def\s+perf_timer\s*\(", re.M)
ALREADY_PEP695_RE = re.compile(r"def\s+perf_timer\s*\[", re.M)

PARAMSPEC_LINE_RE = re.compile(
    r"^\s*(?P<name>[A-Za-z_][A-Za-z0-9_]*)\s*=\s*ParamSpec\(\s*['\"](?P=name)['\"]\s*\)\s*$",
    re.M,
)
TYPEVAR_LINE_RE = re.compile(
    r"^\s*(?P<name>[A-Za-z_][A-Za-z0-9_]*)\s*=\s*TypeVar\(\s*['\"](?P=name)['\"]",
    re.M,
)

TYPING_IMPORT_RE = re.compile(r"^(?P<indent>\s*)from\s+typing\s+import\s+(?P<rest>.*)$", re.M)


def _find_def_pos(text: str) -> int:
    m = DEF_RE.search(text)
    if not m:
        raise SystemExit("perf_timer definition not found")
    return m.start()


def _line_index_at_pos(text: str, pos: int) -> int:
    return text[:pos].count("\n")


def _remove_nearby_defs(text: str, def_pos: int, window_lines: int = 30) -> tuple[str, str, str]:
    lines = text.splitlines(True)
    def_line = _line_index_at_pos(text, def_pos)
    start = max(0, def_line - window_lines)

    block = "".join(lines[start:def_line])
    p_name = None
    r_name = None

    for m in PARAMSPEC_LINE_RE.finditer(block):
        p_name = m.group("name")
    for m in TYPEVAR_LINE_RE.finditer(block):
        r_name = m.group("name")

    p_name = p_name or "P"
    r_name = r_name or "R"

    removed_p = False
    removed_r = False
    out = []
    for i, ln in enumerate(lines):
        if i < def_line and (not removed_p) and re.match(rf"^\s*{re.escape(p_name)}\s*=\s*ParamSpec\(", ln):
            removed_p = True
            continue
        if i < def_line and (not removed_r) and re.match(rf"^\s*{re.escape(r_name)}\s*=\s*TypeVar\(", ln):
            removed_r = True
            continue
        out.append(ln)

    return ("".join(out), p_name, r_name)


def _pep695ize_def(text: str, p_name: str, r_name: str) -> str:
    def repl(m: re.Match) -> str:
        indent = m.group("indent")
        return f"{indent}def perf_timer[**{p_name}, {r_name}]("
    return DEF_RE.sub(repl, text, count=1)


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

    out_lines = []
    for ln in text.splitlines(True):
        if "from typing import" in ln:
            ln2 = fix_line(ln)
            if ln2:
                out_lines.append(ln2)
        else:
            out_lines.append(ln)
    return "".join(out_lines)


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--file", default="common/utils.py")
    args = ap.parse_args()

    path = Path(args.file)
    if not path.exists():
        raise SystemExit(f"file not found: {path}")

    text = path.read_text(encoding="utf-8")

    if ALREADY_PEP695_RE.search(text):
        print("OK (already PEP 695)")
        return

    def_pos = _find_def_pos(text)
    text2, p_name, r_name = _remove_nearby_defs(text, def_pos)
    text3 = _pep695ize_def(text2, p_name, r_name)
    text4 = _cleanup_typing_imports(text3)

    if text4 == text:
        print("NO CHANGE")
        return

    path.write_text(text4, encoding="utf-8")
    print("OK (patched)", str(path))


if __name__ == "__main__":
    main()
