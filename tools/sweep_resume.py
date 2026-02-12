from __future__ import annotations

import argparse
from pathlib import Path

from echonull.orchestrator.run import Params, run


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--out", default="_ci_out", help="Output directory.")
    ap.add_argument("--runs", type=int, default=10)
    ap.add_argument("--thresholds", default="0.25,0.5,0.7,0.8")
    ap.add_argument("--seed-base", type=int, default=1000)
    ap.add_argument("--workers", type=int, default=1)
    ap.add_argument("--zip", action="store_true")
    args = ap.parse_args()

    out = Path(args.out)
    out.mkdir(parents=True, exist_ok=True)

    existing = {p.name for p in out.glob("run_*") if p.is_dir()}
    missing_ids = [i for i in range(1, args.runs + 1) if f"run_{i:04d}" not in existing]
    if not missing_ids:
        print("Nothing to resume.")
        return 0

    params = Params(
        runs=args.runs,
        thresholds=[float(x) for x in args.thresholds.split(",") if x.strip()],
        out=out,
        seed_base=args.seed_base,
        workers=args.workers,
        zip_out=args.zip,
    )

    # Simple strategy: rerun the whole sweep into the same folder.
    # Determinism + idempotency tests ensure stable files.
    run(params)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
