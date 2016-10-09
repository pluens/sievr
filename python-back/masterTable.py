#! /usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat Oct  8 13:37:25 2016

@author: edridge
Part 3 in pipeline: Tie together the restaurant finder and menu retriever into 
1 big structure
"""

import pandas as pd
import buildTable
from flask import Flask, request



app = Flask(__name__)

@app.route('/')
def hello_world():
    a = request.args.get('location')
    b = request.args.get('radius')
    c = request.args.get('name')
    answer = str(a) + str(b) + str(c)
    return answer
    

@app.route('/table')
def mainTable():

    LOCATION = str(request.args.get('location'))
    RADIUS = request.args.get('radius')
    NAME = str(request.args.get('name'))
#    ADDRESS = "01003"
#    RADIUS=15000
#    NAME="burger"
    restaurantTable = buildTable.MapsDataFrame(address=str(LOCATION), radius=RADIUS, name=NAME)

    itemTable = pd.DataFrame()
    visitedlist = []
    for restaurant in restaurantTable['restaurant']:
        if restaurant not in visitedlist:
            print(restaurant) # Comment out when done
            temp = buildTable.QueryUsdaEntries(restaurant)
            if not temp.empty:
                itemTable = itemTable.append(temp)
        visitedlist.append(restaurant)
    joined = pd.merge(restaurantTable, itemTable, on='restaurant', how="outer")
    joinedJSON = joined.to_json()
    return joinedJSON
    
def Joins(restaurantTable, bigtable):
    result = pd.merge(restaurantTable, bigTable, on=['restaurant'], how="outer")
    return result
    
if __name__ == "__main__":
    
    app.run()

