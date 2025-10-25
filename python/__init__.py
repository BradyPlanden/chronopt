# Re-export Rust-backed classes from the compiled submodule
from chronopt import (
    Builder,
    CMAES,
    Problem,
    NelderMead,
    OptimisationResults,
    PythonBuilder,
    builder_factory_py as BuilderFactory,
)

# builder aliases
builder = BuilderFactory()

__all__ = [
    "builder",
    "Builder",
    "CMAES",
    "PythonBuilder",
    "Problem",
    "NelderMead",
    "OptimisationResults",
]
