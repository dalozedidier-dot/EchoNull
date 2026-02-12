from __future__ import annotations

import argparse
import json
import platform
import sys
from importlib import metadata
from typing import Any


def _pkg_version(name: str) -> str | None:
    try:
        return metadata.version(name)
    except metadata.PackageNotFoundError:
        return None


def build_parser() -> argparse.ArgumentParser:
    p = argparse.ArgumentParser(prog="echonull-doctor")
    p.add_argument("--json", action="store_true", help="Output machine-readable JSON.")
    p.add_argument(
        "--quiet",
        action="store_true",
        help="Do not print anything, only set exit code.",
    )
    return p


def collect_info() -> dict[str, Any]:
    deps = ["numpy", "pandas", "networkx"]
    tools = ["black", "ruff", "mypy", "pytest"]
    info: dict[str, Any] = {
        "python": sys.version.split()[0],
        "platform": platform.platform(),
        "deps": {d: _pkg_version(d) for d in deps},
        "dev_tools": {t: _pkg_version(t) for t in tools},
    }
    missing = [k for k, v in info["deps"].items() if v is None]
    info["ok"] = len(missing) == 0
    info["missing"] = missing
    return info


def main(argv: list[str] | None = None) -> int:
    args = build_parser().parse_args(argv)
    info = collect_info()

    rc = 0 if info["ok"] else 2
    if args.quiet:
        return rc

    if args.json:
        print(json.dumps(info, indent=2, sort_keys=True))
    else:
        print(f"python={info['python']}")
        for k, v in info["deps"].items():
            print(f"{k}={v}")
        if not info["ok"]:
            print("missing=" + ",".join(info["missing"]))
    return rc


if __name__ == "__main__":
    raise SystemExit(main())
