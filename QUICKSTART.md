# 🚀 Quick Start Guide - Quant Strategies Repository

## Overview

This repository implements **quantitative trading strategies** with a focus on clean, vectorized code and proper backtesting methodology. It's designed for research and education, not live trading.

## What Does This Repo Do?

The repository provides three main capabilities:

1. **Strategy Signal Generation**: Convert price data into trading signals (-1, 0, +1)
2. **Vectorized Backtesting**: Test strategies without lookahead bias
3. **Performance Metrics**: Evaluate strategies using Sharpe ratio, max drawdown, etc.

## Repository Structure

```
quant-strategies/
├── strategies/           # Signal generation strategies
│   ├── mean_reversion.py # Z-score based mean reversion
│   └── momentum.py       # Rate-of-change momentum
├── backtesting/          # Backtesting infrastructure
│   ├── engine.py         # Vectorized backtest engine
│   └── metrics.py        # Performance metrics
├── utils/                # Data utilities
│   └── data_loader.py    # Load CSV or generate synthetic prices
├── research/             # Research documentation
│   └── experiments.md    # Strategy notes
└── example.py            # Complete working example
```

## How to Execute

### Method 1: Run the Example Script (Recommended)

The easiest way to understand the repo is to run the example:

```bash
# Activate virtual environment
source .venv/bin/activate

# Run the example
python example.py
```

This will:
- Generate synthetic price data
- Test both mean reversion and momentum strategies
- Run backtests
- Display performance metrics
- Compare strategies side-by-side

### Method 2: Use as a Library

You can import and use the modules in your own scripts:

```python
from utils import generate_synthetic_prices
from strategies import mean_reversion_strategy
from backtesting import backtest, compute_metrics

# 1. Get price data
prices = generate_synthetic_prices(n_periods=252, seed=42)

# 2. Generate signals
signals = mean_reversion_strategy(prices, lookback=20, entry_threshold=2.0)

# 3. Run backtest
result = backtest(prices, signals, initial_capital=10000)

# 4. Compute metrics
metrics = compute_metrics(result)
print(f"Sharpe Ratio: {metrics['sharpe_ratio']:.2f}")
print(f"Max Drawdown: {metrics['max_drawdown']:.2%}")
```

### Method 3: Use Your Own Data

To use real price data from a CSV file:

```python
from utils import load_prices
from strategies import momentum_strategy
from backtesting import backtest, compute_metrics

# Load your data (CSV with 'date' and 'close' columns)
prices = load_prices('path/to/your/data.csv')

# Generate signals
signals = momentum_strategy(prices, lookback=20, threshold=0.02)

# Backtest
result = backtest(prices, signals)
metrics = compute_metrics(result)
```

## Available Strategies

### 1. Mean Reversion Strategy

**Concept**: Prices tend to revert to their mean after deviating significantly.

**Parameters**:
- `lookback`: Rolling window for computing mean/std (default: 20)
- `entry_threshold`: Z-score threshold for entry (default: 2.0)

**Signal Logic**:
- **Long (+1)**: When z-score < -2 (price below mean)
- **Short (-1)**: When z-score > +2 (price above mean)
- **Neutral (0)**: Otherwise

**Usage**:
```python
from strategies import mean_reversion_strategy

signals = mean_reversion_strategy(
    prices, 
    lookback=20, 
    entry_threshold=2.0
)
```

### 2. Momentum Strategy

**Concept**: Assets that have performed well tend to continue performing well.

**Parameters**:
- `lookback`: Period for computing rate of change (default: 20)
- `threshold`: Minimum ROC for signal generation (default: 0.02 = 2%)

**Signal Logic**:
- **Long (+1)**: When ROC > threshold
- **Short (-1)**: When ROC < -threshold
- **Neutral (0)**: Otherwise

**Usage**:
```python
from strategies import momentum_strategy

signals = momentum_strategy(
    prices, 
    lookback=20, 
    threshold=0.02
)
```

## Performance Metrics

The `compute_metrics()` function returns:

| Metric | Description |
|--------|-------------|
| `sharpe_ratio` | Risk-adjusted return (annualized) |
| `max_drawdown` | Largest peak-to-trough decline |
| `total_return` | Cumulative return over period |
| `annualized_return` | Geometric average annual return |

## Key Design Principles

1. **No Lookahead Bias**: Signals are lagged by 1 period before computing returns
2. **Vectorized**: All operations use pandas/numpy (no loops)
3. **Simple & Clean**: Each function has a single responsibility
4. **Research-Focused**: No live trading, no optimization, no ML

## Common Workflows

### Workflow 1: Test a Strategy on Synthetic Data

```python
from utils import generate_synthetic_prices
from strategies import mean_reversion_strategy
from backtesting import backtest, compute_metrics

prices = generate_synthetic_prices(n_periods=252, seed=42)
signals = mean_reversion_strategy(prices)
result = backtest(prices, signals)
metrics = compute_metrics(result)
```

### Workflow 2: Compare Multiple Strategies

```python
from strategies import mean_reversion_strategy, momentum_strategy

# Generate signals from both strategies
mr_signals = mean_reversion_strategy(prices)
mom_signals = momentum_strategy(prices)

# Backtest both
mr_result = backtest(prices, mr_signals)
mom_result = backtest(prices, mom_signals)

# Compare metrics
mr_metrics = compute_metrics(mr_result)
mom_metrics = compute_metrics(mom_result)
```

### Workflow 3: Parameter Sensitivity Analysis

```python
lookbacks = [10, 20, 50, 100]
results = {}

for lb in lookbacks:
    signals = mean_reversion_strategy(prices, lookback=lb)
    result = backtest(prices, signals)
    metrics = compute_metrics(result)
    results[lb] = metrics['sharpe_ratio']

# Find best lookback
best_lookback = max(results, key=results.get)
```

## Understanding the Output

When you run `example.py`, you'll see:

1. **Signal Statistics**: How many long/short/neutral signals were generated
2. **Backtest Results**: Final equity value
3. **Performance Metrics**: Sharpe, drawdown, returns
4. **Strategy Comparison**: Side-by-side comparison table

**Example Output**:
```
Mean Reversion Strategy:
✓ Total Return: -1.90%
✓ Sharpe Ratio: -0.16
✓ Max Drawdown: 8.05%
```

## Next Steps

1. **Read the Research Notes**: Check `research/experiments.md` for strategy insights
2. **Modify Parameters**: Experiment with different lookback periods and thresholds
3. **Add Your Own Strategy**: Follow the pattern in `strategies/mean_reversion.py`
4. **Use Real Data**: Load your own CSV files with `load_prices()`

## Troubleshooting

**Q: I get "command not found: pip"**
- Use `pip3` or activate the virtual environment: `source .venv/bin/activate`

**Q: My strategy has negative returns**
- This is normal! Not all strategies work on all data. Try different parameters or different price data.

**Q: How do I add a new strategy?**
- Create a new file in `strategies/` that returns a pandas Series with values in {-1, 0, 1}
- Add it to `strategies/__init__.py`
- Use it with the `backtest()` function

**Q: Can I use this for live trading?**
- No! This is for research only. It doesn't handle transaction costs, slippage, or real-time data.

## Installation

```bash
# Clone the repo (if not already done)
cd quant-strategies

# Create virtual environment (if not exists)
python3 -m venv .venv

# Activate it
source .venv/bin/activate

# Install dependencies
pip install -r requirements.txt
```

## License

MIT - See LICENSE file for details.
