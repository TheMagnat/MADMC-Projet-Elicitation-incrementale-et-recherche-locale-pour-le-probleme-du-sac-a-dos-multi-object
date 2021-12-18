
import numpy as np


def seed(seed = np.random.randint(np.iinfo(np.int32).max)):
	np.random.seed(seed)


def nonCorrelees(n, nbObjectives, maxValue):
	p = np.ceil(np.random.rand(n) * maxValue).astype(np.int64)

	u = np.ceil(np.random.rand(n, nbObjectives) * maxValue).astype(np.int64)

	return p, u

def peuCorrelees(n, nbObjectives, maxValue, maxDiff=None):

	if maxDiff is None:
		maxDiff = maxValue

	p = np.ceil(np.random.rand(n) * maxValue).astype(np.int64)

	r = (np.random.rand(n, nbObjectives) * (maxDiff * 2) - maxDiff)

	u = np.ceil(p.reshape(-1, 1) + r).astype(np.int64)

	#Note: ici, on remplace les valeurs < 1 par 1, mais peut être vaut-il mieux retirer ces valeurs ?
	return p, np.where(u < 1, 1, u)

def tresCorrelees(n, nbObjectives, maxValue, factor=0.1):

	p = np.ceil(np.random.rand(n) * maxValue).astype(np.int64)

	r = ((np.random.rand(n, nbObjectives) * 2 - 1) * factor) * p.reshape(-1, 1)

	u = np.ceil(p.reshape(-1, 1) + r).astype(np.int64)

	#Note: ici, on remplace les valeurs < 1 par 1, mais peut être vaut-il mieux retirer ces valeurs ?
	return p, np.where(u < 1, 1, u)

def egale(n, maxValue):
	ret = np.ceil(np.random.rand(n)*maxValue).astype(np.int64)
	return ret, ret.copy()
