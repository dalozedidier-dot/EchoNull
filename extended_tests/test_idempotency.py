from __future__ import annotations

import json
from pathlib import Path
from typing import Any, cast

from common.utils import compute_sha256
from orchestrator.run import Params, run


def _read_json(path: Path) -> dict[str, Any]:
    return cast(dict[str, Any], json.loads(path.read_text(encoding="utf-8")))


def test_two_identical_runs_keep_overview_and_manifest_stable(tmp_path: Path) -> None:
    out = tmp_path / "_out"
    params = Params(
        runs=5,
        thresholds=[0.25, 0.5],
        out=out,
        seed_base=123,
        workers=1,
        zip_out=False,
    )

    run(params)
    overview_1 = (out / "overview.json").read_text(encoding="utf-8")
    manifest_1 = _read_json(out / "manifest.json")
    sha_1 = compute_sha256(out / "overview.json")

    # Run again into the same folder, same parameters
    run(params)
    overview_2 = (out / "overview.json").read_text(encoding="utf-8")
    manifest_2 = _read_json(out / "manifest.json")
    sha_2 = compute_sha256(out / "overview.json")

    assert overview_1 == overview_2
    assert sha_1 == sha_2

    # Manifest should remain stable too (it contains overview_sha256 which we just checked)
    assert manifest_1 == manifest_2
    assert manifest_2["name"] == "EchoNull"
