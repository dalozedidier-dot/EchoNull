from __future__ import annotations

import json
from pathlib import Path
from typing import Any, cast

from orchestrator.run import Params, run


def _read_json(path: Path) -> dict[str, Any]:
    return cast(dict[str, Any], json.loads(path.read_text(encoding="utf-8")))


def test_empty_thresholds_is_allowed(tmp_path: Path) -> None:
    out = tmp_path / "_out"
    params = Params(
        runs=2,
        thresholds=[],
        out=out,
        seed_base=10,
        workers=1,
        zip_out=False,
    )

    results, zip_path = run(params)
    assert zip_path is None
    assert len(results) == 2

    # Graph results should exist but be empty for each run
    for r in results:
        graph = cast(dict[str, Any], r["results"]["graph_analysis"])
        assert graph == {}

    manifest = _read_json(out / "manifest.json")
    assert manifest["name"] == "EchoNull"
    assert manifest["runs"] == 2


def test_out_dir_with_existing_files_is_not_deleted(tmp_path: Path) -> None:
    out = tmp_path / "_out"
    out.mkdir(parents=True, exist_ok=True)
    sentinel = out / "SENTINEL.txt"
    sentinel.write_text("keep", encoding="utf-8")

    params = Params(
        runs=1,
        thresholds=[0.25],
        out=out,
        seed_base=1,
        workers=1,
        zip_out=False,
    )
    run(params)

    assert sentinel.exists()
    assert sentinel.read_text(encoding="utf-8") == "keep"
