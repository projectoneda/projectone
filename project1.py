#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun Nov 18 12:40:41 2018
#TESTbyALEX
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
import csv
import os
import matplotlib as plt


#Specify the file path
csvpath = os.path.join('market.csv')
   
market = pd.read_csv (csvpath)

# new data frame with split value columns 
market_data = market["Date"].str.split("-", n = 1, expand = True) 
  
# making seperate first name column from new data frame 
market["Year"] = market_data[0] 
  
# making seperate last name column from new data frame 
market["stuff"] = market_data[1] 

#market["Day"] = market_data[2]
  
# Dropping old Name columns 
market.drop(columns =["Date"], inplace = True) 

# new data frame with split value columns 
market_data = market["stuff"].str.split("-", n = 1, expand = True) 

# making seperate first name column from new data frame 
market["Month"] = market_data[0] 
  
# making seperate last name column from new data frame 
market["Day"] = market_data[1] 
  
# Dropping old Name columns 
market.drop(columns =["stuff"], inplace = True) 
market.drop(columns =["Adj Close"], inplace = True) 
market.drop(columns =["Volume"], inplace = True) 
market.drop(columns =["Low"], inplace = True) 
market.drop(columns =["High"], inplace = True) 
market.drop(columns =["Day"], inplace = True) 

# Export the results to text file
market.to_csv('market2.csv', index = False)

# df display 
print (market) 

# Track various financial parameters
total_months = 0
month_of_change = []
net_change_list = []
total_net = 0

# Extract first row to avoid appending to net_change_list
first_row = market.loc[market.index[0]]
print (first_row)



<<<<<<< HEAD
## URL for GET requests to retrieve vehicle data
#url = "https://api.iextrading.com/1.0/stock/aapl/chart/1Y"
## Dons test to see if github works
#url = "https://www.alphavantage.co/query?function=TIME_SERIES_MONTHLY&symbol=.inx&apikey="
#api = "00000000"
=======
    # Track the net change
    net_change = int(row[1]) - prev_net
    prev_net = int(row[1])
    net_change_list = net_change_list + [net_change]
    month_of_change = month_of_change + [row[0]]

print (total_months)
print (net_change_list)

# Calculate the percent changes for each month


# URL for GET requests to retrieve vehicle data
url = "https://api.iextrading.com/1.0/stock/aapl/chart/1Y"
url = "https://www.alphavantage.co/query?function=TIME_SERIES_MONTHLY&symbol=.inx&apikey="
api = "00000000"
>>>>>>> 9c9eafa39c23be297a21969b3ed0e94606e5f681

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

#---------------------------------------------
#CHARTS
#---------------------------------------------
