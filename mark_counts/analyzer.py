from __future__ import annotations

from pathlib import Path
from typing import Any

import numpy as np

from common.utils import AnalyzerProtocol, perf_timer


class MarkCountsAnalyzer(AnalyzerProtocol):
    @perf_timer
    def analyze(self, run_id: int, seed: int, data: Any, output_dir: Path) -> dict[str, Any]:
        np.random.seed(seed)
        count = int(np.random.randint(1, 5))
        out = output_dir / "mark_counts"
        out.mkdir(parents=True, exist_ok=True)
        (out / "count.txt").write_text(str(count), encoding="utf-8")
        return {"mark_counts": {"median_count": count}}
