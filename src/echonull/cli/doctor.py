from __future__ import annotations

import argparse
import json
import platform
import sys
from importlib.metadata import PackageNotFoundError, version
from typing import Any

CORE_DEPS = [
    "numpy",
    "pandas",
    "networkx",
]

DEV_TOOLS = [
    "ruff",
    "black",
    "mypy",
    "pytest",
    "pytest-cov",
]


def _pkg_version(name: str) -> str | None:
    try:
        return version(name)
    except PackageNotFoundError:
        return None


def collect_info() -> dict[str, Any]:
    deps = {name: _pkg_version(name) for name in CORE_DEPS}
    dev_tools = {name: _pkg_version(name) for name in DEV_TOOLS}

    missing: list[str] = []
    for name, ver in {**deps, **dev_tools}.items():
        if ver is None:
            missing.append(name)

    missing.sort()
    ok = not missing

    return {
        "python": sys.version.split()[0],
        "platform": platform.platform(),
        "deps": deps,
        "dev_tools": dev_tools,
        "missing": missing,
        "ok": ok,
    }


def build_parser() -> argparse.ArgumentParser:
    p = argparse.ArgumentParser(prog="echonull-doctor", description="EchoNull environment doctor")
    p.add_argument("--json", action="store_true", help="Print JSON report")
    p.add_argument("--quiet", action="store_true", help="Exit code only, no output")
    return p


def main(argv: list[str] | None = None) -> int:
    args = build_parser().parse_args(argv)
    info = collect_info()

    rc = 0 if bool(info["ok"]) else 2
    if args.quiet:
        return rc

    if args.json:
        print(json.dumps(info, ensure_ascii=False, sort_keys=True))
        return rc

    print("EchoNull Doctor")
    print(f"Python: {info['python']}")
    print(f"Platform: {info['platform']}")
    if info["missing"]:
        print("Missing:")
        for name in info["missing"]:
            print(f"  - {name}")
    else:
        print("OK")

    return rc


def cli_main() -> int:
    return main(None)
