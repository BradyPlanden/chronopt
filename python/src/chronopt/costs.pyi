# Stub file for chronopt.costs submodule
# This file provides IDE autocomplete for the costs submodule

from chronopt._chronopt import CostMetric

def SSE() -> CostMetric:
    """Sum of Squared Errors cost metric."""
    ...

def RMSE() -> CostMetric:
    """Root Mean Squared Error cost metric."""
    ...

def GaussianNLL(variance: float = 1.0) -> CostMetric:
    """Gaussian Negative Log-Likelihood cost metric."""
    ...

__all__ = [
    "CostMetric",
    "SSE",
    "RMSE",
    "GaussianNLL",
]
