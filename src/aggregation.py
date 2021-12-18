

def weightedSum(objectives, weights):
	'''
	Retourne la somme pondérée par les poids (weights) des objectifs (objectives)
	'''
	return (objectives * weights).sum()


def OWA(objectives, weights):

	objectives.sort()

	return (objectives * weights).sum()