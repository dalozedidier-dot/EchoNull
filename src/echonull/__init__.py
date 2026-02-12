from __future__ import annotations

from importlib import metadata


def _get_version() -> str:
    try:
        return metadata.version("echonull")
    except metadata.PackageNotFoundError:
        # Running from a source checkout without an installed distribution.
        return "0.0.0"


__version__ = _get_version()
