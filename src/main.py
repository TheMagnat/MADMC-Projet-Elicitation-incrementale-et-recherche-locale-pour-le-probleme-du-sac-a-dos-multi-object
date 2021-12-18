

from helper import evaluate, feasible

from instanceGenerator import nonCorrelees, peuCorrelees, tresCorrelees

from aggregation import OWA

import numpy as np

n = 5
weights, values = tresCorrelees(n, 3, 5, factor=0.5)

#Exemple de façon pour génerer b
b = int(weights.sum()/2)


solution = np.array([0, 0, 1, 1, 0])

print(values.shape, solution.shape)
objectives = evaluate(values, solution)
feasible(weights, b, solution)

aggregationWeights = [0.3, 0.5, 0.2]

print( objectives )

print( OWA(objectives, aggregationWeights) )
