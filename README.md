# TradingSystem: A backtester for trading pairs strategies

This library provides a comprehensive framework for backtesting algorithmic trading strategies, specifically designed for pairs trading. Key features include:

* Adding financial data to the data feed using yahooFinance
* Creating new trading strategies
* Backtesting trading strategies against historical data
* Analyzing and plotting the results of the backtest

Explore a list of basic trading strategies in the [Examples Notebook](TradingSystem/Examples.ipynb). These strategies are included to demonstrate the functionality of the trading system and are not intended to be profitable.


# Basic usage

The Basic Trading System provides a framework for backtesting algorithmic trading strategies. Follow these steps to get started:

1. **Create an Instance**:
   ```python
   from TradingSystem import *
   trading_system = TradingSystem()
   ```

2. **Add financial data:**

    Use the `TradingSystem.DownloadData(ticker, startDate, endDate)` method to add financial data to the data feed. Currently, data is sourced from `yahooFinance`.
    ```python
    trading_system.DownloadData("AAPL", "2020-01-01", "2021-01-01")
    ```


3. **Define a strategy:**

    Create a new strategy by defining a class that inherits from `Strategy` and overrides the `OnBar()` method. This method is executed once per day during a backtest and is used to create buy and sell orders.
    ```python
    class MyStrategy(Strategy):
    def OnBar(self):
        # Define buy and sell logic here
        pass
    ```


4.  **Set Initial Portfolio Cash:**

    Specify the initial amount of money available in the portfolio using `TradingSystem.portfolio.SetInitialCash(cash)`.
    ```python 
    trading_system.portfolio.SetInitialCash(100000)
    ```


5. **Run the Backtest:**

    Execute the backtest of the defined strategy with the provided data using `TradingSystem.Run()`.
    ```python
    trading_system.Run()
    ```

6. **Analyze the Backtest:**

    Evaluate the backtest results using various statistics provided by `TradingSystem.GetStats()`. Additionally, `TradingSystem.log` tracks the portfolio's value over time and can be used for plotting.
    ```python
    stats = trading_system.GetStats()
    ```

## A toy exampple




The following example demonstrates the usage of the Basic Trading System with a simple toy strategy: buying a stock one day and selling it the next day.
```python
class BuyAndSellStrategy(Strategy):
    def OnBar(self, verbose = False):
        # Uses the first ticker that was added to the data feed
         ticker = self.tickers[0]

        # Check if the asset is already owned
        if self.GetPositionSize(ticker) == 0:
            self.Buy(ticker, size = 1)
            if verbose:
                print(self.current_idx,"Buy order created")
        else:
            self.Sell(ticker, size = 1)
            if verbose:
                print(self.current_idx,"Sell order created")


trading_system = TradingSystem()
trading_system.DownloadData("AAPL", "2020-01-01", "2021-01-01")
trading_system.portfolio.SetInitialCash(100000)
trading_system.SetStrategy(BuyAndSellStrategy())
trading_system.Run()

stats = trading_system.GetStats()

# Show the portfolio value over time
trader.log.plot()
plt.title("Portfolio value over time",size='x-large',color='blue')
plt.show()
```








# Pairs trading
Pairs trading is a fundamental strategy in statistical arbitrage, aimed at identifying pairs of highly correlated assets. By detecting pairs where one asset is overvalued and the other is undervalued, a trading strategy can be developed to profit from the mean-reversion of these assets.

To successfully implement this strategy, suitable pairs must be identified. In [Pairs Selection Notebook](TradingSystem/PairsSelection.ipynb) we demonstrate the following approach to determine suitable pairs from a list of 87 financial assets:
1. **Cointegration test:** 

    Stationary and ergodic stochastic processes return to the mean in the long run  (by Birkhoff's ergodic theorem). As a first step, we want to determine if two time series $X_t, Y_t$ are cointegrated, such that $Y_t -\alpha X_t$, is stationary, we use the two-step Earle-Grenger test,  based on the Augmented Dickey-Fuller test for stationarity.
2. **Clustering:**
    - Initial sorting of time series is done using clustering. Principal Component Analysis (PCA) is applied to reduce data dimensions, followed by the OPTICS algorithm for clustering.
    - For each pair in a cluster, the Engle-Granger test for cointegration is applied, accepting pairs with a p-value less than 0.03.
    
3. **Mean-Reversion Indicators:**
    - **Hurst Exponent:** 
    Measures long-term memory of a time series. Values between 0 and 0.5 indicate frequent crossings of the mean.
    - **Half-life:**  Estimates how quickly a time series reverts to half its initial deviation from the mean, calculated as
    $$-\dfrac{\ln(2)}{\ln(\beta)},
    $$
    where $\beta$ is obtained by linear regression of $Y_t$ against $Y_{t-1}$.
    - **Mean-crossings:**  Counts the number of times the spread crosses its mean.

For instance, our analysis identified strong mean-reversion between 'KEY' (KeyCorp) and 'FITB' (Fifth Third Bank) from January 2021 to October 2023.
![Unknown-2](https://github.com/FrederikBenirschke/BasicTradingSystem/assets/133478072/191ac842-819a-4552-9c4a-a99931ae9670)




After selecting promising pairs, the  [Trading Pairs Example Notebook](TradingSystem/TradingPairsExample.ipynb), demonstrates a pairs trading strategy that generates buy and sell signals based on the z-score of the spread. A z-score > 1 indicates the first asset is overvalued, and a z-score < -1 indicates the second asset is overvalued.

Below is a plot of a simple strategy trading Binance and Citigroup from 2021 to 2023.



![Unknown-4](Images/PairTrading.png)

## Installation

Follow these steps to install the project on your local machine:

1. Clone the repository:

   ```bash
   git clone https://github.com/FrederikBenirschke/BasicTradingSystem.git

2. Install dependencies:
```bash
pip install -r basic_trading_system_conda.yml
```

Note: If you are using a different package manager (such as `conda`), you may need to use the appropriate command to install the dependencies from the `basic_trading_system_conda.yml` file.



# Prerequisites 
The prerequisites are found in the [YML file](basic_trading_sytem.conda.yml).








  
