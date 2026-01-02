import numpy as np
import pandas as pd

def sharpe_ratio(returns: pd.Series, rf: float = 0.0) -> float:
    excess = returns - rf
    return np.sqrt(252) * (excess.mean() / excess.std())

def max_drawdown(series: pd.Series) -> float:
    cum = series.cumsum()
    peak = cum.cummax()
    dd = cum - peak
    return dd.min()