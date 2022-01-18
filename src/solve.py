
from pulp import LpMaximize, LpProblem, lpSum, LpVariable


def LP_OWA(objectsWeights, objectsValues, W, weight):
	"""
	Find the weights for OWA with x predered from y

	Si positif:
		x possiblement préféré à y

	Si nul:
		x est possiblement autant préféré que y

	Si négatif:
		x est tout le temps préféré à y
	"""

	#Number of variables
	n = objectsValues.shape[1]
	m = objectsValues.shape[0]



	model = LpProblem(name="OWA", sense=LpMaximize)



	#

	z = [LpVariable(name=f'z_{i}', lowBound=0) for i in range(n)]

"""
	for i in range(n-1):
		#Contrainte 2
		model += (w[i] >= w[i+1], f"constraint_2(w {i} and {i+1})")


	model += (lpSum(w) == 1,  "constraint_3")


	#const4
	for a, b in prefs:
		sA = np.sort(a) #a
		sB = np.sort(b) #b

		model += (lpSum([w[i] * sA[i] for i in range(n)]) >= lpSum([w[i] * sB[i] for i in range(n)]))

	#Objective
	model += lpSum([w[i] * y[i] for i in range(n)]) - lpSum([w[i] * x[i] for i in range(n)])


	model.solve()

	return model.objective.value(), model.status == 1

"""