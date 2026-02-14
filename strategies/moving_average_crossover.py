"""
Moving Average Crossover Strategy

Generates signals based on the crossover of two simple moving averages (SMA).
Signal logic:
  - Long (+1): Short SMA > Long SMA
  - Short (-1): Short SMA < Long SMA
  - Neutral (0): No signal (or hold previous) - simplified to 0 here/current regime state
"""

import numpy as np
import pandas as pd


def moving_average_crossover_strategy(
    prices: pd.Series,
    short_window: int = 50,
    long_window: int = 200,
) -> pd.Series:
    """
    Generate signals based on Moving Average Crossover.

    Parameters
    ----------
    prices : pd.Series
        Price series (e.g., close prices).
    short_window : int, default 50
        Lookback period for short SMA.
    long_window : int, default 200
        Lookback period for long SMA.

    Returns
    -------
    pd.Series
        Signal series with values in {-1, 0, 1}.
    """
    if not isinstance(prices, pd.Series):
        raise TypeError("prices must be a pandas Series")

    if short_window >= long_window:
        raise ValueError("short_window must be less than long_window")

    # Compute SMAs
    short_sma = prices.rolling(window=short_window).mean()
    long_sma = prices.rolling(window=long_window).mean()

    # Generate signals
    signals = pd.Series(0, index=prices.index, dtype=np.int8)
    
    # Where short > long, we are in a bullish regime (1)
    # Where short < long, we are in a bearish regime (-1)
    signals[short_sma > long_sma] = 1
    signals[short_sma < long_sma] = -1

    return signals
