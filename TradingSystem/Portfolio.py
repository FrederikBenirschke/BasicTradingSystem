class Portfolio:


    def __init__(self):
        self.orders = []
        self.positions = {}
        self.cash = 0
        self.initialCash = 0
         
    def SetInitialCash(self, cash):
        ''' Method to set the initial cash value of portfolio. Used to analyze the returns of the portfolio over time.
        Should only be called once in the beginning.
        '''
        self.cash += cash
        self.initialCash += cash



    def AddCash(self, cash):
        ''' Method to change the current portfolio cash value but does not change the initial cash value.
        Should be used to adjust the portfolio value while backtesting.
        '''
        self.cash += cash
        


    def __repr__(self):
        s = 'Portfolio: \n' + 'Cash value: ' + str(self.cash) + '\n'
        for ticker in self.positions.keys():
            s+= 'Ticker:' + ticker + ', Size:' + str(self.positions[ticker]) + '\n'
        return s


    def HasCash(self, value):
        '''Method checks if the amount of cash is at least as large as value 
        '''
        return value <= self.cash

    def HasPositions(self, ticker, size):
        return size <= self.GetPositionSize(ticker)


    def AddPosition(self, ticker, size = 1):
        if ticker in [tick for tick  in self.positions.keys()]:
            
            self.positions[ticker]+= size
            
        else:
            self.positions[ticker] = size

    def GetPositionSize(self, ticker):
        if ticker in self.positions:
            return self.positions[ticker]
        else:
            return 0
        

    


    


    
        


    