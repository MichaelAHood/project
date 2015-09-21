import pandas as pd
import numpy as np
from sklearn.metrics.pairwise import pairwise_distances
from scipy.stats import beta
from space_lover import space_distance
from walk_lover import walker_distance

class LearnPreferences(object):
	'''
	Implements a multi-armed bayeseian bandit to learn a users preferences in houses.
	'''

	def __init__(self, df1, df2, metrics, ref_listing, num_matches=4):

		self.ref_listing = ref_listing # an no array for the seed house
		self.num_matches = num_matches
		self.user_preferences = np.zeros(len(df1)) # init to all zeros since nobody has wins
		self.user_choices = []
		self.user_history = {}
		self.pages_served = 0
		self.prob_array = np.ones(len(df1)) / float(len(df1)) # probs are equally distributed
		self.metrics = metrics
		
		self.listing_details = pd.read_csv('trx_seattle.csv', index_col=0) # this df contains the untransformed listing data
		self.sim_mat = self.compute_similarity_matrix(df1, df2, distance_metric='cosine')

	def compute_similarity_matrix(self, df1, df2, distance_metric='cosine'):
		self.sim_mat = pairwise_distances(df1, df2, metric=distance_metric, njobs=-1) 

	
	def get_most_similar(self, sim_mat, num_matches):
	    '''
	    Input: similarity matrix with first arg of parwise distances as rows and
	           second arg of pairwise distances as columns, the integer index of the 
	           listing you want to compare other listings to, int for the num of listings
	           to return.
	           
	    Output: an numpy array with the indices of the listings that
	            are most similar to the ref_listing.
	    '''
   		return np.argsort(sim_mat[self.ref_listing])[-(num_matches):]

   

   	def get_user_choice(self, recommendations):
		'''
		Input: an array of recommendations

		Output: the recommendation corresponding to the user choice 
		'''
		print self.listing_details(recommendations)  # use df to html library		
   		user_choice = raw_input("Which house do you like best?:    ")
   		self.user_history.append(user_choice)
   		self.pages_served += 1
   		return recommendations[choice] # 

   	def update_user_history(self, recommendations):
   		self.user_history[self.pages_served] = [recommendations]


   	def iterate_through_metrics(self):
   		for metric in self.metrics:
   			self.compute_similarity_matrix(df1, df2, distance_metric=metric)
   			self.get_most_similar(self.sim_mat, )
   	



   	def guess_preferences(self):

   		rand_samp = []
   		for i, p in enumerate(self.prob_array):
   			rand_samp.append(stats.beta.rvs())





if __name__ == "__maine__":	

	df = pd.read_csv('trx_seattle.csv', index_col=0) # this df contains the untransformed listing data
	my_past_house = df1.ix[0] # user has previously lived in house with index 0
	user_session = LearnPreferences(df1, df2) # init object and a similarity matrix
	recommendations = user_session.get_most_similar(user_session.sim_mat, my_past_house, 4) # provides the 4 most similar listings
	choice = get_user_choice(reccomendations)
	update_user_history(recommendations)

