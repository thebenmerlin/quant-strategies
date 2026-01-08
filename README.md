# Quant Strategies

A clean, research-grade quantitative trading strategy repository.

## Overview

This repository contains implementations of systematic trading strategies with a focus on:

- **Simplicity**: Each module has a single responsibility
- **Vectorization**: All computations are vectorized for performance
- **Research focus**: No live trading, no optimization, no ML—just clean signal generation and backtesting

## Project Structure

```
quant-strategies/
├── strategies/           # Trading strategy implementations
│   ├── momentum.py       # Momentum (ROC-based) strategy
│   └── mean_reversion.py # Mean reversion (z-score) strategy
├── backtesting/          # Backtesting infrastructure
│   ├── engine.py         # Vectorized backtest engine
│   └── metrics.py        # Performance metrics
├── utils/                # Utilities
│   └── data_loader.py    # Data loading and generation
├── research/             # Research notes
│   └── experiments.md    # Strategy experiments and observations
├── README.md
└── requirements.txt
```

## Strategy Ideas

### Mean Reversion

The mean reversion strategy assumes that prices oscillate around a mean and will eventually revert after deviating significantly.

**Signal Generation:**
1. Compute rolling mean and standard deviation
2. Calculate z-score: `z = (price - mean) / std`
3. Generate signals:
   - Long (+1) when z < -2 (price below mean)
   - Short (-1) when z > +2 (price above mean)
   - Neutral (0) otherwise

**Best suited for:** Range-bound markets, pairs trading, mean-reverting assets.

### Momentum

The momentum strategy exploits the tendency of trending assets to continue in their current direction.

**Signal Generation:**
1. Compute rate of change (ROC) over lookback period
2. Generate signals based on ROC threshold

**Best suited for:** Trending markets, breakout scenarios.

## Evaluation Metrics

| Metric | Description |
|--------|-------------|
| **Sharpe Ratio** | Risk-adjusted return: `(mean_return - rf) / std_return * sqrt(252)` |
| **Maximum Drawdown** | Largest peak-to-trough decline in equity |
| **Total Return** | Cumulative return over the backtest period |
| **Annualized Return** | Geometric average annual return |

## Research Philosophy

1. **Start simple**: Begin with well-understood strategies before adding complexity
2. **Avoid overfitting**: Use out-of-sample testing, avoid excessive parameter tuning
3. **Prevent lookahead bias**: Signals are lagged by one period before computing returns
4. **Vectorize everything**: No loops over time series—use pandas/numpy operations
5. **Single responsibility**: Each function does one thing well
6. **No premature optimization**: Focus on correctness first, then performance

## Usage

```python
from utils import generate_synthetic_prices
from strategies import mean_reversion_strategy
from backtesting import backtest, compute_metrics

# Generate or load price data
prices = generate_synthetic_prices(n_periods=252, seed=42)

# Generate signals
signals = mean_reversion_strategy(prices, lookback=20, entry_threshold=2.0)

# Run backtest
result = backtest(prices, signals, initial_capital=10000)

# Compute metrics
metrics = compute_metrics(result)
print(metrics)
```

## Requirements

- Python >= 3.8
- pandas >= 1.3.0
- numpy >= 1.20.0

Install dependencies:

```bash
pip install -r requirements.txt
```


