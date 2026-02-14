# Quantitative Strategy Theory

This document outlines the theoretical underpinnings of the trading strategies implemented in this repository. Understanding *why* a strategy works (and when it fails) is as important as the code itself.

## 1. Moving Average Crossover (Trend Following)

### The Core Idea
Markets often exhibit **serial correlation** (trends) — if prices have been going up, they are likely to continue going up for some time due to fundamental momentum, investor psychology, or macro flows.

### Mechanism
The Moving Average (MA) Crossover is a classic "smoothing" technique to filter out noise and identify the dominant trend direction.
- **Fast MA (Short Window)**: Reacts quickly to recent price changes. Represents "current" price action with some noise reduction.
- **Slow MA (Long Window)**: Represents the longer-term consensus or "fair value".

### Signal Generation
- **Golden Cross (Bullish)**: When the Fast MA crosses *above* the Slow MA, it indicates that recent momentum has overtaken the long-term trend, suggesting a new uptrend.
- **Death Cross (Bearish)**: When the Fast MA crosses *below* the Slow MA, it signals weakening momentum and a potential downtrend.

### Strengths & Weaknesses
- **✅ Pros**: Captures large, sustained moves (fat tails). Extremely robust over long periods (decades).
- **❌ Cons**: **Lag**. By the time the crossover happens, the trend has already started. **Whipsaws**. In range-bound (sideways) markets, the MAs will cross frequently without sustained follow-through, causing multiple small losses.

---

## 2. Volatility Filtering (Regime Detection)

### The Core Idea
Financial markets are not stationary; they switch between different **regimes** (e.g., Low Volatility/Bull, High Volatility/Bear, High Volatility/Choppy). A strategy optimized for one regime often fails in another.

### Risk Conditioning
"Volatility clustering" is a stylized fact of asset returns: large price changes tend to be followed by large price changes.
- **High Volatility**: Often associated with market stress, panic, or turning points. Price action becomes erratic and "noisy". Trend-following signals here are less reliable and subject to higher slippage and risk.
- **Low Volatility**: Often associated with stable uptrends or accumulation phases.

### Implementation
We use a **Rolling Standard Deviation** of returns.
- If `Current Volatility > Threshold * Baseline Volatility`, we assume a "High Risk" regime.
- **Action**: The Volatility Filter acts as a **veto**. It forces the system to stand aside (Cash) or reduce size, preserving capital for calmer, higher-probability conditions. This improves the **Sharpe Ratio** by avoiding the most dangerous trading days.

---

## 3. Breakout Strategy (Price Discovery)

### The Core Idea
"Price has memory." Significant highs and lows act as psychological barriers (Support and Resistance). When price breaches these levels, it indicates a shift in the supply/demand balance.

### Donchian Channels
This strategy monitors the **Rolling Maximum** and **Rolling Minimum** over a lookback period (e.g., 20 days).
- **Breaking a High**: Implies that buyers have cleared all available supply at previous prices. This is a strong signal of demand and often leads to a "momentum burst".
- **Breaking a Low**: Implies that sellers are aggressive and buyers have retreated.

### The "Turtle" Legacy
This approach was made famous by the "Turtle Traders" experiment in the 1980s. They proved that a simple, mechanical system strictly following breakouts could generate massive profits by catching every major trend, even if it had a low win rate (often < 40%).

### Strengths & Weaknesses
- **✅ Pros**: Ensures you never miss a major trend (you are always in when a new high is made). No lag compared to Moving Averages (enters closer to the move's start).
- **❌ Cons**: **False Breakouts**. Prices often poke above a high to "trap" longs, then reverse. This is the primary source of losses.

---

## Summary Table

| Strategy | Type | Best Regime | Worst Regime | Risk Profile |
| :--- | :--- | :--- | :--- | :--- |
| **MA Crossover** | Trend | Sustained Trends | Sideways / Range | moderate (lagged exit) |
| **Trend Breakout** | Momentum | Strong Trends/Explosive Moves | Mean Reverting / Choppy | High (false breakouts) |
| **Mean Reversion** | Counter-Trend | Range-Bound / Sideways | Strong Trend | High (catching falling knives) |
| **Vol Filter** | Risk Mgmt | N/A | High Volatility | Reduces Drawdown |

By combining these components, you build a robust "multi-strategy" portfolio that can adapt to different market faces.
