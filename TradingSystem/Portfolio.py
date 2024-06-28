class Portfolio:


    def __init__(self):
        """ 
        Initializes a new instance of the Portfolio class.

        This constructor sets up the initial state of the Portfolio object. It initializes the following attributes:
        
        - orders: a list to store the orders made by the portfolio
        - positions: a dictionary to store the positions held by the portfolio, where the keys are the tickers and the values are the sizes
        - cash: an integer representing the current cash value of the portfolio
        - initialCash: an integer representing the initial cash value of the portfolio
        
        Parameters:
            None
        
        Returns:
            None
        """
        self.orders = []
        self.positions = {}
        self.cash = 0
        self.initialCash = 0
        


    
         
    def SetInitialCash(self, cash):
        """Sets the initial cash value of portfolio. Used to analyze the returns of the portfolio over time.
        Should only be called once in the beginning.

        Args:
            cash (int): initial amount of cash in the portfolio
        """
        self.cash += cash
        self.initialCash += cash



    def AddCash(self, cash):
        '''  Adds cash value of the portfolio.
        Does not change the initial cash value.
        Should be used to adjust the portfolio value while backtesting.
        Args:
            cash(int): the new value of the portfolio
        '''
        self.cash += cash
        


    def __repr__(self):
        """
        Returns a string representation of the Portfolio object.

        Returns:
            str: A string containing the cash value and the ticker and size of each position in the portfolio.
        """
        s = 'Portfolio: \n' + 'Cash value: ' + str(self.cash) + '\n'
        for ticker in self.positions.keys():
            s+= 'Ticker:' + ticker + ', Size:' + str(self.positions[ticker]) + '\n'
        return s


    def HasCash(self, value):
        '''Checks if there is enough cash in the portfolio.

        Args:
            value(int): Returns true if the value of the portfolio is at least value
        '''
        return value <= self.cash

    def HasPosition(self, ticker, size):
        ''' Returns true if there are more then size stocks of the asset underlying ticket
        in the portfolio.
        Args:
        ticker(string): the ticker of the underlying asset
        size(int): how many stocks should the portfolio have'''
        return size <= self.GetPositionSize(ticker)


    def AddPosition(self, ticker, size = 1):
        ''' Adds size assets underlying ticker.
        args:
        ticker(string): ticker of the corresponding stock
        size(int): how many stocks should be added'''
        if ticker in [tick for tick  in self.positions.keys()]:
            
            self.positions[ticker]+= size
            
        else:
            self.positions[ticker] = size

    def GetPositionSize(self, ticker):
        ''' Returns the number of assets underlying ticker in the portfolio.
        args(string): ticker of the corresponding stock'''
        if ticker in self.positions:
            return self.positions[ticker]
        else:
            return 0
        

    


    


    
        


    