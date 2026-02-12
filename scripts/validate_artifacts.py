from __future__ import annotations

import argparse
import json
from pathlib import Path
from typing import Any, cast


REQUIRED_ROOT = ["overview.json", "manifest.json"]
REQUIRED_RUN_FILES = [
    "multi.csv",
    "delta_stats/stats.json",
    "mark_counts/count.txt",
]


def _load_json(path: Path) -> dict[str, Any]:
    data = json.loads(path.read_text(encoding="utf-8"))
    return cast(dict[str, Any], data)


def validate_run_dir(run_dir: Path, thresholds: list[float]) -> list[str]:
    errors: list[str] = []
    for rel in REQUIRED_RUN_FILES:
        if not (run_dir / rel).exists():
            errors.append(f"missing: {run_dir.name}/{rel}")
    for thr in thresholds:
        rel = f"graph_analysis/thr_{thr:.2f}_report.json"
        if not (run_dir / rel).exists():
            errors.append(f"missing: {run_dir.name}/{rel}")
    return errors


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--out", default="_ci_out", help="Output directory produced by orchestrator.")
    args = ap.parse_args()

    out = Path(args.out)
    errors: list[str] = []
    for rel in REQUIRED_ROOT:
        if not (out / rel).exists():
            errors.append(f"missing: {rel}")

    if errors:
        for e in errors:
            print(e)
        return 2

    manifest = _load_json(out / "manifest.json")
    thresholds = [float(x) for x in manifest.get("thresholds", [])]
    runs = int(manifest.get("runs", 0))

    for run_id in range(1, runs + 1):
        run_dir = out / f"run_{run_id:04d}"
        if not run_dir.exists():
            errors.append(f"missing: {run_dir.name}/")
            continue
        errors.extend(validate_run_dir(run_dir, thresholds))

    if errors:
        for e in errors:
            print(e)
        return 2

    print("OK")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
