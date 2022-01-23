
import numpy as np

def weightedSum(objectives, weights):
	'''
	Retourne la somme pondérée par les poids (weights) des objectifs (objectives)
	'''
	return (objectives * weights).sum()


def OWA(objectives, weights):

	return (np.sort(objectives) * weights).sum()
