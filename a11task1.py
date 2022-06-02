# -*- coding: utf-8 -*-
"""
Created on Tue Apr  5 11:25:31 2022

@author: evely
"""

#Evelyn Baranski
#4/5/22
#Assignment 11: Backtesting


#This assignment, assignment 11 task 1, is working with
#Bollinger bands and backtesting a strategy

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt



def create_bollinger_bands(df, window  = 21, no_of_std = 1, column_name = ''):
    """This function will create bollinger bands and return df
    
    df = pd datagrame containing 1 or more columns of numerical data observations
    to create bollinger bands
    
    window = # of days to use in creating roling mean and std
    
    no_of_Std = # of standard devs to use in calculating bollinger bands
    
    column_name = name of column to use from Dataframe"""
    
    #creating df to hold new variables & setting index
    bollinger_df = pd.DataFrame(index = df.index)

    #if column not provided, use first column
    if column_name == '':
        column_name = 0
    
    #creating observation -- df[column_name]
    bollinger_df["Observations"] = df[column_name]
    
    #getting rolling mean for each observation
    bollinger_df["RollingMean"] = bollinger_df["Observations"].rolling(window).mean()
    
    stdev = (bollinger_df["Observations"].rolling(window).std()) * no_of_std
    
    #creating upper and lower bounds - rolling + 1 stdev
    bollinger_df["UpperBound"] = bollinger_df["RollingMean"] + stdev
    bollinger_df["LowerBound"] = bollinger_df["RollingMean"] - stdev
    
    return bollinger_df



def create_long_short_position(df):
    """This function evalauted the data elements in the 
    observation column against bollinger bands in upperbound
    and lowerbound columns. Function will apply a long/short
    strategy -- create a long position (+1) when observation
    crosses above the upperbound, and create a short positon 
    (-1) when crossing below lower bound.
    
    returns new pd df containing new column - position.
    
    df entered has columns ['observations', rollingmean,
    lowerbound, upperbound]"""
    
    #creating a position df and setting index to date
    position_df = pd.DataFrame(index = df.index)
    
    position_df["Position"] = 1
    
    #counting number of null observations for for loop range
    count_nan = df['Observations'].isna().sum()
    current = 1
    
    #for loop to iterate through
    for col in range(count_nan, len(position_df)):
        
        if df['Observations'].iloc[col] > df['UpperBound'].iloc[col]:
            position_df["Position"][col] = 1
        
        
        elif df['Observations'].iloc[col] < df['LowerBound'].iloc[col]:
            position_df["Position"][col] = -1     
        
        else:
            position_df["Position"][col] = current
        
        current = position_df["Position"][col]

    
    return position_df



def long_short(df):
    """signal long short strategy"""
    
    strat = pd.DataFrame(index = df.index)
    
    count_nan = bb["Observations"].isna().sum()
    
    strat["position"] = 1
    
    for x in range(count_nan, len(df)):
        
        if df["Observations"].iloc[x] > df["UpperBound"].iloc[x]:
            strat["position"].iloc[x] = 1
        
        elif df["Observations"].iloc[x] < df["LowerBound"].iloc[x]:
            strat["position"].iloc[x] = -1
            
        elif df["Observations"].iloc[x] < df["UpperBound"].iloc[x] and df["Observations"].iloc[x] > df["LowerBound"].iloc[x]:
            strat["position"].iloc[x] = strat["position"].iloc[x - 1]
    
    return strat
        
    
def calculate_long_short_returns(df, position, column_name = ''):
    """This function returns a pd df containing the columns
    [Market Return, Strategy Return, & Abnormal Return] taking in parameters
    
    df: pd df with an asset price data series
    positon: pd df with index as df w postion column
    column_name: column to use from dataframe containing asset prices"""
    
    #creating new dataframe with same index as df
    returns_df = pd.DataFrame(index = df.index)
    
    #if column name = ''
    if column_name == '':
        column_name = 0
    
    
    
    #all variables in new data frame
    returns_df["Market Return"] = df[column_name] / df[column_name].shift(1) - 1
    returns_df["Strategy Return"] = position["Position"] * returns_df["Market Return"]
    returns_df["Abnormal Return"] = returns_df["Strategy Return"] - returns_df["Market Return"]
    
    return returns_df
    



def plot_cumulative_returns(df):
    """This function creates a plot of cumulative returns for each column
    within df, a pd, df"""
    
    df.cumsum().plot()
    
    
    






if __name__ == '__main__':
    
    # g = pd.read_csv('GOOG.csv')
    # g.index = g['Date']
    
    # g.head()
    
    # bb = create_bollinger_bands(g, 10, 2, "Adj Close")
    # position = create_long_short_position(bb)
    # position.plot()
    
    
    df = pd.read_csv("SPY.csv")
    df.index = df["Date"]
    
    df = df.loc["2020-01-01" : "2020:12:31"]
    bb = create_bollinger_bands(df, 10, 2, "Adj Close")
    
    print(bb)
    
    bb.plot()
    
    position = create_long_short_position(bb)
    
    position2 = long_short(bb)
    
    
    
    returns = calculate_long_short_returns(df, position, "Adj Close")
    
    returns2 = calculate_long_short_returns(df, position2, "Adj Close")
    
    returns.plot()
    
    returns2.plot()
    
    #plot_cumulative_returns(returns)
    
    
    print(position)
    
    print(position2)
    
    pos = plot_cumulative_returns(df)
    
    pos
    
    # position.plot()

    