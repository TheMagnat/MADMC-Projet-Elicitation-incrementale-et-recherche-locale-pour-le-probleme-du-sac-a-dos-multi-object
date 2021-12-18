

from helper import evaluate, feasible

from instanceGenerator import nonCorrelees, peuCorrelees, tresCorrelees

n = 5
weights, values = tresCorrelees(n, 3, 5, factor=0.5)

#Exemple de façon pour génerer b
b = int(weights.sum()/2)


solution = [0, 0, 1, 1, 0]


evaluate(values, solution)
feasible(weights, b, solution)
