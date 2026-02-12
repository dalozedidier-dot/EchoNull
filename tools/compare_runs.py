from __future__ import annotations

import argparse
import json
from pathlib import Path
from typing import Any


def _load_json(path: Path) -> Any:
    return json.loads(path.read_text(encoding="utf-8"))


def _diff(a: Any, b: Any, prefix: str = "") -> list[str]:
    diffs: list[str] = []
    if type(a) is not type(b):
        return [f"{prefix}: type {type(a).__name__} != {type(b).__name__}"]
    if isinstance(a, dict):
        ak = set(a.keys())
        bk = set(b.keys())
        for k in sorted(ak - bk):
            diffs.append(f"{prefix}/{k}: only in A")
        for k in sorted(bk - ak):
            diffs.append(f"{prefix}/{k}: only in B")
        for k in sorted(ak & bk):
            diffs.extend(_diff(a[k], b[k], prefix=f"{prefix}/{k}"))
        return diffs
    if isinstance(a, list):
        if len(a) != len(b):
            diffs.append(f"{prefix}: len {len(a)} != {len(b)}")
        for i, (x, y) in enumerate(zip(a, b)):
            diffs.extend(_diff(x, y, prefix=f"{prefix}[{i}]"))
        return diffs
    if a != b:
        diffs.append(f"{prefix}: {a!r} != {b!r}")
    return diffs


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("a", help="First run directory (ex: _ci_out)")
    ap.add_argument("b", help="Second run directory (ex: _ci_out_2)")
    ap.add_argument("--what", choices=["manifest", "overview", "all"], default="all")
    args = ap.parse_args()

    a = Path(args.a)
    b = Path(args.b)

    files = []
    if args.what in ("manifest", "all"):
        files.append("manifest.json")
    if args.what in ("overview", "all"):
        files.append("overview.json")

    diffs: list[str] = []
    for f in files:
        pa = a / f
        pb = b / f
        if not pa.exists() or not pb.exists():
            diffs.append(f"{f}: missing in one of the dirs")
            continue
        da = _load_json(pa)
        db = _load_json(pb)
        diffs.extend(_diff(da, db, prefix=f))

    if diffs:
        print("\n".join(diffs))
        return 2

    print("OK")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
