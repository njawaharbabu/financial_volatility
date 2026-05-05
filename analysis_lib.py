import yfinance as yf
import pandas as pd
import numpy as np

def fetch_stock_data(ticker, period='1y'):
    """
    Fetch historical stock data from Yahoo Finance.
    """
    try:
        data = yf.download(ticker, period=period)
        if data.empty:
            return None
        
        # Handle MultiIndex columns (yfinance 1.3.0+ behavior)
        if isinstance(data.columns, pd.MultiIndex):
            data.columns = data.columns.get_level_values(0)
            
        return data
    except Exception as e:
        print(f"Error fetching data: {e}")
        return None

def calculate_volatility(data, window=21):
    """
    Calculate daily returns and rolling volatility.
    """
    # Use 'Adj Close' if available, otherwise fallback to 'Close'
    close_col = 'Adj Close' if 'Adj Close' in data.columns else 'Close'
    
    # Daily Returns
    data['Daily_Return'] = data[close_col].pct_change()
    
    # Rolling Volatility (Standard Deviation of returns)
    data['Rolling_Volatility'] = data['Daily_Return'].rolling(window=window).std()
    
    # Annualized Volatility
    data['Annualized_Volatility'] = data['Rolling_Volatility'] * np.sqrt(252)
    
    return data

def get_summary_stats(data):
    """
    Get summary statistics for volatility.
    """
    stats = {
        'Mean Daily Return': data['Daily_Return'].mean(),
        'Max Daily Return': data['Daily_Return'].max(),
        'Min Daily Return': data['Daily_Return'].min(),
        'Average Annualized Volatility': data['Annualized_Volatility'].mean(),
        'Current Annualized Volatility': data['Annualized_Volatility'].iloc[-1],
        'Volatility Std Dev': data['Annualized_Volatility'].std()
    }
    return stats
