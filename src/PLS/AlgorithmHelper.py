
import random

import numpy as np

from PLS.QuadTree import QuadTree


# Helper functions #

"""
Fill a solution with random objects that can unter in it
"""
def fillRandom(solution, currentSize, objectsWeights, objectsValues, W):

	indexes = list(np.argwhere(solution == 0).ravel())

	random.shuffle(indexes)

	while currentSize < W and indexes:

		for i in range(len(indexes)):

			choice = indexes[i]

			end = True
			if currentSize + objectsWeights[choice] < W:
				solution[choice] = 1
				currentSize += objectsWeights[choice]

				#Remove index choice from possible indexes
				indexes.pop(i)
				end = False

				break

		#No item can enter
		if end:
			break

	return (solution, (objectsValues * solution.reshape(-1, 1)).sum(axis=0))

"""
Convert a population to an array of size (n, 2) of points representing the pareto front
"""
def convertPopulationToFront(population, nbCriteria):

	front = np.empty((len(population), nbCriteria), dtype=int)

	for i, elem in enumerate(population):
		front[i] = elem[1]

	return front


def reduceObjects(objectsWeights, objectsValues, W, nbCriteria=None, factor=0.5, generateW=False):

	if nbCriteria is None:
		nbCriteria = objectsValues.shape[1]

	newSize = int(objectsWeights.shape[0] * factor)

	rng = np.random.default_rng()
	choices = rng.choice(objectsWeights.shape[0], size=newSize, replace=False)

	criteriaChoices = rng.choice(objectsValues.shape[1], size=nbCriteria, replace=False)

	newObjectsWeights = objectsWeights[choices]
	newObjectsValues = objectsValues[choices][:, criteriaChoices]

	newW = W * factor
	if generateW:
		newW = newObjectsWeights.sum()/2

	return newObjectsWeights, newObjectsValues, newW
	

class Population:

	"""
	Return a tuple:
		(solution, (goal1, goal2))

	"""
	@staticmethod
	def randomOnePopulation(objectsWeights, objectsValues, W):

		indexes = list(range(objectsWeights.shape[0]))
		random.shuffle(indexes)

		currentSize = 0
		solution = np.zeros(objectsWeights.shape[0], dtype=int)

		while currentSize < W and indexes:

			for i in range(len(indexes)):

				choice = indexes[i]

				end = True
				if currentSize + objectsWeights[choice] < W:
					solution[choice] = 1
					currentSize += objectsWeights[choice]

					#Remove index choice from possible indexes
					indexes.pop(i)
					end = False

					break

			#No item can enter
			if end:
				break

		return [( solution, (objectsValues * solution.reshape(-1, 1)).sum(axis=0) )]


class Neighborhood:

	@staticmethod
	def exchangeOneAndFillNeighborhood(solution, objectsWeights, objectsValues, W):

		allVois = []

		for i, elem1 in enumerate(solution[0]):

			#Only if object is in the solution
			if elem1 == 1:

				for j, elem0 in enumerate(solution[0]):

					if elem0 == 0:

						solution[0][i] = 0
						solution[0][j] = 1

						currentSize = objectsWeights[solution[0] == 1].sum()

						if currentSize < W:
							newSolution = solution[0].copy()

							newSolution = fillRandom(newSolution, currentSize, objectsWeights, objectsValues, W)

							allVois.append(newSolution)

						#Put back values
						solution[0][i] = 1
						solution[0][j] = 0


		return allVois



class Update:

	@staticmethod
	def updateFrontList(front, solution):

		toRemoveIndex = []
		for i, (sol, objectives) in enumerate(front):

			#Solution is better than i
			if all(objectives < solution[1]):
				toRemoveIndex.append(i)

			#i is better or equal than solution
			elif all(objectives >= solution[1]):

				#print( objectives, "Beaten by", solution[1] )

				return False

		for i in sorted(toRemoveIndex, reverse=True):
			del front[i]

		front.append(solution)

		return True

	def updateFrontQuad(front, solution):
		return front.insert( solution[1], solution[0] )

