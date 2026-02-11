from __future__ import annotations

import sys


def main() -> int:
    """Optional shim for an external 'nulltrace' tool.

    EchoNull does not vendor the 'nulltrace' package. This file is kept only as a
    compatibility entrypoint. If you need it, install the external dependency
    that provides `nulltrace.null_trace`.
    """

    try:
        from nulltrace.null_trace import main as _main  # type: ignore[import-not-found]
    except Exception as exc:
        print(
            "EchoNull: optional dependency 'nulltrace' is not installed "
            "(cannot import nulltrace.null_trace).",
            file=sys.stderr,
        )
        print(f"Details: {exc!r}", file=sys.stderr)
        return 2

    _main()
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
