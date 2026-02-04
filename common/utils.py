from __future__ import annotations

import hashlib
import logging
import time
from collections.abc import Callable
from functools import wraps
from pathlib import Path
from typing import Any, ParamSpec, Protocol, TypeVar, cast

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


from typing import ParamSpec, TypeVar

P = ParamSpec("P")
R = TypeVar("R")


def perf_timer(func: Callable[P, R]) -> Callable[P, R]:
    """Decorator: logs how long the wrapped function took."""

    @wraps(func)
    def wrapper(*args: P.args, **kwargs: P.kwargs) -> R:
        start = time.perf_counter()
        result = func(*args, **kwargs)
        duration = time.perf_counter() - start
        logger.info("%s took %.4fs", func.__name__, duration)
        return result

    return cast(Callable[P, R], wrapper)



class AnalyzerProtocol(Protocol):
    def analyze(
        self,
        run_id: int,
        seed: int,
        data: Any,
        output_dir: Path,
    ) -> dict[str, Any]: ...
