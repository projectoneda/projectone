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


#structure data - idea two - used

def label_month (row):
  if row['Month'] == '01' :
     return 'Jul-Dec'
  if row['Month'] == '02' :
     return 'Aug-Jan'
  if row['Month'] == '03' :
     return 'Sep-Feb'
  if row['Month'] == '04' :
     return 'Oct-Mar'
  if row['Month'] == '05' :
     return 'Nov-Apr'
  if row['Month'] == '06' :
     return 'Dec-May'
  if row['Month'] == '07' :
     return 'Jan-Jun'
  if row['Month'] == '08' :
     return 'Feb-Jul'
  if row['Month'] == '09' :
     return 'Mar-Aug'
  if row['Month'] == '10' :
     return 'Apr-Sep'
  if row['Month'] == '11' :
     return 'May-Oct'
  if row['Month'] == '12' :
     return 'Jun-Nov'
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

market2.head()

# Export the results to text file
market2.to_csv('market2.csv', index = False)

# Track various financial parameters

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
#
#plt.show()


May_Oct = market2.loc[market2["Season"] == "May-Oct", : ]
#Filter May_Oct df by Month to only show pop returns  
May_Oct.head()


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

sort3 = sort2.drop(columns=['pct_sos'])
sort3 = sort3["Season"].tolist()
x_pos = [i for i, _ in enumerate(sort3)]
plt.xticks(x_pos, sort3)



# Save the Figure
plt.savefig("avg_total_ret_sea.png")

# Show the Figure
plt.show()
#---------------------------------------------
# Average Total Return by Yeah and Season
#  -May-Dec & Apr-Nov
#---------------------------------------------


#Create dataframe summarized by year and season
year_season = market2.groupby(['Year', 'Season'])['pct_sos'].mean()
year_season = pd.DataFrame(year_season)
year_season = year_season.reset_index()

year_season.head()
#
##Remove 1950 (the year) from dataframe
#year_season["Year"] = pd.to_numeric(year_season["Year"])
#
#may_dec = year_season.loc[year_season["Season"] == "May-Dec" , : ]
#apr_nov = year_season.loc[year_season["Season"] == "Apr-Nov" , : ]
#
#plt.figure(figsize=(15, 6), dpi=80)
#
## Generate the Plot
#plt.plot(may_dec["pct_sos"], "bo", linestyle="dashed", markersize=10, linewidth=1.5)
#plt.plot(apr_nov["pct_sos"], "go", linestyle="dashed", markersize=10, linewidth=1.5)
#
#plt.title("Average Total Return (May-Dec & Apr-Nov)")
#plt.ylabel("Total Return")
#plt.xlabel("Year & Season")
#plt.xticks()
#plt.grid(True)
#
## plt.legend
#blue_patch = mpatches.Patch(color='Blue', label='May-Dec')
#green_patch = mpatches.Patch(color='Green', label='Apr-Nov')
#plt.legend(handles=[blue_patch, green_patch])
#
## Save the Figure
#plt.savefig("may_dec_apr_nov.png")
#
## Show the Figure
#plt.show()
#
##---------------------------------------------
## Average Total Return by Yeah and Season
##  -May-Dec & Apr-Nov
##---------------------------------------------
#
#
#jul_feb = year_season.loc[year_season["Season"] == "Jul-Feb" , : ]
#aug_mar = year_season.loc[year_season["Season"] == "Aug-Mar" , : ]
#sep_apr = year_season.loc[year_season["Season"] == "Sep-Apr" , : ]
#
#plt.figure(figsize=(15, 6), dpi=80)
#
##Define y variables for plot
#y_jul_feb = jul_feb["pct_sos"].dropna()
#y_jul_feb
#
#
##Define year variable for x tick labels
#years = year_season["Year"].unique()
#years_list = year_season["Year"].unique().tolist()
#length = len(years_list)
#length 
#
## Generate the Plot
#plt.plot(y_jul_feb, "bo", linestyle="dashed", markersize=10, linewidth=1.5)
#plt.plot(aug_mar["pct_sos"], "go", linestyle="dashed", markersize=10, linewidth=1.5)
#plt.plot(sep_apr["pct_sos"], "ro", linestyle="dashed", markersize=10, linewidth=1.5)
#
#plt.title("Average Total Return (Jul-Feb, Aug-Mar, & Sep-Apr)")
#plt.ylabel("Total Return")
#plt.xlabel("Year & Season")
#plt.grid(True)
#
##Set x axis tick labels
#
#tick_locs = plt.xticks()
#tick_locs
#
#plt.xticks(tick_locs,years_list)
#
## plt.legend
#blue_patch = mpatches.Patch(color='Blue', label='May-Dec')
#green_patch = mpatches.Patch(color='Green', label='Aug-Mar')
#red_patch = mpatches.Patch(color='Red', label='Sep-Apr')
#plt.legend(handles=[blue_patch, green_patch, red_patch])
#
## Save the Figure
#plt.savefig("may_dec_apr_nov.png")
#
## Show the Figure
#plt.show()


