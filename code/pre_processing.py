import pandas as pd


class PreProcess(object):

    def __init__(self, df):
        self.df = df
        self.dropped_columns_ = ['_id', 'city', 'latitude', 'longitude', 'state', 'street', 
                                 'zipcode', 'appliances', 'architecture', 'basement', 'coolingsystem',
                                 'coveredparkingspaces', 'exteriormaterial', 'floorcovering',
                                 'floornumber', 'heatingsources', 'heatingsystem', 'lotsizesqft', 
                                 'numfloors', 'numunits', 'parkingtype', 'roof', 'rooms', 'view', 
                                 'yearupdated', 'elementaryschool', 'highschool', 'homedescription', 
                                 'images_count', 'images_image', 'links_homedetails', 'links_homeinfo', 
                                 'links_photogallery', 'middleschool', 'neighborhood', 'pageviewcount_currentmonth',
                                 'pageviewcount_total', 'agentname' ,'agentprofileurl', 'externalurl', 
                                 'lastupdateddate', 'mls', 'openhousedates', 'status', 'schooldistrict', 
                                 'usecode', 'type', 'trans_desc', 'trans_summary', 'walkscore_desc', 'whatownerloves', 'zpid']

    def drop_columns(self):
        """
        
        Notes: this function will drop all of the columns from a dataframe that are note
        needed for computation of any of the similarity metrics. For example, 'heatingsources'
        is not currently used in any of the similarity metrics, so it is dropped.

        """

        self.df = self.df.drop(self.dropped_columns_, axis=1)
        return self.df

    
    def preprocess_df(self):
        self.df = self.df.drop(['price'], axis=1) #there are too many NA values for price for it ot be useful
        self.df = self.df.dropna(axis=0, how='any')
        # remove 'None' values in trans_score
        indices = self.df[self.df['trans_score'].isin(['None'])].index
        self.df = self.df[~(self.df.index.isin(indices))]
        indices = self.df[self.df['walkscore_score'].isin(['None'])].index
        self.df = self.df[~(self.df.index.isin(indices))]
        # cast and ints
        self.df[['trans_score', 'walkscore_score']] = self.df[['trans_score', 'walkscore_score']].astype(int) 
        # remove the rows that are absurdly big and are probably mistakes
        self.df = self.df[self.df.bedrooms <= 20]
        self.df = self.df[self.df.bathrooms <= 20]
        self.df[['bathrooms', 'bedrooms', 'finishedsqft']] = self.df[['bathrooms', 'bedrooms', 'finishedsqft']].astype(float)
        return self.df

    
    def normalize_num(self, x, col_min, col_max):
        """
        Normalize everything from 0 to 1 
        """
        return float((x - col_min)) / (col_max - col_min)

    
    def normalize_columns(self):
        """
        Attempt to normalize all of the columns
        """
        for column in self.df.columns:
            min_val = self.df[column].min()
            max_val = self.df[column].max()
            self.df[column] = self.df[column].apply(self.normalize_num, args=(min_val, max_val))
        return self.df


    def filter_df(df, metric):
        """
        Input: takes a dataframe, and the name of a similarity metric as a string
        Output: the cleaned and filtered df for the appropraite metric

        Notes: this function is meant to trim the dataframe to use only the 
        columns that are relevant to a given similarity metric.  
        """

    def filter_df(df, metric):
        
        if metric == "walk_distance":
            df = df[['trans_score', 'walkscore_score']].dropna(axis=0, how='any')
            return df.astype(int)
                
        if metric == "space_distance":
            df = df[['bathrooms', 'bedrooms', 'finishedsqft']].dropna(axis=0, how='any')
            return df.astype(float)