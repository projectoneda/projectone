#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun Nov 18 12:40:41 2018

@author: riceowl1
"""

# Dependencies
import requests
import json
import time
import pandas as pd
import numpy as np
#import matplotlib.pyplot as plt
#from config import api_key
from pprint import pprint
import os

#Specify the file path
csvpath = os.path.join('market.csv')
   
market = pd.read_csv (csvpath)

# URL for GET requests to retrieve vehicle data
url = "https://api.iextrading.com/1.0/stock/aapl/chart/1Y"
# Dons test to see if github works
url = "https://www.alphavantage.co/query?function=TIME_SERIES_MONTHLY&symbol=.inx&apikey="
api = "00000000"

# Pretty print JSON for all launchpads
response = requests.get(url+api).json()
#print(json.dumps(response, indent=4, sort_keys=True)) 
#
## Pretty print JSON for a specific launchpad
#pprint(response)

#print (len(response))

## Initialize arrays
#open_price = []
#high_price = []
#low_price = []
#close_price = []
#date = []
#
#x = 0
#months = 217
#error = 0
#
#for x in months:
#    response = response
#    time.sleep(1)
#  
#    #Check for bad data
#    
#    try:
#        open_price.append(response['1. open'])
#        high_price.append(response['2. high'])
#        low_price.append(response['3. low'])
#        close_price.append(response['4. close'])
#        date.append(response['data']['speed'])
#
#        print(f"Processing record {x + 1}")
#    except KeyError:
#        open_price.append(np.nan)
#        high_price.append(np.nan)
#        low_price.append(np.nan)
#        close_price.append(np.nan)
#        date.append(np.nan)
#        print(f"Error with record {x + 1} | will be skipped")
#        error += 1
#
#print("--------------------------------------------")
#print("Data Processing Complete")
#print("--------------------------------------------")
#
## Assemble everything into a data frame
#market_data = pd.DataFrame({"Open": open_price,
#                           "High": high_price,
#                           "Low": low_price,
#                           "Close": close_price,
#                           "Date": date,
#                          })
#
## Remove any values that have NaN values
#market_data.dropna(how='any', inplace = True)
#
#market_data.head()

