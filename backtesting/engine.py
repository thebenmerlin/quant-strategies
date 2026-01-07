"""
Vectorized Backtesting Engine

Computes strategy returns and equity curve from signals and prices.
Designed to avoid lookahead bias by using lagged signals.
"""

import numpy as np
import pandas as pd


def backtest(
    prices: pd.Series,
    signals: pd.Series,
    initial_capital: float = 10000.0,
) -> pd.DataFrame:
    """
    Run a vectorized backtest on a signal series.

    The backtest uses lagged signals to avoid lookahead bias:
    - Signal at time t determines position at time t+1
    - Returns at time t+1 are computed from prices at t and t+1

    Parameters
    ----------
    prices : pd.Series
        Price series (e.g., close prices).
    signals : pd.Series
        Signal series with values in {-1, 0, 1}.
    initial_capital : float, default 10000.0
        Starting capital for the backtest.

    Returns
    -------
    pd.DataFrame
        DataFrame containing:
        - 'prices': input price series
        - 'signals': input signal series
        - 'positions': lagged signals (actual positions held)
        - 'returns': price returns
        - 'strategy_returns': returns from strategy positions
        - 'equity_curve': cumulative equity over time
    """
    if not isinstance(prices, pd.Series):
        raise TypeError("prices must be a pandas Series")

    if not isinstance(signals, pd.Series):
        raise TypeError("signals must be a pandas Series")

    if not prices.index.equals(signals.index):
        raise ValueError("prices and signals must have the same index")

    # Compute price returns
    returns = prices.pct_change()

    # Lag signals by 1 period to avoid lookahead bias
    # Position at time t is determined by signal at time t-1
    positions = signals.shift(1).fillna(0)

    # Strategy returns = position * market returns
    strategy_returns = positions * returns

    # Compute equity curve
    cumulative_returns = (1 + strategy_returns).cumprod()
    equity_curve = initial_capital * cumulative_returns

    # Build result DataFrame
    result = pd.DataFrame({
        "prices": prices,
        "signals": signals,
        "positions": positions,
        "returns": returns,
        "strategy_returns": strategy_returns,
        "equity_curve": equity_curve,
    })

    return result
