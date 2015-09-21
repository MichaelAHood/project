from scipy.spatial.distance import euclidean


def distance(v1, v2):
	'''
	Input: takes two real estate listings as vectors.
	Output: returns a distance between the two vectors, where
			distance is inversely proportional to how much a space space_lover
			will prefer this listing.
	'''

	# v1_bath = v1['bathrooms'] 
	# v1_bed = v1['bedrooms']
	# v1_sqft_room = v1['finishedsqft'] / v1['numrooms'] # this computation needs to be done before the normalizing
	# v1_sqft_total = v1['finishedsqft']

	scalar = [20, 20, 20, 1.5, 0.5, 1, 0.5, 0.5]

	return euclidean(v1, scalar * v2)