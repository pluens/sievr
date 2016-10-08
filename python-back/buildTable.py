# -*- coding: utf-8 -*-
"""
Created on Sat Oct  8 10:35:52 2016

@author: edridge
Part 2 in pipeline: import JSON of location data
"""

import pandas as pd
from mapsAPI import MakeQuery, RetrieveQuery
import re
import requests, json
from geopy.distance import vincenty

# Create table of nearby restaurants
def MapsDataFrame(address, radius=15000, name=""):
    query = MakeQuery(address=str(address), radius=radius, name=name)
    myjson = RetrieveQuery(query)
    
    myloc = re.search("location=(.*?),(.*?)\&", query)
    mylat, mylong = myloc.group(1), myloc.group(2)
    
    df = pd.DataFrame.from_dict(myjson['results']).T
    prettyDF = df.T
    prettyDF = prettyDF[['name', 'icon', 'types',  'price_level', 'geometry']]
    
    # Idiomatic code? HAHAHAHA what's that?
    latitude = [prettyDF['geometry'][i]['location']['lat'] for i in range(len(prettyDF['geometry']))]
    longitude = [prettyDF['geometry'][i]['location']['lng'] for i in range(len(prettyDF['geometry']))]
      
    prettyDF['lat'] = latitude
    prettyDF['long'] = longitude
    
    dist = [vincenty((mylat,mylong), (prettyDF['lat'][i], prettyDF['long'][i])).miles for i in range(len(prettyDF))]
    prettyDF['dist'] = dist
    prettyDF.drop('geometry', inplace=True, axis=1)
    prettyDF['restaurant'] = [x.lower() for x in prettyDF['name']]
     
    return prettyDF
    
    
# Given a database accession ID, return calories    
def RetrieveCalories(ndbno):
    base = "http://api.nal.usda.gov/ndb/nutrients/?format=json"
    
    with open("./usdaAPI.txt", "r") as file:
        key = "api_key=" + file.read() # Api key
    nutrients="nutrients=208" # Only kcal
    id="ndbno="+str(ndbno)
    
    query = base + "&" + key + "&" + nutrients + "&" + id
    
    resp = requests.get(url=query)
    data = json.loads(resp.text) 
    
    
    # HAHAAHA "idiomatic"
    measure = dict(pd.DataFrame.from_dict(data).T['foods'])['report'][0]['measure']
    info = dict(pd.DataFrame.from_dict(data).T['foods'])['report'][0]['nutrients'][0]
    unit, value = info['unit'], info['value']
    
    return str(value) + " " + unit + " per " + measure
    #return info

# Use names from restaurant table to query USDA
def QueryUsdaEntries(restaurant):
    base = "http://api.nal.usda.gov/ndb/search/?format=json"
    q = "q=" + str(restaurant).lower()
     

    with open("./usdaAPI.txt", "r") as file:
        key = "api_key=" + file.read() # Api key
    
    query = base + "&" + q + "&" + key
    
    
    resp = requests.get(url=query)
    data = json.loads(resp.text)    
    
    df = pd.DataFrame.from_dict(data['list']['item']).T
    prettyDF = df.T
    
    restaurant = [re.search("(.*?),", i).group(1).lower() for i in prettyDF['name']]
    prettyDF['restaurant'] = restaurant
    
    energy = [RetrieveCalories(str(x)) for x in prettyDF['ndbno']]
    prettyDF['energy'] = energy
    
    return prettyDF
     

         
     
if __name__ == "__main__":
    blah = MapsDataFrame(address="01003",radius=16000,name="burger")
    blah2 = RetrieveCalories("21141")
    blah3 = QueryUsdaEntries("burger king")