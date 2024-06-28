

class Trade():
    """Trade objects are created when an order is filled.
    """


    def __init__(self, ticker,side,size,price,idx):
        """
        Initializes a new Trade object.

        Args:
            ticker (str): The ticker symbol of the trade.
            side (str): The side of the trade, either 'buy' or 'sell'.
            size (int): The size of the trade.
            price (float): The price of the trade.
            idx (int): The index of the trade.

        Returns:
            None    
        """
        self.ticker = ticker
        self.side = side
        self.price = price
        self.size = size
        self.idx = idx

    def __repr__(self):
        """
        Return a string representation of the Trade object.

        Returns:
            str: A string in the format '<Trade: idx ticker size@price>', where idx is the index of the trade,
                 ticker is the ticker symbol of the trade, size is the size of the trade, and price is the price of
                 the trade.
        """
        return f'<Trade: {self.idx} {self.ticker} {self.size}@{self.price}>'



if __name__ == "__main__":
    pass
