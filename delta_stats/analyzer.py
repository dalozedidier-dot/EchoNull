from __future__ import annotations

import json
from pathlib import Path
from typing import Any, Dict

import numpy as np

from common.utils import AnalyzerProtocol, perf_timer


class DeltaStatsAnalyzer(AnalyzerProtocol):
    @perf_timer
    def analyze(self, run_id: int, seed: int, data: Any, output_dir: Path) -> Dict[str, Any]:
        np.random.seed(seed)

        # Deltas très petits avec queue lognormale
        deltas = np.random.lognormal(mean=-8, sigma=1.5, size=50)
        abs_deltas = np.abs(deltas)

        p50 = float(np.percentile(abs_deltas, 50))
        p90 = float(np.percentile(abs_deltas, 90))
        p99 = float(np.percentile(abs_deltas, 99))
        mad = float(np.median(np.abs(abs_deltas - np.median(abs_deltas))))
        mx = float(np.max(abs_deltas))

        stats = {
            "n_deltas": int(abs_deltas.size),
            "abs_p50": p50,
            "abs_p90": p90,
            "abs_p99": p99,
            "mad": mad,
            "max": mx,
        }

        out = output_dir / "delta_stats"
        out.mkdir(parents=True, exist_ok=True)
        (out / "stats.json").write_text(json.dumps(stats, separators=(",", ":")), encoding="utf-8")

        return {"delta_stats": stats}
