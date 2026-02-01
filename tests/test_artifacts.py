from __future__ import annotations

import json
import zipfile
from pathlib import Path
from typing import Any

from common.utils import compute_sha256
from orchestrator.run import Params, run


def _load_json(path: Path) -> dict[str, Any]:
    return json.loads(path.read_text(encoding="utf-8"))


def test_manifest_integrity_and_zip_contents(tmp_path: Path) -> None:
    out = tmp_path / "_out"
    params = Params(
        runs=3,
        thresholds=[0.25, 0.5],
        out=out,
        seed_base=123,
        workers=1,
        zip_out=True,
    )

    _results, zip_path = run(params)
    assert zip_path is not None
    assert zip_path.exists()

    overview_path = out / "overview.json"
    manifest_path = out / "manifest.json"
    assert overview_path.exists()
    assert manifest_path.exists()

    manifest = _load_json(manifest_path)
    assert manifest["name"] == "EchoNull"
    assert manifest["runs"] == 3
    assert manifest["overview_sha256"] == compute_sha256(overview_path)

    with zipfile.ZipFile(zip_path, "r") as zf:
        names = set(zf.namelist())
        assert "overview.json" in names
        assert "manifest.json" in names

        for run_id in range(1, 4):
            prefix = f"run_{run_id:04d}/"
            assert f"{prefix}multi.csv" in names
            assert f"{prefix}delta_stats/stats.json" in names
            assert f"{prefix}mark_counts/count.txt" in names
            assert f"{prefix}graph_analysis/thr_0.25_report.json" in names
            assert f"{prefix}graph_analysis/thr_0.50_report.json" in names

        # Validate one graph report payload is well-formed and within expected ranges
        payload = json.loads(
            zf.read("run_0001/graph_analysis/thr_0.25_report.json").decode("utf-8")
        )
        assert set(payload.keys()) == {"nodes", "edges", "jaccard"}
        assert payload["nodes"] == 10
        assert isinstance(payload["edges"], int)
        assert 0.9 <= float(payload["jaccard"]) <= 1.0
