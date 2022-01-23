
import numpy as np

from scipy import optimize

from pulp import LpMaximize, LpProblem, lpSum, LpVariable
from tqdm import tqdm

from aggregation import OWA, weightedSum

#Avec pulp
def PMR_OWA(x, y, prefs):
	"""
	Find the worst weights for OWA that maximize OWA(y) - OWA(x)

	Si positif:
		x possiblement préféré à y

	Si nul:
		x est possiblement autant préféré que y

	Si négatif:
		x est tout le temps préféré à y
	"""

	#Number of variables
	n = x.shape[0]

	sortedX = np.sort(x)
	sortedY = np.sort(y)


	model = LpProblem(name="PMR_OWA", sense=LpMaximize)

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
	model += lpSum([w[i] * sortedY[i] for i in range(n)]) - lpSum([w[i] * sortedX[i] for i in range(n)])


	model.solve()

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


	res = optimize.linprog(
	    c = -c,
	    A_ub = A,
	    b_ub = b,

	    A_eq=A_eq,
	    b_eq=b_eq,
	)

	return -round(res.fun, 5), res.success


#Avec pulp
def PMR_WS(x, y, prefs):
	"""
	Find the worst weights for OWA that maximize WS(y) - WS(x)

	Si positif:
		x possiblement préféré à y

	Si nul:
		x est possiblement autant préféré que y

	Si négatif:
		x est tout le temps préféré à y
	"""

	#Number of variables
	n = x.shape[0]


	model = LpProblem(name="PMR_OWA", sense=LpMaximize)

	w = [LpVariable(name=f'w_{i}', lowBound=0) for i in range(n)]


	model += (lpSum(w) == 1,  "constraint_3")


	#const4
	for a, b in prefs:
		model += (lpSum([w[i] * a[i] for i in range(n)]) >= lpSum([w[i] * b[i] for i in range(n)]))

	#Objective
	model += lpSum([w[i] * y[i] for i in range(n)]) - lpSum([w[i] * x[i] for i in range(n)])


	model.solve()

	return model.objective.value(), model.status == 1

### Code inachevé, merci d'ignorer
def PMR_Choquet(x, y, prefs):
	"""
	Si positif:
		x possiblement préféré à y

	Si nul:
		x est possiblement autant préféré que y

	Si négatif:
		x est tout le temps préféré à y
	"""

	#Number of variables
	n = x.shape[0]
	xcopy=x.copy()
	xcopy[::-1].sort()
	listX=[np.where(x==xcopy[0])[0]]
	ycopy=y.copy()
	ycopy[::-1].sort()
	listY=[np.where(y==ycopy[0])[0]]

	for i in range(1,len(x)-1):

		listX=listX+[np.concatenate((listX[i-1],np.where(x==xcopy[i] )[0]))]

		listY=listY+[np.concatenate((listY[i-1],np.where(y==ycopy[i] )[0]))]
	strListX=[]
	strListY=[]

	for i in range(0,len(x)-1):
		strListX +=[str(np.sort(listX[i]))]
		strListY +=[str(np.sort(listY[i]))]
	v=dict()
	l=dict()
	u=dict()
	allSets=np.union1d(strListX,strListY)
	for i in range(len(allSets)):
		v[allSets[i]]=LpVariable(name=f'v_{allSets[i]}', lowBound=0,upBound=1)
		l[allSets[i]]=LpVariable(name=f'u_{allSets[i]}', lowBound=0,upBound=1)
		u[allSets[i]]=LpVariable(name=f'l_{allSets[i]}', lowBound=0,upBound=1)
	model = LpProblem(name="Choquet", sense=LpMaximize)
	for i in range(n-2):
		#contrainte 10/11
		model += (v[strListX[i]]<=v[strListX[i+1]], f"constraint_10(v {strListX[i]} and {strListX[i+1]}")
		model += (v[strListY[i]]<=v[strListY[i+1]], f"constraint_11(v {strListY[i]} and {strListY[i+1]}")

	for i in range(n-1):
		#contrainte 14/15
		model += (v[strListX[i]]<=l[strListX[i]], f"constraint_14(v {strListX[i]} and l {strListX[i]}")
		model += (u[strListX[i]]<=v[strListX[i]], f"constraint_14(u {strListX[i]} and v {strListX[i]}")
		model += (v[strListY[i]]<=l[strListY[i]], f"constraint_15(v {strListY[i]} and l {strListY[i]}")
		model += (u[strListY[i]]<=v[strListY[i]], f"constraint_15(u {strListY[i]} and v {strListY[i]}")
	for i in range(len(listX)):
		for j in range(len(listY)):
			if(len(listX[i])<len(listY[j])):
				if( all(a in listX[i] for a in listY[j]) ):
					#contrainte 12
					model += (v[strListX[i]]<=v[strListY[j]], f"constraint_12(v {i} and v{j}")

			if(len(listY[j])<len(listX[i])):
				if(all(a in listY[j] for a in listX[i]) ):
					#contrainte 13
					model += (v[strListY[j]]<=v[strListX[i]], f"constraint_13(v {j} and v{i}")


	#Objective
	x.sort()
	sumX=[v[strListX[-1]]*x[0]]+[v[strListX[-i-1]]*(x[i]-x[i-1]) for i in range(1,len(strListX))]
	y.sort()
	sumY=[v[strListY[-1]]*y[0]]+[v[strListY[-i-1]]*(y[i]-y[i-1]) for i in range(1,len(strListY))]
	model += lpSum([sumY]) - lpSum([sumX])

	model.solve()

	return model.objective.value(), model.status == 1


