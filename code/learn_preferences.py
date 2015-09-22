import pandas as pd
import numpy as np
from sklearn.metrics.pairwise import pairwise_distances
from scipy.spatial.distance import cosine
from scipy.stats import beta
from clean_transform import drop_columns, filter_df
from metrics import space_distance, walk_distance
import re
import sys
import pdb

class LearnPreferences(object):
	
	"""
	Implements a multi-armed bayeseian bandit to learn a users preferences in houses.
	"""

	def __init__(self, df1, df2, metrics, ref_listing, num_matches=1):
		self.ref_listing = df1.ix[ref_listing] # the seed house that all other house are comapred to
		self.num_matches = num_matches # the number of mathces to return
		self.recommendation_history = {}
		self.pairs_served = 0
		self.metrics = metrics
		self.scores = {}
		self.listings_served = set()
		self.df_struct = {} # a container to hold the precomputed dfs for each of the metrics
		#self.listing_details = pd.read_csv('df_sf_ref.csv', index_col=0) # this df contains the untransformed listing data
		self.sim_mat = self.update_similarity_matrix(df1, df2, 'cosine')
		self.init_scores() # populates self.scores with a zero for each of the different distance metrics

	
	def init_scores(self): 
		for metric in self.metrics:
			if metric not in self.scores:
				self.scores[metric] = 0

	
	def build_struct():
		for metric in metrics:
			self.struct[metric] = [filter_df(drop_columns(df), metric) for df in [df1, df2]]


	def update_similarity_matrix(self, df1, df2, distance_metric):
		self.sim_mat = pairwise_distances(df1, df2, metric=distance_metric, n_jobs=-1) 
		return self.sim_mat

	
	def get_recommendation(self):
	    
	    """
	    Input: similarity matrix with first arg of parwise distances as rows and
	           second arg of pairwise distances as columns, the integer index of the 
	           listing you want to compare other listings to, int for the num of listings
	           to return.
	           
	    Output: an numpy array with the indices of the listings that
	            are most similar to the ref_listing.
	    """
   	    recommendation = np.random.choice(np.argsort(self.sim_mat[self.ref_listing])[-(self.num_matches):][0])
   	    while recommendation in self.listings_served:
   	    	recommendation = np.random.choice(np.argsort(self.sim_mat[self.ref_listing])[-(self.num_matches):][0])
   	    self.listings_served.add(rec) # this will prevent showing the same listing over again, or at the same time
   	    return recommendation
   
   	def choose_models(self):
   		# choose two of the available models, where one is the best estimate of the users preference
   		# and the other is randomly chosen of the remaining metrics

   		# assign the best guess to a list
		if self.pairs_served > 0:
			best_guess = self.recommendation_history[self.pairs_served]['estimated_user_preference']
			metrics = [best_guess]
			remaining_metrics = list(self.metrics) # make a copy of the list, so the original is not modified
			remaining_metrics.pop(remaining_metrics.index(best_guess)) # remove the best guess, since it's already in metrics
			metrics.append(np.random.choice(remaining_metrics)) # randomly choose the other metric
			np.random.shuffle(metrics) # shuffle the metrics, so the best guess recommendation is not always the first one presented
		else:
			# this is the starting point and these is no best guess of the best metric
			metrics = np.random.choice(self.metrics, 2, replace=False)
		return metrics 

   	

   	def get_user_choice(self, df1, df2):
		
		"""
		Input: a dataframe for each of the cities

		Output: the recommendation corresponding to the user choice 
		"""
		
		sample_metrics = self.choose_models()
		recommendations = []
		for metric in sample_metrics:
			self.update_similarity_matrix(df1, df2, 'euclidean')
			recommendations.append(self.get_recommendation())
		
		for rec in recommendations:
			 # keeping track of which listings have been served
			print df2.ix[rec]	# Note to self: use df to html library
		user_choice = raw_input("Which house do you like best? (l)eft or (r)ight?:   ")
		if user_choice == "l":
			self.scores[sample_metrics[0]] += 1
			winner = recommendations[0]
		else:
			self.scores[sample_metrics[1]] += 1
			winner = recommendations[1]

		#self.user_choices.append(user_choice)
		self.pairs_served += 1
		self.update_recommendation_history(recommendations, winner)
 

   	def update_recommendation_history(self, recommendations, winner):
   		self.recommendation_history[self.pairs_served] = {'pairs_served': recommendations,
   														  'winner': winner
   														  }
  
   	def guess_preferences(self):

   		user_preference = None
   		max_prob = 0
   		for metric in self.metrics:
   			prob = beta.rvs(self.scores[metric] + 1, self.pairs_served - self.scores[metric] + 1) # sample form the dist for each metric
			if prob > max_prob:
				max_prob = prob
				user_preference = metric
		self.recommendation_history[self.pairs_served]['estimated_user_preference'] = user_preference
		
   	





#if __name__ == "__maine__":	

# 	df = pd.read_csv('trx_seattle.csv', index_col=0) # this df contains the untransformed listing data
# 	my_past_house = df1.ix[0] # user has previously lived in house with index 0
# 	user_session = LearnPreferences(df1, df2) # init object and a similarity matrix
# 	recommendations = user_session.get_most_similar(user_session.sim_mat, my_past_house, 4) # provides the 4 most similar listings
# 	choice = get_user_choice(reccomendations)
# 	update_user_history(recommendations)

