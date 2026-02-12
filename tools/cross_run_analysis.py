from __future__ import annotations

import argparse
import csv
from pathlib import Path
from statistics import mean


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--history", default="ci_metrics/history.csv")
    args = ap.parse_args()

    path = Path(args.history)
    if not path.exists():
        print("No history file.")
        return 0

    with path.open("r", encoding="utf-8", newline="") as f:
        rows = list(csv.DictReader(f))

    if not rows:
        print("Empty history.")
        return 0

    def fnum(x: str) -> float | None:
        try:
            return float(x)
        except Exception:
            return None

    runtimes = [fnum(r.get("runtime_seconds", "")) for r in rows]
    runtimes = [x for x in runtimes if x is not None]
    if runtimes:
        print(f"runs={len(rows)} runtime_mean={mean(runtimes):.3f}s runtime_min={min(runtimes):.3f}s runtime_max={max(runtimes):.3f}s")
    else:
        print(f"runs={len(rows)}")

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
