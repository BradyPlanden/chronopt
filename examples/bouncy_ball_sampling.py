import chronopt as chron
import numpy as np


def ball_states(t: np.ndarray, g: float, h: float) -> tuple[np.ndarray, np.ndarray]:
    height = h - 0.5 * g * np.square(t)
    height = np.maximum(height, 0.0)
    velocity = -g * t
    return height, velocity


# DiffSL program for a falling (bouncy) ball terminated when the height reaches zero.
dsl = """
in = [g, h]
g { 1 } h { 1 }
u_i {x = h, v = 0}
F_i {v, -g}
stop {x}
"""

g_true = 9.81
h_true = 10.0
t_stop = np.sqrt(2.0 * h_true / g_true)
t_final = 0.7 * t_stop
t_span = np.linspace(0.0, t_final, 61)
height, velocity = ball_states(t_span, g_true, h_true)
data = np.column_stack((t_span, height, velocity))

# Configure the problem
builder = (
    chron.DiffsolBuilder()
    .add_diffsl(dsl)
    .add_data(data)
    .add_params({"g": g_true, "h": h_true})
    .with_rtol(1e-6)
    .with_atol(1e-6)
    .add_cost(chron.costs.SSE())
)

problem = builder.build()

# Setup sampler
sampler = (
    chron.samplers.MetropolisHastings()
    .with_num_chains(2)
    .with_num_steps(1000)
    .with_step_size(0.25)
    .with_parallel(True)
    .with_seed(1234)
)

samples = sampler.run(problem, initial=[4.0, 4.0])
print(samples)
