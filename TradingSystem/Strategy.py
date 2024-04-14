from Order import *
import pandas as pd

class Strategy:
    '''A strategy is performed once a day by calling OnBar() in TradingSystem.run() and can create buy and sell orders.
        To create a strategy, create a new class that inherits from strategy and overwrite OnBar().'''


    def __init__(self):
        self.current_idx = None
        self.datas = {}
        self.orders = []
        self.trades = []
        self.portfolio = None
        self.tickers = []
        
        


    def Buy(self,ticker, size = 1):
        self.orders.append(
            Order(ticker,  'buy', size, self.current_idx)
        )
       

    def Sell(self, ticker, size = 1):
        self.orders.append(
            Order(ticker, 'sell', -size ,self.current_idx)
        )


    def OnBar(self):
        pass


    def positionSize(self, ticker):
        '''Returns the current amount of stocks existing in the portfolio'''
        return self.portfolio.GetPositionSize(ticker)






class BasicStrategy(Strategy):
    '''Nonsensical startegy for testing purposes only. Buys on one day and sells on the next.'''

    def OnBar(self):
        ticker = self.tickers[0]
        
        if self.positionSize(ticker) == 0:
            self.Buy(ticker, size = 1)
            print(self.current_idx,"buy order created")
        else:
            self.Sell(ticker, size = 1)
            print(self.current_idx,"sell order created")



class SMACross(Strategy):
    '''Computes the simple moving average with two different time windows and produces sell/buy signals when the
    moving average cross.'''

    slowWindow = 30
    fastWindow = 10


    def crossover(self, ticker):
        
        df = pd.DataFrame(index = self.datas[ticker].index)
        df['Adj Close'] = self.datas[ticker]['Adj Close']
        df['SMAslow'] =  (df['Adj Close']).rolling(window = SMACross.slowWindow).mean()
        df['SMAfast'] =  (df['Adj Close']).rolling(window = SMACross.fastWindow).mean()
        df['SlowDiff'] =  (df['SMAslow']- df['SMAslow'].shift(-1)).fillna(0)
        df['FastDiff'] =  (df['SMAfast']- df['SMAfast'].shift(-1)).fillna(0)
        

        return df.loc[self.current_idx, 'FastDiff'] -df.loc[self.current_idx, 'SlowDiff']




    def OnBar(self):
        thresh = 0.2
        ticker = self.tickers[0]
        
        #If we do not own a position and the fast average crosses
        # upwards through the slow average, generate a buy signal
        if self.positionSize(ticker) == 0:
            if self.crossover(ticker)>thresh: 
            
                self.Buy(ticker, size = 1)
                print(self.current_idx,"buy order created")
         #If we do  own a position and the fast average crosses
        # downwards  through the slow average, generate a sell signal   
        else:
            if self.crossover(ticker)<-thresh: 

                self.Sell(ticker, size = 1)
                print(self.current_idx,"sell order created")


        



        
