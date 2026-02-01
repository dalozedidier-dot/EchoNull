from __future__ import annotations

from pathlib import Path

import pytest

from orchestrator.run import Params, _parse_thresholds, run


def test_parse_thresholds_rejects_invalid() -> None:
    with pytest.raises(ValueError):
        _parse_thresholds("abc")


def test_zero_runs_still_writes_overview_and_manifest(tmp_path: Path) -> None:
    out = tmp_path / "_out"
    params = Params(
        runs=0,
        thresholds=[0.25],
        out=out,
        seed_base=1,
        workers=1,
        zip_out=False,
    )

    results, zip_path = run(params)
    assert results == []
    assert zip_path is None
    assert (out / "overview.json").exists()
    assert (out / "manifest.json").exists()
