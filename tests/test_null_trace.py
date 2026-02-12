from __future__ import annotations

from echonull.null_trace import main


def test_null_trace_missing_dependency(capsys) -> None:
    rc = main([])
    assert rc == 2
    out = capsys.readouterr().out
    assert "nulltrace is not installed" in out
