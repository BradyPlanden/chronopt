# Re-export Rust-backed classes from the compiled submodule
from importlib import import_module

from chronopt import (
    CMAES,
    Builder,
    NelderMead,
    OptimisationResults,
    Problem,
    PythonBuilder,
    costs,
)
from chronopt import (
    PyCostMetric as CostMetric,
)
from chronopt import (
    builder_factory_py as BuilderFactory,
)

# submodules
samplers = import_module("src.samplers")

# builder aliases
builder = BuilderFactory()

__all__ = [
    "CostMetric",
    "costs",
    "builder",
    "Builder",
    "CMAES",
    "PythonBuilder",
    "Problem",
    "NelderMead",
    "OptimisationResults",
    "samplers",
]
