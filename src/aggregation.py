

def weightedSum(objectives, weights):
	'''
	Retourne la somme pondérée par les poids (weights) des objectifs (objectives)
	'''
	return (objectives * weights).sum()