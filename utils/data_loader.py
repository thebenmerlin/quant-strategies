"""
Data Loader

Functions for loading and generating price data.
"""

import numpy as np
import pandas as pd
from pathlib import Path
from typing import Optional


def load_prices(
    filepath: str,
    date_column: str = "date",
    price_column: str = "close",
) -> pd.Series:
    """
    Load price data from a CSV file.

    Parameters
    ----------
    filepath : str
        Path to the CSV file.
    date_column : str, default 'date'
        Name of the date column.
    price_column : str, default 'close'
        Name of the price column.

    Returns
    -------
    pd.Series
        Price series with datetime index.
    """
    path = Path(filepath)

    if not path.exists():
        raise FileNotFoundError(f"File not found: {filepath}")

    df = pd.read_csv(filepath)

    if date_column not in df.columns:
        raise ValueError(f"Date column '{date_column}' not found in file")

    if price_column not in df.columns:
        raise ValueError(f"Price column '{price_column}' not found in file")

    df[date_column] = pd.to_datetime(df[date_column])
    df = df.set_index(date_column)
    df = df.sort_index()

    prices = df[price_column].astype(float)
    prices.name = "close"

    return prices


def generate_synthetic_prices(
    n_periods: int = 252,
    initial_price: float = 100.0,
    drift: float = 0.0001,
    volatility: float = 0.02,
    seed: Optional[int] = None,
) -> pd.Series:
    """
    Generate synthetic price data using geometric Brownian motion.

    Useful for testing strategies without real data.

    Parameters
    ----------
    n_periods : int, default 252
        Number of periods to generate.
    initial_price : float, default 100.0
        Starting price.
    drift : float, default 0.0001
        Daily drift (mean return).
    volatility : float, default 0.02
        Daily volatility (standard deviation of returns).
    seed : int, optional
        Random seed for reproducibility.

    Returns
    -------
    pd.Series
        Synthetic price series with datetime index.
    """
    if seed is not None:
        np.random.seed(seed)

    # Generate returns using GBM
    returns = np.random.normal(drift, volatility, n_periods)

    # Compute prices
    prices = initial_price * np.exp(np.cumsum(returns))

    # Create date index
    dates = pd.date_range(start="2020-01-01", periods=n_periods, freq="B")

    series = pd.Series(prices, index=dates, name="close")

    return series
