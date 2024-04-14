import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns; sns.set()
import yfinance as yf

def PlotStockData(ticker, stockData):
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



# def PlotPair(stockData1, stockData2):
#     df1 = stockData1
#     df2 = stockData2
#     tickers = [stockData1.ticker, stockData2.ticker]
#     fig, ax1 = plt.subplots()
#     ax1.plot(df1, 'b-')
#     ax2 = ax1.twinx()
#     ax2.plot(df2, 'r.')
#     plt.title("Plotting {} & {}".format(tickers[0],tickers[1]))
#     plt.show()





def PlotTickers(tickers, startDate, endDate, normalization = None):
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


def plotPairAnalysis(ticker1, ticker2, startDate,endDate):

    data = pd.DataFrame(columns=[ticker1, ticker2])
    tickers = [ticker1, ticker2]
    for ticker in tickers:
        data[ticker] = yf.download(ticker, 
                                startDate,
                                endDate)['Adj Close']
        data[ticker + ' normalized'] = minMaxNormalization(data[ticker])

   
    # spreadData = spread(df1norm, df2norm)
    # movingAverage = mva(spreadData, 20)

    # data = pd.DataFrame(columns=['Spread', 'MVA'])
    data['Spread'] = data[ticker1 + ' normalized'] - data[ticker2 + ' normalized']
    data['MVA'] = data['Spread'].rolling(window=20).mean() 
    # Print first 5 rows of the data
    data['Spread', 'MVA'].plot(figsize=(10, 7))
    # Show the legend
    plt.legend()
    # Define the label for the title of the figure
    plt.title("Pairs analysis", fontsize=16)
    # Define the labels for x-axis and y-axis
    plt.ylabel('Price', fontsize=14)
    plt.xlabel('Year', fontsize=14)
    # Plot the grid lines
    plt.grid(which="major", color='k', linestyle='-.', linewidth=0.5)
    plt.show()




# def spread(df1, df2):
#     df = pd.DataFrame({})
#     for column in df1: 
#         df[column] = df1[column]-df2[column]
#     return df

# def mva(df, window):
#     return df.rolling(window=window).mean()






def minMaxNormalization(dataFrame):
    dfMinMax = dataFrame.copy() 
  
    # apply normalization techniques 
    # introduces bias since it uses the future
    for column in dfMinMax: 
        dfMinMax[column] = (dfMinMax[column] - dfMinMax[column].min()) / (dfMinMax[column].max() - dfMinMax[column].min())     
    
    return dfMinMax



