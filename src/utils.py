import pandas as pd

def calculate_returns(prices: pd.Series) -> pd.Series:
    """
    Calculate log returns.
    """
    return (prices / prices.shift(1)).apply(lambda x: 0 if pd.isna(x) else x).pct_change()