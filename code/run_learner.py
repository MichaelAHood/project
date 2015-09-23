import pandas as pd
import numpy as np
from sklearn.metrics.pairwise import pairwise_distances
from pre_processing import PreProcess
from learn_preferences import LearnPreferences


df_sea = pd.read_csv('data/metrics/seattle_test.csv', index_col=0)
df_sf = pd.read_csv('data/metricssanfran_test.csv', index_col=0)

sea_ref = df_sea[['city', 'state', 'street', 'finishedsqft', 
             'bedrooms', 'bathrooms', 'trans_score', 'walkscore_score']]
sf_ref = df_sf[['city', 'state', 'street', 'finishedsqft', 
             'bedrooms', 'bathrooms', 'trans_score', 'walkscore_score']]

# create the PreProcesss objects
prep_sf = PreProcess(df_sf)
prep_sea = PreProcess(df_sea)

# drop the unneccessary columns, clean_up NA's and normalize use in the recommender
prep_sf.drop_columns()
sf = prep_sf.preprocess_df()
sf = prep_sf.normalize_columns()
prep_sea.drop_columns()
sea = prep_sea.preprocess_df()
sea = prep_sea.normalize_columns()

# specify the metrics to use for the similarity matrix 
metrics = ['walk_distance', 'space_distance']

# init a LearnPreferences object with seed house of SanFran index 3, and use 50 listings 
lp = LearnPreferences(sf, sea, sf_ref, sea_ref, metrics, 3, 50)

# init the recommendations
lp.update_recommendations()

# iterate the learner 20 times
for i in range(20):
    lp.get_user_choice()
    lp.guess_preferences()