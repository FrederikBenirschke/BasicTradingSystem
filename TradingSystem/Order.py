class Order:
    ''' An order to buy or sell an asset underlying a ticker.
    ticker - str: ticker of the underlying asset, for example 'SPY'
    side - str: 'buy' or 'sell'
    size - the number of assets to buy or sell, can be fractional
    idx - the timestamp when the order is created'''

    def __init__(self, ticker, side, size, idx):
        self.ticker = ticker
        self.side = side
        self.size = size
        self.idx = idx
        

