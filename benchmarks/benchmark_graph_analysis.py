from __future__ import annotations

import time
from pathlib import Path

from graph_analysis.analyzer import GraphAnalysisAnalyzer


def main() -> None:
    a = GraphAnalysisAnalyzer([0.25, 0.5, 0.7, 0.8])
    out = Path("_ci_out/bench_graph_analysis")
    out.mkdir(parents=True, exist_ok=True)

    start = time.perf_counter()
    a.analyze(run_id=1, seed=123, data=None, output_dir=out)
    dur = time.perf_counter() - start
    print(f"graph_analysis single-run took {dur:.4f}s")


if __name__ == "__main__":
    main()
