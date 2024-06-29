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
		"""
		Initialize a new instance of the TradingSystem class.

		This method initializes the attributes of the TradingSystem class. 
		It sets the `strategy` attribute to None, the `datas` attribute to an empty dictionary,
		the `portfolio` attribute to a new instance of the Portfolio class,
		the `calendar` attribute to None, the `current_idx` attribute to None,
		the `format` attribute to '%Y-%m-%d %H:%M:%S',
		and the `log` attribute to an empty dictionary.

		Parameters:
		None

		Returns:
		None
		"""
		self.strategy = None
		self.datas = {}
		self.portfolio = Portfolio()
		self.calendar = None
		self.current_idx = None
		self.format = '%Y-%m-%d %H:%M:%S'
		self.log = {}
		self._transactionCost = 0
		
		






	def Run(self):
		"""
		Runs a backtest of the trading strategy prescribed in self.strategy. 
		The backtest consists of two steps. For each time step:
		- Handle all orders that were created at the end of the previous day. 
		(Unlimited borrowing of cash and shortselling is allowed).	
		- Run the strategy on the current bar.
		- Log the portfolio value at the end of the day.
		This function iterates over the calendar and performs the necessary steps for each time step. The progress is displayed using tqdm.
		
		Parameters:
			None
		
		Returns:
			None
		"""
		
		for idx in tqdm(self.calendar):
			self.current_idx = idx
			self.strategy.current_idx = self.current_idx
			# fill orders from previus period
			self.FillOrders()
			
			# Run the strategy on the current bar
			self.strategy.OnBar()
			self.Log(self.current_idx)


	def FillOrders(self):
		"""
		This method handles all current orders.
		If an order can be fulfilled, it creates a new Trade object 
		and adjusts the cash value and the portfolio position.

		Parameters:
		None

		Returns:
		None

		This function iterates over all the orders in the strategy and performs the following actions:
		- Retrieves the ticker and data for the current order.
		- Retrieves the current date and time in the desired format.
		- Retrieves the open price of the ticker at the current date and time.
		- Creates a new Trade object with the ticker, side, size, price, and current date.
		- Adds the trade to the strategy's trades list.
		- If the order is a buy order, it adds the position to the portfolio and subtracts the price multiplied by the size from the cash balance.
		- If the order is a sell order, it subtracts the position from the portfolio and adds the price multiplied by the size to the cash balance.
		- Clears all orders in the strategy.
		"""
		
		for order in self.strategy.orders:
			
		
			ticker = order.ticker
			data = self.datas[order.ticker]
			time = self.current_idx.strftime(self.format)
			

			# We always use adjusted close price
			price = data.loc[self.current_idx, 'Adj Close'] 
			
			# We allow unlimited borrowing of money and short selling
			# Thus no need to check if sufficient fund or if stock is available
			

			# Create a new trade
			t = Trade(
				order.ticker,
				order.side,
				order.size,
				price,
				self.current_idx)
		

			# The strategy keeps track of all the past trades, so that they can be analyzed later
			# Then add the corresponding position to the portfolio
			# Transaction are applied to every trade
			self.strategy.trades.append(t)
			
			if order.side == 'buy':

				self.portfolio.AddPosition(order.ticker, t.size)
				self.portfolio.AddCash(-t.price * t.size - abs(t.price * t.size) *self._transactionCost)
			elif order.side == 'sell':
				self.portfolio.AddPosition(order.ticker, -t.size)
				self.portfolio.AddCash(t.price * t.size - abs(t.price * t.size) *self._transactionCost)
			
		# Clear all orders in the strategy
		self.strategy.orders = []

	def DownloadData(self, ticker, startDate, endDate):
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
		"""
		Adds the financial data of the asset underlying 'ticker', needs to be already collected, cleaned and scaled.

		Parameters:
			ticker (str): The name of the financial asset.
			df (pandas.DataFrame): The cleaned and scaled financial data.

		Returns:
			None
		"""
		self.datas[ticker] = df
		
		self.calendar = df.index

	

	def GetPrice(self, ticker, time, col = 'Adj Close'):
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
		"""
		Logs the portfolio value at a specific time.
		
		Args:
			time (TimeStamp): The specific time to log the portfolio value.
		
		Returns:
			None
		"""
		
		self.log.at[time, 'Portfolio'] = self.GetPortfolioValue()
		


	def GetStats(self):
		"""
		Returns metrics for analyzing the results of the backtesting. 
		Currently the following metrics are provided:
		- ROI (Return on Investment)
		- Annualized Volatility
		- Max Drawdown
		- Annualized Sharpe Ratio

		Parameters:
		None

		Returns:
		- metrics (dict): A dictionary containing the calculated metrics.
		"""
		

		metrics = {}
		helperMetrics = {}
		# Total return consisits of current value of the portfolio which is the sum of the cash value and the value of the current
		# assets
		totalReturn = self.portfolio.cash
		for ticker in self.datas:
			totalReturn += self.GetPrice(ticker, self.current_idx, col = 'Adj Close') * self.portfolio.GetPositionSize(ticker)
		totalReturn /= self.portfolio.initialCash
		metrics['ROI'] = 100*(totalReturn -1)



		# Daily returns
		daily_returns = self.log['Portfolio'].pct_change().dropna()
		mean_daily_return = daily_returns.mean()
		std_daily_return = daily_returns.std()


		# Volatility 
		

		# Annualize the volatility
		metrics['Annualized Volatility'] = std_daily_return * np.sqrt(252)



		# Calculate the cumulative returns
		cumulative_returns = (1 + daily_returns).cumprod()

		# Calculate the running maximum
		running_max = cumulative_returns.cummax()

		# Calculate the drawdowns
		drawdowns = (cumulative_returns - running_max) / running_max

		# Maximum Drawdown
		metrics['Max Drawdown'] = drawdowns.min()

		# Assuming a risk-free rate of 1%
		r= 0.03
		# Computes the risk free return on the initial cash value
		for time in self.calendar:
			self.log.at[time,'Riskfree'] =self.portfolio.initialCash* np.exp(r* (time- self.calendar[0]).days/365.25)



		# Sharpe ratio
		
		sharpe =  mean_daily_return / std_daily_return
		metrics['Annualized Sharpe'] = sharpe * np.sqrt(252)
		
		for(key, value) in metrics.items():
			print(key, value)
		return metrics

	def GetPortfolioValue(self):
		''' Returns the current value of the portfolio by adding the cash value to the current value of all positions in the
		portfolio.'''
		totalValue = self.portfolio.cash
		for ticker in self.datas:
			totalValue += self.GetPrice(ticker, self.current_idx, col = 'Adj Close') *self.portfolio.GetPositionSize(ticker)
		return totalValue


	def SetTransactionCost(self, cost):
		"""
		Set the transaction cost for trading.

		Parameters
		----------
		cost : float
		    The transaction cost to be set. Should be between 0 and 1.

		Returns
		-------
		None
		"""
		self._transactionCost = cost


		
if __name__ == "__main__":
	pass




		
	   








