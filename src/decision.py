
import numpy as np

from scipy import optimize

from pulp import LpMaximize, LpProblem, lpSum, LpVariable
from tqdm import tqdm

from aggregation import OWA

#Avec pulp
def PMR_OWA(x, y, prefs):
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
	n = x.shape[0]

	x.sort()
	y.sort()


	model = LpProblem(name="OWA", sense=LpMaximize)

	w = [LpVariable(name=f'w_{i}', lowBound=0) for i in range(n)]


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

	# print(f"status: {model.status}, {LpStatus[model.status]}")
	# print(f"objective: {model.objective.value()}")

	return model.objective.value(), model.status == 1



#Avec scipy
def PMR_OWA_Scipy(x, y, prefs):
	"""
	Find the weights for OWA with x predered from y
	"""

	#Number of variables
	n = x.shape[0]

	x.sort()
	y.sort()

	c = y - x

	A = []
	b = []

	for i in range(n):
		#Contrainte 1
		const1 = [0] * n
		const1[i] = -1 #Note: Tout * -1 pour faire inférieur à

		A.append(const1)
		b.append(0)

		#Contrainte 2
		if i < n - 1:
			const2 = const1.copy()
			const2[i+1] = 1

			A.append(const2)
			b.append(0)



	const3 = [1] * n
	A_eq = [const3]
	b_eq = [1]


	#const4
	for first, second in prefs:
		sFirst = np.sort(first) #a
		sSecond = np.sort(second) #b

		const4 = -(sFirst - sSecond) # "-" Pour faire inférieur à 0

		A.append(const4)
		b.append(0)


	# print(c)
	# print(A)
	# print(b)

	# print(A_eq)
	# print(b_eq)


	res = optimize.linprog(
	    c = -c, 
	    A_ub = A, 
	    b_ub = b,

	    A_eq=A_eq,
	    b_eq=b_eq,
	)

	return -round(res.fun, 5), res.success


def MR(x, front, prefs):
	"""
	The Max Regret
	
	MMR(x, front, prefs) = max_y PMR(x, y, prefs)

	return:
		y index and PMR(x, y, prefs)

	"""

	nbSolutions = front.shape[0]

	maxValue = float('-inf')
	maxIndex = -1

	for yIndex in range(nbSolutions):

		if yIndex == x:
			continue

		value, success = PMR_OWA(front[x], front[yIndex], prefs)
		if not success:
			continue

		if value > maxValue:
			maxValue = value
			maxIndex = yIndex


	return maxIndex, maxValue


def MMR(front, prefs):
	"""
	The Minimax Regret
	
	MMR(front, prefs) = min_x MR(x, front, prefs)
	
	return:
		x index, y index (wich maximise the PMR) and PMR(x, y, prefs)

	"""

	nbSolutions = front.shape[0]

	minValue = float('inf')
	minXindex = -1
	minYindex = -1

	for xIndex in tqdm(range(nbSolutions)):

		yIndex, yValue = MR(xIndex, front, prefs)

		#May be useless
		if yIndex == -1:
			continue

		if yValue < minValue:
			minValue = yValue
			minXindex = xIndex
			minYindex = yIndex


	return minXindex, minYindex, minValue


def WMMR(front, pair, prefs):
	"""
	To heavy to be used.
	"""

	x1, y1, minValue1 = MMR(front, prefs + [(pair[0], pair[1])])
	x2, y2, minValue2 = MMR(front, prefs + [(pair[1], pair[0])])

	if minValue1 > minValue2:
		return x1, y1, minValue1
	else:
		return x2, y2, minValue2


def CSS(front, prefs):
	"""
	Heuristic "Current Solution Strategy"
	"""
	x, y, value = MMR(front, prefs)

	return x, y, round(value, 2)


def randomChoice(front, prefs):
	rng = np.random.default_rng()

	nbSolutions = front.shape[0]
	selected = rng.choice(nbSolutions, 2, replace=False)
	return selected[0], selected[1]


