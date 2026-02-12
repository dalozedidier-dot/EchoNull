from __future__ import annotations

import json
from types import SimpleNamespace
from typing import Any

from pytest import CaptureFixture, MonkeyPatch

from echonull import null_trace


def test_null_trace_missing_dependency(
    monkeypatch: MonkeyPatch,
    capsys: CaptureFixture[str],
) -> None:
    def boom(_name: str) -> Any:
        raise ModuleNotFoundError("nulltrace")

    monkeypatch.setattr("echonull.null_trace.importlib.import_module", boom)
    rc = null_trace.main([])
    assert rc == 2
    out = capsys.readouterr().out
    assert "nulltrace is not installed" in out


def test_null_trace_available_json(
    monkeypatch: MonkeyPatch,
    capsys: CaptureFixture[str],
) -> None:
    dummy = SimpleNamespace(__version__="0.0.0")
    monkeypatch.setattr("echonull.null_trace.importlib.import_module", lambda _name: dummy)

    rc = null_trace.main(["--json"])
    assert rc == 0
    out = capsys.readouterr().out
    payload = json.loads(out)
    assert payload["ok"] is True
    assert payload["nulltrace_version"] == "0.0.0"


def test_null_trace_quiet(
    monkeypatch: MonkeyPatch,
    capsys: CaptureFixture[str],
) -> None:
    dummy = SimpleNamespace(__version__="0.0.0")
    monkeypatch.setattr("echonull.null_trace.importlib.import_module", lambda _name: dummy)

    rc = null_trace.main(["--quiet"])
    assert rc == 0
    out = capsys.readouterr().out
    assert out == ""
