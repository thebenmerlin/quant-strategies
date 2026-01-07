"""
Momentum Strategy

Generates signals based on price momentum using rate of change (ROC).
Signal logic:
  - Long (+1): ROC > threshold
  - Short (-1): ROC < -threshold
  - Neutral (0): otherwise
"""

import numpy as np
import pandas as pd


def momentum_strategy(
    prices: pd.Series,
    lookback: int = 20,
    threshold: float = 0.02,
) -> pd.Series:
    """
    Generate momentum signals based on rate of change.

    Parameters
    ----------
    prices : pd.Series
        Price series (e.g., close prices).
    lookback : int, default 20
        Lookback period for computing momentum.
    threshold : float, default 0.02
        Threshold for signal generation (2% by default).

    Returns
    -------
    pd.Series
        Signal series with values in {-1, 0, 1}.
    """
    if not isinstance(prices, pd.Series):
        raise TypeError("prices must be a pandas Series")

    if len(prices) < lookback:
        raise ValueError(f"prices length ({len(prices)}) must be >= lookback ({lookback})")

    # Rate of change: (P_t - P_{t-n}) / P_{t-n}
    roc = prices.pct_change(periods=lookback)

    # Generate signals
    signals = pd.Series(0, index=prices.index, dtype=np.int8)
    signals[roc > threshold] = 1
    signals[roc < -threshold] = -1

    return signals
