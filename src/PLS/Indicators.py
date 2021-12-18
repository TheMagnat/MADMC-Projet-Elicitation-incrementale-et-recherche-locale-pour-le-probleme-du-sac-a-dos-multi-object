
import numpy as np
import sys

def PYN(approx, real):

	app = set(list(map(tuple, approx)))

	rea = set(list(map(tuple, real)))

	return len(app & rea)/len(real)


def DM(approx, real):

	nadir = np.array([real[:, 0].min(), real[:, 1].min()])

	ideal = np.array([real[:, 0].max(), real[:, 1].max()])
	

	p = np.empty(2, dtype=float)

	for k in range(2):
		p[k] = 1 / (ideal[k] - nadir[k])


	bestDists = np.full(real.shape[0], sys.float_info.max, dtype=float)

	for i, point in enumerate(real):

		for appPoint in approx:

			dist = np.sqrt(p[0]*((point[0] - appPoint[0])**2) + p[1]*((point[1] - appPoint[1])**2))

			if dist < bestDists[i]:
				bestDists[i] = dist

	return bestDists.mean()
