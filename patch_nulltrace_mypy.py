from __future__ import annotations

import re
from pathlib import Path


def _remove_collection_from_typing_imports(text: str) -> str:
    # from typing import A, B, Collection, C  -> remove Collection
    pat1 = r"(from\s+typing\s+import\s+[^\n]*?)" r"\bCollection\b\s*,\s*"
    text = re.sub(pat1, r"\1", text)

    pat2 = r"(from\s+typing\s+import\s+[^\n]*?)" r",\s*\bCollection\b"
    text = re.sub(pat2, r"\1", text)

    pat3 = r"(from\s+typing\s+import\s+)\bCollection\b(\s*\n)"
    return re.sub(pat3, r"\1\2", text)


def patch_nulltrace_file(path: Path) -> None:
    original = path.read_text(encoding="utf-8", errors="strict")
    text = original

    # Replace a read-only Collection annotation with a mutable list for `.append(...)`.
    text = text.replace("Collection[Collection[str]]", "list[list[str]]")

    # If no `Collection[` remains, remove Collection from typing imports.
    if "Collection[" not in text:
        text = _remove_collection_from_typing_imports(text)

    # Normalize line endings to LF
    text = text.replace("\r\n", "\n").replace("\r", "\n")

    if text != original:
        path.write_text(text, encoding="utf-8", newline="\n")


def main() -> int:
    target = Path("src/nulltrace/null_trace.py")
    if not target.exists():
        raise SystemExit("Missing src/nulltrace/null_trace.py (path not found).")

    patch_nulltrace_file(target)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
