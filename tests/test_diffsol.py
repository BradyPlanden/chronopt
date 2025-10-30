import chronopt as chron
import numpy as np
import pytest


def test_diffsol_builder():
    """Test basic Diffsol builder functionality"""
    # Example diffsol ODE (logistic growth)
    ds = """
in = [r, k]
r { 1 } k { 1 }
u_i { y = 0.1 }
F_i { (r * y) * (1 - (y / k)) }
"""

    # Generate some test data
    t_span = np.linspace(0, 1, 100)
    # Simple exponential growth for testing
    data = 0.1 * np.exp(t_span)

    # Build the problem
    builder = (
        chron.DiffsolBuilder()
        .add_diffsl(ds)
        .add_data(data)
        .with_rtol(1e-6)
        .with_atol(1e-6)
        .add_params({"r": 1.0, "k": 1.0})
        .add_cost(chron.costs.SSE())
        .add_cost(chron.costs.RMSE())
    )

    problem = builder.build()

    # Test that we can evaluate the problem
    x0 = [1.0, 1.0]  # r, k parameters
    cost = problem.evaluate(x0)

    # Cost should be finite
    assert np.isfinite(cost), f"Cost should be finite, got {cost}"
    assert cost >= 0, f"Cost should be non-negative, got {cost}"

    # Test that we can optimise the problem
    optimiser = (
        chron.NelderMead().with_max_iter(500).with_threshold(1e-7).with_patience(10)
    )
    result = optimiser.run(problem, x0)
    assert result.success
    assert result.fun < 1e-5


@pytest.mark.parametrize("variance", [0.5, 2.0])
def test_diffsol_cost_metrics(variance: float) -> None:
    """Ensure selectable cost metrics produce consistent values."""

    ds = """
in = [r, k]
r { 1 } k { 1 }
u_i { y = 0.1 }
F_i { (r * y) * (1 - (y / k)) }
"""

    time_points = np.linspace(0, 1, 20)
    data = 0.1 * np.exp(time_points)
    params = {"r": 1.0, "k": 1.0}

    def build_problem(cost_metric=None):
        builder = (
            chron.DiffsolBuilder()
            .add_diffsl(ds)
            .add_data(data)
            .with_rtol(1e-6)
            .with_atol(1e-6)
            .add_params(params)
        )
        if cost_metric is not None:
            builder = builder.add_cost(cost_metric)
        return builder.build()

    sse_problem = build_problem()
    sse_problem_explicit = build_problem(chron.costs.SSE())
    rmse_problem = build_problem(chron.costs.RMSE())
    gaussian_problem = build_problem(chron.costs.GaussianNLL(variance))

    test_params = [0.8, 1.2]
    sse_cost = sse_problem.evaluate(test_params)
    assert np.isfinite(sse_cost)
    assert sse_cost >= 0

    sse_cost_explicit = sse_problem_explicit.evaluate(test_params)
    assert pytest.approx(sse_cost, rel=1e-8, abs=1e-10) == sse_cost_explicit

    rmse_cost = rmse_problem.evaluate(test_params)
    expected_rmse = np.sqrt(sse_cost / data.size)
    assert pytest.approx(expected_rmse, rel=1e-6, abs=1e-9) == rmse_cost

    gaussian_cost = gaussian_problem.evaluate(test_params)
    expected_gaussian = (
        0.5 * data.size * np.log(2.0 * np.pi * variance) + 0.5 * sse_cost / variance
    )
    assert pytest.approx(expected_gaussian, rel=1e-6, abs=1e-9) == gaussian_cost

    with pytest.raises(ValueError):
        chron.costs.GaussianNLL(0.0)
