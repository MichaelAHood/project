from bs4 import BeautifulSoup as BS
import requests
import requesocks
import time
import pandas as pd

#http://www.zillow.com/webservice/GetUpdatedPropertyDetails.htm?zws-id=<ZWSID>&zpid=48749425

ZWSID = "X1-ZWz1a49jy1eadn_7dhgw"

FEATURES = ['street', 'zipcode', 'city', 'state', 'zpid', 'latitude', 'longitude', 'type', 'price', 'homedetails', 'photogallery', 
     'homeinfo', 'bedrooms', 'bathrooms', 'finishedsqft', 'lotsizesqft', 'yearbuilt', 'yearupdated', 
     'numfloors', 'basement', 'roof', 'exteriormaterial', 'view', 'parkingtype', 'heatingsource', 
     'heatingsystem', 'coolingsystem', 'appliances', 'floorcovering', 'rooms', 'architecture', 'homedescription', 
     'whatownerloves']

def construct_api_call(ZWSID, listing_zpid):
    base = "http://www.zillow.com/webservice/GetUpdatedPropertyDetails.htm?"
    return base + "zws-id=" + ZWSID + "&zpid=" + str(listing_zpid)

def start_proxy_session():
    session = requesocks.session()
    session.proxies = {'http': 'socks5://127.0.0.1:9150',
                       'https': 'socks5://127.0.0.1:9150'}
    return session

def call_api(session, api_url):
	return session.get(api_url)

def extract_features(api_response, FEATURES):
    soup = BS(api_response.content, 'html.parser')
    data = {}
    api_code = soup.find('code').string 
    if api_code == 0:
    	return data 
    for feature in FEATURES:
        try:
            data[feature] = soup.find('response').find(feature).string
        except:
            data[feature] = soup.find('response').find(feature)

    return data  # returns a dict with features as keys and listing attributes
    			 # as values   

def get_data_and_write_to_dataframe(addresses_df, FEATURES):
 	
 	session = start_proxy_session()

 	base_df = pd.DataFrame(columns=FEATURES)
 	
 	bucket = {}

 	count = 0

 	for row in addresses_df.iterrows():
 		if count > 1:
 			break
 		print "Sleeping between API calls..."
 		time.sleep(5)
 		api_call_url = construct_api_call(ZWSID, row[1])
 		api_response = call_api(session, api_call_url)
		count += 1
		data = extract_features(api_response, FEATURES)
 		print data
 		#api_call_df = pd.DataFrame(data, columns=data.keys(), index=[0])
 		#bucket[row[0]] = data
 		#base_df = pd.concat([base_df, api_call_df])
 	return #bucket # now contains all listing info from addresses_df
 	



















