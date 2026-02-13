from __future__ import annotations

import sys
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
    out = capsys.readouterr().out.lower()
    assert "nulltrace" in out


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


def test_null_trace_available_default_prints(
    monkeypatch: MonkeyPatch,
    capsys: CaptureFixture[str],
) -> None:
    dummy = SimpleNamespace()  # no __version__
    monkeypatch.setattr("echonull.null_trace.importlib.import_module", lambda _name: dummy)

    rc = null_trace.main([])
    assert rc == 0
    out = capsys.readouterr().out.lower()
    assert "nulltrace" in out
    assert "available" in out


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


def test_null_trace_cli_main_delegates(monkeypatch: MonkeyPatch) -> None:
    monkeypatch.setattr("echonull.null_trace.main", lambda _argv: 7)
    monkeypatch.setattr(sys, "argv", ["echonull-null-trace", "--quiet"])

    try:
        rc: Any = null_trace.cli_main()
    except SystemExit as exc:
        rc = exc.code

    assert rc == 7
