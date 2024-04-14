import yfinance as yf
import pandas as pd
import pandas_ta as ta
import numpy as np
from datetime import datetime as dt
import matplotlib.pyplot as plt
from datetime import timedelta as delta
import numpy as np
import os
import seaborn as sb
from tqdm import tqdm




from Portfolio import *
from Strategy import *
from Trade import *
from TradingPlot import *

class TradingSystem:

   

    def __init__(self):
        self.strategy = None
        self.datas = {}
        self.portfolio = Portfolio()
        self.calendar = None
        self.current_idx = None
        self.format = '%Y-%m-%d %H:%M:%S'
        
        






    def Run(self):
         for idx in tqdm(self.calendar):
            self.current_idx = idx
            self.strategy.current_idx = self.current_idx
            # fill orders from previus period
            self.FillOrders()
            
            # Run the strategy on the current bar
            self.strategy.OnBar()
            # print(idx)


    def FillOrders(self, verbose = True):
        '''This method  handles all current orders. If an order can be fulfilled it creates a new Trade object and adjusts the cash value

        - We can only buy if the cash balance is sufficient.
        - We can only sell if the we have enough shares in the portfolio.
        
        '''
        for order in self.strategy.orders:
            canFill = False
        
            ticker = order.ticker
            data = self.datas[order.ticker]
            time = self.current_idx.strftime(self.format)
            
            # print(data[self.current_idx])

            price = data.loc[self.current_idx, 'Open'] 
            # print(price)
            # print(self.portfolio)
            # print(price)

            if order.side == 'buy' and self.portfolio.HasCash(price * order.size):
                    canFill = True 
            elif order.side == 'sell' and self.portfolio.HasPositions(ticker, order.size):
                    canFill = True
           
            if canFill:
                t = Trade(
                    order.ticker,
                    order.side,
                    order.size,
                    price,
                    self.current_idx)
            

                # The strategy keeps track of all the past trades, so that they can be analyzed later
                # Then add the corresponding position to the portfolio
                self.strategy.trades.append(t)
                self.portfolio.AddPosition(order.ticker, t.size)
                self.portfolio.AddCash( -t.price * t.size)
                print('Order filled', 'Ticker:', order.ticker, 'Size: ', order.size, 'Price: ', price)
            else:
                pass
                print('Order cannot be filled', 'Time: ', self.current_idx)
            # print('New portfolio:')
            # print(self.portfolio)

        self.strategy.orders = []

    def AddData(self, ticker, startDate, endDate):
        ''' Collects the financial data of the asset underlying 'ticker' in the date range between 'startDate' and 'endDate'.
        Currently only data from 'yahooFinance' is supported.'''

        self.datas[ticker] = yf.download(ticker, start=startDate, end=endDate)
        self.calendar = self.datas[ticker].index


    def GetPrice(self, ticker, time, col = 'Open'):
        '''Returns the price of teh asset underlying 'ticker' at the time 'time'. 
        'col' determines which value is used. The standard values from YahooFinance are
        'Open, Close, Adj Close, High, Low, Volume.'''
        return self.datas[ticker].loc[self.current_idx,col] 
    
    def SetStrategy(self, strategy):

        self.strategy = strategy
        self.strategy.datas = self.datas
        self.strategy.tickers = list(self.datas.keys())
        self.strategy.portfolio = self.portfolio


    def GetStats(self):
        '''Returns metric for analyzing the results of the backtesting. Currently on the total return is implemented.'''

        metrics = {}
        # Total return conssits of current value of the portfolio which is the sum of the cash value and the value of the current
        # assets
        totalReturn = self.portfolio.cash
        for ticker in self.datas:
            totalReturn += self.GetPrice(ticker, self.current_idx, col = 'Close') *self.portfolio.GetPositionSize(ticker)
        totalReturn /= self.portfolio.initialCash
        metrics['Total Return'] = 100*(totalReturn -1)
        return metrics

    def GetPortfolioValue(self):
        ''' Returns the current value of the portfolio by adding the cash value to the current value of all positions in the
        portfolio.'''
        totalValue = self.portfolio.cash
        for ticker in self.datas:
            totalValue += self.GetPrice(ticker, self.current_idx, col = 'Close') *self.portfolio.GetPositionSize(ticker)
        return totalValue



        
       





# ticker = "AAPL"
# startDate = "2020-01-01"
# endDate = "2020-01-10"


# trader = TradingSystem()
# trader.AddData(ticker, startDate, endDate)

# trader.SetStrategy(BasicStrategy(trader.portfolio,trader.datas))
# trader.portfolio.AddCash(10000)
# # print(trader.portfolio)
# trader.Run()
# PlotStockData(trader.datas[ticker])
# for x in trader.strategy.trades:
#     print(x)
# print(data.loc[trader.current_idx, 'Open'])
# print(type(data.loc[trader.current_idx, 'Open']))
# print(trader.strategy.tickers)
# 
# print(trader.portfolio.cash)


