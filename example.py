#!/usr/bin/env python3
"""
Example: How to Execute Quant Strategies

This script demonstrates the complete workflow:
1. Generate/load price data
2. Generate trading signals using a strategy
3. Run a backtest
4. Compute performance metrics
"""

from utils import generate_synthetic_prices
from strategies import mean_reversion_strategy, momentum_strategy
from backtesting import backtest, compute_metrics

def main():
    print("=" * 60)
    print("QUANT STRATEGIES - EXAMPLE EXECUTION")
    print("=" * 60)
    
    # Step 1: Generate synthetic price data
    print("\n[1] Generating synthetic price data...")
    prices = generate_synthetic_prices(
        n_periods=252,      # 1 year of daily data
        initial_price=100.0,
        drift=0.0001,       # Slight upward drift
        volatility=0.02,    # 2% daily volatility
        seed=42             # For reproducibility
    )
    print(f"    ✓ Generated {len(prices)} price points")
    print(f"    ✓ Price range: ${prices.min():.2f} - ${prices.max():.2f}")
    
    # Step 2: Test Mean Reversion Strategy
    print("\n[2] Testing Mean Reversion Strategy...")
    mr_signals = mean_reversion_strategy(
        prices,
        lookback=20,         # 20-day rolling window
        entry_threshold=2.0  # Enter when z-score > 2
    )
    print(f"    ✓ Generated {len(mr_signals)} signals")
    print(f"    ✓ Long signals: {(mr_signals == 1).sum()}")
    print(f"    ✓ Short signals: {(mr_signals == -1).sum()}")
    print(f"    ✓ Neutral: {(mr_signals == 0).sum()}")
    
    # Step 3: Run backtest for Mean Reversion
    print("\n[3] Running backtest for Mean Reversion...")
    mr_result = backtest(
        prices,
        mr_signals,
        initial_capital=10000.0
    )
    print(f"    ✓ Backtest complete")
    print(f"    ✓ Final equity: ${mr_result['equity_curve'].iloc[-1]:.2f}")
    
    # Step 4: Compute metrics for Mean Reversion
    print("\n[4] Computing performance metrics for Mean Reversion...")
    mr_metrics = compute_metrics(mr_result)
    print(f"    ✓ Total Return: {mr_metrics['total_return']:.2%}")
    print(f"    ✓ Annualized Return: {mr_metrics['annualized_return']:.2%}")
    print(f"    ✓ Sharpe Ratio: {mr_metrics['sharpe_ratio']:.2f}")
    print(f"    ✓ Max Drawdown: {mr_metrics['max_drawdown']:.2%}")
    
    # Step 5: Test Momentum Strategy
    print("\n[5] Testing Momentum Strategy...")
    mom_signals = momentum_strategy(
        prices,
        lookback=20,      # 20-day rate of change
        threshold=0.02    # 2% threshold
    )
    print(f"    ✓ Generated {len(mom_signals)} signals")
    print(f"    ✓ Long signals: {(mom_signals == 1).sum()}")
    print(f"    ✓ Short signals: {(mom_signals == -1).sum()}")
    print(f"    ✓ Neutral: {(mom_signals == 0).sum()}")
    
    # Step 6: Run backtest for Momentum
    print("\n[6] Running backtest for Momentum...")
    mom_result = backtest(
        prices,
        mom_signals,
        initial_capital=10000.0
    )
    print(f"    ✓ Backtest complete")
    print(f"    ✓ Final equity: ${mom_result['equity_curve'].iloc[-1]:.2f}")
    
    # Step 7: Compute metrics for Momentum
    print("\n[7] Computing performance metrics for Momentum...")
    mom_metrics = compute_metrics(mom_result)
    print(f"    ✓ Total Return: {mom_metrics['total_return']:.2%}")
    print(f"    ✓ Annualized Return: {mom_metrics['annualized_return']:.2%}")
    print(f"    ✓ Sharpe Ratio: {mom_metrics['sharpe_ratio']:.2f}")
    print(f"    ✓ Max Drawdown: {mom_metrics['max_drawdown']:.2%}")
    
    # Step 8: Compare strategies
    print("\n" + "=" * 60)
    print("STRATEGY COMPARISON")
    print("=" * 60)
    print(f"\n{'Metric':<25} {'Mean Reversion':<20} {'Momentum':<20}")
    print("-" * 65)
    print(f"{'Total Return':<25} {mr_metrics['total_return']:>18.2%} {mom_metrics['total_return']:>18.2%}")
    print(f"{'Annualized Return':<25} {mr_metrics['annualized_return']:>18.2%} {mom_metrics['annualized_return']:>18.2%}")
    print(f"{'Sharpe Ratio':<25} {mr_metrics['sharpe_ratio']:>18.2f} {mom_metrics['sharpe_ratio']:>18.2f}")
    print(f"{'Max Drawdown':<25} {mr_metrics['max_drawdown']:>18.2%} {mom_metrics['max_drawdown']:>18.2%}")
    
    print("\n" + "=" * 60)
    print("✓ Execution complete!")
    print("=" * 60)

if __name__ == "__main__":
    main()
