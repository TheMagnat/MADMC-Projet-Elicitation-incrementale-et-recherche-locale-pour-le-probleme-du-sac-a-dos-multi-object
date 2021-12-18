

def evaluate(values, solution):
	return (values * solution).sum(axis=1)

def feasible(weights, maxWeight, solution):
	return (weights * solution).sum() <= maxWeight