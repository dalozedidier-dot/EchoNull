from __future__ import annotations

import argparse
import importlib
import json
from typing import Any


def _try_import_nulltrace() -> Any | None:
    try:
        return importlib.import_module("nulltrace")
    except ModuleNotFoundError:
        return None


def build_parser() -> argparse.ArgumentParser:
    p = argparse.ArgumentParser(prog="echonull-null-trace", description="Optional NullTrace probe")
    p.add_argument("--json", action="store_true", help="Print JSON report")
    p.add_argument("--quiet", action="store_true", help="Exit code only, no output")
    return p


def main(argv: list[str] | None = None) -> int:
    args = build_parser().parse_args(argv)

    mod = _try_import_nulltrace()
    ok = mod is not None
    rc = 0 if ok else 2

    if args.quiet:
        return rc

    payload = {
        "ok": ok,
        "nulltrace_version": getattr(mod, "__version__", None) if ok else None,
        "message": None if ok else "nulltrace is not installed",
    }

    if args.json:
        print(json.dumps(payload, ensure_ascii=False, sort_keys=True))
        return rc

    if ok:
        ver = payload["nulltrace_version"] or "unknown"
        print(f"nulltrace available ({ver})")
    else:
        print("nulltrace is not installed")

    return rc


def cli_main() -> int:
    return main(None)
