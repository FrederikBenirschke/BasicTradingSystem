class Order:
    ''' An order to buy or sell an asset underlying a ticker.
    ticker - str: ticker of the underlying asset, for example 'SPY'
    side - str: 'buy' or 'sell'
    size - the number of assets to buy or sell, can be fractional
    idx - the timestamp when the order is created'''

    def __init__(self, ticker, side, size, idx):
        """
        Initializes a new Order object.

        Args:
            ticker (str): The ticker symbol of the underlying asset.
            side (str): The side of the order, either 'buy' or 'sell'.
            size (float): The number of assets to buy or sell.
            idx (int): The timestamp when the order is created.

        Returns:
            None
        """
        self.ticker = ticker
        self.side = side
        self.size = size
        self.idx = idx
        

