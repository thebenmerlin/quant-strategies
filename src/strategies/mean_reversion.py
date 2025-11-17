import pandas as pd

def bollinger_bands(prices: pd.Series, window: int = 20, num_sd: float = 2):
    ma = prices.rolling(window).mean()
    std = prices.rolling(window).std()
    upper = ma + (std * num_sd)
    lower = ma - (std * num_sd)
    return ma, upper, lower