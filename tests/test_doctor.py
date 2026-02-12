from __future__ import annotations

from pytest import CaptureFixture

from echonull.cli.doctor import collect_info, main


def test_collect_info_shape() -> None:
    info = collect_info()
    assert set(info.keys()) == {"python", "platform", "deps", "dev_tools", "ok", "missing"}
    assert isinstance(info["deps"], dict)
    assert isinstance(info["dev_tools"], dict)
    assert isinstance(info["missing"], list)


def test_doctor_json_output(capsys: CaptureFixture[str]) -> None:
    rc = main(["--json"])
    assert rc in (0, 2)
    out = capsys.readouterr().out
    assert out.strip().startswith("{")
    assert '"python"' in out


def test_doctor_quiet_only_exit_code(capsys: CaptureFixture[str]) -> None:
    rc = main(["--quiet"])
    assert rc in (0, 2)
    out = capsys.readouterr().out
    assert out == ""
