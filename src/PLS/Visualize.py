import matplotlib.pyplot as plt


def plotNotDominated(allFronts):

	plt.title('Nuage de points avec Matplotlib')
	plt.xlabel('x')
	plt.ylabel('y')

	for front in allFronts:
		plt.scatter(front[:, 0], front[:, 1], s=4, marker='s')

	plt.show()

