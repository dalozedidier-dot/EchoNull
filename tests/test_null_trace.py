from __future__ import annotations

import importlib
import json
import runpy
import sys
from types import SimpleNamespace
from typing import Any

from pytest import CaptureFixture, MonkeyPatch

from echonull import null_trace


def test_null_trace_missing_dependency(monkeypatch: MonkeyPatch, capsys: CaptureFixture[str]) -> None:
    def boom(_name: str) -> Any:
        raise ModuleNotFoundError("nulltrace")

    monkeypatch.setattr("echonull.null_trace.importlib.import_module", boom)
    rc = null_trace.main([])
    assert rc == 2
    out = capsys.readouterr().out
    assert "nulltrace" in out.lower()


def test_null_trace_available_json(monkeypatch: MonkeyPatch, capsys: CaptureFixture[str]) -> None:
    dummy = SimpleNamespace(__version__="0.0.0")
    monkeypatch.setattr("echonull.null_trace.importlib.import_module", lambda _name: dummy)

    rc = null_trace.main(["--json"])
    assert rc == 0
    out = capsys.readouterr().out
    payload = json.loads(out)
    assert payload["ok"] is True
    assert payload["nulltrace_version"] == "0.0.0"


def test_null_trace_available_default_prints(monkeypatch: MonkeyPatch, capsys: CaptureFixture[str]) -> None:
    dummy = SimpleNamespace()  # no __version__
    monkeypatch.setattr("echonull.null_trace.importlib.import_module", lambda _name: dummy)

    rc = null_trace.main([])
    assert rc == 0
    out = capsys.readouterr().out.lower()
    assert "nulltrace" in out
    assert "available" in out


def test_null_trace_quiet(monkeypatch: MonkeyPatch, capsys: CaptureFixture[str]) -> None:
    dummy = SimpleNamespace(__version__="0.0.0")
    monkeypatch.setattr("echonull.null_trace.importlib.import_module", lambda _name: dummy)

    rc = null_trace.main(["--quiet"])
    assert rc == 0
    out = capsys.readouterr().out
    assert out == ""


def test_null_trace_main_guard_executes(monkeypatch: MonkeyPatch) -> None:
    # Execute module as __main__ to cover the guard line(s) in null_trace.py.
    def boom(_name: str) -> Any:
        raise ModuleNotFoundError("nulltrace")

    monkeypatch.setattr(importlib, "import_module", boom)
    monkeypatch.setattr(sys, "argv", ["echonull-null-trace", "--quiet"])
    try:
        runpy.run_module("echonull.null_trace", run_name="__main__")
    except SystemExit as exc:
        code = exc.code
    else:
        raise AssertionError("Expected SystemExit")

    if code is None:
        code_i = 0
    elif isinstance(code, int):
        code_i = code
    else:
        code_i = 1

    assert code_i in (0, 2)
