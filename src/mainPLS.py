
from PLS.PLS import PLS

from PLS.AlgorithmHelper import Update, Population, Neighborhood
from PLS.AlgorithmHelper import convertPopulationToFront


from PLS.InstanceLoader import readInstance, notDominated
from PLS.Indicators import PYN, DM
from PLS.Visualize import plotNotDominated


#Exemple de PLS1

path = "../instances/2KP200-TA-0"

objectsWeights, objectsValues, W = readInstance(path+".dat")
#optFront = notDominated(path+'.eff')



solver = PLS(objectsWeights, objectsValues, W, Population.randomOnePopulation, Neighborhood.exchangeOneAndFillNeighborhood, Update.updateFront)


eff, elapsedTime = solver.run(verbose=1)

front = convertPopulationToFront(eff)

#print("PYN:", PYN(front, optFront))
#print("DM: ", DM(front, optFront))
print("Elapsed time:", elapsedTime, "sec")

plotNotDominated([front])
