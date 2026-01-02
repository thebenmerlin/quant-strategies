import pandas as pd

def backtest(prices: pd.Series, signals: pd.Series) -> pd.DataFrame:
    """
    Vectorized backtesting engine.

    prices  : Series of asset prices
    signals : Series of positions (-1, 0, 1)
    """

    prices = prices.loc[signals.index]

    returns = prices.pct_change().fillna(0)
    strategy_returns = returns * signals.shift(1).fillna(0)

    equity_curve = (1 + strategy_returns).cumprod()

    return pd.DataFrame({
        "price": prices,
        "returns": returns,
        "signal": signals,
        "strategy_returns": strategy_returns,
        "equity_curve": equity_curve
    })
