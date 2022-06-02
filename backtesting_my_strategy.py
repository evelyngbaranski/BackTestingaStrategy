# -*- coding: utf-8 -*-
"""
Created on Wed Apr  6 16:43:33 2022

@author: evely
"""

#Evelyn Baranski
#4/5/22
#Assignment 11: Backtesting


#This assignment, assignment 11 task 2, is backtesting my own strategy


### Assumptions: can buy fractional shares, no restrictions on short selling & no
### margin requirements, no taxes


### Trading / frictional costs
#trading and comission 2 ways: 1st way, 0 comm, 2nd way with $10 fixed trading fee


### Strategy -- interest rate drops below lowerbound, buy 1% VOO
### interest rate rises above upperbound, sell 1% of VOO


### Can implement strategy functions on whichever stocks/commodity CSV files
### Overall strategy based on two securities that have inverse relationship / correlation


from a11task1 import *

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt


def strategy(inv, inv_name, comp, comp_name):
    """Creating function to read in the CSVs given for the strategy.
    inv = csv file of the investment
    comp = csv file of the comparable -- what investment strategy on inv is being 
    based on.
    
    inv_name and comp_name -- typed names for each CSV
    
    Main Strategy, applying to VOO and interest rates: for every decrease
    below lowerbound of the interest rate, buying 1% of VOO, for each 
    increase above upperbound of the interest rate, selling 1% of VOO
    """
    
    #making indexes date, converting date to date time
    inv_df = pd.read_csv(inv)
    inv_df['Date'] = pd.to_datetime(inv_df['Date'])
    inv_df.index = inv_df["Date"]
    inv_df = inv_df.sort_index()
    
    comp_df = pd.read_csv(comp)
    comp_df['Date'] = pd.to_datetime(comp_df['Date'])
    comp_df.index = comp_df["Date"]
    comp_df = comp_df.sort_index()


    #creating overall strategy dataframe
    strategy_df = pd.DataFrame()
    
    comp_bollinger_df = create_bollinger_bands(comp_df, 21, 1, 'Price')
    
    #Creating columns
    strategy_df[f"{inv_name} price"] = inv_df["Price"]
    strategy_df[f"{comp_name} price"] = comp_df["Price"]
    strategy_df["Observation Comp"] = comp_bollinger_df["Observations"]
    strategy_df["RollingMean"] = comp_bollinger_df["RollingMean"]
    strategy_df["UpperBound"] = comp_bollinger_df["UpperBound"]
    strategy_df["LowerBound"] = comp_bollinger_df["LowerBound"]
    
    
    
    #Creating signal -- when to take investment action
    strategy_df["signal"] = 1
    
    #creating current at start val 0
    current = 0
    
    #for loop -- if comp < lowerbound: creating signal for when to use the strategy
    for col in range(21, len(strategy_df)):
        
        if strategy_df["Observation Comp"].iloc[col] < strategy_df["LowerBound"].iloc[col]:
            strategy_df["signal"][col] = 1
        
        elif strategy_df["Observation Comp"].iloc[col] > strategy_df["UpperBound"].iloc[col]:
            strategy_df["signal"][col] = -1
        
        else:
            strategy_df["signal"][col] = current
        
        #setting current signal to signal put in place -- for no signal change
        current = strategy_df["signal"][col]
    
    
    
    #getting column for total amoount invested based on signal
    #setting current investment to 100 -- calculating amount invested based on signal
    current_investment = 10000
    strategy_df["TotalInv"] = 10000
    
    strategy_df["TradingFee"] = 0
    
    #for loop iterating through -- also getting times when there's trading fee
    for col in range(21, len(strategy_df)):
       
        #if signal == 1, implementing strategy
        if strategy_df["signal"].iloc[col] == 1:
            strategy_df["TotalInv"][col] = current_investment * 1.01
            
            #setting trading fee to 10
            strategy_df["TradingFee"][col] = 10
            
        
        elif strategy_df["signal"].iloc[col] == -1:
            strategy_df["TotalInv"][col] = current_investment * .99
            
            #setting trading fee to 10
            strategy_df["TradingFee"] = 10
        
        #otherwise keeping investment at current level & trading fee @ 0
        else:
            strategy_df["TotalInv"][col] = current_investment 
            strategy_df["TradingFee"] = 0
        
        #adjusting current investment amount
        current_investment = strategy_df["TotalInv"][col]
    
    

    #Getting returns columns
    #getting market return -- if investment held not sold at all, and market r
    strategy_df["MarketRet"] = ((strategy_df[f"{inv_name} price"] / strategy_df[f"{inv_name} price"].shift(1) - 1))
    
    strategy_df["MarketRetDol"] = strategy_df["MarketRet"] * 10000
    
    
    
    #getting return when strategy implemented
    strategy_df["StratRetDol"] = (strategy_df["MarketRet"] * strategy_df["TotalInv"]) 
    
    #getting dollar return with trading fees in place - $10 per trade
    strategy_df["StratRetDolFee"] = (strategy_df["MarketRet"] * strategy_df["TotalInv"]) \
        - strategy_df["TradingFee"]
    
    
    #Getting abnormal return
    strategy_df["AbnormalRet"] = strategy_df["StratRetDol"] - strategy_df["MarketRetDol"]
    
    return strategy_df

    

def graph_str(strat_df):
    """Plotting strategy to see how it adds up compared to the standard
    
    plotting strategy cumulative dollar returns against cumulative
    dollar market returns and cumulative dollar abnormal returns"""
    
    #Plotting cumulative returns of $ amount Market Return and Strategy Return
    cumulative = strat_df[["MarketRetDol", "StratRetDol"]].copy()
    cumulative.cumsum().plot(title = "Cumulative $ Returns - Market v Strategy, no fee")

    #Plotting against returns with $10 fee
    cumulative2 = strat_df[["MarketRetDol", "StratRetDolFee"]].copy()
    cumulative2.cumsum().plot(title = "Cumulative $ Returns - Market v Strategy, w fee")
    
    
    #Plotting cumulative returns with abnromal returns
    cumulative3 = strat_df[["MarketRetDol", "StratRetDol", "AbnormalRet"]].copy()
    cumulative3.cumsum().plot(title = "Cumulative $ Returns - Market v Strategy v Abnormal")
    



#Descriptive statistics of strategy
def desc_stat(strat_df):
    """Printing out descriptive statistics for how strategy compares with standard
    strategy
    
    mean rate of return, standard deviation
    cumulative abnormal returns
    """
    
    
    cumulative3 = strat_df[["MarketRetDol", "StratRetDol", "AbnormalRet"]].copy()
    print(cumulative3.describe())
    
    print("Cumulative Abnormal Returns: ")
    print(strat_df["AbnormalRet"].cumsum())

    
    


    





if __name__ == '__main__':
    inv = 'VOO.csv'
    comp = 'yield.csv'
    
    s = (strategy(inv, 'VOO', comp, 'Yield'))
    
    s.loc["2020-01-01" : "2020-12-31"]
    
    print(s)
    
    s.plot()
    
    graph_str(s)
    
    desc_stat(s)
    
    
    
    
    
    
    




