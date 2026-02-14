"""
Volatility Filter

Filters trading signals based on market volatility.
Logic:
  - Calculate rolling standard deviation of prices.
  - If volatility is high (above threshold), filter out signals (set to 0) or avoid entries.
  - Can be applied to any signal series.
"""

import numpy as np
import pandas as pd


def apply_volatility_filter(
    signals: pd.Series,
    prices: pd.Series,
    lookback: int = 20,
    threshold_std: float = 2.0,
) -> pd.Series:
    """
    Apply volatility filter to signals.

    If current volatility is high, signals are set to 0 (flat/neutral).

    Parameters
    ----------
    signals : pd.Series
        Original signal series.
    prices : pd.Series
        Price series used to calculate volatility.
    lookback : int, default 20
        Lookback period for rolling standard deviation.
    threshold_std : float, default 2.0
        Threshold multiplier. If rolling_std > threshold_std * mean_volatility, signal is filtered.
        Wait, simply comparing to a fixed multiple of mean volatility over the whole period is look-ahead bias.
        Instead, let's use a rolling mean of volatility as the baseline, or just a raw threshold.
        
        To be more robust and avoids look-ahead bias:
        We will compare the current rolling std to the average of the rolling std over a longer window (e.g. 100 days).
        
        Condition:
        long_term_vol = rolling_std.rolling(long_window).mean()
        if rolling_std > threshold_std * long_term_vol:
            signal = 0
            
    Returns
    -------
    pd.Series
        Filtered signal series.
    """
    if len(prices) < lookback:
         return signals # Not enough data
            
    # Compute rolling volatility (std dev of prices? Or returns?)
    # Standard practice is volatility of returns, but the prompt says "Rolling standard deviation" 
    # and context implies price volatility. Let's use returns volatility for better normalization.
    # actually prompt says "Rolling standard deviation" in context of risk conditioning. 
    # Price std dev scales with price. Returns std dev is better.
    # However, to keep it simple and consistent with simple price-based stats, I can use price std, 
    # but normalized by price (Coefficient of Variation) or just log returns std.
    # Let's use log returns standard deviation.
    
    returns = np.log(prices / prices.shift(1))
    rolling_vol = returns.rolling(window=lookback).std()
    
    # Baseline volatility (moving average of volatility to adapt to regimes)
    # Use a longer window for baseline, e.g., 5x lookback
    baseline_window = lookback * 5
    baseline_vol = rolling_vol.rolling(window=baseline_window).mean()
    
    # Fill NaN baselines with the expanding mean to have *some* value early on, or just 0
    # For simulation, forward fill or similar is dangerous. Let's just keep NaNs where we can't compute.
    
    # Create mask: True if volatility is "normal", False if "high"
    # If baseline is NaN, we assume it's normal (safe fallback) or high (conservative)?
    # Let's assume normal if we don't have enough history to judge "high".
    
    # We employ a multiplier. e.g. if current vol > 1.5 * normal vol, step aside.
    # Shift baseline by 1 to avoid lookahead? 
    # rolling_vol includes current day. mean() includes current day. 
    # Strictly speaking for trading "tomorrow", we use "today's" vol. 
    # Signals usually align with "close". So we filter "today's" signal based on "today's" vol.
    
    is_high_volatility = rolling_vol > (baseline_vol * threshold_std)
    
    filtered_signals = signals.copy()
    
    # Mask out high volatility periods
    # We replace with 0 (neutral). 
    # Depends if 0 means "reduce position" or "don't enter". 
    # In this simple framework, 0 usually implies cash/neutral.
    filtered_signals[is_high_volatility] = 0
    
    return filtered_signals
