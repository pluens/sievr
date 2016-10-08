# -*- coding: utf-8 -*-
"""
Created on Sat Oct  8 10:35:52 2016

@author: edridge
Part 2 in pipeline: import JSON of location data
"""

import pandas as pd
from mapsAPI import MakeQuery, RetrieveQuery
import re
from geopy.distance import vincenty

def MapsDataFrame(address, radius=15000, name=""):
    query = MakeQuery(address=str(address), radius=radius, name=name)
    json = RetrieveQuery(query)
    
    myloc = re.search("location=(.*?),(.*?)\&", query)
    mylat, mylong = myloc.group(1), myloc.group(2)
    
    df = pd.DataFrame.from_dict(json['results']).T
    prettyDF = df.T
    prettyDF = prettyDF[['name', 'icon', 'types',  'price_level', 'geometry']]
    
    # Idiomatic code? HAHAHAHA what's that?
    latitude = [prettyDF['geometry'][i]['location']['lat'] for i in range(len(prettyDF['geometry']))]
    longitude = [prettyDF['geometry'][i]['location']['lng'] for i in range(len(prettyDF['geometry']))]
      
    prettyDF['lat'] = latitude
    prettyDF['long'] = longitude
    
    dist = [vincenty((mylat,mylong), (prettyDF['lat'][i], prettyDF['long'][i])).miles for i in range(len(prettyDF))]
    prettyDF['dist'] = dist
     
    return prettyDF
    
    
def QueryUSDA():
     "http://api.nal.usda.gov/ndb/search/?format=json"
     
     
     
if __name__ == "__main__":
    blah2=MapsDataFrame(address="01003",radius=16000,name="burger")