#----------------------------------------------------------------
#DON START HERE FOR NOV 29 LAST MINUTE CHANGES
#JOSE SCROLL DOWN TO LINE 1000
#----------------------------------------------------------------

#THIS WAS ALL JUST COPIED FROM LINES 489-572 ABOVE SO THAT I COULD COMMENT THEM OUT
#DID THIS SO THAT ALL NOV 29 CHANGES WOULD START AT LINE 579

#Remove 1950 (the year) from dataframe
#Convert Year column from object to numeric
year_season["Year"] = pd.to_numeric(year_season["Year"])
year_season = year_season.drop(year_season[year_season.Year < 1951].index)

#Create variable to hold list of years
years = year_season["Year"].unique()
years_list = year_season["Year"].unique().tolist()


may_dec = year_season.loc[year_season["Season"] == "Dec-May" , : ]
apr_nov = year_season.loc[year_season["Season"] == "Nov-Apr" , : ]

may_dec.head()

plt.figure(figsize=(15, 6), dpi=80)

# Generate the Plot
plt.plot(years_list,may_dec["pct_sos"], "bo", linestyle="dashed", markersize=10, linewidth=1.5)
plt.plot(years_list,apr_nov["pct_sos"], "go", linestyle="dashed", markersize=10, linewidth=1.5)

plt.title("Average Percentage Change (May-Dec & Apr-Nov)")
plt.ylabel("Total Return")
plt.xlabel("Year & Season")
plt.xticks()
plt.grid(True)

# plt.legend
blue_patch = mpatches.Patch(color='Blue', label='May-Dec')
green_patch = mpatches.Patch(color='Green', label='Apr-Nov')
plt.legend(handles=[blue_patch, green_patch])

# Save the Figure
plt.savefig("may_dec_apr_nov.png")

# Show the Figure
plt.show()

#---------------------------------------------
# Average Total Return by Yeah and Season
#  -May-Dec & Apr-Nov
#---------------------------------------------



#jul_feb = year_season.loc[year_season["Season"] == "Jul-Feb" , : ]
#aug_mar = year_season.loc[year_season["Season"] == "Aug-Mar" , : ]
#sep_apr = year_season.loc[year_season["Season"] == "Sep-Apr" , : ]
#
#plt.figure(figsize=(15, 6), dpi=80)
#
##Define y variables for plot
#y_jul_feb = jul_feb["pct_sos"].dropna()
#y_jul_feb
#
#
##Define year variable for x tick labels
#years = year_season["Year"].unique()
#years_list = year_season["Year"].unique().tolist()
#length = len(years_list)
#length 
#
## Generate the Plot
#plt.plot(years_list,y_jul_feb, "bo", linestyle="dashed", markersize=10, linewidth=1.5)
#plt.plot(years_list,aug_mar["pct_sos"], "go", linestyle="dashed", markersize=10, linewidth=1.5)
##plt.plot(sep_apr["pct_sos"], "ro", linestyle="dashed", markersize=10, linewidth=1.5)
#
#plt.title("Average Total Return (Jul-Feb, Aug-Mar, & Sep-Apr)")
#plt.ylabel("Total Return")
#plt.xlabel("Year & Season")
#plt.grid(True)
#
##Set x axis tick labels
#
#tick_locs = plt.xticks()
#tick_locs
#
#plt.xticks(tick_locs,years_list)
#
## plt.legend
#blue_patch = mpatches.Patch(color='Blue', label='May-Dec')
#green_patch = mpatches.Patch(color='Green', label='Aug-Mar')
#red_patch = mpatches.Patch(color='Red', label='Sep-Apr')
#plt.legend(handles=[blue_patch, green_patch, red_patch])
#
## Save the Figure
#plt.savefig("may_dec_apr_nov.png")
#
## Show the Figure
#plt.show()

#---------------------------------------------
# Average Total Return by Yeah and Season
#  -Nov-Apr & May-Oct
#---------------------------------------------


nov_apr = year_season.loc[year_season["Season"] == "Nov-Apr" , : ]
may_oct = year_season.loc[year_season["Season"] == "May-Oct" , : ]

nov_apr.head()

plt.figure(figsize=(15, 6), dpi=80)

# Generate the Plot
plt.plot(years_list,nov_apr["pct_sos"], "bo", linestyle="dashed", markersize=10, linewidth=1.5)
plt.plot(years_list,may_oct["pct_sos"], "ro", linestyle="dashed", markersize=10, linewidth=1.5)

plt.title("Average Total Return (Nov-Apr & May-Oct)")
plt.ylabel("Total Return")
plt.xlabel("Year & Season")
plt.grid(True)

# plt.legend
blue_patch = mpatches.Patch(color='Blue', label='Nov-Apr')
red_patch = mpatches.Patch(color='red', label='May-Oct')
plt.legend(handles=[blue_patch, red_patch])

# Save the Figure
plt.savefig("may_dec_apr_nov.png")

# Show the Figure
plt.show()































































































































































































































































































































































































































#----------------------------------------------------------------
#JOSE START HERE FOR NOV 29 LAST MINUTE CHANGES
#DON DO NOT GO BEYOND THIS LINE....SERIOUSLY MAN
#----------------------------------------------------------------













































