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
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
#from config import api_key
from pprint import pprint
import csv
import os

# URL for GET requests to retrieve vehicle data
url = "https://api.iextrading.com/1.0/stock/aapl/chart/1Y"
#Dons test to see if github works
url = "https://www.alphavantage.co/query?function=TIME_SERIES_MONTHLY&symbol=.inx&apikey="
api = "2AIJQKQXSZ6F4FE9"
# ts = TimeSeries(key=api, output_format='pandas')
#print(url+api)

# Pretty print JSON for all launchpads
response = requests.get(url+api).json()
#print(json.dumps(response, indent=4, sort_keys=True))
#pprint(response)
# data, meta_data = ts.get_monthly(symbol= ".inix")
# pprint(data.head(2))

alpha_df = response["Monthly Time Series"]
#alpha_df

alpha_df2= pd.DataFrame.from_dict(alpha_df, orient = 'index')

# alpha_df2.rename_axis('Date')
alpha_df3 = alpha_df2.reset_index()
alpha_df4=alpha_df3.rename(columns= {"index":"Date","1. open":"Open","4. close": "Close","5. volume": "Volume"})
alpha_v= alpha_df4.drop(columns=["2. high","3. low"])
alpha_v[["Open", "Close"]] = alpha_v[["Open", "Close"]].astype(float)
#alpha_v.head(10)

# new data frame with split value columns 
market_data2 = alpha_v["Date"].str.split("-", n = 1, expand = True) 
  
# making seperate first name column from new data frame 
alpha_v["Year"] = market_data2[0] 
  
# making seperate last name column from new data frame 
alpha_v["stuff"] = market_data2[1] 

#market["Day"] = market_data[2]
  
# Dropping old Name columns 
#market.drop(columns =["Date"], inplace = True) 

# new data frame with split value columns 
market_data2 = alpha_v["stuff"].str.split("-", n = 1, expand = True) 

# making seperate first name column from new data frame 
alpha_v["Month"] = market_data2[0] 
  
# making seperate last name column from new data frame 
alpha_v["Day"] = market_data2[1] 
# market2.drop(columns =["High"], inplace = True) 
# market.drop(columns =["Low"], inplace = True) 
# # market.drop(columns =["Open"], inplace = True) 
# market.drop(columns =["Close"], inplace = True) 
# market2.rename(columns={'Adj Close':'Close'}, inplace=True)

# Dropping old Name columns 
alpha_v.drop(columns =["stuff"], inplace = True) 
# df display 
#alpha_v.head(10)

alpha_v2 = alpha_v
alpha_v3 = alpha_v

#initalize market types
high_profit_market_av = alpha_v
low_profit_market_av = alpha_v

def label_nov_apr_month2 (row):
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

def label_may_oct_month2 (row):
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

def label_month2 (row):
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
alpha_v2 = alpha_v.dropna(axis = 0, how ='any') 
alpha_v2.drop(alpha_v2.index[:3], inplace=True)
alpha_v2 = alpha_v2.reset_index(drop = True)

#calculate returns e ery month and every 6 months
alpha_v2['pct_pop'] = alpha_v2['Open'].pct_change()
alpha_v2['pct_sos'] = alpha_v2['Open'].pct_change(6)
alpha_v2['Season'] = alpha_v2.apply (lambda row: label_month2 (row),axis=1)

#create label column and drop NaN - idea 1
high_profit_market_av['Season'] = high_profit_market_av.apply (lambda row: label_nov_apr_month2 (row),axis=1)
high_profit_market_av = high_profit_market_av.dropna(axis = 0, how ='any') 
high_profit_market_av = high_profit_market_av.reset_index(drop = True)
high_profit_market_av.drop(alpha_v.index[:1], inplace=True)
high_profit_market_av = high_profit_market_av.reset_index(drop = True)

low_profit_market_av['Season'] = low_profit_market_av.apply (lambda row: label_may_oct_month2 (row),axis=1)
low_profit_market_av = low_profit_market_av.dropna(axis = 0, how ='any') 
low_profit_market_av = low_profit_market_av.reset_index(drop = True)
low_profit_market_av['Return'] = low_profit_market_av.Open.pct_change(1)

###################################################


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
      return 'Apr-Nov'
   if row['Month'] == '05' :
      return 'May-Dec'
   if row['Month'] == '06' :
      return 'Jun-Jan'
   if row['Month'] == '07' :
      return 'Jul-Feb'
   if row['Month'] == '08' :
      return 'Aug-Mar'
   if row['Month'] == '09' :
      return 'Sep-Apr'
   if row['Month'] == '10' :
      return 'Oct-May'
   if row['Month'] == '11' :
      return 'Nov-Jun'
   if row['Month'] == '12' :
      return 'Dec-Jul' 
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
#------------------------------------------------------------------

