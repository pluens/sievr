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
import argparse



def mainTable(restaurantTable):

    itemTable = pd.DataFrame()
    visitedlist = []
    for restaurant in restaurantTable['restaurant']:
        if restaurant not in visitedlist:
            print(restaurant) # Comment out when done
            temp = buildTable.QueryUsdaEntries(restaurant)
            if not temp.empty:
                itemTable = itemTable.append(temp)
        visitedlist.append(restaurant)
    return itemTable
    
def Joins(restaurantTable, bigtable):
    result = pd.merge(restaurantTable, bigTable, on=['restaurant'], how="outer")
    return result
    
if __name__ == "__main__":
    
    
    ADDRESS = "01003"
    RADIUS = 17000
    NAME = "burger"
    
    restaurantTable = buildTable.MapsDataFrame(address=ADDRESS, radius=RADIUS, name=NAME)
    BIGTABLE = mainTable(restaurantTable = restaurantTable)
    print(BIGTABLE)
    joined = pd.merge(restaurantTable, BIGTABLE, on='restaurant', how="outer")
    print(joined)
