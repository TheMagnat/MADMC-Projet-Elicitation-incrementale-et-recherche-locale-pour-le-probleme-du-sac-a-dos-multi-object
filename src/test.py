
from InstanceLoader import readInstance

from PLS.PLS import PLS
from PLS.AlgorithmHelper import Update, Population, Neighborhood
from PLS.AlgorithmHelper import convertPopulationToFront, reduceObjects

from decision import incrementalElicitation, simulatedIncrementalElicitation, simulatedRandomIncrementalElicitation


from helper import evaluate, feasible
from instanceGenerator import nonCorrelees, peuCorrelees, tresCorrelees
from aggregation import OWA

import numpy as np

class Test:

	path = "../instances/2KP200-TA-0"

	def generateInstances():
		n = 5 #Nb objects
		weights, values = tresCorrelees(n, 3, maxValue=5, factor=0.5)

		#Exemple de façon pour génerer b
		b = int(weights.sum()/2)

		solution = np.array([0, 0, 1, 1, 0])

		objectives = evaluate(values, solution)
		feasible(weights, b, solution)

		aggregationWeights = [0.3, 0.5, 0.2]

		print("Objective space:", objectives)

		print("OWA Value:", OWA(objectives, aggregationWeights) )


	def PLS():

		objectsWeights, objectsValues, W = readInstance(Test.path+".dat")
		#optFront = notDominated(Test.path+'.eff')

		#We reduce data size
		objectsWeights, objectsValues, W = reduceObjects(objectsWeights, objectsValues, W, factor=0.1, generateW=True)

		#Quad-Tree version
		#solver = PLS(objectsWeights, objectsValues, W, Population.randomOnePopulation, Neighborhood.exchangeOneAndFillNeighborhood, Update.updateFrontQuad)

		#List version
		solver = PLS(objectsWeights, objectsValues, W, Population.randomOnePopulation, Neighborhood.exchangeOneAndFillNeighborhood, Update.updateFrontList)


		#eff, elapsedTime = solver.runQuad(verbose=1)
		eff, elapsedTime = solver.runList(verbose=1)

		print("Elapsed time:", elapsedTime, "sec")

	def incrementalElicitation():

		objectsWeights, objectsValues, W = readInstance(Test.path+".dat")

		#We reduce data size
		objectsWeights, objectsValues, W = reduceObjects(objectsWeights, objectsValues, W, factor=0.055, generateW=True)


		solver = PLS(objectsWeights, objectsValues, W, Population.randomOnePopulation, Neighborhood.exchangeOneAndFillNeighborhood, Update.updateFrontList)

		eff, elapsedTime = solver.runList(verbose=0)

		front = convertPopulationToFront(eff, eff[0][1].shape[0])


		finalBestSolution, questionCount = incrementalElicitation(front)

		print(f"Best solution is n°{finalBestSolution}: {front[finalBestSolution]}")


	def simulatedRandomIncrementalElicitation():

		objectsWeights, objectsValues, W = readInstance(Test.path+".dat")

		#We reduce data size
		objectsWeights, objectsValues, W = reduceObjects(objectsWeights, objectsValues, W, nbCriteria=6, factor=0.055, generateW=True)

		print(f"PLS exécuté sur {objectsValues.shape[0]} objets.")

		solver = PLS(objectsWeights, objectsValues, W, Population.randomOnePopulation, Neighborhood.exchangeOneAndFillNeighborhood, Update.updateFrontList)

		eff, elapsedTime = solver.runList(verbose=0)

		front = convertPopulationToFront(eff, eff[0][1].shape[0])


		finalBestSolution, questionCount, unknownWeights = simulatedRandomIncrementalElicitation(front, verbose=1)

		print(f"Best solution is n°{finalBestSolution}: {front[finalBestSolution]}")
		print(f"Note: Weights used for decision are {unknownWeights}")
		print(f"{questionCount} questions posées pour {front.shape[0]} solutions.")


	def PLSwithElicitation():

		objectsWeights, objectsValues, W = readInstance(Test.path+".dat")

		#We reduce data size
		objectsWeights, objectsValues, W = reduceObjects(objectsWeights, objectsValues, W, factor=0.1, generateW=True)

		#List version
		solver = PLS(objectsWeights, objectsValues, W, Population.randomOnePopulation, Neighborhood.exchangeOneAndFillNeighborhood, Update.updateFrontList)


		unknownWeights = np.random.random(objectsValues.shape[1])
		unknownWeights = unknownWeights/unknownWeights.sum()


		selectedSolution, elapsedTime, questionCount = solver.runSelection(selector=simulatedIncrementalElicitation, selectorArgs=[unknownWeights], verbose=1)

		print(f"Best solution is: {selectedSolution[1]}")
		print(f"Object array: {selectedSolution[0]}")
		print(f"Obtened with {questionCount} questions.")
		print("Elapsed time:", round(elapsedTime, 3), "sec")
