

class Trade():
    """Trade objects are created when an order is filled.
    """
    def __init__(self, ticker,side,size,price,idx):
        self.ticker = ticker
        self.side = side
        self.price = price
        self.size = size
        self.idx = idx

    def __repr__(self):
        return f'<Trade: {self.idx} {self.ticker} {self.size}@{self.price}>'



if __name__ == "__main__":
    pass
