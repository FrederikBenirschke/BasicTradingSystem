import yfinance as yf
import pandas as pd
# import pandas_ta as ta
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
		self.log = {}
		
		






	def Run(self):
		''' Performs a backtest of the trading strategy prescribed in self.strategy.
		The backtest consists of two steps. For each time step:
		- Handle all orders that were created at the end of the previous day. An order will be filled if there are enough
		funds to buy or enough stocks to sell.
		- Run the OnBar() function of self.strategy and create new orders.'''
		for idx in tqdm(self.calendar):
			self.current_idx = idx
			self.strategy.current_idx = self.current_idx
			# fill orders from previus period
			self.FillOrders()
			
			# Run the strategy on the current bar
			self.strategy.OnBar()
			self.Log(self.current_idx)
			# print(idx)


	def FillOrders(self):
		'''This method  handles all current orders. If an order can be fulfilled,
		 it creates a new Trade object and adjusts the cash value.

		- We can only buy if the cash balance is sufficient.
		- We can only sell if the we have enough shares in the portfolio.
		'''
		for order in self.strategy.orders:
			canFill = False
		
			ticker = order.ticker
			data = self.datas[order.ticker]
			time = self.current_idx.strftime(self.format)
			

			price = data.loc[self.current_idx, 'Open'] 
			# For a buy order check if there are sufficients funds in the portfolio to buy assets
			if order.side == 'buy' and self.portfolio.HasCash(price * order.size):
					canFill = True 
			# For a sell order check if there are enough assets available to sell
			elif order.side == 'sell' and self.portfolio.HasPosition(ticker, order.size):
					canFill = True
		   
			# If the order can be filled create a new trade
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
				# print('Order filled', 'Ticker:', order.ticker, 'Size: ', order.size, 'Price: ', price)
			else:
				pass
				# print('Order cannot be filled', 'Time: ', self.current_idx)
			
		# Clear all orders in the strategy
		self.strategy.orders = []

	def AddData(self, ticker, startDate, endDate):
		''' Collects the financial data of the asset underlying 'ticker' in the date range between 'startDate' and 'endDate'.
		Currently only data from 'yahooFinance' is supported.
		Parameters
		----------
		ticker :'string'
			The name of the financial asset
		
		startDate/endDate: 'string' in Date format
			Downloads the financial data for 'ticker' between startDate and endDate
		'''
		self.datas[ticker] = yf.download(ticker, start=startDate, end=endDate)
		self.calendar = self.datas[ticker].index

	def AddCleanData(self, ticker, df):
		# ''' Adds the financial data of the asset underlying 'ticker', needs to be already collected, cleaned and scaled.'''
		self.datas[ticker] = df
		
		self.calendar = df.index

	def GetPrice(self, ticker, time, col = 'Open'):
		'''Returns the price of the asset underlying 'ticker' at the time 'time'. 
		Args:

		ticker(str): name of the asset
		time(TimeStamp): price at the given time 
		
		col(Index): determines which column of the data frame is used.
		 The standard values from YahooFinance are
		'Open, Close, Adj Close, High, Low, Volume.'''
		return self.datas[ticker].loc[self.current_idx,col] 
	
	def SetStrategy(self, strategy):
		''' Sets the strategy for the backtest.
		Args:
		strategy(Strategy): the strategy to be used.'''
		self.strategy = strategy
		self.strategy.datas = self.datas
		self.strategy.tickers = list(self.datas.keys())
		self.strategy.portfolio = self.portfolio
		# Log is used to track the value over time
		self.log = pd.DataFrame(index=self.calendar, columns =['Portfolio'])


	def Log(self,time):
		self.log.at[time, 'Portfolio'] = self.GetPortfolioValue()


	def GetStats(self):
		'''Returns metrics for analyzing the results of the backtesting. 
		Currently the following metrics are provided:
		-the total return
		-Average return
		-volatility
		-risk-ree return(default risk-free rate is 1%)
		-Sharpe ratio'''

		metrics = {}
		# Total return consits of current value of the portfolio which is the sum of the cash value and the value of the current
		# assets
		totalReturn = self.portfolio.cash
		for ticker in self.datas:
			totalReturn += self.GetPrice(ticker, self.current_idx, col = 'Close') * self.portfolio.GetPositionSize(ticker)
		totalReturn /= self.portfolio.initialCash
		metrics['Total Return'] = 100*(totalReturn -1)


		# Assuming a risk-free rate of 1%
		r= 0.01
		# Computes the risk free return on the initial cash value
		for time in self.calendar:
			self.log.at[time,'Riskfree'] =self.portfolio.initialCash* np.exp(r* (time- self.calendar[0]).days/365.25)



		metrics['Volatility'] = self.log['Portfolio'].std().mean()/self.log['Portfolio'].mean()
		metrics['Average Return'] = ((self.log['Portfolio'] - self.portfolio.initialCash)/self.portfolio.initialCash).mean()
		
		# length of time series in years
		time = (self.calendar[-1]- self.calendar[0]).days/365.25
		metrics['Riskfree Return'] = self.portfolio.initialCash* np.exp(r* time)
		metrics['Riskfree Return']  = (metrics['Riskfree Return']  - self.portfolio.initialCash)/self.portfolio.initialCash
		# Sharpe ratio is (Excess return - risk free return)/ Volatility
		metrics['Sharpe'] = (metrics['Average Return'] -metrics['Riskfree Return'])/metrics['Volatility']
		return metrics

	def GetPortfolioValue(self):
		''' Returns the current value of the portfolio by adding the cash value to the current value of all positions in the
		portfolio.'''
		totalValue = self.portfolio.cash
		for ticker in self.datas:
			totalValue += self.GetPrice(ticker, self.current_idx, col = 'Close') *self.portfolio.GetPositionSize(ticker)
		return totalValue

if __name__ == "__main__":
	pass




		
	   








