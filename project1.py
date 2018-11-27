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
market['Date'] = market['Month'].astype(str) + '/' + market['Day'] + '/' + market['Year']
market.drop(columns =["Day"], inplace = True) 


# Export the results to text file
market.to_csv('market_data.csv', index = False)

market2 = market
market3 = market

#initalize market types
high_profit_market = market
low_profit_market = market

#df display 
#print (market.head()) 
#print (market2.head())
#print (market3.head())

#structure data - idea 1 

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

#structure data - idea two - used

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

#create label column and drop NaN - idea 2
# 'pop' = period over period
# 'sos' = season over season; returns are 6 months apart;
market2 = market.dropna(axis = 0, how ='any') 
market2.drop(market2.index[:3], inplace=True)
market2 = market2.reset_index(drop = True)
#print (market2.head(10))

#calculate returns every month and every 6 months
market2['pct_pop'] = market2['Open'].pct_change()
market2['pct_sos'] = market2['Open'].pct_change(6)
market2['Season'] = market2.apply (lambda row: label_month (row),axis=1)
market2 = market2[['Date', 'Open', 'pct_sos', 'Month', 'Year', 'pct_pop', 'Season', 'Close']]


#create label column and drop NaN - idea 1
high_profit_market['Season'] = high_profit_market.apply (lambda row: label_nov_apr_month (row),axis=1)
high_profit_market = high_profit_market.dropna(axis = 0, how ='any') 
high_profit_market = high_profit_market.reset_index(drop = True)
high_profit_market.drop(market.index[:1], inplace=True)
high_profit_market = high_profit_market.reset_index(drop = True)

low_profit_market['Season'] = low_profit_market.apply (lambda row: label_may_oct_month (row),axis=1)
low_profit_market = low_profit_market.dropna(axis = 0, how ='any') 
low_profit_market = low_profit_market.reset_index(drop = True)
low_profit_market['Return'] = low_profit_market.Open.pct_change(1)

#view data
#print (high_profit_market.head())
#print (low_profit_market.head())
#print (market2.head(20))

#filter1 = market2.groupby.Season.values()
#print (filter1.head())

# Export the results to text file
market2.to_csv('market2.csv', index = False)
high_profit_market.to_csv('high_profit_market.csv', index = False)
low_profit_market.to_csv('low_profit_market.csv', index = False)


# Track various financial parameters


#---------------------------------------------
#CHARTS
#---------------------------------------------

#Average Return % by Season (for all years)

#Group by year and time period 
#Market_By_Season = market2.groupby(["Year","Season"]).mean()
##Market_By_Season.head()
#
#Market_By_Season = Market_By_Season.reset_index()
##Market_By_Season.head()
#
##Filter Market_by_Season dataframe by Season column to only include May-Oct
#May_Oct = Market_By_Season.loc[Market_By_Season["Season"]== "May-Oct",:]
#May_Oct.head()

#Filter market2 df by Season column for May-Oct and Nov-Apr
May_Oct = market2.loc[market2["Season"] == "May-Oct", : ]
Nov_Apr = market2.loc[market2["Season"] == "Nov-Apr" , :]

#Calculate average pop and sos returns for different time periods
#I think we actually just want the average sos returns for April and October??
May_Oct_Avgp = May_Oct["pct_pop"].mean()
May_Oct_Avgs = May_Oct["pct_sos"].mean()

May_Oct_Avgs

#Calculate 

#---------------------------------------------
#Line Charts
#---------------------------------------------


high_profit = pd.read_csv("high_profit_market.csv")
low_profit = pd.read_csv("low_profit_market.csv")
high_low = pd.concat([high_profit, low_profit_market])

high_mean = high_profit.groupby(["Year"]).mean()["Return"]
low_mean = low_profit.groupby(["Year"]).mean()["Return"]
high_low = high_low.groupby(["Year"]).mean()["Return"]

# Generate the Plot 
plt.errorbar(high_profit.index, high_profit["Return"], yerr=high_profit["high_profit_market"], color="r", marker="o", markersize=5, linestyle="dashed", linewidth=0.50)
plt.errorbar(low_profit.index, low_profit["Return"], yerr=low_profit["low_profit_market"], color="b", marker="^", markersize=5, linestyle="dashed", linewidth=0.50)
plt.errorbar(high_low.index, high_low["Return"], yerr=high_low["market2"], color="g", marker="X", markersize=5, linestyle="dashed", linewidth=0.50)

plt.title("Average Total Return")
plt.ylabel("Total Return")
plt.xlabel("Time (Years)")
plt.grid(True)
plt.legend(loc="best", fontsize="small", fancybox=True)

# Save the Figure
# plt.savefig("analysis/Fig1.png")

# Show the Figure
# plt.show()















