import yfinance as yf
import pandas as pd

def load_data(ticker: str, period: str = "5y") -> pd.DataFrame:
    """
    Download historical OHLCV data using Yahoo Finance.
    """
    data = yf.download(ticker, period=period)
    data.dropna(inplace=True)
    return data