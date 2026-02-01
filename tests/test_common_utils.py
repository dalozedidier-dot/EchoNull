from __future__ import annotations

from pathlib import Path

from common.utils import compute_sha256, perf_timer


def test_compute_sha256(tmp_path: Path) -> None:
    p = tmp_path / "x.bin"
    p.write_bytes(b"abc")
    h = compute_sha256(p)
    assert isinstance(h, str)
    assert len(h) == 64


def test_perf_timer_wraps() -> None:
    calls = {"n": 0}

    @perf_timer
    def f(x: int) -> int:
        calls["n"] += 1
        return x + 1

    assert f(1) == 2
    assert calls["n"] == 1