def incrementalElicitation(front, verbose=0):

	prefs = []

	oldSelected = None

	questionCount = 0

	while True:

		x, y, value = CSS(front, prefs)

		if verbose > 0:
			print(f"Valeur du regret minimax: {value}")

		if value == 0:
			return x, questionCount

		elif x == -1 or y == -1:
			return oldSelected, questionCount

		solutions = [front[x], front[y]]

		print(f"0: {solutions[0]} (Solution n°{x})")
		print(f"1: {solutions[1]} (Solution n°{y})")

		try:
			selected = int(input("Select 0 or 1: "))

			assert( selected == 0 or selected == 1 )

		except ValueError:
			print("Not an integer value.")

		except AssertionError:
			print(selected, "is not 0 or 1.")

		else:

			questionCount += 1

			oldSelected = x * (1 - selected) + y * selected

			notSelected = 1 - selected

			#Tout les ensemble de poids tel que f(rez[selected]) > f(rez[notSelected])
			prefs.append( (solutions[selected], solutions[notSelected]) )


"""Exemple d'éxécution:

100%|█████████████████████████████████████████████████████████████████████████████████████████████████████| 121/121 [02:35<00:00,  1.29s/it]
0: [3545 3678 3908 4216 4240 5053] (Solution n°101)
1: [2663 4134 4142 4815 4844 5309] (Solution n°32)
Select 0 or 1: 0
100%|█████████████████████████████████████████████████████████████████████████████████████████████████████| 121/121 [02:29<00:00,  1.24s/it]
0: [3571 3813 3840 4101 4471 4524] (Solution n°8)
1: [2751 4181 4269 4516 4892 5063] (Solution n°31)
Select 0 or 1: 0
100%|█████████████████████████████████████████████████████████████████████████████████████████████████████| 121/121 [02:24<00:00,  1.20s/it]
0: [3571 3813 3840 4101 4471 4524] (Solution n°8)
1: [3545 3678 3908 4216 4240 5053] (Solution n°101)
Select 0 or 1: 0
100%|█████████████████████████████████████████████████████████████████████████████████████████████████████| 121/121 [02:35<00:00,  1.29s/it]
0: [3571 3813 3840 4101 4471 4524] (Solution n°8)
1: [3168 4015 4082 4238 4260 4582] (Solution n°6)
Select 0 or 1: 0
100%|█████████████████████████████████████████████████████████████████████████████████████████████████████| 121/121 [02:38<00:00,  1.31s/it]
8: [3571 3813 3840 4101 4471 4524]

"""

def simulatedRandomIncrementalElicitation(front, verbose=0):

	unknownWeights = np.random.random(front.shape[1])
	unknownWeights = unknownWeights/unknownWeights.sum()

	return simulatedIncrementalElicitation(front, unknownWeights, verbose)


def simulatedIncrementalElicitation(front, unknownWeights, verbose=0):

	prefs = []

	oldSelected = None

	questionCount = 0

	while True:

		x, y, value = CSS(front, prefs)

		if verbose > 0:
			print(f"Valeur du regret minimax: {value}")

		if value == 0:
			return x, questionCount, unknownWeights

		elif x == -1 or y == -1:
			return oldSelected, questionCount, unknownWeights

		solutions = [front[x], front[y]]

		print(f"0: {solutions[0]} (Solution n°{x})")
		print(f"1: {solutions[1]} (Solution n°{y})")

		selected = np.array([OWA(solutions[0], unknownWeights), OWA(solutions[1], unknownWeights)]).argmax()
		
		oldSelected = x * (1 - selected) + y * selected

		print(f"{selected} selected (Solution n°{oldSelected}).")

		questionCount += 1

		notSelected = 1 - selected

		#Tout les ensemble de poids tel que f(rez[selected]) > f(rez[notSelected])
		prefs.append( (solutions[selected], solutions[notSelected]) )



