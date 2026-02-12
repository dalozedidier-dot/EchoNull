from __future__ import annotations

import argparse
from dataclasses import dataclass
from typing import Callable

from echonull.delta_stats.analyzer import DeltaStatsAnalyzer
from echonull.graph_analysis.analyzer import GraphAnalysisAnalyzer
from echonull.mark_counts.analyzer import MarkCountsAnalyzer


@dataclass(frozen=True)
class Plugin:
    name: str
    factory: Callable[[], object]


BUILTINS: dict[str, Plugin] = {
    "delta_stats": Plugin("delta_stats", factory=DeltaStatsAnalyzer),
    "graph_analysis": Plugin("graph_analysis", factory=GraphAnalysisAnalyzer),
    "mark_counts": Plugin("mark_counts", factory=MarkCountsAnalyzer),
}


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--list", action="store_true", help="List available plugins.")
    ap.add_argument("--select", default=None, help="Comma-separated plugin names.")
    args = ap.parse_args()

    if args.list or args.select is None:
        for name in sorted(BUILTINS):
            print(name)
        return 0

    selected = [x.strip() for x in args.select.split(",") if x.strip()]
    missing = [x for x in selected if x not in BUILTINS]
    if missing:
        print("Missing: " + ",".join(missing))
        return 2

    for name in selected:
        _ = BUILTINS[name].factory()
        print(f"OK: {name}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
