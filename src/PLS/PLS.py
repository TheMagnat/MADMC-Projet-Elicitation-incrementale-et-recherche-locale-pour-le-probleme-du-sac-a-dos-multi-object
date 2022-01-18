import time

from PLS.QuadTree import QuadTree
from PLS.AlgorithmHelper import convertPopulationToFront


from copy import deepcopy


class PLS:


	#Problem parameters and functions
	def __init__(self, objectsWeights, objectsValues, W, populationGenerator, neighborhoodGenerator, updateFunction):

		self.objectsWeights = objectsWeights
		self.objectsValues = objectsValues
		self.W = W

		self.nbCriteria = objectsValues.shape[1]

		self.populationGenerator = populationGenerator
		self.neighborhoodGenerator = neighborhoodGenerator
		self.updateFunction = updateFunction


	def runQuad(self, verbose=0):


		startTime = time.time()


		initialPopulation = self.populationGenerator(self.objectsWeights, self.objectsValues, self.W)

		initialPopQuad = QuadTree(self.nbCriteria)
		initialPopQuad.bulkInsert(initialPopulation)



		population = deepcopy(initialPopQuad)
		efficaces = deepcopy(initialPopQuad)

		Pa = QuadTree(self.nbCriteria)

		it = 0
		while population:

			if verbose == 1:
				print(f"Taille de nouvelle population au temps {it}: {len(population)}")

			for solution in population:

				for voisin in self.neighborhoodGenerator(solution, self.objectsWeights, self.objectsValues, self.W):
					#If voisin is not dominated by solution
					if any(solution[1] < voisin[1]):

						if self.updateFunction(efficaces, voisin):
							self.updateFunction(Pa, voisin)


			population = Pa

			Pa = QuadTree(self.nbCriteria)

			it += 1

		return efficaces, time.time() - startTime


	def runList(self, verbose=0):

		startTime = time.time()


		initialPopulation = self.populationGenerator(self.objectsWeights, self.objectsValues, self.W)

		population = initialPopulation.copy()
		efficaces = initialPopulation.copy()

		Pa = []

		it = 0
		while population:

			if verbose == 1:
				print(f"Taille de nouvelle population au temps {it}: {len(population)}")

			for solution in population:

				for voisin in self.neighborhoodGenerator(solution, self.objectsWeights, self.objectsValues, self.W):
					#If voisin is not dominated by solution
					if not all(solution[1] >= voisin[1]):

						if self.updateFunction(efficaces, voisin):
							self.updateFunction(Pa, voisin)

			population = Pa

			Pa = []

			it += 1

		return efficaces, time.time() - startTime

	def runSelection(self, selector, selectorArgs=[], verbose=0):

		startTime = time.time()


		initialPopulation = self.populationGenerator(self.objectsWeights, self.objectsValues, self.W)

		tempoFront = convertPopulationToFront(initialPopulation, self.nbCriteria)

		currentSolutionIndex = selector(tempoFront, *selectorArgs)[0]
		currentSolution = initialPopulation[currentSolutionIndex]

		it = 0

		totalSelectorIt = 0

		while True:

			if verbose == 1:
				pass
				#print(f"Taille de nouvelle population au temps {it}: {len(population)}")

			currentPopulation = [currentSolution] + self.neighborhoodGenerator(currentSolution, self.objectsWeights, self.objectsValues, self.W)

			tempoFront = convertPopulationToFront(currentPopulation, self.nbCriteria)

			currentSolutionIndex, nbSelectorIt = selector(tempoFront, *selectorArgs)

			totalSelectorIt += nbSelectorIt

			if verbose == 1:
				print(f"Selected solution n°{currentSolutionIndex}: {currentPopulation[currentSolutionIndex][1]}")

			#If currentSolutionIndex equal 0, parent is selected
			if currentSolutionIndex == 0:

				if verbose == 1:
					print(f"Solution séléctionné en {it} itérations.")

				return currentSolution, time.time() - startTime, totalSelectorIt

			currentSolution = currentPopulation[currentSolutionIndex]

			it += 1

		


