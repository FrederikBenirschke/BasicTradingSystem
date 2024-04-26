# BasicTradingSystem

Provides basic functionality for backtesting algorithmic trading strategies.
Currently, the following features are supported:
* Adding financial data to the data feed (using yahooFinance)
* Create new trading strategies
* Backtest trading strategies against the historical data
* Analyze and plot the results of the backtest


A list of basic trading strategies can be found [here](TradingSystem/Examples.ipynb). These strategies are not meant to be profitable and are only included to demonstrate the functionality of the trading system.

# Pairs trading
A basic strategy in Statistical Arbitrage is to find a pair of two assets that are highly correlated. If, due to marked inefficiencies, one of the stocks is overvalued and the other is undervalued, we enter a short position in the overvalued stock and a long position in the undervalued stock. The assumption is that in the long run, both assets will return to their common mean, a process known as mean-reversion. To apply this strategy successfully one needs to first find suitable pairs whose time series shows a strong mean-reversion effect.
In [this notebook ](TradingSystem/PairsSelection.ipynb) we implement the following approach to determine suitable pairs among a list of 87 financial assets.
- Stochastic processes that are stationary and ergodic have the property that in the long run the time average returns to the mean. (Birkhoff's ergodic theorem). As a first step, we want to determine if two time series $X_t, Y_t$ are cointegrated, i.e. such that $Y_t -\alpha X_t$ is a stationary stochastic process. For this, we use the two-step Earle-Grenger test, which is based on the Augmented Dickey-Fuller test for stationarity of a time series.
- As an initial step we  use clustering to sort the time series. We first apply principal component analysis to reduce the dimensions of the data and then use the OPTICS algorithm for clustering.
- For each possible pair in a cluster we use the Earle-Grenger test for cointegration and only accept pairs with a resulting p-Value less than $0.03$.
- Once we find a suitably cointegrated pair, the next step is to establish that the time series is mean-reverting. Here we use three technical indicators:
- The Hurst exponent is a measure of the long-term memory of a time series. A value between 0-0.5 indicates that the time series will switch between very large and very small values and frequently cross the mean.
- The half-life time measures how fast a time series reverts back to half its initial deviation from the mean. Assuming an AR(1) model for the spread we can estimate the half-life time as \begin{equation} -\dfrac{\ln(2)}{\ln(\beta)} \end{equation} where $\beta$ is obtained by linear regression of $Y_t$ against $Y_{t-1}$.
- Lastly, we count the number of times the spread crosses its mean.
For example, our analysis found that the time series for 'KEY' and 'FITB' show strong mean-reversion between Jan 2021 and October 2023.
![Unknown-2](https://github.com/FrederikBenirschke/BasicTradingSystem/assets/133478072/191ac842-819a-4552-9c4a-a99931ae9670)


After we have selected promising pairs, [in this notebook](TradingSystem/TradingPairsExample.ipynb), we use the trading system to implement a pair trading strategy
that generates buy and sell signals based on the z-score of the spread. We use a z-Score > 1 as an indicator that the first asset is overvalued and a z-Score < -1 as an indicator that the second asset is overvalued.
Here is a plot of a simple strategy trading Binance and CitiGroup from 2021 to 2023.

![Unknown-4](https://github.com/FrederikBenirschke/BasicTradingSystem/assets/133478072/413490e9-dadc-4745-8255-da8387025cf5)










  
