"""
Breakout Strategy

Generates signals based on price breakouts from a rolling high/low channel.
Signal logic:
  - Long (+1): Price > Rolling Max (Breakout Up)
  - Short (-1): Price < Rolling Min (Breakout Down)
  - Neutral (0): No signal (or hold previous) - simplified to 0 here.
"""

import numpy as np
import pandas as pd


def breakout_strategy(
    prices: pd.Series,
    lookback: int = 20,
) -> pd.Series:
    """
    Generate signals based on price breakouts.

    Parameters
    ----------
    prices : pd.Series
        Price series (e.g., close prices).
    lookback : int, default 20
        Lookback period for computing rolling high/low.

    Returns
    -------
    pd.Series
        Signal series with values in {-1, 0, 1}.
    """
    if not isinstance(prices, pd.Series):
        raise TypeError("prices must be a pandas Series")

    # Compute rolling channel
    # Usually uses High and Low prices, but we only have 'prices' (assumed close)
    # So we use rolling max/min of Close prices.
    
    # We shift by 1 to avoid lookahead bias on signal generation?
    # Standard breakout: if *today's* close > *yesterday's* 20-day high, then we have a breakout.
    # Because today's close is part of today's channel calculation if not shifted.
    # So we compare Price[t] vs RollingMax[t-1]
    
    rolling_max = prices.rolling(window=lookback).max().shift(1)
    rolling_min = prices.rolling(window=lookback).min().shift(1)
    
    signals = pd.Series(0, index=prices.index, dtype=np.int8)
    
    # Breakout Up
    signals[prices > rolling_max] = 1
    
    # Breakout Down
    signals[prices < rolling_min] = -1
    
    return signals
