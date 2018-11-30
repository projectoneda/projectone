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

#structure data

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

#Create tick labels
ticks = [ "Nov-Apr" , "May-Oct" ]

#Set bar locations on x axis
bar_pos = [0,0.65]

#Create plot
barc = plt.bar(bar_pos,
        seas_avgs,
        width = 0.4,
        color = ["b","g"],
        tick_label = ticks, 
        align = "center")

#Hide Y axis
barc_ax = plt.axes()
barc_y = barc_ax.axes.get_yaxis()
barc_y.set_visible(False)

#Add chart title and adjust y axis limit
plt.title("S&P500 Average % Return Over Time Period")
plt.ylim(0,0.08)

#Define function to label bar chart (i.e. copy it from the internet)
def autolabel(bars):
    """
    Attach a text label above each bar displaying its height
    Copied from https://matplotlib.org/examples/api/barchart_demo.html
    
    """
    for bar in bars:
        height = bar.get_height()
        plt.text(bar.get_x() + bar.get_width()/2.,1.05*height,
                 '{:.1%}'.format(height),
                 ha='center', va='bottom')
autolabel(barc)

plt.savefig("avg_returns_bar.png")

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
#plt.show()
#---------------------------------------------
# Average Total Return by Year and Season
#  -May-Dec & Apr-Nov
# Nov-Apr & Oct-Mar
#---------------------------------------------


#Create dataframe summarized by year and season
year_season = market2.groupby(['Year', 'Season'])['pct_sos'].mean()
year_season = pd.DataFrame(year_season)
year_season = year_season.reset_index()

#Remove 1950 (the year) from dataframe
#Convert Year column from object to numeric
year_season["Year"] = pd.to_numeric(year_season["Year"])
year_season = year_season.drop(year_season[year_season.Year < 1951].index)

#Create variable to hold list of years
years_list = year_season["Year"].unique().tolist()

Oct_Mar = year_season.loc[year_season["Season"] == "Oct-Mar" , : ]
Nov_Apr = year_season.loc[year_season["Season"] == "Nov-Apr" , : ]

plt.figure(figsize=(15, 6), dpi=80)

# Generate the Plot
plt.plot(years_list,Oct_Mar["pct_sos"], "bo", linestyle="dashed", markersize=10, linewidth=1.5)
plt.plot(years_list,Nov_Apr["pct_sos"], "go", linestyle="dashed", markersize=10, linewidth=1.5)

plt.title("Average Percentage Change (Oct-Mar & Nov-Apr)")
plt.ylabel("Total Return")
plt.xlabel("Year & Season")
plt.xticks()
plt.grid(True)

# plt.legend
blue_patch = mpatches.Patch(color='Blue', label='Oct-Mar')
green_patch = mpatches.Patch(color='Green', label='Nov-Apr')
plt.legend(handles=[blue_patch, green_patch])

# Save the Figure
plt.savefig("oct_mar_nov_apr.png")

# Show the Figure
#plt.show()

#---------------------------------------------
# Average Total Return by Yeah and Season
#  -May-Dec & Apr-Nov
#---------------------------------------------

jul_feb = year_season.loc[year_season["Season"] == "Feb-Jul" , : ]
aug_mar = year_season.loc[year_season["Season"] == "Mar-Aug" , : ]
sep_apr = year_season.loc[year_season["Season"] == "Apr-Sep" , : ]

plt.figure(figsize=(15, 6), dpi=80)

#Define y variables for plot
y_jul_feb = jul_feb["pct_sos"].dropna()
y_jul_feb


#Define year variable for x tick labels
years_list = year_season["Year"].unique().tolist() 

# Generate the Plot
plt.plot(years_list,jul_feb["pct_sos"], "yo", linestyle="dashed", markersize=10, linewidth=1.5)
plt.plot(years_list,aug_mar["pct_sos"], "mo", linestyle="dashed", markersize=10, linewidth=1.5)
plt.plot(years_list,sep_apr["pct_sos"], "ko", linestyle="dashed", markersize=10, linewidth=1.5)

plt.title("Average Total Return (Feb-Jul, Mar-Aug, & Apr-Sep)")
plt.ylabel("Total Return")
plt.xlabel("Year & Season")
plt.grid(True)

#Set x axis tick labels


plt.legend()

olive_patch = mpatches.Patch(color="y", label='Feb-Jul')
purple_patch = mpatches.Patch(color="m", label='Mar-Aug')
black_patch = mpatches.Patch(color="k", label='Apr-Sep')
plt.legend(handles=[olive_patch, purple_patch, black_patch])

# Save the Figure
plt.savefig("may_dec_apr_nov.png")

# Show the Figure
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
plt.plot(years_list,nov_apr["pct_sos"], "go", linestyle="dashed", markersize=10, linewidth=1.5)
plt.plot(years_list,may_oct["pct_sos"], "ro", linestyle="dashed", markersize=10, linewidth=1.5)

plt.title("Average Total Return (Nov-Apr & May-Oct)")
plt.ylabel("Total Return")
plt.xlabel("Year & Season")
plt.grid(True)

# plt.legend
green_patch = mpatches.Patch(color='green', label='Nov-Apr')
red_patch = mpatches.Patch(color='red', label='May-Oct')
plt.legend(handles=[green_patch, red_patch])

# Save the Figure
plt.savefig("may_dec_apr_nov.png")

# Show the Figure
#plt.show()


