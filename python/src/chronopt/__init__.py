"""Chronopt public Python API."""

from __future__ import annotations

from chronopt import plotting
from chronopt._chronopt import (
    CMAES,
    CostMetric,
    DiffsolBuilder,
    NelderMead,
    OptimisationResults,
    Problem,
    ScalarBuilder,
    VectorBuilder,
    builder,
    costs,
    samplers,
)

# Top-level convenience exports for builders
VectorProblemBuilder = VectorBuilder
ScalarProblemBuilder = ScalarBuilder
DiffsolProblemBuilder = DiffsolBuilder

# Top-level convenience exports for cost functions
SSE = costs.SSE
RMSE = costs.RMSE
GaussianNLL = costs.GaussianNLL

__all__ = [
    # Original exports
    "ScalarBuilder",
    "builder",
    "CMAES",
    "CostMetric",
    "DiffsolBuilder",
    "VectorBuilder",
    "NelderMead",
    "OptimisationResults",
    "Problem",
    "costs",
    "samplers",
    "plotting",
    # Convenience aliases for builders
    "VectorProblemBuilder",
    "ScalarProblemBuilder",
    "DiffsolProblemBuilder",
    # Convenience aliases for cost functions
    "SSE",
    "RMSE",
    "GaussianNLL",
]
