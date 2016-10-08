#! /usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat Oct  8 13:37:25 2016

@author: edridge
Part 3 in pipeline: Tie together the restaurant finder and menu retriever into 
1 big structure
"""

import pandas as pd
from buildTable import *
import argparse

def mainTable():
    ADDRESS = "01003"
    RADIUS = 17000
    NAME = "burger"
    
    restaurantTable = MapsDataFrame(address=ADDRESS, radius=RADIUS, name=NAME)
    itemTable = pd.DataFrame()
    visitedlist = []
    for restaurant in restaurantTable['restaurant']:
        print(restaurant) # Comment out when done
        if restaurant not in visitedlist:
            itemTable = itemTable.append(QueryUsdaEntries(restaurant))
        visitedlist.append(restaurant)
    return itemTable
    
    
    
if __name__ == "__main__":
    BIGTABLE = mainTable()
    print(BIGTABLE)
