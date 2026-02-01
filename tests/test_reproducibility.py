from __future__ import annotations

from pathlib import Path
from typing import Any

from orchestrator.run import Params, process_run


def _strip_paths(obj: Any) -> Any:
    if isinstance(obj, dict):
        return {k: _strip_paths(v) for k, v in obj.items() if k != "path"}
    if isinstance(obj, list):
        return [_strip_paths(x) for x in obj]
    return obj


def test_process_run_is_deterministic_for_same_seed(tmp_path: Path) -> None:
    p1 = Params(
        runs=1,
        thresholds=[0.25, 0.5],
        out=tmp_path / "a",
        seed_base=100,
        workers=1,
        zip_out=False,
    )
    p2 = Params(
        runs=1,
        thresholds=[0.25, 0.5],
        out=tmp_path / "b",
        seed_base=100,
        workers=1,
        zip_out=False,
    )

    r1 = _strip_paths(process_run(1, p1))
    r2 = _strip_paths(process_run(1, p2))

    assert r1["results"] == r2["results"]
    assert r1["hashes"] == r2["hashes"]


def test_seed_base_changes_output(tmp_path: Path) -> None:
    p1 = Params(
        runs=1,
        thresholds=[0.25],
        out=tmp_path / "a",
        seed_base=100,
        workers=1,
        zip_out=False,
    )
    p2 = Params(
        runs=1,
        thresholds=[0.25],
        out=tmp_path / "b",
        seed_base=101,
        workers=1,
        zip_out=False,
    )

    r1 = process_run(1, p1)
    r2 = process_run(1, p2)

    # The dataset hash is extremely unlikely to match if seed changes.
    assert r1["hashes"]["multi.csv"] != r2["hashes"]["multi.csv"]
