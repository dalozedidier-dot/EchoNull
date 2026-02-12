from __future__ import annotations

import argparse
from pathlib import Path

import pandas as pd

from echonull.delta_stats.analyzer import DeltaStatsAnalyzer
from echonull.graph_analysis.analyzer import GraphAnalysisAnalyzer
from echonull.mark_counts.analyzer import MarkCountsAnalyzer


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("csv", help="Input CSV file.")
    ap.add_argument("--out", default="_ci_out_ingest", help="Output directory.")
    ap.add_argument("--run-id", type=int, default=1)
    ap.add_argument("--seed", type=int, default=1)
    ap.add_argument("--thresholds", default="0.25,0.5")
    args = ap.parse_args()

    out = Path(args.out) / f"run_{args.run_id:04d}"
    out.mkdir(parents=True, exist_ok=True)

    df = pd.read_csv(args.csv)
    (out / "multi.csv").write_text(df.to_csv(index=False), encoding="utf-8")

    delta = DeltaStatsAnalyzer()
    mark = MarkCountsAnalyzer()
    graph = GraphAnalysisAnalyzer()

    delta.analyze(args.run_id, args.seed, df, out)
    mark.analyze(args.run_id, args.seed, df, out)

    thresholds = [float(x) for x in args.thresholds.split(",") if x.strip()]
    for thr in thresholds:
        graph.analyze(args.run_id, args.seed, df, out, threshold=thr)

    print(out)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
