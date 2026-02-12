from __future__ import annotations

from collections.abc import Callable
from importlib.metadata import PackageNotFoundError, version as pkg_version

from pytest import CaptureFixture, MonkeyPatch

from echonull.cli import doctor


def test_collect_info_shape() -> None:
    info = doctor.collect_info()
    assert set(info.keys()) == {"python", "platform", "deps", "dev_tools", "ok", "missing"}
    assert isinstance(info["deps"], dict)
    assert isinstance(info["dev_tools"], dict)
    assert isinstance(info["missing"], list)
    assert isinstance(info["ok"], bool)


def test_doctor_json_output(capsys: CaptureFixture[str]) -> None:
    rc = doctor.main(["--json"])
    assert rc in (0, 2)
    out = capsys.readouterr().out
    assert out.strip().startswith("{")
    assert '"python"' in out


def test_doctor_default_output_ok(capsys: CaptureFixture[str]) -> None:
    rc = doctor.main([])
    assert rc in (0, 2)
    out = capsys.readouterr().out
    assert "EchoNull Doctor" in out


def test_doctor_missing_dep_branch(monkeypatch: MonkeyPatch, capsys: CaptureFixture[str]) -> None:
    def fake_version(name: str) -> str:
        if name == "numpy":
            raise PackageNotFoundError(name)
        return pkg_version(name)

    monkeypatch.setattr("echonull.cli.doctor.version", fake_version)
    rc = doctor.main([])
    assert rc == 2
    out = capsys.readouterr().out
    assert "Missing:" in out
    assert "numpy" in out


def test_doctor_quiet_only_exit_code(capsys: CaptureFixture[str]) -> None:
    rc = doctor.main(["--quiet"])
    assert rc in (0, 2)
    out = capsys.readouterr().out
    assert out == ""
