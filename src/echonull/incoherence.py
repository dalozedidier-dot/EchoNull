from __future__ import annotations

from collections.abc import Callable
from typing import Any


def compute_incoherence(
    x: dict[str, Any],
    phis: list[Callable[[dict[str, Any]], float]],
    weights: list[float] | dict[str, float] | None = None,
) -> float:
    if not phis:
        raise ValueError("phis must be non-empty")

    if weights is None:
        w_list = [1.0 / len(phis)] * len(phis)
    elif isinstance(weights, dict):
        w_list = [float(weights.get(getattr(f, "__name__", ""), 1.0)) for f in phis]
    else:
        if len(weights) != len(phis):
            raise ValueError("weights must have the same length as phis")
        w_list = [float(w) for w in weights]

    total = 0.0
    for w, phi in zip(w_list, phis, strict=True):
        v = float(phi(x))
        if v > 0.0:
            total += w * v
    return float(total)
