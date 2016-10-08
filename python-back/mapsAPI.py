# -*- coding: utf-8 -*-
"""
Created on Sat Oct  8 01:45:15 2016

@author: Edrige D'Souza

Part 1 in Python pipeline: given location, use Google Maps API to find restaurants
"""

import json, requests
from geopy.geocoders import Nominatim
from geopy.exc import GeocoderTimedOut

def MakeQuery(address, radius = 15000, name=""): 
    # https://developers.google.com/places/web-service/search
    base = "https://maps.googleapis.com/maps/api/place/nearbysearch/"
    output = "json"
    placetype = "type=restaurant"
    radius = radius # Default to 15km
    
    with open("./googlePlacesAPI.txt", "r") as file:
        key = "key=" + file.read() # Api key

    try:    
        geolocator = Nominatim()
        loc = geolocator.geocode(str(address), timeout=10)
        location = "location="+str(loc.latitude)+","+str(loc.longitude)
        query = base + output + "?" + placetype + "&" + "radius=" + str(radius) + "&" + location + "&"
        if name != "":
            name= "name="+name
            query += name
        query += "&" + key
    except GeocoderTimedOut as e:
        print("Error: address \"%s\" failed"%(address))
        query = ""
    return query
    
    
def RetrieveQuery(query):
    resp = requests.get(url=query)
    data = json.loads(resp.text)
    return data
    
if __name__ == "__main__":
    #print(MakeQuery(address="01003"))
    #print(MakeQuery(address="01003", radius=16000,name="anglo"))
    print(MakeQuery(address="01003",radius=16000,name="anglo"))
    print(RetrieveQuery(MakeQuery(address="01003",radius=16000,name="anglo")))