#Filter market2 df by Month Nov(11) and May(5)
Nov_df = market2.loc[market2["Month"] == "11" , : ]
May_df =  market2.loc[market2["Month"] == "05" , : ]
May_df = May_df.dropna()

#Calculate average seasonal percent changes
Nov_pop_avg = Nov_df["pct_sos"].mean() 
May_pop_avg = May_df["pct_sos"].mean()


#BAR CHART--------------------------------------------------

#Create list of seasonal averages for bar chart values
seas_avgs = [May_pop_avg,Nov_pop_avg]

#Create x value locations
x_axis = np.arange(len(seas_avgs))

#Create tick labels
ticks = market2["Season"].unique()

#Set space between bars
bar_pos = [0,0.3]

#Create plot
#plt.bar(bar_pos,
#        seas_avgs,
#        width = 0.3,
#        color = ["b","g"],
#        tick_label = ticks, 
#        align = "center")


May_Oct = market2.loc[market2["Season"] == "May-Oct", : ]
#Filter May_Oct df by Month to only show pop returns  


Nov_Apr = market2.loc[market2["Season"] == "Nov-Apr" , :]

#Calculate average pop and sos returns for different time periods
May_Oct_Avgp = May_Oct["pct_pop"].mean()
May_Oct_Avgs = May_Oct["pct_sos"].mean()

May_Oct_Avgs




#---------------------------------------------
# Average Total Return by Month
#---------------------------------------------

season = market2.groupby(["Season"]).mean()["pct_sos"]
sort = pd.DataFrame(season)
sort = sort.sort_values(by='pct_sos', ascending=False)
sort2 = sort.reset_index()
barheight = sort2["pct_sos"]
ax = plt.subplots(figsize=(10,4))

# Generate the Plot 
x_axis = np.arange(len(season))

plt.bar(x_axis,barheight , color="gold", align="center")

plt.title("Average Total Return (Seasons)")
plt.ylabel("Total Return")
plt.xlabel("Time (Seasons)")
plt.grid(True)


x = ['Dec-May', 'Nov-Apr', 'Jan-Jun', 'Apr-Nov', 'Feb-Jul', 'Mar-Aug', 'Apr-Sep', 'Jul-Dec', 'May-Oct', 'Jun-Nov']
x_pos = [i for i, _ in enumerate(x)]
plt.xticks(x_pos, x)



# Save the Figure
plt.savefig("avg_total_ret_sea.png")

# Show the Figure
plt.show()


# year_season = market2.groupby(['Year', 'Season'])['pct_sos'].mean()
# year_season = pd.DataFrame(year_season)
# year_season = reset_index
may_dec = market2.loc[market2["Season"] == "May-Dec" , : ]
apr_nov = market2.loc[market2["Season"] == "Apr-Nov" , : ]

plt.figure(figsize=(15, 6), dpi=80)

# Generate the Plot
plt.plot(may_dec["pct_sos"], "bo", linestyle="dashed", markersize=10, linewidth=1.5)
plt.plot(apr_nov["pct_sos"], "go", linestyle="dashed", markersize=10, linewidth=1.5)

plt.title("Average Total Return (May-Dec & Apr-Nov)")
plt.ylabel("Total Return")
plt.xlabel("Month in Season")
plt.grid(True)

# plt.legend
blue_patch = mpatches.Patch(color='Blue', label='May-Dec')
green_patch = mpatches.Patch(color='Green', label='Apr-Nov')
plt.legend(handles=[blue_patch, green_patch])

# Save the Figure
plt.savefig("may_dec_apr_nov.png")

# Show the Figure
plt.show()

jul_feb = market2.loc[market2["Season"] == "Jul-Feb" , : ]
aug_mar = market2.loc[market2["Season"] == "Aug-Mar" , : ]
sep_apr = market2.loc[market2["Season"] == "Sep-Apr" , : ]

plt.figure(figsize=(15, 6), dpi=80)

# Generate the Plot
plt.plot(jul_feb["pct_sos"], "bo", linestyle="dashed", markersize=10, linewidth=1.5)
plt.plot(aug_mar["pct_sos"], "go", linestyle="dashed", markersize=10, linewidth=1.5)
plt.plot(sep_apr["pct_sos"], "ro", linestyle="dashed", markersize=10, linewidth=1.5)

plt.title("Average Total Return (Jul-Feb, Aug-Mar, & Sep-Apr)")
plt.ylabel("Total Return")
plt.xlabel("Month in Season")
plt.grid(True)

# plt.legend
blue_patch = mpatches.Patch(color='Blue', label='May-Dec')
green_patch = mpatches.Patch(color='Green', label='Aug-Mar')
red_patch = mpatches.Patch(color='Red', label='Sep-Apr')
plt.legend(handles=[blue_patch, green_patch, red_patch])

# Save the Figure
plt.savefig("may_dec_apr_nov.png")

# Show the Figure
plt.show()
