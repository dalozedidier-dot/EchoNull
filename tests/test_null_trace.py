from __future__ import annotations

from pytest import CaptureFixture

from echonull.null_trace import main


def test_null_trace_missing_dependency(capsys: CaptureFixture[str]) -> None:
    rc = main([])
    assert rc == 2
    out = capsys.readouterr().out
    assert "nulltrace is not installed" in out
