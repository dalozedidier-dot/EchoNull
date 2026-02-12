from __future__ import annotations

import argparse
import csv
from pathlib import Path


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--in-dir", default="ci_metrics/raw", help="Folder containing per-run CSV summaries.")
    ap.add_argument("--out", default="ci_metrics/history.csv", help="Append-only consolidated file.")
    args = ap.parse_args()

    in_dir = Path(args.in_dir)
    out = Path(args.out)
    out.parent.mkdir(parents=True, exist_ok=True)

    rows: list[dict[str, str]] = []
    for p in sorted(in_dir.glob("*.csv")):
        with p.open("r", encoding="utf-8", newline="") as f:
            r = csv.DictReader(f)
            rows.extend(list(r))

    if not rows:
        print("No input rows.")
        return 0

    fieldnames = sorted({k for row in rows for k in row.keys()})
    with out.open("w", encoding="utf-8", newline="") as f:
        w = csv.DictWriter(f, fieldnames=fieldnames)
        w.writeheader()
        for row in rows:
            w.writerow({k: row.get(k, "") for k in fieldnames})

    print(f"Wrote {out} with {len(rows)} rows.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