def MR(x, front, prefs, mode="OWA"):
	"""
	The Max Regret

	MMR(x, front, prefs) = max_y PMR(x, y, prefs)

	return:
		y index and PMR(x, y, prefs)

	"""

	if mode == "WS":
		PMR_func = PMR_WS
	elif mode == "Choquet":
		PMR_func = PMR_Choquet
	else:
		PMR_func = PMR_OWA


	nbSolutions = front.shape[0]

	maxValue = float('-inf')
	maxIndex = -1

	for yIndex in range(nbSolutions):

		if yIndex == x:
			continue


		value, success = PMR_func(front[x], front[yIndex], prefs)

		if not success:
			continue

		if value > maxValue:
			maxValue = value
			maxIndex = yIndex


	return maxIndex, maxValue


def MMR(front, prefs, mode="OWA", verbose=0):
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

	for xIndex in tqdm(range(nbSolutions), disable=(verbose == 0)):

		yIndex, yValue = MR(xIndex, front, prefs, mode)

		#May be useless
		if yIndex == -1:
			continue

		if yValue < minValue:
			minValue = yValue
			minXindex = xIndex
			minYindex = yIndex

	return minXindex, minYindex, minValue


def WMMR(front, pair, prefs, mode="OWA"):
	"""
	To heavy to be used.
	"""

	x1, y1, minValue1 = MMR(front, prefs + [(pair[0], pair[1])], mode)
	x2, y2, minValue2 = MMR(front, prefs + [(pair[1], pair[0])], mode)

	if minValue1 > minValue2:
		return x1, y1, minValue1
	else:
		return x2, y2, minValue2


def CSS(front, prefs, mode="OWA", verbose=0):
	"""
	Heuristic "Current Solution Strategy"
	"""
	x, y, value = MMR(front, prefs, mode, verbose)

	return x, y, round(value, 2)


def randomChoice(front, prefs):
	rng = np.random.default_rng()

	nbSolutions = front.shape[0]
	selected = rng.choice(nbSolutions, 2, replace=False)
	return selected[0], selected[1]


def incrementalElicitation(front, verbose=0):

	prefs = []

	if front.shape[0] == 1:
		return 0, 0, prefs

	oldSelected = None

	questionCount = 0

	while True:

		x, y, value = CSS(front, prefs, verbose=1)

		if verbose > 0:
			print(f"Valeur du regret minimax: {value}")

		if value <= 0:
			return x, questionCount, prefs

		elif x == -1 or y == -1:
			return oldSelected, questionCount, prefs

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

def simulatedRandomIncrementalElicitation(front, mode="OWA", verbose=0):

	unknownWeights = np.random.random(front.shape[1])
	unknownWeights = np.sort(unknownWeights/unknownWeights.sum())[::-1]

	return *simulatedIncrementalElicitation(front, unknownWeights, mode=mode, verbose=verbose), unknownWeights


def simulatedIncrementalElicitation(front, unknownWeights, prefs=None, mode="OWA", verbose=0, save=None):

	if prefs is None:
		prefs = []

	if front.shape[0] == 1:
		return 0, 0, prefs

	if mode == "WS":
		aggregator = weightedSum
	elif mode == "Choquet":
		pass
		###ICI Rajouter choquet dans aggregation.py
		#aggregator = choquet
	else:
		aggregator = OWA

	oldSelected = None

	questionCount = 0

	while True:

		x, y, value = CSS(front, prefs, mode, verbose)

		if save is not None:
			save.append([questionCount, value])

		if verbose > 1:
			print(f"Valeur du regret minimax: {value}")

		if value <= 0:
			return x, questionCount, prefs

		elif x == -1 or y == -1:
			return oldSelected, questionCount, prefs

		solutions = [front[x], front[y]]

		if verbose > 0:
			print(f"0: {solutions[0]} (Solution n°{x})")
			print(f"1: {solutions[1]} (Solution n°{y})")

		selected = np.array([aggregator(solutions[0], unknownWeights), aggregator(solutions[1], unknownWeights)]).argmax()
		
		oldSelected = x * (1 - selected) + y * selected

		if verbose > 0:
			print(f"{selected} selected (Solution n°{oldSelected}).")

		questionCount += 1

		notSelected = 1 - selected

		#Tout les ensemble de poids tel que f(rez[selected]) > f(rez[notSelected])
		prefs.append( (solutions[selected], solutions[notSelected]) )
