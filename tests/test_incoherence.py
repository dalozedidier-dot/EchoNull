from __future__ import annotations

from typing import Any

import pytest

from echonull import compute_incoherence


def _phi_pos(x: dict[str, Any]) -> float:
    return float(x["a"])


def _phi_neg(_x: dict[str, Any]) -> float:
    return -10.0


def test_compute_incoherence_weights_none_equal() -> None:
    x = {"a": 2.0}
    out = compute_incoherence(x, [_phi_pos, _phi_neg])
    assert out == pytest.approx(1.0)


def test_compute_incoherence_weights_list() -> None:
    x = {"a": 2.0}
    out = compute_incoherence(x, [_phi_pos, _phi_neg], weights=[0.25, 0.75])
    assert out == pytest.approx(0.5)


def test_compute_incoherence_weights_dict_by_name_default() -> None:
    x = {"a": 2.0}
    out = compute_incoherence(x, [_phi_pos, _phi_neg], weights={"_phi_pos": 0.2})
    assert out == pytest.approx(0.4)


def test_compute_incoherence_empty_phis_raises() -> None:
    with pytest.raises(ValueError, match="phis must be non-empty"):
        compute_incoherence({}, [])


def test_compute_incoherence_weights_length_mismatch_raises() -> None:
    with pytest.raises(ValueError, match="same length"):
        compute_incoherence({"a": 1.0}, [_phi_pos, _phi_neg], weights=[1.0])
