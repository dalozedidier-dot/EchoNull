from __future__ import annotations

import json
import zipfile
from pathlib import Path
from typing import Any, cast

from common.utils import compute_sha256
from orchestrator.run import Params, run


def _read_json(path: Path) -> dict[str, Any]:
    return cast(dict[str, Any], json.loads(path.read_text(encoding="utf-8")))


def test_parallel_sweep_produces_complete_artifacts(tmp_path: Path) -> None:
    out = tmp_path / "_out"
    params = Params(
        runs=10,
        thresholds=[0.25, 0.5, 0.7, 0.8],
        out=out,
        seed_base=777,
        workers=2,
        zip_out=True,
    )

    results, zip_path = run(params)
    assert len(results) == 10
    assert zip_path is not None and zip_path.exists()

    overview_path = out / "overview.json"
    manifest_path = out / "manifest.json"
    assert overview_path.exists()
    assert manifest_path.exists()

    manifest = _read_json(manifest_path)
    assert manifest["name"] == "EchoNull"
    assert manifest["runs"] == 10
    assert manifest["overview_sha256"] == compute_sha256(overview_path)

    with zipfile.ZipFile(zip_path, "r") as zf:
        names = set(zf.namelist())
        assert "overview.json" in names
        assert "manifest.json" in names

        for run_id in range(1, 11):
            prefix = f"run_{run_id:04d}/"
            assert f"{prefix}multi.csv" in names
            assert f"{prefix}delta_stats/stats.json" in names
            assert f"{prefix}mark_counts/count.txt" in names
            for thr in ("0.25", "0.50", "0.70", "0.80"):
                assert f"{prefix}graph_analysis/thr_{thr}_report.json" in names
