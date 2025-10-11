import chronopt as chron


# Example function
def rosenbrock(x):
    return (1 - x[0]) ** 2 + 100 * (x[1] - x[0] ** 2) ** 2


# Simple API
builder = chron.builder.SimpleProblem().add_callable(rosenbrock)
problem = builder.build()

optim = chron.NelderMead(problem)
# sampler = chron.Hamiltonian()
# sampler.set_number_of_chains(6)
# sampler.set_parallel(True)


# Run
results = optim.run()
# samples = sampler.run()

print(results)
print(f"Optimal x: {results.x}")
print(f"Optimal value: {results.fun}")
