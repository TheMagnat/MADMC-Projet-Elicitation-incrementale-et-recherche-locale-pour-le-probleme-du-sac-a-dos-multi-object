
import time

from InstanceLoader import readInstance

from PLS.PLS import PLS
from PLS.AlgorithmHelper import Update, Population, Neighborhood
from PLS.AlgorithmHelper import convertPopulationToFront, reduceObjects

from decision import incrementalElicitation, simulatedIncrementalElicitation, simulatedRandomIncrementalElicitation


from helper import evaluate, feasible
from instanceGenerator import nonCorrelees, peuCorrelees, tresCorrelees
from aggregation import OWA, weightedSum
from solve import LP_OWA, LP_WS

import matplotlib.pyplot as plt

import numpy as np

class Test:

	path = "../instances/2KP200-TA-0"

	def generateInstances():
		n = 5 #Nb objectifs
		m = 5 #Nb objects
		weights, values = tresCorrelees(m, n, maxValue=5, factor=0.5)

		#Exemple de façon pour générer w
		w = int(weights.sum()/2)

		solution = np.array([0, 0, 1, 1, 0])

		objectives = evaluate(values, solution)
		feasible(weights, w, solution)

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


	def simulatedRandomIncrementalElicitation(mode="OWA"):

		objectsWeights, objectsValues, W = readInstance(Test.path+".dat")

		n = 3

		#We reduce data size
		objectsWeights, objectsValues, W = reduceObjects(objectsWeights, objectsValues, W, nbCriteria=n, factor=0.055, generateW=True)

		print(f"PLS exécuté sur {objectsValues.shape[0]} objets.")

		solver = PLS(objectsWeights, objectsValues, W, Population.randomOnePopulation, Neighborhood.exchangeOneAndFillNeighborhood, Update.updateFrontList)

		eff, elapsedTime = solver.runList(verbose=0)

		front = convertPopulationToFront(eff, eff[0][1].shape[0])


		finalBestSolution, questionCount, prefs, unknownWeights = simulatedRandomIncrementalElicitation(front, mode=mode, verbose=2)

		print(f"Best solution is n°{finalBestSolution}: {front[finalBestSolution]}")
		print(f"Note: Weights used for decision are {unknownWeights}")
		print(f"Decision maker preferences:")

		for a, b in prefs:
			print(f"{a} > {b}")

		print(f"{questionCount} questions posées pour {front.shape[0]} solutions.")


	def PLSwithElicitation(mode="OWA"):

		objectsWeights, objectsValues, W = readInstance(Test.path+".dat")

		n = 3

		#We reduce data size
		objectsWeights, objectsValues, W = reduceObjects(objectsWeights, objectsValues, W, nbCriteria=n, factor=0.1, generateW=True)

		#List version
		solver = PLS(objectsWeights, objectsValues, W, Population.randomOnePopulation, Neighborhood.exchangeOneAndFillNeighborhood, Update.updateFrontList)


		unknownWeights = np.random.random(objectsValues.shape[1])
		unknownWeights = np.sort(unknownWeights/unknownWeights.sum())[::-1]


		selectedSolution, elapsedTime, questionCount = solver.runSelection(selector=simulatedIncrementalElicitation, mode=mode, selectorArgs=[unknownWeights], verbose=1)

		print(f"Best solution is: {selectedSolution[1]}")
		print(f"Object array: {selectedSolution[0]}")
		print(f"Obtened with {questionCount} questions.")
		print("Elapsed time:", round(elapsedTime, 3), "sec")


	def LP_OWA():

		objectsWeights, objectsValues, W = readInstance(Test.path+".dat")


		n = 3

		#We reduce data size
		objectsWeights, objectsValues, W = reduceObjects(objectsWeights, objectsValues, W, nbCriteria=n, factor=0.055, generateW=True)

		m = objectsValues.shape[0]


		#objectsWeights = np.array([3, 2, 6, 4])
		#objectsValues = np.array([[2, 4], [1, 3], [8, 4], [5, 3]])
		#W = 10

		#weight = np.sort(np.array([0.1, 0.9]))[::-1]

		weight = np.random.random(n)
		weight = np.sort(weight/weight.sum())[::-1]


		#weight = np.sort(np.array([0.1, 0.9]))[::-1]

		rez, statue = LP_OWA(objectsWeights, objectsValues, W, weight)

		print(rez, statue)


	def compare():
		
		objectsWeights, objectsValues, W = readInstance(Test.path+".dat")

		n = 3

		#Génération d'une instance de problème :
		reducedObjectsWeights, reducedObjectsValues, W = reduceObjects(objectsWeights, objectsValues, W, nbCriteria=n, factor=0.1, generateW=True)

		unknownWeights = np.random.random(n)
		unknownWeights = np.sort(unknownWeights/unknownWeights.sum())[::-1]



		#Première procédure : PLS Puis Élicitation
		solver = PLS(reducedObjectsWeights, reducedObjectsValues, W, Population.randomOnePopulation, Neighborhood.exchangeOneAndFillNeighborhood, Update.updateFrontList)

		eff, elapsedTime = solver.runList(verbose=0)

		front = convertPopulationToFront(eff, eff[0][1].shape[0])

		startTime = time.time()
		finalBestSolution, questionCount, prefs = simulatedIncrementalElicitation(front, unknownWeights, verbose=0)
		totalTime = time.time() - startTime

		selectedBy1 = front[finalBestSolution]

		print(f"Best solution is n°{finalBestSolution}: {selectedBy1}")
		print(f"Note: Weights used for decision are {unknownWeights}")
		print(f"{questionCount} questions posées pour {front.shape[0]} solutions.")
		print("Elapsed time:", round(elapsedTime + totalTime, 3), "sec")


		#Seconde procédure : PLS Puis Élicitation
		selectedSolution, elapsedTime, questionCount = solver.runSelection(selector=simulatedIncrementalElicitation, selectorArgs=[unknownWeights], verbose=0)

		selectedBy2 = selectedSolution[1]

		print(f"Best solution is: {selectedBy2}")
		#print(f"Object array: {selectedSolution[0]}")
		print(f"Obtened with {questionCount} questions.")
		print("Elapsed time:", round(elapsedTime, 3), "sec")


		trueValue, statue = LP_OWA(reducedObjectsWeights, reducedObjectsValues, W, unknownWeights)

		firstValue = OWA(selectedBy1, unknownWeights)
		secondValue = OWA(selectedBy2, unknownWeights)

		print(round(firstValue, 2), round(trueValue/firstValue, 3))
		print(round(secondValue, 2), round(trueValue/secondValue, 3))
		print(round(trueValue, 2), statue)

	def generateLogs(nbIterations, mode="OWA"):

		objectsWeights, objectsValues, W = readInstance(Test.path+".dat")

		if mode == "WS":
			name = 'logs/solveLogsWS2.csv'
			LP_Aggregator = LP_WS
			aggregator = weightedSum
		else:
			name = 'logs/solveLogsOWA2.csv'
			LP_Aggregator = LP_OWA
			aggregator = OWA


		csvFile = open(name, 'a+')

		#Add this line if the file does not exist
		#csvFile.write('PLS_Puis_EI(1),questions(1),temps(1),PLS_ET_EI(2),questions(2),temps(2),Optimale\n')


		#Nb critères
		n = 3

		for i in range(nbIterations):

			#Génération d'une instance de problème :
			reducedObjectsWeights, reducedObjectsValues, W = reduceObjects(objectsWeights, objectsValues, W, nbCriteria=n, factor=0.1, generateW=True)

			unknownWeights = np.random.random(n)
			unknownWeights = np.sort(unknownWeights/unknownWeights.sum())[::-1]


			#Première procédure : PLS Puis Élicitation
			solver = PLS(reducedObjectsWeights, reducedObjectsValues, W, Population.randomOnePopulation, Neighborhood.exchangeOneAndFillNeighborhood, Update.updateFrontList)

			eff, elapsedTime = solver.runList(verbose=0)

			front = convertPopulationToFront(eff, eff[0][1].shape[0])

			#To save numbers of questions and score
			saved = []

			startTime = time.time()
			finalBestSolution, questionCount1, prefs = simulatedIncrementalElicitation(front, unknownWeights, mode=mode, verbose=1, save=saved)
			totalTime = time.time() - startTime

			time1 = round(elapsedTime + totalTime, 3)
			selectedBy1 = front[finalBestSolution]


			#Seconde procédure : PLS Puis Élicitation
			selectedSolution, elapsedTime, questionCount2 = solver.runSelection(selector=simulatedIncrementalElicitation, selectorArgs=[unknownWeights], mode=mode, verbose=1)

			selectedBy2 = selectedSolution[1]

			time2 = round(elapsedTime, 3)


			trueValue, statue = LP_Aggregator(reducedObjectsWeights, reducedObjectsValues, W, unknownWeights)

			firstValue = aggregator(selectedBy1, unknownWeights)
			secondValue = aggregator(selectedBy2, unknownWeights)

			csvFile.write(f'{round(firstValue, 2)},{questionCount1},{time1},{round(secondValue, 2)},{questionCount2},{time2},{round(trueValue, 2)}\n')


			if mode == "WS":
				name = f"logs/questionsLogsWS_{i+5}.csv"
			else:
				name = f"logs/questionsLogsOWA_{i+10}.csv"

			with open(name, 'w+') as csvFileQuestions:
				csvFileQuestions = open(name, 'w+')
				csvFileQuestions.write('questions,PMR\n')

				for save in saved:
					csvFileQuestions.write(f'{save[0]},{save[1]}\n')



		csvFile.close()

	def loadLogs(mode="OWA"):

		if mode == "WS":
			name = "logs/solveLogsWS2.csv"
		else:
			name = "logs/solveLogsOWA2.csv"


		data = np.genfromtxt(name, delimiter=',')[1:]
		
		data[:, 0] = data[:, 0] / data[:, 6]
		data[:, 3] = data[:, 3] / data[:, 6]

		np.set_printoptions(suppress=True)
		meanData = data.mean(axis=0)

		print(np.round(meanData, 4)[:-1])

	def generateQuestionsLogs(index=1, mode="OWA"):
		
		objectsWeights, objectsValues, W = readInstance(Test.path+".dat")

		n = 3

		if mode == "WS":
			name = f"logs/questionsLogsWS_{index}.csv"
		else:
			name = f"logs/questionsLogsOWA_{index}.csv"

		csvFile = open(name, 'w+')
		csvFile.write('questions,PMR\n')

		#Génération d'une instance de problème :
		reducedObjectsWeights, reducedObjectsValues, W = reduceObjects(objectsWeights, objectsValues, W, nbCriteria=n, factor=0.1, generateW=True)

		unknownWeights = np.random.random(n)
		unknownWeights = np.sort(unknownWeights/unknownWeights.sum())[::-1]


		#Première procédure : PLS Puis Élicitation
		solver = PLS(reducedObjectsWeights, reducedObjectsValues, W, Population.randomOnePopulation, Neighborhood.exchangeOneAndFillNeighborhood, Update.updateFrontList)

		eff, elapsedTime = solver.runList(verbose=0)

		front = convertPopulationToFront(eff, eff[0][1].shape[0])

		saved = []

		finalBestSolution, questionCount1, prefs = simulatedIncrementalElicitation(front, unknownWeights, mode=mode, verbose=1, save=saved)

		for save in saved:
			csvFile.write(f'{save[0]},{save[1]}\n')

		csvFile.close()

	def loadQuestionsLogs(start, end, mode="OWA"):

		allArray = []

		for i in range(start, end+1):

			if mode == "WS":
				name = f'logs/questionsLogsWS_{i}.csv'
			else:
				name = f'logs/questionsLogsOWA_{i}.csv'
		
			data = np.genfromtxt(name, delimiter=',')[1:]

			allArray.append(data)
		
		fig, ax = plt.subplots(1)

		if mode == "WS":
			plt.title("Pour WS")
		elif mode == "Choquet":
			plt.title("Pour Choquet")
		else:
			plt.title("Pour OWA")


		for data in allArray:
			ax.plot(data[:, 0], data[:, 1])

		ax.set_xlabel('Questions')
		ax.set_ylabel('Valeur PMR')
		ax.grid()


		plt.show()

		#np.set_printoptions(suppress=True)
		#meanData = data.mean(axis=0)

		#print(np.round(meanData, 4)[:-1])


"""

{1, 2, 3}

[  1,   2,   3,  12,  13,  23, 123]
[0.3, 0.3, 0.3, 0.6, 0.6, 0.6, 1]


12 -> (1 + 2)

123 -> (12, 13, 23)


"""