import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

# Logic


def check_uniqueness(lst):
    """
    Check if a list contains only unique values.
    Returns True only if all values in the list are unique, False otherwise
    """
    # we can check for every element in the list if it already has been present before, but the complexity here would be O(n^2), but we can do it linearly
    
    elements_count = {}  # a dictionary to count the occurrence of each element in the list
    
    for element in lst:
        
        elements_count[element] = elements_count.get(element, 0) + 1 # .get to check if the element is already in the dictionary
        
        if elements_count[element] > 1 : return False
       
    return True  # we could use len(set(lst)) == len(lst) but this requires more memory space if the list is very large and contains duplicate


def smallest_difference(array):
    """
    Code a function that takes an array and returns the smallest
    absolute difference between two elements of this array
    Please note that the array can be large and that the more
    computationally efficient the better
    """
    # the naive approach is to check every couple and compute their difference, but the complexity would be also O(n^2), we can do it in O(n log(n))
    # the idea is to sort the list and see the smallest difference between two consecutive elements
    
    sorted_array = sorted(array)
    
    n = len(array)
    
    minimum = np.Inf # we initialize the current minimum with an infinite value
    
    for i in range(1,n):
        
        difference = sorted_array[i] - sorted_array[i-1]
        
        if difference < minimum : minimum = difference          

    return minimum


# Finance and DataFrame manipulation


def macd(prices, window_short=12, window_long=26):
    """
    Code a function that takes a DataFrame named prices and
    returns it's MACD (Moving Average Convergence Difference) as
    a DataFrame with same shape
    Assume simple moving average rather than exponential moving average
    The expected output is in the output.csv file
    """
    first_values = np.empty(window_long -1) # to ensure the same size
    first_values[:] = np.NaN 
    ###
    def moving_average(lst, n):
    
        return pd.Series(lst).rolling(window = n).mean()
    ###
    indexes = prices.columns
    
    MACD = pd.DataFrame(columns=indexes)
    
    for index_ in indexes:
        
        index_prices = prices[index_]
    
        moving_long = moving_average(index_prices, window_long)
        moving_short = moving_average(index_prices, window_short)


        MACD[index_] = np.concatenate((first_values, moving_short - moving_long))
    
    return MACD


def sortino_ratio(prices):
    """
    Code a function that takes a DataFrame named prices and
    returns the Sortino ratio for each column
    Assume risk-free rate = 0
    On the given test set, it should yield 0.05457
    """
    indexes = prices.columns
    
    sortinos = {} # dictionary containing the sortino for each column
    
    days = 255 # trading days in a year, to annualize the daily returns in the dataset
    
    rf = 0 # it can be changed
    
    for index_ in indexes:
        
        index_prices = prices[index_]
        
        mean_index = index_prices.mean()*days - rf
        
        std_index = index_prices[index_prices < 0].std() * np.sqrt(days) # downside standard deviation
        
        sortinos[index_] = mean_index/std_index
        
    return sortinos    
    
def expected_shortfall(prices, level=0.95):
    """
    Code a function that takes a DataFrame named prices and
    returns the expected shortfall at a given level
    On the given test set, it should yield -0.03468
    """
	
	
    indexes = prices.columns
	
	expected_shortfalls = pd.DataFrame(columns=indexes)
	
	for index_ in indexes:
		
		index_prices = prices[index_]
		
		VaR =  index_prices.quantile(level, axis = 0) # value at risk
		
		expected_shortfalls[index_] = index_prices[index_prices.lt(VaR, axis = 1)].mean()
		
	return expected_shortfalls
		
		


# Plot


def visualize(prices, path):
    """
    Code a function that takes a DataFrame named prices and
    saves the plot to the given path
    """
    indexes = prices.columns
    
    for index_ in indexes:
        
        index_prices=[index_]
        
        plt.plot(index_prices)
        
        plt.title(index_)
        
        plt.savefig(path + 'plot ' + str(index_))
        
        
        
        
        
        
        
