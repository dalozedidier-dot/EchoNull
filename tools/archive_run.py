from __future__ import annotations

import argparse
import shutil
from pathlib import Path


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--src", default="_ci_out", help="Run output directory.")
    ap.add_argument("--runs-dir", default="runs", help="Archive root directory.")
    ap.add_argument("--name", default=None, help="Optional archive name (defaults to manifest run_id).")
    args = ap.parse_args()

    src = Path(args.src)
    if not src.exists():
        raise SystemExit(f"Missing {src}")

    manifest_path = src / "manifest.json"
    if not manifest_path.exists():
        raise SystemExit("manifest.json not found in src")

    import json

    manifest = json.loads(manifest_path.read_text(encoding="utf-8"))
    run_id = args.name or str(manifest.get("run_id", "run"))
    dst = Path(args.runs_dir) / run_id

    if dst.exists():
        raise SystemExit(f"Destination already exists: {dst}")

    dst.parent.mkdir(parents=True, exist_ok=True)
    shutil.copytree(src, dst)
    print(dst)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
