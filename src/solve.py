
from pulp import LpMaximize, LpProblem, lpSum, LpVariable, LpSolverDefault
from itertools import combinations, permutations

def LP_OWA(objectsWeights, objectsValues, W, weight):
	"""
	Find best solution with OWA at given weight (Only work with decreasing weights)
	"""

	#Number of variables
	n = objectsValues.shape[1] #Objectifs
	m = objectsValues.shape[0] #Objets


	model = LpProblem(name="OWA", sense=LpMaximize)



	#
	x = [LpVariable(name=f'x_{j}', cat='Binary') for j in range(m)] #Si on prend l'objet j ou non
	y = [LpVariable(name=f'y_{i}', lowBound=0) for i in range(n)] #Valeur sur l'objectif i

	z = LpVariable(name='z', lowBound=0)
	

	#Contrainte de poid sur x
	model += (lpSum([x[j] * objectsWeights[j] for j in range(m)]) <= W, "Contrainte de poid")

	#Lier y avec x
	for i in range(n):
		model += (y[i] == lpSum([x[j] * objectsValues[j, i] for j in range(m)]), f"Lier y et x n°{i}")

	#permutations
	for count, combination in enumerate(permutations(range(n))):
		model += (z <= lpSum([y[i] * weight[index] for i, index in enumerate(combination)]), f"Lier z et y n°{count}")


	#Objective
	model += z

	#LpSolverDefault.msg = 1
	model.solve()

	# print(model)

	# for j, solox in enumerate(x):
	# 	print(f"x_{j}:", solox.varValue)


	# for i, soloy in enumerate(y):
	# 	print(f"y_{i}:",soloy.varValue)

	# print("z:", z.varValue)

	return model.objective.value(), model.status == 1


def LP_WS(objectsWeights, objectsValues, W, weight):
	"""
	Find best solution with WS at given weight
	"""

	#Number of variables
	n = objectsValues.shape[1] #Objectifs
	m = objectsValues.shape[0] #Objets


	model = LpProblem(name="WS", sense=LpMaximize)



	#
	x = [LpVariable(name=f'x_{j}', cat='Binary') for j in range(m)] #Si on prend l'objet j ou non
	y = [LpVariable(name=f'y_{i}', lowBound=0) for i in range(n)] #Valeur sur l'objectif i
	

	#Contrainte de poid sur x
	model += (lpSum([x[j] * objectsWeights[j] for j in range(m)]) <= W, "Contrainte de poid")

	#Lier y avec x
	for i in range(n):
		model += (y[i] == lpSum([x[j] * objectsValues[j, i] for j in range(m)]), f"Lier y et x n°{i}")


	#Objective
	model += lpSum([y[i] * weight[i] for i in range(n)])

	#LpSolverDefault.msg = 1
	model.solve()

	return model.objective.value(), model.status == 1



def LP_OWA_old(objectsWeights, objectsValues, W, weight):
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
	n = objectsValues.shape[1] #Objectifs
	m = objectsValues.shape[0] #Objets


	model = LpProblem(name="OWA", sense=LpMaximize)



	#
	x = [LpVariable(name=f'x_{j}', cat='Binary') for j in range(m)] #Si on prend l'objet j ou non
	y = [LpVariable(name=f'y_{i}', lowBound=0) for i in range(n)] #Valeur sur l'objectif i
	z = [LpVariable(name=f'z_{i}', lowBound=0) for i in range(n)] #Valeur sur l'objectif trié i
	

	#Contrainte de poid sur x
	model += (lpSum([x[j] * objectsWeights[j] for j in range(m)]) <= W, "Contrainte de poid")

	#Lier y avec x
	for i in range(n):
		model += (y[i] == lpSum([x[j] * objectsValues[j, i] for j in range(m)]), f"Lier y et x n°{i}")


	#Lier z avec y
	for k in range(1, n+1):

		#combinations
		for count, combination in enumerate(combinations(range(n), k)):
			model += (lpSum([z[i] for i in range(k)]) <= lpSum([y[index] for index in combination]), f"Lier z et y n°{k}, combinaison n°{count}")


	#Objective
	model += lpSum([z[i] * weight[i] for i in range(n)])

	#LpSolverDefault.msg = 1
	model.solve()

	# print(model)

	# for j, solox in enumerate(x):
	# 	print(f"x_{j}:", solox.varValue)


	# for i, soloy in enumerate(y):
	# 	print(f"y_{i}:",soloy.varValue)

	# for i, soloy in enumerate(z):
	# 	print(f"z_{i}:",soloy.varValue)

	return model.objective.value(), model.status == 1
