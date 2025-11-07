"""Cost metric helpers exposed by the Chronopt Python API."""

from __future__ import annotations

from chronopt._chronopt import RMSE as _RMSE
from chronopt._chronopt import SSE as _SSE
from chronopt._chronopt import CostMetric
from chronopt._chronopt import GaussianNLL as _GaussianNLL


def SSE() -> CostMetric:
    """Sum of Squared Errors cost metric."""
    return _SSE()


def RMSE() -> CostMetric:
    """Root Mean Squared Error cost metric."""
    return _RMSE()


def GaussianNLL(variance: float = 1.0) -> CostMetric:
    """Gaussian Negative Log-Likelihood cost metric."""
    return _GaussianNLL(variance)


__all__ = ["CostMetric", "SSE", "RMSE", "GaussianNLL"]
