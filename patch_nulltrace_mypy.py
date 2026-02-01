from __future__ import annotations

import re
from pathlib import Path


def _update_typing_imports(text: str) -> str:
    # Ensure `cast` is available if we end up using it.
    if "cast(" in text:
        return text

    # If we replaced annotations, we might not need cast.
    return text


def patch_nulltrace_file(path: Path) -> None:
    original = path.read_text(encoding="utf-8", errors="strict")
    text = original

    # 1) Prefer the clean fix: replace `Collection[Collection[str]]` with `list[list[str]]`
    # This makes `.append(...)` valid on the declared type.
    text = text.replace("Collection[Collection[str]]", "list[list[str]]")

    # 2) If we removed all uses of `Collection[` from the file, try to remove Collection from typing imports
    if "Collection[" not in text:
        # from typing import A, B, Collection, C
        text = re.sub(
            r"(from\s+typing\s+import\s+[^\n]*?)\bCollection\b\s*,\s*",
            r"\1",
            text,
        )
        text = re.sub(
            r"(from\s+typing\s+import\s+[^\n]*?),\s*\bCollection\b",
            r"\1",
            text,
        )
        text = re.sub(
            r"(from\s+typing\s+import\s+)\bCollection\b(\s*\n)",
            r"\1\2",
            text,
        )

    # 3) Normalize line endings to LF (can avoid formatter churn)
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
