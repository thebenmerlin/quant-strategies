# Research Experiments

## Mean Reversion Strategy

### Strategy Description

Mean reversion is based on the statistical principle that prices tend to revert to their historical mean over time. This strategy exploits temporary deviations from equilibrium by:

- **Going long** when prices fall significantly below the rolling mean (negative z-score)
- **Going short** when prices rise significantly above the rolling mean (positive z-score)

The z-score measures how many standard deviations the current price is from its rolling mean:

```
z = (price - rolling_mean) / rolling_std
```

### Implementation Notes

**Parameters:**
- `lookback`: Rolling window for computing mean and standard deviation (default: 20 periods)
- `entry_threshold`: Z-score threshold for signal generation (default: 2.0)

**Signal Logic:**
| Z-Score Condition | Signal | Interpretation |
|-------------------|--------|----------------|
| z < -threshold    | +1     | Price below mean → expect rise → long |
| z > +threshold    | -1     | Price above mean → expect fall → short |
| \|z\| ≤ threshold | 0      | Price near mean → no position |

**Design Decisions:**
1. Uses rolling statistics (not expanding) to adapt to changing market conditions
2. Division by zero handled via NaN replacement
3. Output is cast to `int8` for memory efficiency

### Observations

**Strengths:**
- Works well in range-bound markets
- Simple, interpretable signal generation
- No lookahead bias in signal computation

**Weaknesses:**
- Underperforms in trending markets
- Sensitive to lookback and threshold parameters
- Assumes stationarity in price dynamics

**Future Experiments:**
- [ ] Test different lookback periods (10, 20, 50, 100)
- [ ] Explore dynamic thresholds based on regime detection
- [ ] Compare performance across asset classes
- [ ] Investigate exit conditions vs. pure threshold signals

---

## Momentum Strategy

### Strategy Description

Momentum strategies exploit the tendency of assets that have performed well (poorly) to continue performing well (poorly) in the short term.

### Implementation Notes

**Parameters:**
- `lookback`: Period for computing rate of change (default: 20 periods)
- `threshold`: Minimum ROC for signal generation (default: 2%)

**Signal Logic:**
| ROC Condition      | Signal |
|--------------------|--------|
| ROC > threshold    | +1     |
| ROC < -threshold   | -1     |
| otherwise          | 0      |

### Observations

**Strengths:**
- Captures trending behavior
- Historically proven across markets

**Weaknesses:**
- Suffers in mean-reverting environments
- Transaction costs can erode profits

---

## Backtesting Methodology

### Lookahead Bias Prevention

The backtesting engine uses **lagged signals** to prevent lookahead bias:

```
position[t] = signal[t-1]
```

This ensures that:
- The signal at time t is computed using data available up to time t
- The position is only taken at time t+1 (after observing the signal)
- Returns at t+1 are attributed to the position held

### Metrics Computed

| Metric | Formula | Interpretation |
|--------|---------|----------------|
| Sharpe Ratio | `(mean_excess / std) * sqrt(252)` | Risk-adjusted return |
| Max Drawdown | `max(running_max - equity) / running_max` | Worst peak-to-trough |
| Total Return | `(final_equity / initial_equity) - 1` | Cumulative performance |
| Annualized Return | `(1 + total_return)^(1/years) - 1` | Yearly equivalent |
