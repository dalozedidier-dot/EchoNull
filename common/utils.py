from __future__ import annotations

import hashlib
import logging
import time
from collections.abc import Callable
from functools import wraps
from pathlib import Path
from typing import Any, Protocol, TypeVar, cast

logger = logging.getLogger("EchoNull")
if not logger.handlers:
    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s %(levelname)s %(message)s",
    )


def compute_sha256(path: Path) -> str:
    sha256 = hashlib.sha256()
    with path.open("rb") as f:
        for chunk in iter(lambda: f.read(65536), b""):
            sha256.update(chunk)
    return sha256.hexdigest()


F = TypeVar("F", bound=Callable[..., Any])


def perf_timer(func: F) -> F:
    @wraps(func)
    def wrapper(*args: Any, **kwargs: Any) -> Any:
        start = time.perf_counter()
        result = func(*args, **kwargs)
        duration = time.perf_counter() - start
        logger.info("%s took %.4fs", func.__name__, duration)
        return result

    return cast(F, wrapper)


class AnalyzerProtocol(Protocol):
    def analyze(
        self,
        run_id: int,
        seed: int,
        data: Any,
        output_dir: Path,
    ) -> dict[str, Any]: ...
