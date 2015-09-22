from scipy.spatial.distance import euclidean


def space_distance(v1, v2):
	'''
	Input: takes two real estate listings as vectors.
	Output: returns a distance between the two vectors, where
			distance is inversely proportional to how much a space space_lover
			will prefer this listing.
	'''
	correction = [1.2, 1.2, 1.2, 1.5, 0.5, 1, 0.2, 0.2]

	return euclidean(correction * v1, correction * v2)

def walk_distance(v1, v2):
	'''
	Input: takes two real estate listings as vectors.
	Output: returns a distance between the two vectors, where
			distance is inversely proportional to how much a space space_lover
			will prefer this listing.
	'''
	correction = [0.2, 0.2, 0.2, 0.2, 1.0, 1.5, 2, 2]

	return euclidean(correction * v1, correction * v2)