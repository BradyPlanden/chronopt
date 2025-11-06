# Stub file for chronopt.builder submodule
# This file provides IDE autocomplete for the builder submodule

from chronopt._chronopt import (
    DiffsolBuilder,
    ScalarBuilder,
    VectorBuilder,
)

# Aliases with "Problem" naming convention
DiffsolProblemBuilder = DiffsolBuilder
ScalarProblemBuilder = ScalarBuilder
VectorProblemBuilder = VectorBuilder

__all__ = [
    "DiffsolBuilder",
    "ScalarBuilder",
    "VectorBuilder",
    "DiffsolProblemBuilder",
    "ScalarProblemBuilder",
    "VectorProblemBuilder",
]
