import pandas as pd

def drop_columns(df):
    """
    Input: a dataframe
    Output: a dataframe

    Notes: this function will drop all of the columns from a dataframe that are note
    needed for computation of any of the similarity metrics. For example, 'heatingsources'
    is not currently used in any of the similarity metrics, so it is dropped.

    """

    df = df.drop(['_id', 'city', 'latitude', 'longitude', 'state', 'street', 
                'zipcode', 'appliances', 'architecture', 'basement', 'coolingsystem',
               'coveredparkingspaces', 'exteriormaterial', 'floorcovering',
               'floornumber', 'heatingsources', 'heatingsystem', 'lotsizesqft', 'numfloors', 'numunits',
               'parkingtype', 'roof', 'rooms', 'view', 'yearupdated', 'elementaryschool', 
               'highschool', 'homedescription', 'images_count', 'images_image', 'links_homedetails',
                'links_homeinfo', 'links_photogallery', 'middleschool', 'neighborhood', 'pageviewcount_currentmonth',
             'pageviewcount_total', 'agentname' ,'agentprofileurl', 'externalurl', 'lastupdateddate',
             'mls', 'openhousedates', 'status', 'schooldistrict', 'usecode', 'type', 'trans_desc', 'trans_summary', 'walkscore_desc',
             'whatownerloves', 'zpid'], axis=1)
    return df

def filter_df(df, metric):
    """
    Input: takes a dataframe, and the name of a similarity metric as a string
    Output: the cleaned and filtered df for the appropraite metric

    Notes: this function is meant to trim the dataframe to use only the 
    columns that are relevant to a given similarity metric.  
    """

    if metric == "walk_distance":
        df = df[['trans_score', 'walkscore_score']].dropna(axis=0, how='any')
        indices = df[df['trans_score'].isin(['None'])].index 
        df = df[~(df.index.isin(indices))]
        indices = df[df['walkscore_score'].isin(['None'])].index
        df = df[~(df.index.isin(indices))]
        return df.astype(int)
            
    if metric == "space_distance":
        df = df[['bathrooms', 'bedrooms', 'finishedsqft']].dropna(axis=0, how='any')
        df = df[df.bedrooms <= 20]
        df = df[df.bathrooms <= 20]
        return df.astype(float)