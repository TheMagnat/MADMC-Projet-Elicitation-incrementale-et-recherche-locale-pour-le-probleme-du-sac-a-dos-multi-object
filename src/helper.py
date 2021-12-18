

def evaluate(values, solution):
	return (values * solution.reshape(-1, 1)).sum(axis=0)

def feasible(weights, maxWeight, solution):
	return (weights * solution.reshape(-1, 1)).sum() <= maxWeight