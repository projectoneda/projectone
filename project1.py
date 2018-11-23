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
market['Date']=market['Month'].astype(str)+'/'+market['Day']+'/'+market['Year']
market.drop(columns =["Day"], inplace = True) 


# Export the results to text file
market.to_csv('market2.csv', index = False)

#initalize market types
high_profit_market = market
low_profit_market = market
market2 = market
market3 = market

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

def label_month (row):
   if row['Month'] == '01' :
      return 'Nov-Apr'
   if row['Month'] == '02' :
      return 'Nov-Apr'
   if row['Month'] == '03' :
      return 'Nov-Apr'
   if row['Month'] == '04' :
      return 'Nov-Apr'
   if row['Month'] == '05' :
      return 'May-Oct'
   if row['Month'] == '06' :
      return 'May-Oct'
   if row['Month'] == '07' :
      return 'May-Oct'
   if row['Month'] == '08' :
      return 'May-Oct'
   if row['Month'] == '09' :
      return 'May-Oct'
   if row['Month'] == '10' :
      return 'May-Oct'
   if row['Month'] == '11' :
      return 'Nov-Apr'
   if row['Month'] == '12' :
      return 'Nov-Apr' 
   return 'Other'

market['P_Season'] = market.apply (lambda row: label_month (row),axis=1)

#create label column and drop NaN
high_profit_market['Season'] = high_profit_market.apply (lambda row: label_nov_apr_month (row),axis=1)
high_profit_market = high_profit_market.dropna(axis = 0, how ='any') 
high_profit_market = high_profit_market.reset_index(drop = True)
high_profit_market.drop(market.index[:1], inplace=True)
high_profit_market = high_profit_market.reset_index(drop = True)

#high_profit_market ['return'] = high_profit_market (lambda row: 'Open'/'Close'.shift(1))

low_profit_market['Season'] = low_profit_market.apply (lambda row: label_may_oct_month (row),axis=1)
low_profit_market = low_profit_market.dropna(axis = 0, how ='any') 
low_profit_market = low_profit_market.reset_index(drop = True)

low_profit_market['Return'] = low_profit_market.Open.pct_change(1)


market2.drop(market.columns[[5]], axis=1, inplace=True)
market2 = market.dropna(axis = 0, how ='any') 
market2 = market.reset_index(drop = True)

#rng = pd.date_range('5/1/1950', periods=180, freq='M')
#market2 = market2.set_index('Date')
#market2 ['Return'] = market2['Open'] - market2['Open'].shift(6)/ market2

#view data
print (high_profit_market.head())
print (low_profit_market.head())
print (market2.head())

# Track various financial parameters


#---------------------------------------------
#CHARTS
#---------------------------------------------
