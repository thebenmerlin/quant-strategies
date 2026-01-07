"""
Mean Reversion Strategy

Generates signals based on z-score of price deviations from rolling mean.
Signal logic:
  - Long (+1): z-score < -entry_threshold (price is below mean)
  - Short (-1): z-score > entry_threshold (price is above mean)
  - Neutral (0): |z-score| <= entry_threshold
"""

import numpy as np
import pandas as pd


def mean_reversion_strategy(
    prices: pd.Series,
    lookback: int = 20,
    entry_threshold: float = 2.0,
) -> pd.Series:
    """
    Generate mean reversion signals based on z-score.

    The strategy assumes prices will revert to the mean:
    - When prices are significantly below the mean (negative z-score),
      we expect them to rise → go long.
    - When prices are significantly above the mean (positive z-score),
      we expect them to fall → go short.

    Parameters
    ----------
    prices : pd.Series
        Price series (e.g., close prices).
    lookback : int, default 20
        Lookback period for computing rolling statistics.
    entry_threshold : float, default 2.0
        Z-score threshold for signal generation.

    Returns
    -------
    pd.Series
        Signal series with values in {-1, 0, 1}.
    """
    if not isinstance(prices, pd.Series):
        raise TypeError("prices must be a pandas Series")

    if len(prices) < lookback:
        raise ValueError(f"prices length ({len(prices)}) must be >= lookback ({lookback})")

    if entry_threshold <= 0:
        raise ValueError("entry_threshold must be positive")

    # Compute rolling statistics
    rolling_mean = prices.rolling(window=lookback).mean()
    rolling_std = prices.rolling(window=lookback).std()

    # Compute z-score: (price - mean) / std
    # Handle division by zero with replace
    z_score = (prices - rolling_mean) / rolling_std.replace(0, np.nan)

    # Generate signals
    signals = pd.Series(0, index=prices.index, dtype=np.int8)
    signals[z_score < -entry_threshold] = 1   # Price below mean → long
    signals[z_score > entry_threshold] = -1   # Price above mean → short

    return signals
