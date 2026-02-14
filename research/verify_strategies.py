
import pandas as pd
import numpy as np
import sys
import os

# Add project root to path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from strategies.moving_average_crossover import moving_average_crossover_strategy
from strategies.volatility import apply_volatility_filter
from strategies.breakout import breakout_strategy
from utils.data_loader import generate_synthetic_prices

def main():
    print("Generating synthetic data...")
    # Generate prices with a trend
    prices = generate_synthetic_prices(n_periods=500, seed=42, drift=0.0005, volatility=0.01)
    
    print(f"Prices generated: {len(prices)} periods")
    print(f"Start: {prices.iloc[0]:.2f}, End: {prices.iloc[-1]:.2f}")
    
    print("\n--- Testing Moving Average Crossover Strategy ---")
    ma_signals = moving_average_crossover_strategy(prices, short_window=20, long_window=50)
    print("Signal counts:")
    print(ma_signals.value_counts().sort_index())
    
    print("\n--- Testing Breakout Strategy ---")
    breakout_signals = breakout_strategy(prices, lookback=20)
    print("Signal counts:")
    print(breakout_signals.value_counts().sort_index())
    
    print("\n--- Testing Volatility Filter ---")
    # Generate high volatility data by adding noise to a section
    high_vol_prices = prices.copy()
    noise = np.random.normal(0, 0.05, 100) # High noise
    # Add noise to the middle 100 periods
    high_vol_prices.iloc[200:300] *= (1 + noise)
    
    # Generate base signals on high vol prices (e.g. breakout)
    base_signals = breakout_strategy(high_vol_prices)
    
    # Apply filter
    filtered_signals = apply_volatility_filter(base_signals, high_vol_prices, lookback=20, threshold_std=1.5)
    
    print("Original Signal counts:")
    print(base_signals.value_counts().sort_index())
    print("Filtered Signal counts:")
    print(filtered_signals.value_counts().sort_index())
    
    # Check if we actually filtered something
    diff = (base_signals != 0) & (filtered_signals == 0)
    print(f"Signals filtered out: {diff.sum()}")

if __name__ == "__main__":
    main()
