import time

class PLS:


	#Problem parameters and functions
	def __init__(self, objectsWeights, objectsValues, W, populationGenerator, neighborhoodGenerator, updateFunction):

		self.objectsWeights = objectsWeights
		self.objectsValues = objectsValues
		self.W = W

		self.populationGenerator = populationGenerator
		self.neighborhoodGenerator = neighborhoodGenerator
		self.updateFunction = updateFunction


	def run(self, verbose=0):


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
					#if solution[1][0] < voisin[1][0] or solution[1][1] < voisin[1][1]:

						if self.updateFunction(efficaces, voisin):
							self.updateFunction(Pa, voisin)

			population = Pa

			Pa = []

			it += 1

		return efficaces, time.time() - startTime



