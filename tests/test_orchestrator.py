from __future__ import annotations

import json
from pathlib import Path

from orchestrator.run import Params, _parse_thresholds, process_run, run


def test_parse_thresholds() -> None:
    assert _parse_thresholds("0.25, 0.5") == [0.25, 0.5]


def test_process_run_and_run(tmp_path: Path) -> None:
    params = Params(
        runs=2,
        thresholds=[0.25],
        out=tmp_path / "_out",
        seed_base=100,
        workers=1,
        zip_out=True,
    )

    one = process_run(1, params)
    assert one["run_id"] == 1
    assert (params.out / "run_0001" / "multi.csv").exists()

    results, z = run(params)
    assert len(results) == 2
    assert (params.out / "overview.json").exists()
    assert (params.out / "manifest.json").exists()

    manifest = json.loads((params.out / "manifest.json").read_text(encoding="utf-8"))
    assert manifest["runs"] == 2
    assert manifest["name"] == "RiftTrace"

    assert z is not None
    assert z.exists()
