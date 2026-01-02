import pandas as pd

def momentum_signal(prices: pd.Series, window: int = 20) -> pd.Series:
    """
    Simple rate-of-change momentum signal.
    """
    return prices.pct_change(window)