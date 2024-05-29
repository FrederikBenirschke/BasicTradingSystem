import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns; sns.set()
import yfinance as yf

def PlotStockData(ticker, stockData):
    ''' Plots a DataFrame representing the financial data of a single ticker.
    
    Args:
    stockData(pd.DataFrame): time series for stock that will be plotted'''
    plt.figure(figsize=(14,5))

    # sns.set_style("ticks")
    # sns.lineplot(data=stockData,x="Date",y='Close',color='firebrick')
    # sns.despine()
    stockData.plot(figsize=(10, 7))
    # Add title
    plt.title("The Stock Price of {}".format(ticker),size='x-large',color='blue')
    # Add labels
    plt.ylabel('Price', fontsize=14)
    plt.xlabel('Year', fontsize=14)
    #Add legend
    plt.legend()
    # Plot the grid lines
    plt.grid(which="major", color='k', linestyle='-.', linewidth=0.5)
    plt.show()





def PlotTickers(tickers, startDate, endDate, normalization = None):
    """Plots the asset prices corresponding to a list of tickers.

    Args:
        tickers (string):name of the asset
        startDate (str): first day to be plotted
        endDate (str): last day to be plotted
        normalization (sklearn.preprocessing.Normalizer, optional): normalizes the data. Defaults to None.
    """
   
   
    # Create placeholder for data
    data = pd.DataFrame(columns=tickers)
    # Fetch the data
    for ticker in tickers:
        data[ticker] = yf.download(ticker, 
                                startDate,
                                endDate)['Adj Close']
    
    if normalization:
        data = normalization(data)
    # Print first 5 rows of the data
    data.plot(figsize=(10, 7))
    # Show the legend
    plt.legend()
    # Define the label for the title of the figure
    plt.title("Adjusted Close Price", fontsize=16)
    # Define the labels for x-axis and y-axis
    plt.ylabel('Price', fontsize=14)
    plt.xlabel('Year', fontsize=14)
    # Plot the grid lines
    plt.grid(which="major", color='k', linestyle='-.', linewidth=0.5)
    plt.show()




def minMaxNormalization(dataFrame):
    '''Normalizes a dataFrame using MinMaxNormalization.
    Args:
    dataFrame(pd.DataFrame): data to be normalized'''
    dfMinMax = dataFrame.copy() 
  
    # apply normalization techniques 
    # introduces bias since it uses the future
    for column in dfMinMax: 
        dfMinMax[column] = (dfMinMax[column] - dfMinMax[column].min()) / (dfMinMax[column].max() - dfMinMax[column].min())     
    
    return dfMinMax

if __name__ == "__main__":
	pass


