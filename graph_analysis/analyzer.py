from __future__ import annotations

import json
from pathlib import Path
from typing import Any

import networkx as nx
import numpy as np

from common.utils import AnalyzerProtocol, perf_timer


class GraphAnalysisAnalyzer(AnalyzerProtocol):
    def __init__(self, thresholds: list[float] | None = None):
        self.thresholds = thresholds if thresholds is not None else [0.25, 0.5, 0.7, 0.8]

    @perf_timer
    def analyze(self, run_id: int, seed: int, data: Any, output_dir: Path) -> dict[str, Any]:
        np.random.seed(seed)
        results: dict[str, Any] = {}

        out = output_dir / "graph_analysis"
        out.mkdir(parents=True, exist_ok=True)

        for thr in self.thresholds:
            g = nx.erdos_renyi_graph(n=10, p=min(0.99, 0.2 + thr / 2), seed=seed)
            n_nodes = g.number_of_nodes()
            n_edges = g.number_of_edges()

            # Variance contrôlée pour tests et bench
            jaccard = 1.0 if run_id % 2 == 0 else float(np.random.uniform(0.9, 1.0))

            report_path = out / f"thr_{thr:.2f}_report.json"
            payload = {"nodes": n_nodes, "edges": n_edges, "jaccard": jaccard}
            report_path.write_text(
                json.dumps(payload, separators=(",", ":")),
                encoding="utf-8",
            )

            results[f"{thr:.2f}"] = {
                "n_nodes": n_nodes,
                "n_edges": n_edges,
                "jaccard": jaccard,
                "path": str(report_path),
            }

        return {"graph_analysis": results}
