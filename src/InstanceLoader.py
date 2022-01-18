
import numpy as np


def readInstance(path, generateW=False):

	nPos = 1

	with open(path, 'r') as f:
		allLines = f.readlines()

	n = int(allLines[nPos].split(" ")[1])

	size = len(allLines[nPos+1].rstrip().lstrip("c ").split(" "))

	objects = np.empty((n, size))
	for i, line in enumerate(allLines[nPos+2:nPos+2+n]):
		objects[i] = list( map(int, line.rstrip().lstrip("i ").split(" ")) )

	W = int(allLines[-2].split(" ")[1])

	if generateW:
		W = objects[:, 0].sum()/2

	return objects[:, 0], objects[:, 1:], W


def notDominated(path):

	with open(path, 'r') as f:
		allLines = f.readlines()

	allPoints = []
	for line in allLines:
		allPoints.append( list(map(int, line.rstrip().split("\t"))) )

	return np.array(allPoints)




###Exemple
if __name__ == "__main__":

	path = "../InstancesMOKP/100_items/2KP100-TA-0"

	#objects, W = readInstance(path+'.dat')
	notDominated(path+'.eff')


