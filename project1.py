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

#initalize market types
high_profit_market = market
low_profit_market = market


#df display 
#print (market) 

#structure data

def label_nov_apr_month (row):
   if row['Month'] == '01' :
      return np.NaN
   if row['Month'] == '02' :
      return np.NaN
   if row['Month'] == '03' :
      return np.NaN
   if row['Month'] == '04' :
      return 'Nov-Apr'
   if row['Month'] == '05' :
      return np.NaN
   if row['Month'] == '06' :
      return np.NaN
   if row['Month'] == '07' :
      return np.NaN
   if row['Month'] == '08' :
      return np.NaN
   if row['Month'] == '09' :
      return np.NaN
   if row['Month'] == '10' :
      return np.NaN
   if row['Month'] == '11' :
      return 'Nov-Apr'
   if row['Month'] == '12' :
      return np.NaN  
   return 'Other'

def label_may_oct_month (row):
   if row['Month'] == '01' :
      return np.NaN
   if row['Month'] == '02' :
      return np.NaN
   if row['Month'] == '03' :
      return np.NaN
   if row['Month'] == '04' :
      return np.NaN
   if row['Month'] == '05' :
      return 'May-Oct'
   if row['Month'] == '06' :
      return np.NaN
   if row['Month'] == '07' :
      return np.NaN
   if row['Month'] == '08' :
      return np.NaN
   if row['Month'] == '09' :
      return np.NaN
   if row['Month'] == '10' :
      return 'May-Oct'
   if row['Month'] == '11' :
      return np.NaN
   if row['Month'] == '12' :
      return np.NaN  
   return 'Other'

#create label column and drop NaN
high_profit_market['Season'] = high_profit_market.apply (lambda row: label_nov_apr_month (row),axis=1)
high_profit_market = high_profit_market.dropna(axis = 0, how ='any') 
high_profit_market = high_profit_market.reset_index()
high_profit_market.drop(market.index[:1], inplace=True)
high_profit_market = high_profit_market.reset_index()

low_profit_market['Season'] = low_profit_market.apply (lambda row: label_may_oct_month (row),axis=1)
low_profit_market = low_profit_market.dropna(axis = 0, how ='any') 
low_profit_market = low_profit_market.reset_index()

#view data
print (high_profit_market)
print (low_profit_market)


# Track various financial parameters


#---------------------------------------------
#CHARTS
#---------------------------------------------
