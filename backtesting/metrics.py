"""
Performance Metrics

Contains functions for computing strategy performance metrics.
"""

import numpy as np
import pandas as pd
from typing import Dict


def sharpe_ratio(
    returns: pd.Series,
    risk_free_rate: float = 0.0,
    periods_per_year: int = 252,
) -> float:
    """
    Compute annualized Sharpe ratio.

    Parameters
    ----------
    returns : pd.Series
        Series of periodic returns.
    risk_free_rate : float, default 0.0
        Annualized risk-free rate.
    periods_per_year : int, default 252
        Number of periods per year (252 for daily data).

    Returns
    -------
    float
        Annualized Sharpe ratio.
    """
    if len(returns) == 0:
        return np.nan

    # Remove NaN values
    clean_returns = returns.dropna()

    if len(clean_returns) == 0:
        return np.nan

    # Convert annual risk-free rate to periodic
    rf_periodic = (1 + risk_free_rate) ** (1 / periods_per_year) - 1

    excess_returns = clean_returns - rf_periodic
    mean_excess = excess_returns.mean()
    std_excess = excess_returns.std()

    if std_excess == 0 or np.isnan(std_excess):
        return np.nan

    # Annualize
    sharpe = (mean_excess / std_excess) * np.sqrt(periods_per_year)

    return float(sharpe)


def max_drawdown(equity_curve: pd.Series) -> float:
    """
    Compute maximum drawdown from equity curve.

    Maximum drawdown is the largest peak-to-trough decline
    in the equity curve.

    Parameters
    ----------
    equity_curve : pd.Series
        Equity curve series.

    Returns
    -------
    float
        Maximum drawdown as a decimal (e.g., 0.15 = 15% drawdown).
    """
    if len(equity_curve) == 0:
        return np.nan

    # Remove NaN values
    clean_equity = equity_curve.dropna()

    if len(clean_equity) == 0:
        return np.nan

    # Compute running maximum
    running_max = clean_equity.cummax()

    # Compute drawdown at each point
    drawdown = (clean_equity - running_max) / running_max

    # Return maximum drawdown (most negative value, but return as positive)
    mdd = drawdown.min()

    return float(abs(mdd))


def compute_metrics(
    backtest_result: pd.DataFrame,
    risk_free_rate: float = 0.0,
    periods_per_year: int = 252,
) -> Dict[str, float]:
    """
    Compute all performance metrics from backtest results.

    Parameters
    ----------
    backtest_result : pd.DataFrame
        DataFrame from backtest() containing 'strategy_returns' and 'equity_curve'.
    risk_free_rate : float, default 0.0
        Annualized risk-free rate.
    periods_per_year : int, default 252
        Number of periods per year.

    Returns
    -------
    Dict[str, float]
        Dictionary containing:
        - 'sharpe_ratio': Annualized Sharpe ratio
        - 'max_drawdown': Maximum drawdown
        - 'total_return': Total cumulative return
        - 'annualized_return': Annualized return
    """
    strategy_returns = backtest_result["strategy_returns"]
    equity_curve = backtest_result["equity_curve"]

    # Compute total return
    clean_equity = equity_curve.dropna()
    if len(clean_equity) > 0:
        total_return = (clean_equity.iloc[-1] / clean_equity.iloc[0]) - 1
    else:
        total_return = np.nan

    # Compute annualized return
    n_periods = len(strategy_returns.dropna())
    if n_periods > 0 and not np.isnan(total_return):
        years = n_periods / periods_per_year
        annualized_return = (1 + total_return) ** (1 / years) - 1 if years > 0 else np.nan
    else:
        annualized_return = np.nan

    return {
        "sharpe_ratio": sharpe_ratio(strategy_returns, risk_free_rate, periods_per_year),
        "max_drawdown": max_drawdown(equity_curve),
        "total_return": float(total_return) if not np.isnan(total_return) else np.nan,
        "annualized_return": float(annualized_return) if not np.isnan(annualized_return) else np.nan,
    }
