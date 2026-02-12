from __future__ import annotations

import argparse
import hashlib
from pathlib import Path


def sha256_file(path: Path) -> str:
    h = hashlib.sha256()
    with path.open("rb") as f:
        for chunk in iter(lambda: f.read(65536), b""):
            h.update(chunk)
    return h.hexdigest()


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("root", nargs="?", default=".", help="Root directory to hash.")
    ap.add_argument("--out", default="checksums.sha256", help="Output file.")
    args = ap.parse_args()

    root = Path(args.root).resolve()
    skip_prefixes = (".git/", ".venv", "_ci_out", "dist/")

    lines: list[str] = []
    for p in sorted(root.rglob("*")):
        if not p.is_file():
            continue
        rel = p.relative_to(root).as_posix()
        if any(rel.startswith(pfx) for pfx in skip_prefixes):
            continue
        lines.append(f"{sha256_file(p)}  {rel}")

    Path(args.out).write_text("\n".join(lines) + "\n", encoding="utf-8")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
