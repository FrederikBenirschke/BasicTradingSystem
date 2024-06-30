from Order import *
import pandas as pd
import math

class Strategy:
    '''A strategy is performed once a day by calling OnBar() in TradingSystem.run() 
    and can create buy and sell orders. Strategy is a base class and every new strategy
    should inherit from it.
        To create a strategy, create a new class that inherits from strategy and overwrite OnBar().'''


    def __init__(self):
        self.current_idx = None
        self.datas = {}
        self.orders = []
        self.trades = []
        self.portfolio = None
        self.tickers = []
        
        
        


    def Buy(self,ticker, size = 1):
        """Create a buy order for ticker.

        Args:
            ticker (string): the ticker of the underlying stock
            size (int, optional): number of stocks that should be bought. Defaults to 1.
        """
        self.orders.append(
            Order(ticker,  'buy', size, self.current_idx)
        )
       

    def Sell(self, ticker, size = 1):
        """Create a sell order for the asset underlying ticker.

        Args:
            ticker (string): ticker for the corresponding asset
            size (int, optional): number of stocks to be sold. Defaults to 1.
        """
        self.orders.append(
            Order(ticker, 'sell', size ,self.current_idx)
        )


    def OnBar(self):
        ''' The key function for implementing a strategy. Every new strategy needs to override OnBar().
        This is where the strategy is implemented.'''
        pass


    def GetPositionSize(self, ticker):
        '''Returns the current amount of stocks existing in the portfolio.
        
        Args:
        ticker(string): the name of the stock'''
        return self.portfolio.GetPositionSize(ticker)






class BasicStrategy(Strategy):
    '''Basic strategy for testing purposes only. Buys on one day and sells on the next.'''

    def OnBar(self, verbose = False):
        ticker = self.tickers[0]
        
        if self.GetPositionSize(ticker) == 0:
            self.Buy(ticker, size = 1)
            if verbose:
                print(self.current_idx,"buy order created")
        else:
            self.Sell(ticker, size = 1)
            if verbose:
                print(self.current_idx,"sell order created")


class BuyAndHold(Strategy):
    ''' Buy maximum amount of an asset on day 1 and hold until the end.'''

    def OnBar(self, verbose = False):
        ticker = self.tickers[0]
        
        if self.GetPositionSize(ticker) == 0:
            price = self.datas[ticker].loc[self.current_idx,'Adj Close']
            self.Buy(ticker, size = math.floor(self.portfolio.cash/price))
            if verbose:
                print(self.current_idx,"buy order created")
       




class SMACross(Strategy):
    '''Computes the simple moving average with two different time windows and produces sell/buy signals when the
    moving average cross.'''

    slowWindow = 30
    fastWindow = 10


    def crossover(self, ticker):
        ''' Computes the difference between the slopes of the secant lines of the fast and slow moving averages.'''
        
        df = pd.DataFrame(index = self.datas[ticker].index)
        df['Adj Close'] = self.datas[ticker]['Adj Close']
        df['SMAslow'] =  (df['Adj Close']).rolling(window = SMACross.slowWindow).mean()
        df['SMAfast'] =  (df['Adj Close']).rolling(window = SMACross.fastWindow).mean()
        df['SlowDiff'] =  (df['SMAslow']- df['SMAslow'].shift(-1)).fillna(0)
        df['FastDiff'] =  (df['SMAfast']- df['SMAfast'].shift(-1)).fillna(0)
        

        return df.loc[self.current_idx, 'FastDiff'] -df.loc[self.current_idx, 'SlowDiff']




    def OnBar(self, verbose = False):
        """
        Executes a trading strategy based on the crossover of two moving averages.

        Parameters:
            verbose (bool, optional): If True, prints the order creation messages. Defaults to False.

        Returns:
            None
        """
        thresh = 0.2
        ticker = self.tickers[0]
        
        #If we do not own a position and the fast average crosses
        # upwards through the slow average, generate a buy signal
        if self.GetPositionSize(ticker) == 0:
            if self.crossover(ticker)>thresh: 
            
                self.Buy(ticker, size = 1)
                if verbose:
                    print(self.current_idx,"buy order created")
         #If we do  own a position and the fast average crosses
        # downwards  through the slow average, generate a sell signal   
        else:
            if self.crossover(ticker)<-thresh: 

                self.Sell(ticker, size = 1)
                if verbose:
                    print(self.current_idx,"sell order created")


        



        
