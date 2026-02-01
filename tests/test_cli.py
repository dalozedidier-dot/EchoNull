from __future__ import annotations

import json
from pathlib import Path

from orchestrator.run import build_parser, main


def test_build_parser_defaults_are_sane() -> None:
    parser = build_parser()
    args = parser.parse_args([])
    assert args.runs == 10
    assert isinstance(args.thresholds, str)
    assert args.out == "_out"
    assert args.seed_base == 1000
    assert args.workers >= 1
    assert args.zip_out is False


def test_main_writes_outputs(tmp_path: Path) -> None:
    out = tmp_path / "_out"
    rc = main(
        [
            "--runs",
            "2",
            "--thresholds",
            "0.25,0.5",
            "--out",
            str(out),
            "--seed-base",
            "123",
            "--workers",
            "1",
            "--zip",
        ]
    )
    assert rc == 0
    assert (out / "overview.json").exists()
    assert (out / "manifest.json").exists()

    manifest = json.loads((out / "manifest.json").read_text(encoding="utf-8"))
    assert manifest["name"] == "EchoNull"
    assert manifest["runs"] == 2
