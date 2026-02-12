from __future__ import annotations

import sys
from pathlib import Path


def _ensure_src_on_syspath() -> None:
    # Keep tests runnable without installing the package.
    repo_root = Path(__file__).resolve().parents[1]
    src_root = repo_root / "src"
    src_root_str = str(src_root)
    if src_root_str not in sys.path:
        sys.path.insert(0, src_root_str)


_ensure_src_on_syspath()
